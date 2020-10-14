import fire
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
from icalendar import Calendar, Event
import recurring_ical_events
from platforms.notifier import Notifier
from datetime import datetime, timedelta
import os
import logging
from errors import NetworkRequestFailed, MissingResource
#logging.basicConfig(filename='schedule_bot.log', level=logging.DEBUG)

class SchedulerBot:
    def __init__(self, platform_data, minutes_before_event):
        self.platform_data = platform_data
        self.minutes_before_event = minutes_before_event

    def parse_events(self, cal_resource):
        """
        :param ical_resource:
        :return:
        """
        events = []
        calendar = Calendar.from_ical(cal_resource)
        logging.info('Found the following events!')

        start_date = (2020,1,1)
        end_date = (2021,1,1)

        for event in recurring_ical_events.of(calendar).between(start_date, end_date):
            if event.name == "VEVENT":
                event_data = {
                    "subject": event["summary"].to_ical().decode('utf-8'),
                    "description": event["description"].to_ical().decode('utf-8'),
                    "start_date": event["dtstart"].dt,
                    "location": event["location"].to_ical().decode('utf-8')
                }
                logging.info(event_data)
                #print(event_data)
                events.append(event_data)
        self.schedule_events(events)


    def schedule_events(self, events):
        jobs = []
        notification_platform = Notifier(self.platform_data)

        # Start the scheduler
        scheduler = BlockingScheduler()

        print('working')
        for event in events:
            job_date = event["start_date"] - timedelta(minutes=self.minutes_before_event)
            job = scheduler.add_job(notification_platform.notify, 'date', run_date=job_date, args=[event])
            jobs.append(job)
        scheduler.start()


def startBot(platform="discord", calType="file", calResource = None, minutes_before_event=5,
             discord_webhook_url=None, telegram_api_token = None, telegram_chat_id = None):
    """
    Start the bot

    :param platform: Current Option Discord
    :param calType: Local File or Online. file / network
    :param calResource: Link to the said file
    :param minutes_before_event: How many minutes before an event should the bot notify. Default 5
    :param discord_webhook_url: The Webhook where the bot should post
    :param telegram_api_token: The API Token for the bot
    :param telegram_chat_id: The Chat ID where the messages should be sent
    """

    # Lower Text for easily parsing data
    platform = platform.lower()
    calType = calType.lower()

    # Check if there's a resource we can parse
    if calResource is None:
        raise MissingResource("URL or File was empty!")

    if platform == "discord":
        if discord_webhook_url is None:
            raise MissingAuthData("A Webhook URL for Discord was not found! Exiting.")
        platform_data = {"platform": "discord", "webhook_url": discord_webhook_url}
    elif platform == "telegram":
        if telegram_api_token is None:
            raise MissingAuthData("A Token for Telegram was not found! Exiting.")
        if telegram_chat_id is None:
            raise MissingAuthData("A Chat ID for Telegram was not found! Exiting.")
        platform_data = {"platform": "telegram", "api_token": telegram_api_token, "chat_id": telegram_chat_id}


    if calType == 'file':
        logging.info('Opening Calendar file from File...')
        file_content = open(calResource, 'rb')
    elif calType == 'network':
        logging.info('Opening Calendar file from Network...')
        import requests
        try:
            cal = requests.get(calResource)
            if cal.status_code != 200:
                raise NetworkRequestFailed(f"Network request failed!")
            file_content = cal.text
        except:
            raise NetworkRequestFailed(f"Network request failed!")

    bot = SchedulerBot(platform_data, minutes_before_event)
    bot.parse_events(file_content)

if __name__ == '__main__':
    fire.Fire(startBot)