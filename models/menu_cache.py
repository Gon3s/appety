from database.menu_db import MenuDatabase
from utils.image_utils import get_image_hash

class MenuCache:
    def __init__(self, parser_name: str):
        self.parser_name = parser_name
        self.db = MenuDatabase()

    def is_new_image(self, image_url: str) -> bool:
        current_hash = get_image_hash(image_url)

        if self.db.exists(self.parser_name, current_hash):
            return False

        self.db.add_menu(self.parser_name, current_hash, image_url)
        return True
