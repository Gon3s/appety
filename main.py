from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
from facebook_scraper import get_latest_menu

def post_menu_to_slack():
    """Poste le menu dans le canal Slack spécifié"""
    # Charge les variables d'environnement
    load_dotenv()
    
    # Initialise le client Slack
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    if not slack_token:
        raise ValueError("SLACK_BOT_TOKEN non trouvé dans le fichier .env")
    
    client = WebClient(token=slack_token)
    channel = "#menu-appety"  # Le canal où poster le menu
    
    # Récupère le menu
    menu_data = get_latest_menu()
    
    if not menu_data:
        print("Aucun menu trouvé")
        return
    
    try:
        # Poste le message avec l'image
        response = client.chat_postMessage(
            channel=channel,
            text=f"Menu du jour Appety",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Menu du jour Appety*"
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
        print("Menu posté avec succès!")
        
    except SlackApiError as e:
        print(f"Erreur lors de l'envoi sur Slack: {e.response['error']}")

if __name__ == "__main__":
    post_menu_to_slack()