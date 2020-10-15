def replace_values(message_raw):
    return message_raw.replace('[EVENT TITLE]', self.event_data['subject']) \
        .replace('[DESCRIPTION]', self.event_data['description']) \
        .replace('[LOCATION]', self.event_data['location'])
