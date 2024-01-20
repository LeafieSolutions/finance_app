"""The main application file for the project."""


# Built-in imports
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_error("Please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_error("Please provide password", 403)

        # Ensure username exists and password is correct
        if (not User.username_exists(username)) or (
            not check_password_hash(User.get_hash(username), password)
        ):
            return render_error("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = User.get_id(username)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        if session.get("user_id") is not None:
            return redirect("/")
        return render_template("login.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username, password, confirmation = (
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("confirm_password"),
        )

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

    elif request.method == "GET":
        print("SESSION", session.get("user_id"))
        if session.get("user_id") is not None:
            return redirect("/")
        return render_template("register.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/home")
@app.route("/")
@login_required
def homepage():
    """Show portfolio of stocks"""

    if request.method == "POST":
        return render_error("Invalid request method", 403)
    elif request.method == "GET":
        user_id = session["user_id"]
        user_state = State.get_user_state(user_id)

        stocks_total = 0
        for state in user_state:
            stocks_total += state["total"]

        cash = User.get_cash(user_id)

        return render_template(
            "homepage.html",
            **{
                "summary": user_state,
                "cash": format_number(cash),
                "stocks_total": format_number(stocks_total),
                "portfolio_total": format_number(stocks_total + cash),
            },
        )
    else:
        return render_error("Invalid request method", 403)


@app.route("/companies")
@login_required
def get_company_names():
    """Get company names"""
    if request.method == "POST":
        return render_error("Invalid request method", 403)
    elif request.method == "GET":
        return jsonify(COMPANY_NAMES)
    else:
        return render_error("Invalid request method", 403)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        company_name = request.form.get("company_name")

        print(company_name)

        # Ensure company name is provided
        if not company_name:
            return render_error("Please provide company name", 403)

        # Ensure company name is valid
        if not Company.exists(company_name):
            return render_error("Company name doesn't exist", 403)

        ticker = Company.get_ticker(company_name)

        # Get share price
        price = Company.get_share_price(ticker)

        # Show quote popup message
        return render_template(
            "quote_popup.html",
            **{
                "company_name": company_name,
                "price": price,
            },
        )

    elif request.method == "GET":
        # select names column from users table
        return render_template(
            "quote.html",
            **{
                "company_names": COMPANY_NAMES,
            },
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        user_id = session["user_id"]
        company_name = request.form.get("company_name")
        shares = int(request.form.get("shares"))

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
        cash = User.get_cash(user_id)
        if cash < total_share_cost:
            return render_error("Not enough cash", 403)

        # Insert transaction into database
        Transaction.insert(user_id, ticker, "buy", shares, price)

        # Update user cash
        User.update_cash(user_id, total_share_cost, "remove")

        # Update user state
        State.update(user_id, ticker, shares, "buy")

        # Show buy popup message
        return render_template(
            "buy_popup.html",
            **{
                "company_name": company_name,
                "shares": shares,
            },
        )

    elif request.method == "GET":
        return render_template(
            "buy.html",
            **{
                "company_names": COMPANY_NAMES,
            },
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]

    if request.method == "POST":
        company_name = request.form.get("company_name")
        shares = request.form.get("shares")

        # Ensure values are provided
        if not company_name:
            return render_error("Please provide company name", 403)
        if not shares:
            return render_error("Please provide number of shares", 403)

        print(company_name)

        ticker = Company.get_ticker(company_name)

        # Ensure values are valid
        validate_cash_value(shares)

        if not Company.ticker_exists(ticker):
            return render_error("Ticker symbol doesn't exist", 403)

        # Ensure user has shares in the company
        if not State.ticker_exists(user_id, ticker):
            return render_error("You don't have any shares in this company", 403)

        # Ensure user has enough shares
        if shares > State.get_share(user_id, ticker):
            return render_error("You don't have enough shares", 403)

        # Get share price and calculate total cost
        price = Company.get_share_price(ticker)
        total_share_cost = price * shares

        # Insert transaction into database
        Transaction.insert(user_id, ticker, "sell", shares, price)

        # Update user cash
        User.update_cash(user_id, total_share_cost, "add")

        # Update user state
        State.update(user_id, ticker, shares, "sell")

        # Show sell popup message
        return render_template(
            "sell_popup.html",
            **{
                "company_name": company_name,
                "shares": shares,
            },
        )

    elif request.method == "GET":
        # select names column from users table
        return render_template(
            "sell.html",
            **{
                "company_names": State.get_companies(user_id),
            },
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "POST":
        return render_error("Invalid request method", 403)
    elif request.method == "GET":
        return render_template(
            "history.html",
            **{
                "transactions": Transaction.get_all(session["user_id"]),
            },
        )
    else:
        return render_error("Invalid request method", 403)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def update_profile():
    """Update user profile"""

    if request.method == "POST":
        username, password, confirmation = (
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("confirm_password"),
        )

        # Confirmed password matches
        if password != confirmation:
            return render_error("Passwords don't match", 403)

        # Username is unique
        if User.username_exists(username) and (
            not username == User.get_username(session["user_id"])
        ):
            return render_error("Username already exists", 403)

        # Update user info in database
        User.update_info(session["user_id"], username, generate_password_hash(password))

        # Redirect user to home page
        return redirect("/profile-popup")

    elif request.method == "GET":
        username = User.get_username(session["user_id"])
        return render_template(
            "profile.html",
            **{
                "username": username,
            },
        )

    else:
        return render_error("Invalid request method", 403)
