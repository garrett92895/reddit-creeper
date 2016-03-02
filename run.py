#!/usr/bin/python3
import watcher
import config
from recipients import PostRecipient, ProcessorRecipient, EmailerEndRecipient

texter_end_recipient = EmailerEndRecipient(config.smtp_host, config.from_email, config.to_email_list)
reddit_post_processor = ProcessorRecipient(texter_end_recipient, lambda x: x.title + '\n' + x.permalink)

post_recipient = PostRecipient(reddit_post_processor, config.user_agent)

pwatcher = watcher.PostWatcher(post_recipient)
rule1 = watcher.PostSubscriptionRule(subreddits=["funny"])
rule2 = watcher.PostSubscriptionRule(subreddits=["pics"])
pwatcher.add_include_rule(rule1)
pwatcher.add_include_rule(rule2)
pwatcher.start()
