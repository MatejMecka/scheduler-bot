import requests
import json
import os
import logging
from errors import NetworkRequestFailed
from platforms.utils import replace_values

class DiscordPlatform:
    def __init__(self, event_data, webhook_url):
        self.event_data = event_data
        self.webhook_url = webhook_url
        self.load_message()

    def load_message(self):
        """
        Load the JSON Webhook template for Discord and prepend the fields
        :return:
        """
        message_raw = open('message-texts/message-discord.json').read()
        message_raw = replace_values(message_raw, self.event_data)
        message_json = json.loads(message_raw)
        self.sendMessage(message_json)

    def sendMessage(self, message_json):
        """
        Send a Message to the Discord Weebhook
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }

        webhook_url = self.webhook_url
        response = requests.post(webhook_url, data=json.dumps(message_json), headers=headers)
        if response.status_code == 200:
            logging.info('Discord Channel has succesfully been notified!')
        else:
            logging.critical('The Network Request failed!')
            raise NetworkRequestFailed(f"Network Request Failed. Error: {response.text}")
