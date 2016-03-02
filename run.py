#!/usr/bin/python3
import watcher
import config
from recipients import PostRecipient, ProcessorRecipient, EmailerEndRecipient, FilterRecipient

def processor_func(message):
    return {
        'subject': '/r/' + str(message.subreddit),
        'body': message.title + ': ' + message.permalink
    }

def filter_func(post):
    return post.link_flair_text.lower() == 'selling'

texter_end_recipient = EmailerEndRecipient(config.to_email_list)
reddit_post_processor = ProcessorRecipient(texter_end_recipient, processor_func)
selling_flair_filter = FilterRecipient([filter_func], reddit_post_processor)
post_recipient = PostRecipient(reddit_post_processor, config.user_agent)

contains = ['(770)|(960)|(380)|([Gg]raphics)|([Gg][Pp][Uu])']
pwatcher = watcher.PostWatcher(post_recipient)
rule1 = watcher.PostSubscriptionRule(contains=contains, subreddits=["hardwareswap"])
rule2 = watcher.PostSubscriptionRule(contains=contains, subreddits=["buildapcsales"])
pwatcher.add_include_rule(rule1)
pwatcher.add_include_rule(rule2)
pwatcher.start()
