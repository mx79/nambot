import os
import time
import random
import string
import smtplib

from os import getenv
from pymongo import MongoClient
from email.utils import formatdate
from email.message import EmailMessage
from passlib.context import CryptContext

# =================================================== VARIABLES =================================================== #

# DB file
client = MongoClient(getenv("MONGO_CLUSTER"))
db = client.cnambot

# Hashing method
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Characters to generate password or temporary url from
characters = list(string.ascii_letters + string.digits)
characters_with_punct = list(string.ascii_letters + string.digits + string.punctuation)


# =============================================== PASSWORDS FUNCTIONS =============================================== #


def pwd_generator() -> str:
    """Generates a password for those user who have no idea.

    :return: Password of length 10
    """
    random.shuffle(characters_with_punct)
    password = [random.choice(characters_with_punct) for _ in range(10)]
    random.shuffle(password)
    return "".join(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password between one not hashed and its hashed representation.

    :param plain_password: Password to test, as plain string
    :param hashed_password: Password hashed
    :return: `True` if the password matched the hash, else `False`
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Function used to transform plain string password to hashed password.

    :param password: Password to hash
    :return: Hashed password
    """
    return pwd_context.hash(password)


# =============================================== DATABASES FUNCTIONS =============================================== #


def create_user(username: str, promo: str, email: str, pwd: str, tmp: bool = False):
    """Basic function to create a json file for a new user, temporary or not.

    :param username: Unique username
    :param promo: Promotion to choose in a drop-down list
    :param email: CNAM email
    :param pwd: Password to hash
    :param tmp: Temporary parameter used to create an entry in tmp_users if true or users by default if false
    """
    if tmp:
        db.tmp_users.insert_one({
            "username": username,
            "promo": promo,
            "email": email,
            "password": get_password_hash(pwd),
            "created_at": int(time.time())
        })
    else:
        db.users.insert_one({
            "username": username,
            "firstname": email.split(".")[0].capitalize(),
            "lastname": email.split(".")[1].capitalize(),
            "promo": promo,
            "email": email,
            "password": pwd
        })


def update_password(email: str, new_password: str):
    """Function that handles the forgot password process.

    :param email: CNAM email
    :param new_password: The new password wished by the user
    """
    db.users.update_one(filter={"email": email},
                        update={"$set": {"password": get_password_hash(new_password)}})


def user_in_db(name: str, email: str):
    """Check whether a user is in database or not.

    :param name: Unique username
    :param email: CNAM email
    :return: Error message to print on user screen if the user already exist
    """
    if db.users.find_one({"username": name}):
        return "Ce nom d'utilisateur est déjà pris sur CnamBot !"
    elif db.users.find_one({"email": email}):
        return "Cette adresse email est déjà utilisée sur CnamBot !"

    return


def create_email_validation_url(key: str, email: str):
    """It creates the temporary url to validate email address.

    :param key: The generated key to construct the URL
    :param email: CNAM email
    """
    db.tmp_email_validation_url.insert_one({
        "url": key,
        "created_at": int(time.time()),
        "email": email
    })


def create_forgot_url(key: str, email: str):
    """It creates the temporary url to regenerate the user password.

    :param key: The generated key to construct the URL
    :param email: CNAM email
    """
    db.tmp_forgot_url.insert_one({
        "url": key,
        "created_at": int(time.time()),
        "email": email
    })


# ============================================= EMAIL RELATED FUNCTIONS ============================================= #


def get_random_string(length: int):
    """Generates a random string for dynamic link.

    :return: Random string of desired length
    """
    random.shuffle(characters)
    password = [random.choice(characters) for _ in range(length)]
    random.shuffle(password)
    return "".join(password)


def send_email(email: str, option: str):
    """Function used to send email from CnamBot address when we are validating
    user email address or following the process of the forgotten email.

    :param email: CNAM email
    :param option: `verification` or `forgot` email sending process
    """
    # Exit func if option param is wrong
    if option not in ["verification", "forgot"]:
        raise KeyError("Invalid option for func send_email")

    # Server start and login with credentials
    server = smtplib.SMTP('SMTP.gmail.com', 587)
    server.connect('SMTP.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(getenv("CNAMBOT_EMAIL"), getenv("CNAMBOT_PASSWORD"))

    # Strip eventual space in user address
    mail = email.strip()

    # Headers : cnambot_address, user_address, actual_date, subject, message
    msg = EmailMessage()
    msg['From'] = f'CnamBot <{getenv("CNAMBOT_EMAIL")}>'
    msg['To'] = mail
    msg["Date"] = formatdate(localtime=True)
    url = "http://localhost:5000" if os.getenv("DEV_MODE") else "https://lecnambot.herokuapp.com"
    key = get_random_string(16)
    if option == "verification":
        msg['Subject'] = "Votre lien de validation d'email"
        msg.set_content(f"""\
        Bonjour,

        Bienvenue sur CnamBot, voici le lien à suivre pour achever la validation de votre adresse email :
        {url}/email-verified/{key}

        Une fois cela fait, vous pourrez profitez pleinement des services de la plateforme.

        Bonne journée,
        L'équipe de développement
        """)
        create_email_validation_url(key, mail)
    elif option == "forgot":
        msg['Subject'] = "Votre lien de réinitialisation de mot de passe"
        msg.set_content(f"""\
        Bonjour,

        Voici votre lien de réinitialisation de mot de passe :
        {url}/forgot-password/{key}

        Bonne journée,
        L'équipe de développement
        """)
        create_forgot_url(key, mail)

    # Try to send the message, catch if there are any error
    try:
        server.send_message(msg)
        print(option)
        print('{0} : send'.format(mail))
    except smtplib.SMTPException as e:
        print(option)
        print('{0} : {1}'.format(mail, e))

    server.quit()
