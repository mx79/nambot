from flask import redirect, render_template, session, url_for


def root():
    """
    Description:
    :return:
    """
    if session.get("user_id") is None:
        return redirect(url_for("login"))
    return render_template("home.html")
