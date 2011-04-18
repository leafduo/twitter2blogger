#!/usr/bin/env python2.6
#encoding=utf-8

import datetime
from oauth import oauth
from oauthtwitter import OAuthApi
import smtplib
import email
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import smtplib
import mimetypes

from config import *

twitter = OAuthApi(consumer_key, consumer_secret)

# Get the temporary credentials for our next few calls
temp_credentials = twitter.getRequestToken()

# User pastes this into their browser to bring back a pin number
print(twitter.getAuthorizationURL(temp_credentials))

# Do a test API call using our new credentials
twitter = OAuthApi(consumer_key, consumer_secret, access_token['oauth_token'], access_token['oauth_token_secret'])
user_timeline = twitter.GetUserTimeline({"trim_user": True, "since_id": since_id, "count": 200})

tweets_list = []

since_id = user_timeline[0]['id']
print since_id

for tweet in user_timeline:
    tweets_list.append(tweet['created_at'])
    tweets_list.append('\n')
    tweets_list.append(tweet['text'])
    tweets_list.append('\n\n')

content = u''.join(tweets_list)

smtp = smtplib.SMTP("localhost")

m = MIMEMultipart()
m["To"] = receiver
m["From"] = sender
m["Subject"] = u'Twitter for ' + datetime.date.today().isoformat()
m.attach(MIMEText(content, 'plain', 'utf-8'))

smtp.sendmail(sender, receiver, m.as_string())
smtp.quit()
