from flask import Flask, render_template, redirect, url_for, request, session, flash
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


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():

    error = None

    if request.method == "GET" and session.get('logged_in'):
        return redirect(url_for("home"))

    elif request.method == "POST":
        login_pressed = request.form.get("loginbutton", None)
        register_pressed = request.form.get("registerbutton", None)

        if login_pressed == "login":
            email = request.form.get("em")
            password = request.form.get("pw")

            if not email or not password:
                error = "All fields must be filled"
            else:
                check_login = db.execute(
                    "SELECT * FROM db WHERE email=?", email)
                returned_login = list(check_login)

                if not len(returned_login):
                    error = "Account not found"
                elif email == returned_login[0]['email'] and not check_password_hash(returned_login[0]['password'], password):
                    error = "Wrong Password"
                elif email == returned_login[0]['email'] and check_password_hash(returned_login[0]['password'], password):
                    session["logged_in"] = True
                    session["user_id"] = returned_login[0]['id']
                    return redirect(url_for("home"))

        elif register_pressed == "register":
            uname = request.form.get("uname-reg")
            email = request.form.get("email-reg")
            password = generate_password_hash(request.form.get("pw-reg"))

            if not uname or not email or not password:
                error = "All fields must be filled"

            user_count = db.execute("SELECT COUNT(*) FROM db")
            is_username_taken = db.execute(
                "SELECT username FROM db WHERE username=?", uname)
            is_email_taken = db.execute(
                "SELECT email FROM db WHERE email=?", email)

            if len(is_username_taken):
                error = "Username already taken"
            elif len(is_email_taken):
                error = "Email already registered"
            else:
                id_num = 0
                int_user_count = user_count[0]['COUNT(*)']
                id_num = int_user_count

                db.execute("INSERT INTO db (id, username, email, password) VALUES (?, ?, ?, ?)",
                           id_num, uname, email, password)
                db.execute(
                    "INSERT INTO profile_info (profile_img_id, user_id) VALUES (?, ?)", 1, id_num)
    return render_template("landing.html", error=error)


@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    if request.method == "GET" and not session.get('logged_in'):
        return redirect(url_for("login"))
    elif request.method == "GET" and session.get('logged_in'):
        return render_template("home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# requirement for better profanity to work
if __name__ == '__main__':
    profanity.load_censor_words()
    app.run()
