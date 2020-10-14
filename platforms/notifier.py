class Notifier:
    def __init__(self, platform_data):
        self.platform_data = platform_data

    def notify(self, event_data):
        if self.platform_data["platform"] == "discord":
            from platforms.discord import DiscordPlatform
            webhook_url = self.platform_data["webhook_url"]
            DiscordPlatform(event_data, webhook_url)
        if self.platform_data["platform"] == "telegram":
            from platforms.telegram import TelegramPlatform
            api_token = self.platform_data["api_token"]
            chat_id = self.platform_data["chat_id"]
            TelegramPlatform(event_data, api_token, chat_id)
