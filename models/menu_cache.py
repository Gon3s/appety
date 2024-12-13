from database.menu_db import MenuDatabase
from utils.image_utils import get_image_hash

class MenuCache:
    """
    A class to manage caching of menu images and avoid processing duplicate images.
    Uses a database to store image hashes and their corresponding URLs.
    """

    def __init__(self):
        """Initialize the MenuCache with a database connection."""
        self.db = MenuDatabase()
    
    def is_new_image(self, image_url: str) -> bool:
        """
        Check if an image is new by comparing its hash with stored hashes.
        
        Args:
            image_url (str): The URL of the image to check
            
        Returns:
            bool: True if the image is new, False if it already exists in cache
        """
        current_hash = get_image_hash(image_url)
        
        if self.db.exists(current_hash):
            return False
        
        self.db.add_menu(current_hash, image_url)
        return True
