def replace_values(message_raw, event_data):
    return message_raw.replace('[EVENT TITLE]', event_data['subject']) \
        .replace('[DESCRIPTION]', event_data['description']) \
        .replace('[LOCATION]', event_data['location'])
