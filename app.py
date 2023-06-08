from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from cs50 import SQL
from better_profanity import profanity


app = Flask(__name__)
app.secret_key = "this is just a test"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///database.db")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def login_user(user):
    session["logged_in"] = True
    session["user_id"] = user[0]['id']
    return redirect(url_for("home"))


def check_password(email, password):
    check_login = db.execute(
        "SELECT * FROM logins WHERE email=?", email)
    returned_login = list(check_login)

    if not len(returned_login):
        return "Account not found"
    elif email == returned_login[0]['email'] and not check_password_hash(returned_login[0]['password'], password):
        return "Wrong Password"
    elif email == returned_login[0]['email'] and check_password_hash(returned_login[0]['password'], password):
        login_user(returned_login)


def register():
    return 0


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

    error = None

    if request.method == "GET" and session.get('logged_in'):
        return redirect(url_for("dashboard"))

    elif request.method == "POST":
        login_pressed = request.form.get("loginbutton", None)
        register_pressed = request.form.get("registerbutton", None)

        if login_pressed == "login":
            email = request.form.get("em")
            password = request.form.get("pw")

            if not email or not password:
                error = "All fields must be filled"

            error_msg = check_password(email, password)

            if error_msg:
                return render_template("index.html", error=error_msg)

        elif register_pressed == "register":
            uname = request.form.get("uname-reg")
            email = request.form.get("email-reg")
            password = generate_password_hash(request.form.get("pw-reg"))
            agree_tcs = request.form.get("agree-tcs")

            if not uname or not email or not password:
                error = "All fields must be filled"
                return render_template("index.html", error=error)
            elif len(password) < 10:
                error = "Password must be at least 10 characters long"
                return render_template("index.html", error=error)

            is_username_taken = db.execute(
                "SELECT username FROM logins WHERE username=?", uname)
            is_email_taken = db.execute(
                "SELECT email FROM logins WHERE email=?", email)

            if agree_tcs != "agreed":
                error = "You must agree to the T&C's to register"
                return render_template("index.html", error=error)

            if len(is_username_taken):
                error = "Username already taken"
            elif len(is_email_taken):
                error = "Email already registered"
            else:
                db.execute("INSERT INTO logins (username, email, password) VALUES (?, ?, ?)",
                           uname, email, password)
    return render_template("index.html", error=error)


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


# requirement for better profanity to work
if __name__ == '__main__':
    profanity.load_censor_words()
    app.run()
