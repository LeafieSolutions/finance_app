"""Main execution module for the application"""


# Second-party modules
from . import app


# Main execution
if __name__ == "__main__":
    app.run(debug=True)
