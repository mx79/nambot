from flask import redirect, render_template, request, session, url_for
from routes import no_auth_required
from pkg.authlib.auth import send_email


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
            create_user()
            session["user_id"] =
            return redirect(url_for("/"))

    return render_template("forgot.html", arg=tmp_string)
