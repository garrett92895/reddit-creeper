"""
This is an EndRecipient, this recipient won't pass the message down the chain
(perhaps that is a poor design decision). This Recipient merely sends an email
and will typically have a processor attached before it to prepare the message
into an emailable format.

There is a lot of room for more features here, but considering I'm only using
this for sending text messages to myself, this will suffice
"""
from smtplib import SMTP

class EmailerEndRecipient:
    def __init__(self, host, from_email, to_email_list):
        self.from_email = from_email
        self.to_email_list = to_email_list
        self.host = host

    def notify(self, message):
        with SMTP(self.host) as smtp:
            for to_email in self.to_email_list:
                smtp.sendmail(self.from_email, to_email, message)
