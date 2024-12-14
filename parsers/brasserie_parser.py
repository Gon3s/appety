from seleniumbase import SB
import time
from typing import Optional, Dict
from parsers.base_parser import BaseParser
import base64


class BrasserieParser(BaseParser):
    """Parser for La Brasserie."""

    @property
    def name(self) -> str:
        return "brasserie"

    def get_latest_menu(self) -> Optional[Dict[str, str]]:
        BRASSERIE_URL = "https://labrasserie-aubiere.fr/"

        with SB(uc=True, headless=True) as sb:
            try:
                # Accès à la page
                sb.open(BRASSERIE_URL)
                time.sleep(3)

                # Trouve la div featuretext_middle
                menu_div = sb.find_element("css selector", "div.featuretext_middle")

                if menu_div:
                    # Capture le contenu texte
                    menu_text = menu_div.text

                    # Prend un screenshot de la div
                    menu_div.screenshot("brasserie_menu.png")

                    # Encode l'image redimensionnée en base64 pour l'URL
                    with open("brasserie_menu_resized.png", "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode()

                    # Crée l'URL de données
                    data_url = f"data:image/png;base64,{img_base64}"

                    return {
                        "image_url": data_url,
                        "image_alt": menu_text,
                    }

            except Exception as e:
                print(f"Erreur lors de la récupération du menu: {e}")
                return None
        return None
