from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, session, redirect, g
from re import match
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:allentestdb123@127.0.0.1:5432/spend_it_smart"

db = SQLAlchemy(app)


@app.before_request
def before_request():
    g.db = db.session


@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()


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

    query_fetch_login_from_db = text(
        "SELECT * FROM users JOIN logins ON users.id=logins.user_id WHERE email=:email")
    fetch_login_from_db = g.db.execute(
        query_fetch_login_from_db, {"email": email})

    fetched_login = list(fetch_login_from_db)

    if not fetched_login:
        return "Wrong Username or Password"
    elif fetched_login[0]['account_disabled'] == True:
        return "Account Disabled - Too Many Failed Login Attempts"
    elif check_password_hash(fetched_login[0]['password'], password) == False:
        g.db.execute("UPDATE logins SET attempt_count=attempt_count+1 WHERE user_id=:user_id",
                     {"user_id": fetched_login[0]['user_id']})
        if fetched_login[0]['attempt_count'] >= 3:
            g.db.execute("UPDATE logins SET account_disabled=True WHERE user_id=:user_id",
                         {"user_id": fetched_login[0]['user_id']})
        return "Wrong Username or Password"
    elif email == fetched_login[0]['email'] and check_password_hash(fetched_login[0]['password'], password):
        g.db.execute("UPDATE logins SET account_disabled=False, attempt_count=0 WHERE user_id=:user_id",
                     {"user_id": fetched_login[0]['user_id']})
        session["user_id"] = fetched_login[0]['id']
        session["logged_in"] = True


def register(user, email, password, agree):
    if not user or not email or not password:
        return "All fields must be filled"
    elif agree != "agreed":
        return "You must agree to the T&C's to register"
    elif check_password_strength(password) != 'strong':
        return "Password not strong enough. Please don't change the code in the developer console."
    elif g.db.execute(
            "SELECT username FROM users WHERE username=:user", {"user": user}).first() is not None:
        return "Username already taken"
    elif g.db.execute(
            "SELECT email FROM users WHERE email=:email", {"email": email}).first() is not None:
        return "Email already registered"
    else:
        generated_id = g.db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password) RETURNING id",
                                    {"username": user, "email": email, "password": generate_password_hash(password)}).first()
        g.db.execute(
            "INSERT INTO logins (user_id, attempt_count, last_attempt) VALUES (:generated_id, 0, CURRENT_TIMESTAMP)", {"generated_id": generated_id[0]})
        g.db.commit()
        return "Register success"


def check_password_strength(password):
    if match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$', password):
        return 'strong'
    else:
        return 'weak'


def get_current_user(id):
    query = text(
        "SELECT username FROM users WHERE id=:current_session_user_id")
    return g.db.execute(query, {"current_session_user_id": id}).fetchall()


def get_user_transactions(id):
    query = text("SELECT transaction_id, account_title, category, amount, transaction_date FROM transactions WHERE user_id=:current_session_user_id")
    return g.db.execute(query, {"current_session_user_id": id}).fetchall()


def add_transaction(user_id, subcat, category, amount):
    query = text(
        "INSERT INTO transactions (user_id, account_title, category, amount) VALUES (:user_id, :subcat, :category, :amount)")
    g.db.execute(query, {"user_id": user_id, "subcat": subcat,
                 "category": category, "amount": amount})
    g.db.commit()
