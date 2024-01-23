"""Handle users table data"""


# Second party imports
from . import boot_connection, execute_sql, TRANS_TYPES
from .company import Company


# Establish connection to database
boot_connection()


class State:
    """Class to handle state data"""

    @staticmethod
    def get_share(user_id, ticker):
        """Get the state of a user"""
        return execute_sql(
            """
            SELECT shares FROM states
            WHERE user_id = ? AND comp_ticker = ?
            """,
            user_id,
            ticker,
        )[0]["shares"]

    @staticmethod
    def get_user_state(user_id) -> list:
        """Get the state of a user"""

        ticker_states = execute_sql(
            "SELECT comp_ticker, shares FROM states WHERE user_id = ?",
            user_id,
        )

        formatted_states = []
        for ticker_state in ticker_states:
            shares = ticker_state["shares"]

            if shares > 0:
                price = Company.get_share_price(ticker_state["comp_ticker"])
                formatted_states.append(
                    {
                        "name": Company.get_name(ticker_state["comp_ticker"]),
                        "ticker": ticker_state["comp_ticker"],
                        "price": price,
                        "shares": shares,
                        "total": ticker_state["shares"] * price,
                    }
                )

        formatted_states.sort(key=lambda x: x["name"], reverse=False)
        return formatted_states

    @staticmethod
    def get_companies(user_id):
        """Get all companies of a user"""
        tickers = execute_sql(
            """
            SELECT comp_ticker FROM states
            WHERE user_id = ?
            """,
            user_id,
        )
        return [Company.get_name(ticker["comp_ticker"]) for ticker in tickers]

    @staticmethod
    def state_exists(user_id, ticker):
        """Check if state exists"""
        state = execute_sql(
            """
            SELECT comp_ticker FROM states
            WHERE user_id = ? AND comp_ticker = ?
            """,
            user_id,
            ticker,
        )
        return len(state) == 1

    @staticmethod
    def update(user_id, ticker, shares, action):
        """Update the state of a user"""

        if not State.state_exists(user_id, ticker):
            execute_sql(
                """
                INSERT INTO states (user_id, comp_ticker, shares)
                VALUES (?, ?, ?)
                """,
                user_id,
                ticker,
                0,
            )

        current_shares = State.get_share(user_id, ticker)

        shares *= TRANS_TYPES[action]
        shares += current_shares

        execute_sql(
            """
            UPDATE states SET shares = ?
            WHERE user_id = ? AND comp_ticker = ?
            """,
            shares,
            user_id,
            ticker,
        )

    @staticmethod
    def get_shares(user_id):
        """Get shares owned by a user"""

        ticker_states = execute_sql(
            "SELECT comp_ticker, shares FROM states WHERE user_id = ?",
            user_id,
        )

        shares_info = {}
        for ticker_state in ticker_states:
            shares = ticker_state["shares"]
            if shares > 0:
                name = Company.get_name(ticker_state["comp_ticker"])
                shares_info[name] = shares

        return shares_info
