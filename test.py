import watcher

subscriber = None
pwatcher = watcher.PostWatcher(subscriber)
rule1 = watcher.PostSubscriptionRule(subreddits=["funny"])
rule2 = watcher.PostSubscriptionRule(subreddits=["pics"])
pwatcher.add_include_rule(rule1)
pwatcher.add_include_rule(rule2)
pwatcher.start()
