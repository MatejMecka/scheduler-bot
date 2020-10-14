class NetworkRequestFailed(Exception):
    """
    Executed when the network request fails
    """
    pass

class MissingResource(Exception):
    """
    Executed when the Resource was empty
    """
    pass

class InvalidOption(Exception):
    """
    Executed when the user provides an invalid option
    """
    pass

class MissingAuthData(Exception):
    """
    Executed when the user doesn't provide a webhook url for discord or API token for Telegram
    """
    pass