"""Helper functions"""


# Built-in imports
from re import match as regex_match

# PIP imports
from flask import render_template


def render_error(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message)), code


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def format_number(value):
    """Format value as USD."""
    return round(value, 2)


def validate_cash_value(value):
    """Validate cash value"""
    if not value:
        return render_error("Please provide cash value", 403)

    if (not value.isdigit()) or (int(value) < 0):
        return render_error("Value must be an integer more than zero", 403)


def validate_username(username):
    """Parse username"""

    if not regex_match(r"^[a-zA-Z][a-z_A-Z0-9]{3,}$", username):
        return render_error("Invalid username", 403)
