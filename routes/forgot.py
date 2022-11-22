from routes import no_auth_required
from flask import redirect, render_template, request, session
from pkg.authlib.auth import db, send_email, update_password


@no_auth_required
def forgot_password(tmp_string: str = None):
    """
    Description:
    :param tmp_string:
    :return:
    """
    # Checking HTTP method used
    if request.method == "POST":
        if tmp_string is None:
            forgot_email = request.form.get("forgot_email", "")
            send_email(forgot_email, "forgot")
            return render_template("forgot.html", send=True)
        else:
            new_pwd = request.form.get("new_password")
            doc = db.tmp_forgot_url.find_one({"url": tmp_string})
            update_password(doc["email"], new_pwd)
            return render_template("forgot.html", pwd_changed=True, send=True)

    if tmp_string:
        if db.tmp_forgot_url.find_one({"url": tmp_string}):
            return render_template("forgot.html", arg=tmp_string)
        return render_template("404.html")

    return render_template("forgot.html")
