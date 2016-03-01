import websocket
import json
import config
import logger

class PostSubscriptionRules:
    def __init__(self, contains, subreddits, author, domain, url, nsfw):
        self.contains = contains
        self.subreddits = subreddits
        self.author = author
        self.domain = domain
        self.url = url
        self.nsfw = nsfw

class PostWatcher:
    def __init__(self, subscriber):
        self.socket = websocket.WebSocketApp(config.rockets_connection,
                on_message = self.on_message,
                on_error = self.on_error,
                on_close = self.on_close,
                on_open = self.on_open)
        self.subscriber = subscriber

    def start(self):
        self.socket.run_forever()

    def on_open(self, ws):
        ps_rules = PostSubscriptionRules("contsins k", ['pics'], None, None, None, False)
        print(json.dumps(ps.__dict__))
        ws.send('{"channel":"posts", "include": { "subreddit":["todayilearned"] } }')

    def on_close(self, ws):
        logger.info('close') 

    def on_error(self, ws, error):
        logger.error('error ' + str(error))

    def on_message(self, ws, message):
        logger.info('message ' + str(message))
