import hashlib
import requests

def get_image_hash(image_url: str) -> str:
    """
    Récupère le hash MD5 d'une image à partir de son URL.
    
    Args:
        image_url (str): L'URL de l'image.
        
    Returns:
        str: Le hash MD5 de l'image.
    """
    response = requests.get(image_url)
    return hashlib.md5(response.content).hexdigest()
