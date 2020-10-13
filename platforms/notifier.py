class Notifier:
    def __init__(self, platform):
        self.platform = platform
        #self.webhook_url = webhook_url

    def notify(self, event_data):
        if self.platform == "discord":
            from platforms.discord import DiscordPlatform
            DiscordPlatform(event_data)
