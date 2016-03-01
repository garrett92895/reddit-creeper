"""
The SwitchRecipient can be though of as a switch in the railroad sense.
Its purpose is to direct traffic to specific recipients based off of
filter functions
"""
class SwitchRecipient:
    def __init__(self, switchers):
        self.switchers = switchers

    def notify(self, message):
        for switcher in switchers:
            pass_on = switcher.filter_func(message)
            if pass_on:
                for recipient in switcher.recipients:
                    recipient.notify(message)

class Switcher:
    def __init__(self, filter_func, recipients):
        self.filter_func = filter_func
        self.recipients = recipients
