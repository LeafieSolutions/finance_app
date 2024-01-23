"""Functions to handle data"""


# Builtins imports
from pathlib import Path


# PIP imports
from cs50 import SQL


# Directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"


# Configure CS50 Library to use SQLite database
DB = SQL(f"sqlite:///{DATA_DIR / 'finance.db'}")
execute_sql = DB.execute


# Hot boot
def boot_connection():
    """Boot connection to database"""
    execute_sql("SELECT * FROM sqlite_sequence")


# Define transaction types
TRANS_TYPES = {
    "buy": 1,
    "sell": -1,
}
