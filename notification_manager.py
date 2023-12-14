from twilio.rest import Client
from smtplib import SMTP
import os

# Get your own details from twilio
SID = os.environ.get("SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
VIRTUAL_NUMBER = os.environ.get("VIRTUAL_NUMBER")

# use your own gmail and app password
MY_GMAIL = os.environ.get("MY_GMAIL")
password_gmail = os.environ.get("password_gmail")


class NotificationManager:

    def __init__(self):
        self.client = Client(SID, AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(body=message, from_=VIRTUAL_NUMBER, to="+918617747631", )
        print(message.status)

    def send_email(self, name, mail, message):
        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_GMAIL, password=password_gmail)
            connection.sendmail(from_addr=MY_GMAIL, to_addrs=f"{mail}",
                                msg=f"Subject: Hey {name}! Got a Lowest Flight Deal for you!\n\n{message}".encode('utf-8'))
            print("sent\n")
