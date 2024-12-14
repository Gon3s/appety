import sqlite3

class MenuDatabase:
    """A database manager class for handling menu data storage.
    
    This class provides methods to store and retrieve menu information using SQLite.
    
    Attributes:
        db_path (str): Path to the SQLite database file.
    """

    def __init__(self, db_path="menus.db"):
        """Initialize the MenuDatabase with a specified database path.
        
        Args:
            db_path (str, optional): Path to the database file. Defaults to "menus.db".
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database by creating the required tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS menus (
                    parser_name TEXT,
                    hash TEXT,
                    url TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (parser_name, hash)
                )
            """)

    def add_menu(self, parser_name: str, hash: str, url: str):
        """Add a new menu entry to the database.

        Args:
            parser_name (str): The name of the parser.
            hash (str): The hash value of the menu content.
            url (str): The URL where the menu was found.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO menus (parser_name, hash, url) VALUES (?, ?, ?)",
                (parser_name, hash, url),
            )

    def exists(self, parser_name: str, hash: str) -> bool:
        """Check if a menu with the given parser name and hash exists in the database.

        Args:
            parser_name (str): The name of the parser.
            hash (str): The hash value to check.

        Returns:
            bool: True if the menu exists, False otherwise.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM menus WHERE parser_name = ? AND hash = ?",
                (parser_name, hash),
            )
            return cursor.fetchone() is not None
