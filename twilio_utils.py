from twilio.rest import Client


class TwilioUtil(object):

            client = Client("AC0e087aa2bf931060cecc7b44522dd8b1",
                "5e77e5a337f870ca3c5c936f85ea833b")

            client.messages.create(to="+447901648812",
                from_="+447533025324",
                body="Here is your auto_gen passcode: 888990")

        twilio_util()

        def send_email():
            # Create a text/plain message
            gmail_user = 'alanwilliamswastaken@gmail.com'
            gmail_password = 'a@280989aW'

            sent_from = gmail_user
            to = ['theydonthaveit@gmail.com']
