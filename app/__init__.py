"""The main application file for the project."""


# Built-in imports
from copy import deepcopy as copy
from functools import wraps
import os

# PIP imports
from flask import Flask, jsonify, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# Second party imports
from .helpers import (
    format_number,
    render_error,
    render_template,
    usd,
    validate_cash_value,
    validate_username,
)
from .handlers import (
    ASSETS_DIR,
    COMPANY_NAMES,
    TEMPLATES_DIR,
    Company,
    State,
    Transaction,
    User,
)


# Configure application
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_url_path="/assets",
    static_folder=ASSETS_DIR,
)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(func):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)

    return decorated_function


@app.route("/login/<string:username>/<string:password>")
def get_login_info(username, password):
    """Get login info"""
    if request.method == "GET":
        # Ensure username exists and password is correct
        if (not User.username_exists(username)) or (
            not check_password_hash(User.get_hash(username), password)
        ):
            return render_error("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = User.get_id(username)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_error("Invalid request method", 403)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        if session.get("user_id") is not None:
            return redirect("/")
        return render_template("login.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/register/<string:username>/<string:password>/<string:confirmation>")
def get_register_info(username, password, confirmation):
    """Get register info"""
    if request.method == "GET":
        # Confirmed password matches
        if password != confirmation:
            return render_error("Passwords don't match", 403)

        # Username is unique
        if User.username_exists(username):
            return render_error("Username already exists", 403)

        # Insert user into database
        User.insert(username, generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = User.get_id(username)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_error("Invalid request method", 403)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        if session.get("user_id") is not None:
            return redirect("/")
        return render_template("register.html"), 403

    else:
        return render_error("Invalid request method", 403)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/api/user/summary")
@login_required
def get_summary():
    """Get user summary"""
    if request.method == "GET":
        user_state = State.get_user_state(session["user_id"])

        stocks_total = 0
        for state in user_state:
            stocks_total += state["total"]

        cash = User.get_cash(session["user_id"])

        return jsonify(
            {
                "state": user_state,
                "cash": format_number(cash),
                "stocks_total": format_number(stocks_total),
                "portfolio_total": format_number(stocks_total + cash),
            }
        )
    else:
        return render_error("Invalid request method", 403)


@app.route("/home")
@app.route("/")
@login_required
def homepage():
    """Show portfolio of stocks"""

    if request.method == "GET":
        return render_template("homepage.html")
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/companies")
@login_required
def get_company_names():
    """Get company names"""
    if request.method == "GET":
        return jsonify(COMPANY_NAMES)
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/quote/<string:company_name>")
@login_required
def get_quote(company_name):
    """Get stock quote"""
    if request.method == "GET":
        # Ensure company name is provided
        if not company_name:
            return render_error("Please provide company name", 403)

        # Ensure company name is valid
        if not Company.exists(company_name):
            return render_error("Company name doesn't exist", 403)

        ticker = Company.get_ticker(company_name)

        # Get share price
        price = Company.get_share_price(ticker)

        return jsonify({"price": price})

    else:
        return render_error("Invalid request method", 403)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        # select names column from users table
        return render_template("quote.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/buy/<string:company_name>/<int:shares>")
@login_required
def get_buy_info(company_name, shares):
    """Get buy info"""

    if request.method == "GET":
        # Ensure values are provided
        if not company_name:
            return render_error("Please provide company name", 403)
        if not shares:
            return render_error("Please provide number of shares", 403)

        ticker = Company.get_ticker(company_name)

        # Ensure values are valid
        validate_cash_value(str(shares))

        if not Company.ticker_exists(ticker):
            return render_error("Ticker symbol doesn't exist", 403)

        # Get share price and calculate total cost
        price = Company.get_share_price(ticker)
        total_share_cost = price * shares

        # Get user cash and ensure user has enough cash
        cash = User.get_cash(session["user_id"])
        if cash < total_share_cost:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "insufficient cash",
                    "cash": cash,
                }
            )

        return jsonify(
            {
                "flag": "success",
                "shares": shares,
                "price": price,
                "total_share_cost": total_share_cost,
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/company_names")
@login_required
def get_user_companies():
    """Get user companies"""
    if request.method == "GET":
        return jsonify(State.get_companies(session["user_id"]))
    else:
        return render_error("Invalid request method", 403)


@app.route("/sell/<string:company_name>/<int:shares>")
@login_required
def get_sell_info(company_name, shares):
    """Get sell info"""

    if request.method == "GET":
        # Ensure values are provided
        if not company_name:
            return render_error("Please provide company name", 403)
        if not shares:
            return render_error("Please provide number of shares", 403)

        ticker = Company.get_ticker(company_name)

        # Ensure values are valid
        validate_cash_value(str(shares))

        if not Company.ticker_exists(ticker):
            return render_error("Ticker symbol doesn't exist", 403)

        # Ensure user has shares in the company
        if not State.ticker_exists(session["user_id"], ticker):
            return render_error("You don't have any shares in this company", 403)

        # Ensure user has enough shares
        if shares > State.get_share(session["user_id"], ticker):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "non-existent shares",
                }
            )

        # Get share price and calculate total cost
        price = Company.get_share_price(ticker)
        total_share_cost = price * shares

        # Insert transaction into database
        Transaction.insert(session["user_id"], ticker, "sell", shares, price)

        # Update user cash
        User.update_cash(session["user_id"], total_share_cost, "add")

        # Update user state
        State.update(session["user_id"], ticker, shares, "sell")

        return jsonify(
            {
                "flag": "success",
                "shares": shares,
                "price": price,
                "total_share_cost": total_share_cost,
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        # select names column from users table
        return render_template("sell.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/history")
@login_required
def get_transactions():
    """Get user transactions"""
    if request.method == "GET":
        return jsonify(Transaction.get_all(session["user_id"]))
    else:
        return render_error("Invalid request method", 403)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        return render_template("history.html")
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/username")
@login_required
def get_username():
    """Get username"""
    if request.method == "GET":
        return jsonify(User.get_username(session["user_id"]))
    else:
        return render_error("Invalid request method", 403)


@app.route("/profile/<string:username>")
@login_required
def get_profile_username(username):
    """Get profile username"""
    if request.method == "GET":
        # Ensure values are provided
        if not username:
            return render_error("Please provide username", 403)

        # Validate username
        validate_username(username)

        # Username is unique
        if User.username_exists(username):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "already taken",
                }
            )

        # Username is not changed
        elif not username == User.get_username(session["user_id"]):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "not changed",
                }
            )

        # Update username in database
        User.update_username(session["user_id"], username)

        return jsonify(
            {
                "flag": "success",
                "username": username,
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/profile/<string:old_password>/<string:password>")
@login_required
def get_profile_password(old_password, password):
    """Get profile password"""

    if request.method == "GET":
        # Ensure values are provided
        if not old_password:
            return render_error("Please provide old password", 403)
        if not password:
            return render_error("Please provide new password", 403)

        # Old password is correct
        if not check_password_hash(User.get_hash(session["user_id"]), old_password):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "incorrect password",
                }
            )

        # Update password in database
        User.update_password(session["user_id"], generate_password_hash(password))

        return jsonify(
            {
                "flag": "success",
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def update_profile():
    """Update user profile"""

    if request.method == "GET":
        return render_template("profile.html")

    else:
        return render_error("Invalid request method", 403)
