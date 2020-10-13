import fire
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
from icalendar import Calendar, Event
from platforms.notifier import Notifier
from datetime import datetime, timedelta

import logging

class SchedulerBot():
    def __init__(self, platform, minutes_before_event):
        self.platform = platform
        self.minutes_before_event = minutes_before_event

    def parse_events(self, cal_resource):
        """
        :param ical_resource:
        :return:
        """
        events = []
        calendar = Calendar.from_ical(cal_resource)
        for event in calendar.walk():
            if event.name == "VEVENT":
                event_data = {
                    "subject": event["summary"].to_ical().decode('utf-8'),
                    "description": event["description"].to_ical().decode('utf-8'),
                    "start_date": event["dtstart"].dt,
                    "location": event["location"].to_ical().decode('utf-8')
                }
                #print(event_data)
                events.append(event_data)
        self.schedule_events(events)


    def schedule_events(self, events):
        jobs = []
        notification_platform = Notifier(self.platform)

        # Start the scheduler
        scheduler = BlockingScheduler()

        print('working')
        for event in events:
            job_date = event["start_date"] - timedelta(minutes=self.minutes_before_event)
            job = scheduler.add_job(notification_platform.notify, 'date', run_date=job_date, args=[event])
            jobs.append(job)
        scheduler.start()


def startBot(platform="discord", calType="file", calResource=None, minutes_before_event=5):
    """
    Start the bot

    :param platform: Current Option Discord
    :param calType: Local File or Online. file / network
    :param calResource: Link to the said file
    :param minutes_before_event: How many minutes before an event should the bot notify. Default 5

    """

    # Lower Text for easily parsing data
    platform = platform.lower()
    calType = calType.lower()

    # Check if there's a resource we can parse
    if calResource is None:
        raise MissingResource("URL or File was empty!")



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

    bot = SchedulerBot(platform, minutes_before_event)
    bot.parse_events(file_content)

if __name__ == '__main__':
    fire.Fire(startBot)