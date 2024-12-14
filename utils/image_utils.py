import hashlib
import requests
import base64

def get_image_hash(image_url: str) -> str:
    """
    Récupère le hash MD5 d'une image à partir de son URL ou d'une URL de données base64.

    Args:
        image_url (str): L'URL de l'image ou une URL de données base64.

    Returns:
        str: Le hash MD5 de l'image.
    """
    if image_url.startswith("data:image"):
        # L'image est encodée en base64
        header, encoded = image_url.split(",", 1)
        image_data = base64.b64decode(encoded)
    else:
        # L'image est une URL HTTP/HTTPS
        response = requests.get(image_url)
        image_data = response.content

    return hashlib.md5(image_data).hexdigest()
