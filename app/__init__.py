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
    render_error,
    render_template,
    usd,
    validate_request_method,
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


@app.errorhandler(404)
def page_not_found(err):
    """Handle 404 errors"""
    return render_error("Page not found", 404)


@app.route("/api/login/authenticate")
def login_authenticate():
    """Authenticate user"""

    validate_request_method(request, "GET")

    # Redirect user to homepage if already logged in
    if session.get("user_id") is not None:
        return redirect("/")

    username = request.args.get("username")
    password = request.args.get("password")

    # Check if username and password are provided
    if not username:
        return jsonify(
            {
                "flag": "error",
                "reason": "null username",
            }
        )
    if not password:
        return jsonify(
            {
                "flag": "error",
                "reason": "null password",
            }
        )

    else:
        # Ensure username exists and password is correct
        if (not User.username_exists(username)) or (
            not check_password_hash(User.get_hash(username), password)
        ):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid",
                }
            )

        # Remember which user has logged in
        session["user_id"] = User.get_id(username)
        session["username"] = username
        session["hash"] = generate_password_hash(password)

        return jsonify(
            {
                "flag": "success",
            }
        )


@app.route("/login", methods=["GET"])
def render_login_page():
    """Log user in"""

    validate_request_method(request, "GET")

    # Redirect user to homepage if already logged in
    if session.get("user_id") is not None:
        return redirect("/")

    return render_template("login.html")


@app.route("/api/register/username_exists")
def username_exists():
    """Check if username exists"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        username = request.args.get("username")

        # Check if username is provided
        if not username:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null username",
                }
            )

        # Check if username exists
        if User.username_exists(username):
            return jsonify(
                {
                    "flag": "success",
                    "answer": "exist",
                }
            )
        else:
            return jsonify(
                {
                    "flag": "success",
                    "answer": "not exist",
                }
            )

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/register")
def register_user():
    """Create user"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        # Redirect user to homepage if already logged in
        if session.get("user_id") is not None:
            return redirect("/")

        username = request.args.get("username")
        password = request.args.get("password")

        # Check if username, password, and confirmation are provided
        if not username:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null username",
                }
            )
        if not password:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null password",
                }
            )

        # Validate username
        if not validate_username(username):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid username",
                }
            )

        # Username is unique
        if User.username_exists(username):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "username exists",
                }
            )

        # Insert user into database
        User.insert(username, generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = User.get_id(username)
        session["username"] = username
        session["hash"] = generate_password_hash(password)

        return jsonify(
            {
                "flag": "success",
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/register", methods=["GET"])
def render_register_page():
    """Register user"""

    if request.method == "GET":
        if session.get("user_id") is not None:
            return redirect("/")
        return render_template("register.html"), 403

    else:
        return render_error("Invalid request method", 403)


@app.route("/logout")
def logout_user():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/api/user/summary")
@login_required
def get_user_summary():
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
                "cash": cash,
                "stocks_total": stocks_total,
                "portfolio_total": stocks_total + cash,
            }
        )
    else:
        return render_error("Invalid request method", 403)


@app.route("/home")
@app.route("/")
@login_required
def render_home_page():
    """Show portfolio of stocks"""

    if request.method == "GET":
        return render_template("homepage.html")
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/company_names")
@login_required
def get_company_names():
    """Get company names"""
    if request.method == "GET":
        return jsonify(COMPANY_NAMES)
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/quote/")
@login_required
def get_stock_quote():
    """Get stock quote"""
    if request.method == "GET":
        company_name = request.args.get("company_name")

        # Ensure company name is provided
        if not company_name:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null company_name",
                }
            )

        # Ensure company name is valid
        if not Company.exists(company_name):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid company_name",
                }
            )

        ticker = Company.get_ticker(company_name)

        # Get share price
        price = Company.get_share_price(ticker)

        return jsonify(
            {
                "flag": "success",
                "ticker": ticker,
                "name": company_name,
                "price": price,
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/quote", methods=["GET"])
@login_required
def render_quote_page():
    """Get stock quote."""

    if request.method == "GET":
        # select names column from users table
        return render_template("quote.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/buy")
@login_required
def buy_stock():
    """Get buy info"""

    if request.method == "GET":
        company_name = request.args.get("company_name")
        shares = request.args.get("shares", type=int)

        # Ensure values are provided
        if not company_name:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null company_name",
                }
            )
        if not shares:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null shares",
                }
            )

        if shares <= 0 or not isinstance(shares, int):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid shares",
                }
            )

        if not Company.exists(company_name):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid company_name",
                }
            )

        ticker = Company.get_ticker(company_name)

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

        # Insert transaction into database
        Transaction.insert(session["user_id"], ticker, "buy", shares, price)

        # Update user cash
        User.update_cash(session["user_id"], total_share_cost, "buy")

        # Update user state
        State.update(session["user_id"], ticker, shares, "buy")

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


