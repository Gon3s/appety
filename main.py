from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import argparse
import time

from utils.slack_logger import SlackLogger
from models.menu_cache import MenuCache
from parsers import get_parser

def check_and_post_menu(
    client: WebClient,
    parser_name: str,
    channel: str,
    logger: SlackLogger,
    retry_count: int = 0,
    max_retries: int = 4,
    delay_minutes: int = 30,
):
    """
    Vérifie et poste le menu avec retry.

    Args:
        client (WebClient): Le client Slack.
        parser_name (str): Le nom du parser à utiliser.
        channel (str): Le canal Slack où poster le menu.
        logger (SlackLogger): Le logger pour enregistrer les messages.
        retry_count (int, optional): Le nombre de tentatives actuelles. Par défaut à 0.
        max_retries (int, optional): Le nombre maximum de tentatives. Par défaut à 4.
        delay_minutes (int, optional): Le délai entre les tentatives en minutes. Par défaut à 30.

    Returns:
        bool: True si le menu a été posté avec succès, False sinon.
    """
    parser = get_parser(parser_name)
    logger.log(f"📋 Utilisation du parser: {parser_name}")

    while retry_count < max_retries:
        try:
            logger.log(
                f"🔄 Tentative {retry_count + 1}/{max_retries} de récupération du menu"
            )
            menu_data = parser.get_latest_menu()

            if not menu_data:
                logger.log("❌ Aucun menu trouvé pour aujourd'hui")
                return False

            logger.log("✅ Menu récupéré, vérification du cache...")
            cache = MenuCache(parser_name)

            if cache.is_new_image(menu_data["image_url"]):
                logger.log("🆕 Nouveau menu détecté, préparation du message...")

                image_url = menu_data["image_url"]
                if menu_data["image_url"].startswith("data:image"):
                    logger.log("📝 Utilisation du format texte pour le menu")
                    block = {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": menu_data["image_alt"],
                        },
                    }
                else:
                    logger.log("🖼️ Utilisation du format image pour le menu")
                    block = {
                        "type": "image",
                        "title": {
                            "type": "plain_text",
                            "text": menu_data["image_alt"],
                        },
                        "image_url": image_url,
                        "alt_text": "Menu " + parser_name,
                    }

                logger.log(f"📤 Envoi du menu dans le canal {channel}")
                client.chat_postMessage(
                    channel=channel,
                    text=f"Menu du jour {parser_name} (trouvé après {retry_count + 1} tentatives)",
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Menu du jour {parser_name}*\n_Trouvé après {retry_count + 1} tentative(s)_",
                            },
                        },
                        block,
                    ],
                )
                logger.log(f"✅ Menu posté avec succès dans {channel}")
                return True

            retry_count += 1
            if retry_count < max_retries:
                wait_message = f"⏳ Menu inchangé, nouvelle vérification dans {delay_minutes} minutes (tentative {retry_count + 1}/{max_retries})"
                logger.log(wait_message)
                time.sleep(delay_minutes * 60)
            else:
                logger.log(
                    f"❌ Échec: aucun nouveau menu trouvé après {max_retries} tentatives ({max_retries * delay_minutes} minutes)"
                )
                return False

        except Exception as e:
            logger.log(
                f"❌ Erreur lors de la récupération/publication du menu: {str(e)}"
            )
            return False

def post_menu_to_slack(
    parser_name: str,
    channel: str,
    max_retries: int,
    delay_minutes: int,
    log_user: str = None,
):
    """
    Poste le menu dans le canal Slack spécifié.

    Args:
        parser_name (str): Le nom du parser à utiliser.
        channel (str): Le canal Slack où poster le menu.
        max_retries (int): Le nombre maximum de tentatives.
        delay_minutes (int): Le délai entre les tentatives en minutes.
        log_user (str, optional): L'ID utilisateur Slack pour recevoir les logs. Par défaut à None.
    """
    logger = None
    try:
        load_dotenv()

        slack_token = os.getenv("SLACK_BOT_TOKEN")
        if not slack_token:
            raise ValueError("Token Slack non trouvé dans le fichier .env")

        client = WebClient(token=slack_token)
        logger = SlackLogger(client, log_user)

        logger.log(f"🚀 Démarrage du bot ({parser_name})")
        logger.log(
            f"📊 Configuration: canal={channel}, max_retries={max_retries}, delay={delay_minutes}min"
        )

        success = check_and_post_menu(
            client,
            parser_name,
            channel,
            logger,
            max_retries=max_retries,
            delay_minutes=delay_minutes,
        )

        if success:
            logger.log("✨ Exécution terminée avec succès")
        else:
            logger.log("⚠️ Exécution terminée sans avoir trouvé de nouveau menu")

    except Exception as e:
        if logger:
            logger.log(f"💥 Erreur fatale: {str(e)}")
        else:
            print(f"Erreur critique: {str(e)}")
    finally:
        if logger:
            logger.send_summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poste le menu sur Slack")
    parser.add_argument(
        "--parser",
        "-p",
        default="appety",
        help="Nom du parser à utiliser (défaut: appety)",
    )
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
    post_menu_to_slack(
        args.parser, args.channel, args.retries, args.delay, args.log_user
    )
