import logging

logging.basicConfig(level=logging.WARN)

from slack_sdk import WebClient

client = WebClient()
api_response = client.api_test()
print(api_response)
