from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from cs50 import SQL
from markupsafe import escape
from datetime import timedelta
import re


app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_REFRESH_EACH_REQUEST"] = True
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)

Session(app)
csrf = CSRFProtect()
csrf.init_app(app)

db = SQL("sqlite:///database.db")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_password(email, password):
    if not email or not password:
        return "All fields must be filled"

    fetch_login_from_db = db.execute(
        "SELECT * FROM logins WHERE email=?", email)

    fetched_login = list(fetch_login_from_db)

    if not fetched_login or check_password_hash(fetched_login[0]['password'], password) == False:
        return "Wrong Username or Password"
    elif email == fetched_login[0]['email'] and check_password_hash(fetched_login[0]['password'], password):
        session["user_id"] = fetched_login[0]['id']
        session["logged_in"] = True


def register(user, email, password, agree):
    if not user or not email or not password:
        return "All fields must be filled"
    elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
        return "Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character"
    elif agree != "agreed":
        return "You must agree to the T&C's to register"
    elif db.execute(
            "SELECT username FROM logins WHERE username=?", user):
        return "Username already taken"
    elif db.execute(
            "SELECT email FROM logins WHERE email=?", email):
        return "Email already registered"
    else:
        db.execute("INSERT INTO logins (username, email, password) VALUES (?, ?, ?)",
                   user, email, generate_password_hash(password))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.route("/pdf/<path:filename>")
def serve_pdf(filename):
    return send_from_directory("static", filename)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET" and session.get('logged_in'):
        return redirect(url_for("dashboard"))

    elif request.method == "POST":
        login_pressed = request.form.get("loginbutton", None)
        register_pressed = request.form.get("registerbutton", None)

        if login_pressed == "login":
            email = escape(request.form.get("em"))
            password = escape(request.form.get("pw"))

            error_msg = check_password(email, password)

            if error_msg:
                flash(error_msg)

        elif register_pressed == "register":
            user = escape(request.form.get("uname-reg"))
            email = escape(request.form.get("email-reg"))
            password = escape(request.form.get("pw-reg"))
            agree_tcs = request.form.get("agree-tcs")

            reg_error = register(user, email, password, agree_tcs)

            if reg_error:
                flash(reg_error)

        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    if request.method == "GET" and not session.get('logged_in'):
        return redirect(url_for("login"))
    elif request.method == "GET" and session.get('logged_in'):
        return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
