#!/usr/bin/python3
import pprint
import watcher

class ConsoleRecipient:
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=1)

    def notify(self, message):
        print('\n\n\n')
        self.pp.pprint(message)

subscriber = ConsoleRecipient()
pwatcher = watcher.PostWatcher(subscriber)
rule1 = watcher.PostSubscriptionRule(subreddits=["hardwareswap"])
rule2 = watcher.PostSubscriptionRule(subreddits=["buildapcsales"])
pwatcher.add_include_rule(rule1)
pwatcher.add_include_rule(rule2)
pwatcher.start()
