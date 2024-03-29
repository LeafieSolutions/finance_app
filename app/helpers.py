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

    return (
        render_template(
            "error.html",
            **{
                "error_code": code,
                "error_message": escape(message),
            },
        ),
        code,
    )


def validate_request_method(request, method):
    """Validate request method"""
    if request.method != method:
        return render_error("Invalid request method", 405), 405


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def validate_cash_value(value):
    """Validate cash value"""
    if not value:
        return render_error("Please provide cash value", 403), 403

    if (not value.isdigit()) or (int(value) < 0):
        return render_error("Value must be an integer more than zero", 403), 403


def validate_username(username):
    """Parse username"""
    return regex_match(r"^[a-zA-Z][a-z_A-Z0-9]{3,}$", username)


def validate_password(password):
    """Parse password"""
    return regex_match(r"^\S{6,}$", password)
