from routes import no_auth_required
from flask import redirect, render_template, request, session
from pkg.authlib.auth import db, send_email, update_password


@no_auth_required
def forgot_password(tmp_string: str = None):
    """
    Description:
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
            session["user_id"] = db.users.find_one({"email": doc["email"]})["username"]
            return redirect("/")

    if tmp_string:
        if db.tmp_forgot_url.find_one({"url": tmp_string}):
            return render_template("forgot.html", arg=tmp_string)
        return redirect("/")

    return render_template("forgot.html")
