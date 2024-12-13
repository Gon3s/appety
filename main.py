from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import argparse
from facebook_scraper import get_latest_menu
import time

from utils.slack_logger import SlackLogger
from models.menu_cache import MenuCache

def check_and_post_menu(client: WebClient, channel: str, logger: SlackLogger, retry_count: int = 0, max_retries: int = 4, delay_minutes: int = 30):
    """
    Vérifie et poste le menu avec retry.

    Args:
        client (WebClient): Le client Slack.
        channel (str): Le canal Slack où poster le menu.
        logger (SlackLogger): Le logger pour enregistrer les messages.
        retry_count (int, optional): Le nombre de tentatives actuelles. Par défaut à 0.
        max_retries (int, optional): Le nombre maximum de tentatives. Par défaut à 4.
        delay_minutes (int, optional): Le délai entre les tentatives en minutes. Par défaut à 30.

    Returns:
        bool: True si le menu a été posté avec succès, False sinon.
    """
    while retry_count < max_retries:
        try:
            logger.log(f"Tentative {retry_count + 1}/{max_retries} de récupération du menu")
            menu_data = get_latest_menu()
            
            if not menu_data:
                logger.log("❌ Aucun menu trouvé")
                return False

            cache = MenuCache()
            if cache.is_new_image(menu_data["image_url"]):
                # Nouveau menu trouvé
                logger.log("✅ Nouveau menu détecté")
                client.chat_postMessage(
                    channel=channel,
                    text=f"Menu du jour Appety (trouvé après {retry_count + 1} tentatives)",
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Menu du jour Appety*\n_Trouvé après {retry_count + 1} tentative(s)_"
                            }
                        },
                        {
                            "type": "image",
                            "title": {
                                "type": "plain_text",
                                "text": menu_data["image_alt"] or "Menu Appety"
                            },
                            "image_url": menu_data["image_url"],
                            "alt_text": menu_data["image_alt"] or "Menu Appety"
                        }
                    ]
                )
                logger.log(f"✅ Menu posté avec succès dans {channel}")
                return True
            
            retry_count += 1
            if retry_count < max_retries:
                wait_message = f"⏳ Menu inchangé, nouvelle vérification dans {delay_minutes} minutes"
                logger.log(wait_message)
                time.sleep(delay_minutes * 60)
            else:
                logger.log(f"❌ Aucun nouveau menu trouvé après {max_retries * delay_minutes} minutes")
                return False
                
        except Exception as e:
            logger.log(f"❌ Erreur: {str(e)}")
            return False

def post_menu_to_slack(channel: str, max_retries: int, delay_minutes: int, log_user: str = None):
    """
    Poste le menu dans le canal Slack spécifié.

    Args:
        channel (str): Le canal Slack où poster le menu.
        max_retries (int): Le nombre maximum de tentatives.
        delay_minutes (int): Le délai entre les tentatives en minutes.
        log_user (str, optional): L'ID utilisateur Slack pour recevoir les logs. Par défaut à None.
    """
    load_dotenv()
    
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    if not slack_token:
        raise ValueError("SLACK_BOT_TOKEN non trouvé dans le fichier .env")
    
    client = WebClient(token=slack_token)
    logger = SlackLogger(client, log_user)
    
    logger.log("🚀 Démarrage de la récupération du menu")
    check_and_post_menu(client, channel, logger, max_retries=max_retries, delay_minutes=delay_minutes)
    logger.send_summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Poste le menu Appety sur Slack')
    parser.add_argument('--channel', '-c', 
                       default='#appety-menu',
                       help='Nom du channel Slack (défaut: #appety-menu)')
    parser.add_argument('--retries', '-r',
                       type=int,
                       default=5,
                       help='Nombre maximum de tentatives (défaut: 5)')
    parser.add_argument('--delay', '-d',
                       type=int,
                       default=30,
                       help='Délai entre les tentatives en minutes (défaut: 30)')
    parser.add_argument('--log-user', '-l',
                       help='ID utilisateur Slack pour recevoir les logs (ex: @U1234567)')
    
    args = parser.parse_args()
    post_menu_to_slack(args.channel, args.retries, args.delay, args.log_user)
