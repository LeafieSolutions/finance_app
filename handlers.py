"""Functions to handle data"""


# Builtins imports
from json import dump, load
from os import environ
from urllib.parse import quote_plus as url_quote

# PIP imports
from cs50 import SQL
from requests import get as get_request, RequestException

# Second-party imports
from helpers import init_cls, render_error


# Configure CS50 Library to use SQLite database
DB = SQL("sqlite:///data/finance.db")


# Get company names from database
COMPANY_NAMES = DB.execute("SELECT name FROM companies")

# Define transaction types
TRANS_TYPES = {
    "buy": 1,
    "sell": -1,
}

# Get API url
API_KEY = environ.get("API_KEY")
API_URL = (
    lambda ticker: f"https://cloud.iexapis.com/stable/stock/{url_quote(ticker)}/quote?token={API_KEY}"
)


class User:
    """Class to handle user data"""

    @staticmethod
    def username_exists(username: str):
        """Check if username already exists in the database"""
        user = DB.execute("SELECT * FROM users WHERE username = ?", username)
        return len(user) == 1

    @staticmethod
    def get_hash(username: str):
        """Get the hash of a user"""
        return DB.execute("SELECT hash FROM users WHERE username = ?", username)

    @staticmethod
    def get_id(username: str):
        """Get the id of a user"""
        return DB.execute("SELECT id FROM users WHERE username = ?", username)

    @staticmethod
    def insert(username: str, password_hash: str):
        """Insert a user into the database"""
        DB.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            password_hash,
        )

    @staticmethod
    def update_info(user_id: int, username: str, password_hash: str):
        """Update user info in the database"""
        DB.execute(
            "UPDATE users SET username = ?, hash = ? WHERE id = ?",
            username,
            password_hash,
            user_id,
        )

    @staticmethod
    def get_cash(user_id: str):
        """Get the cash value of a user"""
        cash = DB.execute("SELECT cash FROM users WHERE id = ?", user_id)
        return cash

    @staticmethod
    def update_cash(user_id, cash_change, action):
        """Update user cash"""
        if action == "remove":
            DB.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                User.get_cash(user_id) - cash_change,
                user_id,
            )
        elif action == "add":
            DB.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                User.get_cash(user_id) + cash_change,
                user_id,
            )
        else:
            raise RuntimeError(f"Invalid action: '{action}'")

    @staticmethod
    def get_username(user_id):
        """Get the username of a user"""
        username = DB.execute("SELECT username FROM users WHERE id = ?", user_id)
        return username


class Company:
    """Class to handle company data"""

    @staticmethod
    def ticker_exists(ticker):
        """Check if ticker already exists in the database"""
        ticker = DB.execute("SELECT * FROM companies WHERE ticker = ?", ticker)
        return len(ticker) == 1

    @staticmethod
    def get_ticker(company_name):
        """Get the ticker symbol of a company"""
        ticker = DB.execute("SELECT ticker FROM companies WHERE name = ?", company_name)
        return ticker

    @staticmethod
    def get_name(ticker):
        """Get the name of a company"""
        name = DB.execute("SELECT name FROM companies WHERE ticker = ?", ticker)
        return name

    @staticmethod
    def exists(company_name):
        """Check if company name already exists in the database"""
        return company_name in COMPANY_NAMES

    @staticmethod
    def get_share_price(ticker):
        """Get the share price of a company"""

        # Contact API
        try:
            response = get_request(API_URL(ticker), timeout=3)
            response.raise_for_status()
        except RequestException:
            return render_error("API request failed", 403)

        # Parse response
        try:
            quote = response.json()
            return float(quote["latestPrice"])

        except (KeyError, TypeError, ValueError):
            return render_error("Invalid response", 403)


class Transaction:
    """Class to handle transaction data"""

    @staticmethod
    def insert(user_id, ticker, action, shares, price):
        """Insert a transaction into the database"""
        DB.execute(
            """
            INSERT INTO transactions (user_id, comp_ticker, trans_type, shares, price)
            VALUES (?, ?, ?, ?, ?)
            """,
            user_id,
            ticker,
            action,
            shares,
            price,
        )

    @staticmethod
    def get_all(user_id):
        """Get all transactions of a user"""
        transactions = DB.execute(
            """
            SELECT 
                transactions.time_stamp,
                companies.name,
                companies.ticker,
                transactions.trans_type,
                transactions.price,
                transactions.shares
            FROM transactions
            INNER JOIN companies ON transactions.comp_ticker = companies.ticker
            WHERE transactions.user_id = ?
            """,
            user_id,
        )
        return transactions


@init_cls
class State:
    """Class to handle state data"""

    @classmethod
    def init(cls):
        """Initialize the class"""
        cls.refresh()

    @classmethod
    def get_share(cls, user_id, ticker):
        """Get the state of a user"""
        return cls.STATES[user_id][ticker]

    @classmethod
    def get_user_state(cls, user_id) -> dict:
        """Get the state of a user"""
        return cls.STATES[user_id]

    @classmethod
    def update(cls, user_id, ticker, shares, action):
        """Update the state of a user"""

        if user_id not in cls.STATES:
            cls.STATES[user_id] = {}

        if ticker not in cls.STATES[user_id]:
            cls.STATES[user_id][ticker] = 0

        cls.STATES[user_id][ticker] += shares * TRANS_TYPES[action]

        with open("data/states.json", mode="w", encoding="utf-8") as f:
            dump(cls.STATES, f)

        cls.refresh()

    @classmethod
    def refresh(cls) -> None:
        """Refresh data of states"""

        with open("data/states.json", mode="r", encoding="utf-8") as f:
            cls.STATES = load(f)
