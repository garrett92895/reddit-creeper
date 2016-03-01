import websocket
from websocket._exceptions import WebSocketConnectionClosedException
import json
from json import JSONEncoder
import functools
import config
import logger

def reduce(ruleset):
    if ruleset:
        return functools.reduce(reduce_rules, ruleset)
    else:
        return PostSubscriptionRule()

def reduce_rules(rule1, rule2):
    contains = rule1.contains + rule2.contains
    subreddits = rule1.subreddit + rule2.subreddit
    authors = rule1.author + rule2.author
    domains = rule1.domain + rule2.domain
    urls = rule1.url + rule2.url
    nsfw = rule1.nsfw or rule2.nsfw 

    return PostSubscriptionRule(contains, subreddits, authors, domains, urls, nsfw)

class PostSubscriptionRule:
    def __init__(self, contains = [], 
            subreddits = [], authors = [], 
            domains = [], urls = [], nsfw=None):
        self.contains = contains
        self.subreddit = subreddits
        self.author = authors
        self.domain = domains
        self.url = urls
        self.nsfw = nsfw

    def to_json_dict(self):
        encode = {}
        if self.contains:
            encode['contains'] = self.contains
        if self.subreddit:
            encode['subreddit'] = self.subreddit
        if self.author:
            encode['author'] = self.author
        if self.domain:
            encode['domain'] = self.domain
        if self.url:
            encode['url'] = self.url
        if self.nsfw:
            encode['nsfw'] = str(self.nsfw)

        return encode

class PostWatcher:
    def __init__(self, recipient):
        self.socket = websocket.WebSocketApp(config.rockets_connection,
                on_message = self.on_message,
                on_error = self.on_error,
                on_close = self.on_close,
                on_open = self.on_open)
        self.recipient = subscriber
        self.include_rules = []
        self.exclude_rules = []

    def start(self):
        self.socket.run_forever()

    def add_include_rule(self, rule):
        self.include_rules.append(rule)
        try:
            self.subscribe()
        except WebSocketConnectionClosedException:
            err_msg = 'Tried to send subscription to websocket after adding' \
                      ' include rule\n' + json.dumps(rule.to_json_dict(), indent=2) + '' \
                      '\nbut the websocket is not open'
            logger.error(err_msg)

    def add_exclude_rule(self, rule):
        self.exclude_rules.append(rule)
        try:
            self.subscribe()
        except WebSocketConnectionClosedException:
            err_msg = 'Tried to send subscription to websocket after adding' \
                      ' exclude rule\n' + json.dumps(rule.to_json_dict(), indent=2) + '' \
                      '\nbut the websocket is not open'
            logger.error(err_msg)

    def subscribe(self):
        subscription_payload = {
            'channel': 'posts',
            'include': reduce(self.include_rules).to_json_dict(),
            'exclude': reduce(self.exclude_rules).to_json_dict()
        }
        self.socket.send(json.dumps(subscription_payload))

    def on_open(self, ws):
        logger.info('Connection opened')
        self.subscribe()

    def on_close(self, ws):
        logger.info('Connection closed') 

    def on_error(self, ws, error):
        logger.error(str(error))

    def on_message(self, ws, message):
        logger.info('Received message...\n' + str(message))
        reddit_post = json.loads(message)
        self.recipient.notify(reddit_post)
