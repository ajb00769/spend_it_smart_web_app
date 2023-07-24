from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, redirect
from cs50 import SQL
import re
from functools import wraps

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
        return "Password must contain at least 1 upper and lower case letter, 1 digit, and 1 special character [@$!%*#?&]"
    elif db.execute(
            "SELECT username FROM users WHERE username=?", user):
        return "Username already taken"
    elif db.execute(
            "SELECT email FROM users WHERE email=?", email):
        return "Email already registered"
    else:
        generated_id = db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                                  user, email, generate_password_hash(password))
        db.execute("INSERT INTO logins (user_id, attempt_count, last_attempt, account_disabled) VALUES (?, 0, CURRENT_TIMESTAMP, 0)", generated_id)
        return "Register success"
