"""Handle users table data"""


# Second party imports
from . import boot_connection, execute_sql, TRANS_TYPES


# Establish connection to database
boot_connection()


class Transaction:
    """Class to handle transaction data"""

    @staticmethod
    def insert(user_id, ticker, action, shares, price):
        """Insert a transaction into the database"""
        execute_sql(
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
        transactions = execute_sql(
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

        len_transactions = len(transactions)

        formatted_transactions = []
        i = 1
        while i <= len_transactions:
            transaction = transactions[len_transactions - i]
            formatted_transactions.append(
                {
                    "timestamp": transaction["time_stamp"],
                    "name": transaction["name"],
                    "ticker": transaction["ticker"],
                    "price": transaction["price"],
                    "shares": (
                        transaction["shares"] * TRANS_TYPES[transaction["trans_type"]]
                    ),
                    "total": (
                        transaction["shares"]
                        * TRANS_TYPES[transaction["trans_type"]]
                        * transaction["price"]
                    ),
                }
            )
            i += 1

        return formatted_transactions
