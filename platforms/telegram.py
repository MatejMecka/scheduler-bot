import requests
import json
import os
from platforms.utils import replace_values
from errors import NetworkRequestFailed

class TelegramPlatform:
    def __init__(self, event_data, api_token, chat_id):
        self.event_data = event_data
        self.api_token = api_token
        self.chat_id = chat_id
        self.load_message()

    def load_message(self):
        """
        Load the JSON Webhook template for Discord and prepend the fields
        :return:
        """
        message_raw = open('message-texts/message-telegram.txt').read()
        message_raw = self.replace_values(message_raw)
        self.sendMessage(message_raw)

    def sendMessage(self, message_text):
        """
        Send a Message to the Discord Webhook
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }

        url = f"https://api.telegram.org/bot{self.api_token}/sendMessage"

        data = {
            text: message_text,
            chat_id: self.chat_id
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            logging.info('Discord Channel has succesfully been notified!')
        else:
            logging.critical('The Network Request failed!')
            raise NetworkRequestFailed(f"Network Request Failed. Error: {response.text}")
