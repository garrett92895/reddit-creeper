import praw
from smtplib import SMTP
import logger
from chainnode import ChainNode
"""
If it wasn't already self evident, this class filters messages

based off of functions given to it and uses the results from
those filters to determine whether or not to pass a message down
the chain. Many hopes and dreams die here.
"""
from threading import RLock

class FilterRecipient(ChainNode):
    def __init__(self, filter_funcs, next_recipient):
        self.next_recipient = next_recipient
        self.filter_funcs = []
        self.filter_funcs.extend(filter_funcs)
        self.lock = RLock()

    def notify(self, message):
        with self.lock:
            pass_on = len(self.filter_funcs > 0)
            for filter_func in self.filter_funcs:
                pass_on and filter_func(message)
    
            if pass_on:
                self.next_recipient.notify(message)

    def add_filter(self, filter_func):
        with self.lock:
            self.filter_funcs.append(filter_func)

    def remove_filter(self, index):
        with self.lock:
            self.filter_funcs.remove(index)


"""
This class is tightly coupled to the watcher, but oh well.
This Recipient grabs the latest post from reddit in order to get
more information that isn't provided by the watcher. It does not
require an OAuth2 authenticated connection
"""
class PostRecipient(ChainNode):
    def __init__(self, next_recipient, user_agent):
        self.next_recipient = next_recipient
        self.reddit = praw.Reddit(user_agent=user_agent)
    
    def notify(self, post_dict):
        logger.debug('Post Recipient notified of post in sub ' + str(post_dict['data']['subreddit']))
        subreddit = self.reddit.get_subreddit(post_dict['data']['subreddit'])

        newest_post = None
        for post in subreddit.get_new(limit=1):
            newest_post = post

        self.next_recipient.notify(newest_post)


"""
The ProcessorRecipient's use is to perform some processing function
on the message so that the output is different than the input as
opposed to merely performing some side effect and handing the message
down the chain
"""
class ProcessorRecipient(ChainNode):
    def __init__(self, next_recipient, process_func):
        self.next_recipient = next_recipient
        self.process_func = process_func

    def notify(self, message):
        logger.debug('Processor Recipient received message')
        self.next_recipient.notify(self.process_func(message))


"""
The SwitchRecipient can be though of as a switch in the railroad sense.
Its purpose is to direct traffic to specific recipients based off of
filter functions

It does not subclass ChainNode because it does not have a direct
next_recipient but rather a list of Switchers which have a list
of recipients that they decide whether or not to pass on the message to
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


"""
This is an EndRecipient, this recipient won't pass the message down the chain
(perhaps that is a poor design decision). This Recipient merely sends an email
and will typically have a processor attached before it to prepare the message
into an emailable format.

Because this Recipient will not pass along the message, it does not subclass
ChainNode

There is a lot of room for more features here, but considering I'm only using
this for sending text messages to myself, this will suffice
"""
class EmailerEndRecipient:
    def __init__(self, host, from_email, to_email_list):
        self.from_email = from_email
        self.to_email_list = to_email_list
        self.host = host

    def notify(self, message):
        logger.debug('Email Recipient sending ' + message + ' to ' + str(self.to_email_list))
        with SMTP(self.host) as smtp:
            for to_email in self.to_email_list:
                smtp.sendmail(self.from_email, to_email, message)
