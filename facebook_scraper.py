from seleniumbase import SB
import time
from typing import Optional, Dict

def get_latest_menu() -> Optional[Dict[str, str]]:
    """
    Récupère le dernier menu posté sur la page Facebook d'Appety.
    
    Returns:
        Optional[Dict[str, str]]: Un dictionnaire contenant l'URL de l'image et le texte alternatif de l'image du dernier menu,
                                  ou None en cas d'erreur.
    """
    APPETY_URL = "https://www.facebook.com/people/Appety/100091477011703/"
    
    with SB(uc=True, headless=True) as sb:
        try:
            # Accès à la page
            sb.driver.get(APPETY_URL)
            time.sleep(3)
            
            # Trouve le premier post
            post = sb.find_element("css selector", "div[aria-posinset='1']")
            
            # Cherche l'image
            image_container = post.find_element("css selector", "div.x78zum5.xdt5ytf.x6ikm8r.x10wlt62.x1n2onr6.xh8yej3")
            image = image_container.find_element("css selector", "img.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3.xl1xv1r")
            
            if image:
                return {
                    "image_url": image.get_attribute('src'),
                    "image_alt": image.get_attribute('alt')
                }
                
        except Exception as e:
            print(f"Erreur lors de la récupération du menu: {e}")
            return None