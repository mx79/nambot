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
    """
    Description: Generates a password for those user who have no idea
    :return: Password of length 10
    """
    random.shuffle(characters_with_punct)
    password = [random.choice(characters_with_punct) for _ in range(10)]
    random.shuffle(password)
    return "".join(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Description: Verify password between one not hashed and its hashed representation.
    :param plain_password: Password to test, as plain string
    :param hashed_password: Password hashed
    :return: ``True`` if the password matched the hash, else ``False``
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Description: Function used to transform plain string password to hashed password.
    :param password: Password to hash
    :return: Hashed password
    """
    return pwd_context.hash(password)


# =============================================== DATABASES FUNCTIONS =============================================== #


def create_user(username: str, promo: str, email: str, pwd: str, tmp: bool = False):
    """
    Description: Basic function to create a json file for a new user, temporary or not.
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
        })
    else:
        db.users.insert_one({
            "username": username,
            "promo": promo,
            "email": email,
            "password": get_password_hash(pwd),
        })


def user_in_db(name: str, email: str):
    """
    Description: Check whether a user is in database or not.
    :param name: Unique username
    :param email: CNAM email
    :return: Error message to print on user screen if the user already exist
    """
    for doc in db.users.find():
        if name == doc["username"] and email == doc["email"]:
            return "Ce nom d'utilisateur et cette adresse email sont déjà utilisés sur CnamBot !"
        if name == doc["username"]:
            return "Ce nom d'utilisateur est déjà pris sur CnamBot !"
        if email == doc["email"]:
            return "Cette adresse email est déjà utilisée sur CnamBot !"
    return


def create_email_validation_url(key: str):
    """
    Description:
    :param key:
    """
    db.tmp_email_validation_url.insert_one({
        "url": key,
        "created_at": int(time.time())
    })


def create_forgot_url(key: str):
    """
    Description:
    :param key:
    """
    db.tmp_forgot_url.insert_one({
        "url": key,
        "created_at": int(time.time())
    })


# ============================================= EMAIL RELATED FUNCTIONS ============================================= #


def get_random_string(length: int):
    """
    Description: Generates a random string for dynamic link
    :return: Random string of desired length
    """
    random.shuffle(characters)
    password = [random.choice(characters) for _ in range(length)]
    random.shuffle(password)
    return "".join(password)


def send_email(email: str, option: str):
    """
    Description: Function used to send email from CnamBot address when we are validating
    user email address or following the process of the forgotten email.
    :param email: CNAM email
    :param option: <verification> or <forgot> email sending process
    """
    # Exit func if option param is wrong
    if option not in ["verification", "forgot"]:
        return KeyError("Invalid option for func send_email")

    # Server start and login with credentials
    server = smtplib.SMTP('SMTP.gmail.com', 587)
    server.connect('SMTP.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(getenv("CNAMBOT_EMAIL"), getenv("CNAMBOT_PASSWORD"))

    # Strip eventual space in user address
    email = email.strip()

    # Headers : cnambot_address, user_address, actual_date, subject, message
    msg = EmailMessage()
    msg['From'] = f'CnamBot <{getenv("CNAMBOT_EMAIL")}>'
    msg['To'] = email
    msg["Date"] = formatdate(localtime=True)
    key = get_random_string(16)
    dynamic_url = "http://localhost:5000/{}".format(key)
    if option == "verification":
        msg['Subject'] = "Votre lien de validation d'email"
        msg.set_content(f"""\
        Bonjour,
        
        Bienvenue sur CnamBot, voici le lien à suivre pour achever la validation de votre adresse email :
        {dynamic_url}
        
        Une fois cela fait, vous pourrez profitez pleinement des services de la plateforme.
        
        Bonne journée,
        L'équipe de développement
        """)
        create_email_validation_url(key)
    elif option == "forgot":
        msg['Subject'] = "Votre lien de réinitialisation de mot de passe"
        msg.set_content(f"""\
        Bonjour,

        Voici votre lien de réinitialisation de mot de passe :
        {dynamic_url}

        Bonne journée,
        L'équipe de développement
        """)
        create_forgot_url(key)

    # Try to send the message, catch if there are any error
    try:
        server.send_message(msg)
        print(option)
        print('{0} : send'.format(email))
    except smtplib.SMTPException as e:
        print(option)
        print('{0} : {1}'.format(email, e))

    server.quit()
