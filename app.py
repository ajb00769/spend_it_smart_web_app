from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, flash, jsonify
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from cs50 import SQL
from datetime import timedelta, date, datetime
from login_utils import check_password, register, login_required
from form_validation import validate_form_inputs
from spend_it_smart_classes import CategorySums
import os


app = Flask(__name__)
app.secret_key = os.environ.get('CSRF_SECRET_KEY')
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_REFRESH_EACH_REQUEST"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config['PREFERRED_URL_SCHEME'] = 'https'


Session(app)
csrf = CSRFProtect(app)
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
    # response.headers["Content-Security-Policy"] = "default-src 'self' https://spend-it-smart-web-app.vercel.app";
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
            email = request.form.get("em")
            password = request.form.get("pw")

            error_msg = check_password(email, password)

            if error_msg:
                flash((error_msg, 'error'))

        elif register_pressed == "register":
            user = request.form.get("uname-reg")
            email = request.form.get("email-reg")
            password = request.form.get("pw-reg")
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
        formatted_date = date.today().strftime("%B %d, %Y")

        # fetch all user transactions since account creation, do not include user_id for security (sensitive data)

        fetch_user_transactions = db.execute(
            "SELECT transaction_id, account_title, category, amount, transaction_date FROM transactions WHERE user_id=?", current_session_userid)

        # create object instance for current month

        current_month_sums = CategorySums()

        # filter transactions to only current MONTH

        current_month_transacts = []

        for transaction in fetch_user_transactions:
            date_str = transaction['transaction_date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date_obj.month == datetime.now().month:
                current_month_transacts.append(transaction)

        # iteratively sort per category for the current MONTH

        for transaction in current_month_transacts:
            category = transaction['category']
            amount = transaction['amount']
            current_month_sums.increment(category, amount)

        # filter transactions for current YEAR

        current_month_dict = vars(current_month_sums)
        current_month_labels = list(current_month_dict.keys())
        current_month_values = list(current_month_dict.values())

        # bar chart data

        current_year_transacts = []

        # gets all user transactions for the current year

        relevant_transactions = ['purchase', 'income', 'sell']

        for transaction in fetch_user_transactions:
            date_str = transaction['transaction_date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date_obj.year == datetime.now().year and transaction['category'] in relevant_transactions:
                current_year_transacts.append(transaction)

        sorted_transactions = sorted(
            current_year_transacts, key=lambda x: x['transaction_date'])

        monthly_transactions = {}

        for transaction in sorted_transactions:
            transaction_date = datetime.strptime(
                transaction['transaction_date'], '%Y-%m-%d %H:%M:%S')
            month = transaction_date.strftime('%B')
            monthly_transactions.setdefault(month, []).append(transaction)

        totals = {}

        for month, transactions in monthly_transactions.items():
            totals[month] = {}
            for category in relevant_transactions:
                total_amount = 0
                for transaction in transactions:
                    if transaction['category'] == category:
                        total_amount += transaction['amount']
                totals[month][category] = total_amount

        totals_values = list(totals.values())

        bar_chart_purchases = [item['purchase'] for item in totals_values]
        bar_chart_income = [item['income'] for item in totals_values]
        bar_chart_sell = [item['sell'] for item in totals_values]

        breakdown_headers = ['transaction_date', 'account_title', 'amount']

        breakdown_transacts = []

        for transaction in current_year_transacts:
            if transaction['account_title'] == 'businesssvc':
                transaction['account_title'] = 'Service Income'
            else:
                transaction['account_title'] = transaction['account_title'].title()
            date_string = transaction['transaction_date']
            date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            transaction['transaction_date'] = date_obj.strftime('%m/%d/%Y')
            transaction['amount'] = "{:,.2f}".format(transaction['amount'])
            breakdown_transacts.append(transaction)

        return render_template("dashboard.jinja-html", username=current_user, date=formatted_date, labels=current_month_labels, values=current_month_values, categories=current_month_labels, months=list(totals.keys()), income=bar_chart_income, sell=bar_chart_sell, expense=bar_chart_purchases, table_headers=breakdown_headers, transact_data=current_year_transacts)

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
    return render_template("dashboard.jinja-html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()

# TEST ACCOUNT
# uname: test_user
# email: test@test.com
# pw: &%H7wuScgiq?
