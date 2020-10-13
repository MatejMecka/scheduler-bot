import requests
import json
import os

class DiscordPlatform:
    def __init__(self, event_data):
        self.event_data = event_data
        self.load_message()

    def load_message(self):
        """
        Load the JSON Webhook template for Discord and prepend the fields
        :return:
        """
        message_raw = open('message-texts/message-discord.json').read()
        message_raw = self.replace_values(message_raw)
        message_json = json.loads(message_raw)
        self.sendMessage(message_json)

    def replace_values(self, message_raw):
        return message_raw.replace('[EVENT TITLE]', self.event_data['subject'])\
            .replace('[DESCRIPTION]', self.event_data['description'])\
            .replace('[LOCATION]', self.event_data['location'])\



    def sendMessage(self, message_json):
        """
        Send a Message to the Discord Weebhook
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }

        webhook_url = os.environ['WEBHOOK_URL'] 
        response = requests.post(webhook_url, data=json.dumps(message_json), headers=headers)
        if response.status_code == 200:
            print('success!')