@app.route("/buy", methods=["GET"])
@login_required
def render_buy_page():
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


@app.route("/api/sell")
@login_required
def sell_stock():
    """Get sell info"""

    if request.method == "GET":
        company_name = request.args.get("company_name")
        shares = request.args.get("shares", type=int)

        # Ensure values are provided
        if not company_name:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null company_name",
                }
            )
        if not shares:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null shares",
                }
            )

        if shares <= 0 or not isinstance(shares, int):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid shares",
                }
            )

        if not company_name in State.get_companies(session["user_id"]):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid company_name",
                }
            )

        ticker = Company.get_ticker(company_name)

        # Ensure user has enough shares
        current_user_shares = State.get_share(session["user_id"], ticker)
        if shares > current_user_shares:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "insufficient shares",
                    "shares": current_user_shares,
                }
            )

        # Get share price and calculate total cost
        price = Company.get_share_price(ticker)
        total_share_cost = price * shares

        # Insert transaction into database
        Transaction.insert(session["user_id"], ticker, "sell", shares, price)

        # Update user cash
        User.update_cash(session["user_id"], total_share_cost, "sell")

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


@app.route("/sell", methods=["GET"])
@login_required
def render_sell_page():
    """Sell shares of stock"""

    if request.method == "GET":
        # select names column from users table
        return render_template("sell.html")

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/history")
@login_required
def get_user_history():
    """Get user transactions"""
    if request.method == "GET":
        return jsonify(Transaction.get_all(session["user_id"]))
    else:
        return render_error("Invalid request method", 403)


@app.route("/history")
@login_required
def render_history_page():
    """Show history of transactions"""
    if request.method == "GET":
        return render_template("history.html")
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/profile/username")
@login_required
def get_username():
    """Get username"""
    if request.method == "GET":
        return jsonify(session["username"])
    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/profile/change/username")
@login_required
def change_profile():
    """Get profile username"""
    if request.method == "GET":
        new_username = request.args.get("new_username")

        # Ensure values are provided
        if not new_username:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null username",
                }
            )

        # Validate username
        if not validate_username(new_username):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "invalid username",
                }
            )

        # Username is unique
        # Username is not changed
        if new_username == User.get_username(session["user_id"]):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "not changed",
                }
            )
        elif User.username_exists(new_username):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "already taken",
                }
            )

        # Update username in database
        User.update_username(session["user_id"], new_username)

        session["username"] = new_username

        return jsonify(
            {
                "flag": "success",
                "username": new_username,
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/api/user/profile/change/password")
@login_required
def get_profile_password():
    """Get profile password"""

    if request.method == "GET":
        old_password = request.args.get("old_password")
        new_password = request.args.get("new_password")

        # Ensure values are provided
        if not old_password:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null old_password",
                }
            )
        if not new_password:
            return jsonify(
                {
                    "flag": "error",
                    "reason": "null new_password",
                }
            )

        # Old password is correct
        if not check_password_hash(session["hash"], old_password):
            return jsonify(
                {
                    "flag": "error",
                    "reason": "incorrect old_password",
                }
            )

        # Modify hash in session
        session["hash"] = generate_password_hash(new_password)

        # Update password in database
        User.update_password(session["user_id"], generate_password_hash(new_password))

        return jsonify(
            {
                "flag": "success",
            }
        )

    else:
        return render_error("Invalid request method", 403)


@app.route("/profile", methods=["GET"])
@login_required
def update_profile():
    """Update user profile"""

    if request.method == "GET":
        return render_template("profile.html")

    else:
        return render_error("Invalid request method", 403)
