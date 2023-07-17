from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, flash, jsonify
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape
from cs50 import SQL
from datetime import timedelta, date, datetime
from login_utils import check_password, register, login_required
from form_validation import validate_form_inputs


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
        login_pressed = escape(request.form.get("loginbutton", None))
        register_pressed = escape(request.form.get("registerbutton", None))

        if login_pressed == "login":
            email = escape(request.form.get("em"))
            password = escape(request.form.get("pw"))

            error_msg = check_password(email, password)

            if error_msg:
                flash((error_msg, 'error'))

        elif register_pressed == "register":
            user = escape(request.form.get("uname-reg"))
            email = escape(request.form.get("email-reg"))
            password = escape(request.form.get("pw-reg"))
            agree_tcs = request.form.get("agree-tcs")

            reg_error = register(user, email, password, agree_tcs)

            if reg_error == "Register success":
                flash((reg_error, 'success'))
            elif reg_error:
                flash((reg_error, 'error'))

        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    current_session_userid = session.get("user_id")
    if request.method == "GET" and not session.get('logged_in'):
        return redirect(url_for("login"))
    elif request.method == "GET" and session.get('logged_in'):
        get_user = db.execute(
            "SELECT username FROM users WHERE id=?", current_session_userid)
        current_user = get_user[0]['username']
        current_date = date.today()
        formatted_date = current_date.strftime("%B %d, %Y")
        # fetch sum of each category for the month
        fetch_purchase_data = db.execute(
            "SELECT SUM(amount) AS total_purchases FROM transactions WHERE category='purchase' AND user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now')", current_session_userid)
        fetch_sell_data = db.execute(
            "SELECT SUM(amount) AS total_assets_sold FROM transactions WHERE category='sell' AND user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now')", current_session_userid)
        fetch_income_data = db.execute(
            "SELECT SUM(amount) AS total_income FROM transactions WHERE category='income' AND user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now')", current_session_userid)
        fetch_invest_data = db.execute(
            "SELECT SUM(amount) AS total_investments FROM transactions WHERE category='invest' AND user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now')", current_session_userid)
        fetch_debt_data = db.execute(
            "SELECT SUM(amount) AS total_debt FROM transactions WHERE category='debt' AND user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now')", current_session_userid)
        chart_kvps = [fetch_purchase_data[0], fetch_debt_data[0],
                      fetch_income_data[0], fetch_invest_data[0], fetch_sell_data[0]]
        chart_labels = []
        chart_values = []
        for item in chart_kvps:
            key = list(item.keys())[0]
            title_key = key.replace("_", " ").title()
            value = item[key]
            if value == None:
                value = 0
            chart_labels.append(title_key)
            chart_values.append(value)
        # fetch values for bar chart
        fetch_barchart_data = db.execute(
            "SELECT STRFTIME('%m-%Y', transaction_date) AS month_year, category, SUM(amount) AS total_amount FROM transactions WHERE category IN ('income', 'purchase') AND STRFTIME('%Y', transaction_date) = STRFTIME('%Y', 'now') GROUP BY month_year, category")
        for item in fetch_barchart_data:
            new_item = datetime.strptime(
                item['month_year'], '%m-%Y').strftime('%b')
            item['month_year'] = new_item
        months = []
        income_data = []
        expense_data = []
        for item in fetch_barchart_data:
            if item['month_year'] not in months:
                months.append(item['month_year'])
            if item['category'] == 'income':
                income_data.append(item['total_amount'])
            elif item['category'] == 'purchase':
                expense_data.append(item['total_amount'])
        # fetch transaction breakdown for the month
        fetch_user_transactions = db.execute(
            "SELECT STRFTIME('%m/%d/%Y', transaction_date) AS transaction_date, account_title, category, amount FROM transactions WHERE user_id=? AND strftime('%m', transaction_date)=strftime('%m', 'now') ORDER BY category", current_session_userid)
        breakdown_categories = list(
            set(category['category'] for category in fetch_user_transactions))
        theads = list(fetch_user_transactions[0].keys())
        return render_template("dashboard.jinja-html", username=current_user, date=formatted_date, labels=chart_labels, values=chart_values, month_labels=months, income=income_data, expense=expense_data, categories=breakdown_categories, table_headers=theads, transact_data=fetch_user_transactions)
    elif request.method == "POST":
        category = escape(request.form.get("category-select"))
        subcat = escape(request.form.get("second-select"))
        amount = escape(request.form.get("transact-amount"))
        active_user = session.get("user_id")

        if validate_form_inputs(category, subcat, amount):
            db.execute(
                "INSERT INTO transactions (user_id, account_title, category, amount) VALUES (?, ?, ?, ?)", active_user, subcat, category, amount)
            data = {'success': True}
            return jsonify(data)
        else:
            data = {'success': False}
            return jsonify(data)
    return render_template("dashboard.jinja-html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
