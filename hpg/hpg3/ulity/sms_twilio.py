# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.environ.get( 'account_sid' )
auth_token = os.environ.get( 'auth_token' )
print('twillo account_id:{},auth_token:{}'.format(account_sid,auth_token))
client = Client(account_sid, auth_token)

def msm(msg='test'):
    message = client.messages.create(
        from_=os.environ.get( 'from_' ),
        body=msg,
        to=os.environ.get( 'to' )

    )

    print(message.sid)

if __name__ == '__main__':
    msm()