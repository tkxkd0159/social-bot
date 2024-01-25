import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, token):
        self.client = WebClient(token=token)
        self.conversations_store = {}

    def fetch_conversations(self):
        try:
            result = self.client.conversations_list()
            for conversation in result["channels"]:
                self.conversations_store[conversation["id"]] = conversation

        except SlackApiError as e:
            logger.error("Error fetching conversations: {}".format(e))

    def post_message(self, channel, text):
        try:
            result = self.client.chat_postMessage(
                as_user=True, channel=channel, text=text
            )
            return result
        except SlackApiError as e:
            logger.error("Error posting message: {}".format(e))


def health_check():
    client = WebClient()
    result = client.api_test()
    if not result["ok"]:
        raise Exception(result["error"])
