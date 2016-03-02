"""
Base class for recipients. Useful for the attach method, if useful at all
"""
class ChainNode:
    def attach(self, next_recipient):
        self.next_recipient = next_recipient
