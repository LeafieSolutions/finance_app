"""Handle companies table data"""


# Builtins imports

from datetime import datetime, timedelta
from os import environ
from urllib.parse import quote_plus as url_quote

# PIP imports
from requests import get as get_request, RequestException

# Second party imports
from . import boot_connection, execute_sql


# Establish connection to database
boot_connection()


# Get API url
API_KEY = environ.get("API_KEY")


def iex_ticker_url(ticker):
    """Get API url"""
    return f"https://cloud.iexapis.com/stable/stock/{url_quote(ticker)}/quote?token={API_KEY}"


class Company:
    """Class to handle company data"""

    @staticmethod
    def get_names():
        """Get all company names"""
        return [
            company["name"] for company in execute_sql("SELECT name FROM companies")
        ]

    @staticmethod
    def ticker_exists(ticker):
        """Check if ticker already exists in the database"""
        ticker = execute_sql("SELECT ticker FROM companies WHERE ticker = ?", ticker)
        return len(ticker) == 1

    @staticmethod
    def get_ticker(company_name):
        """Get the ticker symbol of a company"""
        ticker = execute_sql(
            "SELECT ticker FROM companies WHERE name = ?", company_name
        )[0]["ticker"]
        return ticker

    @staticmethod
    def get_name(ticker):
        """Get the name of a company"""
        name = execute_sql("SELECT name FROM companies WHERE ticker = ?", ticker)[0][
            "name"
        ]
        return name

    @staticmethod
    def exists(company_name):
        """Check if company name already exists in the database"""
        return company_name in Company.get_names()

    @staticmethod
    def get_last_update(ticker):
        """Get the last update of a company"""
        update_string = execute_sql(
            "SELECT last_update FROM companies WHERE ticker = ?", ticker
        )[0]["last_update"]

        return datetime.strptime(update_string, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_latest_price(ticker):
        """Get the latest price of a company"""
        return execute_sql(
            "SELECT latest_price FROM companies WHERE ticker = ?", ticker
        )[0]["latest_price"]

    @staticmethod
    def update_price(ticker, price):
        """Update the latest price  and last update time of a company"""
        execute_sql(
            "UPDATE companies SET latest_price = ?, last_update = ? WHERE ticker = ?",
            price,
            datetime.now(),
            ticker,
        )

    @staticmethod
    def get_share_price(ticker):
        """Get the share price of a company"""

        # Check if ticker exists
        if not Company.ticker_exists(ticker):
            raise ValueError("Ticker does not exist")

        # Check if 3 hours have passed since last update
        last_update = Company.get_last_update(ticker)
        if datetime.now() - last_update <= timedelta(hours=3):
            return Company.get_latest_price(ticker)
        else:
            # Contact API
            try:
                response = get_request(iex_ticker_url(ticker), timeout=3)

                # Raise for status
                response.raise_for_status()

            except RequestException as err:
                raise RequestException(err.response.text) from err

            # Parse response
            try:
                latest_price = response.json()["latestPrice"]

                # Update price
                Company.update_price(ticker, latest_price)

                return float(latest_price)

            except (KeyError, TypeError, ValueError) as err:
                raise RequestException("Unable to parse IEX API response") from err
