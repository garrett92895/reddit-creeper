"""
This class is tightly coupled to the watcher, but oh well.
This Recipient grabs the latest post from reddit in order to get
more information that isn't provided by the watcher. It does not
require an OAuth2 authenticated connection
"""
import praw

class PostRecipient:
    def __init__(self, next_recipient, user_agent):
        self.next_recipient
        self.reddit = praw.Reddit(user_agent=user_agent)
    
    def notify(self, post_dict):
        subreddit = self.reddit.get_subreddit(post_dict[])

        newest_post = None
        for post in subreddit.get_new(limit=1):
            newest_post = post

        self.next_receipient.notify(newest_post)
