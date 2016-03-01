"""
The ProcessorRecipient's use is to perform some processing function
on the message so that the output is different than the input as
opposed to merely performing some side effect and handing the message
down the chain
"""
class ProcessorRecipient:
    def __init__(self, next_recipient, process_func):
        self.next_recipient = next_recipient
        self.process_func = process_func

    def notify(self, message):
        return process_func(message)
