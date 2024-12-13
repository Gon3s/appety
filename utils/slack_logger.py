from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

class SlackLogger:
    """
    A logger that sends log messages to a Slack user via the Slack API.
    """
    def __init__(self, client: WebClient, user_id: str = None):
        """
        Initialize the SlackLogger.

        :param client: An instance of WebClient to interact with Slack API.
        :param user_id: The Slack user ID to send log messages to.
        """
        self.client = client
        self.user_id = user_id
        self.logs = []
    
    def log(self, message: str):
        """
        Log a message and send it to the specified Slack user.

        :param message: The message to log.
        """
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
        """
        Send a summary of all logged messages to the specified Slack user.
        """
        if self.user_id and self.logs:
            try:
                summary = "\n".join(self.logs)
                self.client.chat_postMessage(
                    channel=self.user_id,
                    text=f"📋 *Résumé des opérations*\n```\n{summary}\n```"
                )
            except SlackApiError as e:
                print(f"Erreur lors de l'envoi du résumé: {e}")
