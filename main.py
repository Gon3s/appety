from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
import argparse
from facebook_scraper import get_latest_menu
import hashlib
import json
from datetime import datetime
import requests
import time

class SlackLogger:
    def __init__(self, client: WebClient, user_id: str = None):
        self.client = client
        self.user_id = user_id
        self.logs = []
    
    def log(self, message: str):
        """Log un message et l'envoie à l'utilisateur si configuré"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.logs.append(log_message)
        
        if self.user_id:
            try:
                self.client.chat_postMessage(
                    channel=self.user_id,
                    text=f"🤖 *Log*: {message}"
                )
            except SlackApiError as e:
                print(f"Erreur lors de l'envoi du log: {e}")

    def send_summary(self):
        """Envoie un résumé des logs à l'utilisateur"""
        if self.user_id and self.logs:
            try:
                summary = "\n".join(self.logs)
                self.client.chat_postMessage(
                    channel=self.user_id,
                    text=f"📋 *Résumé des opérations*\n```\n{summary}\n```"
                )
            except SlackApiError as e:
                print(f"Erreur lors de l'envoi du résumé: {e}")


class MenuCache:
    def __init__(self, cache_file="menu_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def is_new_image(self, image_url: str) -> bool:
        current_hash = get_image_hash(image_url)
        last_hash = self.cache.get('last_hash')
        
        self.cache['last_hash'] = current_hash
        self.cache['last_update'] = datetime.now().isoformat()
        self._save_cache()
        
        return last_hash != current_hash

def get_image_hash(image_url: str) -> str:
    response = requests.get(image_url)
    return hashlib.md5(response.content).hexdigest()


def check_and_post_menu(client: WebClient, channel: str, logger: SlackLogger, retry_count: int = 0, max_retries: int = 4, delay_minutes: int = 30):
    """Vérifie et poste le menu avec retry"""
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
    """Poste le menu dans le canal Slack spécifié"""
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
