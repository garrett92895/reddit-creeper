from threading import RLock

class FilterRecipient:
    def __init__(self, next_recipient, filter_funcs):
        self.next_recipient = next_recipient
        self.filter_funcs = []
        self.filter_funcs.extend(filter_funcs)
        self.lock = RLock()

    def notify(self, message):
        with self.lock:
            pass_on = len(self.filter_funcs > 0)
            for filter_func in self.filter_funcs:
                pass_on && filter_func(message)
    
            if pass_on:
                self.next_recipient.notify(message)

    def add_filter(self, filter_func):
        with self.lock:
            self.filter_funcs.append(filter_func)

    def remove_filter(self, index):
        with self.lock:
            self.filter_funcs.remove(index)
