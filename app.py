from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, flash, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from cs50 import SQL
from markupsafe import escape
from datetime import timedelta, date
import re
import time


app = Flask(__name__)
app.config["SECRET_KEY"] = "x8dxf1xcaxb7Ex03S^xd5x04x80xeaxc0x90xe1(x83x13V4Hxbcx9fxec"
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
        "SELECT * FROM users JOIN logins ON users.id=logins.user_id WHERE email=?", email)

    fetched_login = list(fetch_login_from_db)

    if not fetched_login:
        return "Wrong Username or Password"
    elif fetched_login[0]['account_disabled'] == 1:
        return "Account Disabled - Too Many Failed Login Attempts"
    elif check_password_hash(fetched_login[0]['password'], password) == False:
        db.execute("UPDATE logins SET attempt_count=attempt_count+1 WHERE user_id=?",
                   fetched_login[0]['user_id'])
        if fetched_login[0]['attempt_count'] >= 3:
            db.execute("UPDATE logins SET account_disabled=1 WHERE user_id=?",
                       fetched_login[0]['user_id'])
        return "Wrong Username or Password"
    elif email == fetched_login[0]['email'] and check_password_hash(fetched_login[0]['password'], password):
        db.execute("UPDATE logins SET account_disabled=0, attempt_count=0 WHERE user_id=?",
                   fetched_login[0]['user_id'])
        session["user_id"] = fetched_login[0]['id']
        session["logged_in"] = True


def register(user, email, password, agree):
    if not user or not email or not password:
        return "All fields must be filled"
    elif agree != "agreed":
        return "You must agree to the T&C's to register"
    elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
        return "Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character"
    elif db.execute(
            "SELECT username FROM users WHERE username=?", user):
        return "Username already taken"
    elif db.execute(
            "SELECT email FROM users WHERE email=?", email):
        return "Email already registered"
    else:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   user, email, generate_password_hash(password))
        return "Register success"


def validate_form_inputs(category, subcat, amount):
    form_category = ['purchase', 'sell', 'income', 'invest', 'debt']
    form_purchase_sub = ['snacks', 'groceries', 'resto', 'clothing',
                         'shoes', 'bags', 'luxury', 'electronics', 'utilities', 'transpo']
    form_sell_sub = ['oldelectronics', 'oldfurniture',
                     'oldclothes', 'oldshoes', 'oldbags', 'oldluxury']
    form_income_sub = ['salary', 'businesssvc', 'businesssku', 'allowance']
    form_invest_sub = ['stocks', 'bonds', 'mfund',
                       'insurance', 'crypto', 'preciousmetals']
    form_debt_sub = ['studentloan', 'salaryloan', 'carloan', 'mortgage']

    if category and subcat and amount:
        if amount.isdigit() and int(amount) > 0:
            if category == form_category[0] and subcat in form_purchase_sub:
                return True
            elif category == form_category[1] and subcat in form_sell_sub:
                return True
            elif category == form_category[2] and subcat in form_income_sub:
                return True
            elif category == form_category[3] and subcat in form_invest_sub:
                return True
            elif category == form_category[4] and subcat in form_debt_sub:
                return True
    return False


@app.before_request
def make_session_permanent():
    session.permanent = True
    if request.form.get("remember-me") == "yes-remember":
        app.permanent_session_lifetime = timedelta(days=30)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Frame-Options"] = "DENY"
    # response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https://secure.example.com; script-src 'self' https://secure.example.com; style-src 'self' https://secure.example.com; connect-src 'self' https://secure.example.com; font-src 'self' https://secure.example.com; object-src 'self' https://secure.example.com; frame-src 'self' https://secure.example.com"
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
            time.sleep(3)

            if error_msg:
                flash((error_msg, 'error'))

        elif register_pressed == "register":
            user = escape(request.form.get("uname-reg"))
            email = escape(request.form.get("email-reg"))
            password = escape(request.form.get("pw-reg"))
            agree_tcs = request.form.get("agree-tcs")

            reg_error = register(user, email, password, agree_tcs)
            time.sleep(2)

            if reg_error == "Register success":
                flash((reg_error, 'success'))
            elif reg_error:
                flash((reg_error, 'error'))

        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    if request.method == "GET" and not session.get('logged_in'):
        return redirect(url_for("login"))
    elif request.method == "GET" and session.get('logged_in'):
        get_user = db.execute(
            "SELECT username FROM users WHERE id=?", session.get("user_id"))
        current_user = get_user[0]['username']
        current_date = date.today()
        formatted_date = current_date.strftime("%B %d, %Y")
        return render_template("dashboard.html", username=current_user, date=formatted_date)
    elif request.method == "POST":
        category = request.form.get("category-select")
        subcat = request.form.get("second-select")
        amount = request.form.get("transact-amount")
        active_user = session.get("user_id")

        if validate_form_inputs(category, subcat, amount):
            db.execute(
                "INSERT INTO transactions (user_id, account_title, category, amount) VALUES (?, ?, ?, ?)", active_user, subcat, category, amount)
            data = {'success': True}
            return jsonify(data)
        else:
            data = {'success': False}
            return jsonify(data)
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
