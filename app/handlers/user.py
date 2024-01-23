"""Handle users table data"""


# Second party imports
from . import boot_connection, execute_sql


# Establish connection to database
boot_connection()


class User:
    """Class to handle user data"""

    @staticmethod
    def username_exists(username: str):
        """Check if username already exists in the database"""
        user = execute_sql("SELECT * FROM users WHERE username = ?", username)
        return len(user) == 1

    @staticmethod
    def get_hash(username: str):
        """Get the hash of a user"""
        return execute_sql("SELECT hash FROM users WHERE username = ?", username)[0][
            "hash"
        ]

    @staticmethod
    def get_id(username: str):
        """Get the id of a user"""
        return execute_sql("SELECT id FROM users WHERE username = ?", username)[0]["id"]

    @staticmethod
    def insert(username: str, password_hash: str):
        """Insert a user into the database"""
        execute_sql(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            password_hash,
        )

    @staticmethod
    def update_username(user_id: int, username: str):
        """Update user username in the database"""
        execute_sql(
            "UPDATE users SET username = ? WHERE id = ?",
            username,
            user_id,
        )

    @staticmethod
    def update_password(user_id: int, password_hash: str):
        """Update user password in the database"""
        execute_sql(
            "UPDATE users SET hash = ? WHERE id = ?",
            password_hash,
            user_id,
        )

    @staticmethod
    def get_cash(user_id: int):
        """Get the cash value of a user"""
        cash = execute_sql("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        return cash

    @staticmethod
    def update_cash(user_id, cash_change, action):
        """Update user cash"""

        cash_types = {
            "buy": -1,
            "sell": 1,
        }

        cash_change *= cash_types[action]

        execute_sql(
            "UPDATE users SET cash = ? WHERE id = ?",
            User.get_cash(user_id) + cash_change,
            user_id,
        )

    @staticmethod
    def get_username(user_id):
        """Get the username of a user"""
        username = execute_sql("SELECT username FROM users WHERE id = ?", user_id)[0][
            "username"
        ]
        return username
