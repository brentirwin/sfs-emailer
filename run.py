import sys
import argparse
import smtplib
import traceback
import datetime

from src import *
from src.enums import Frequency
from src.emailer import email

print(datetime.datetime.now().strftime('%B %d %H:%M'))

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--weekly',
                    help='Sends weekly call, daily is default',
                    action='store_true')
parser.add_argument('-e', '--emailerrors',
                    help='email errors to emergency contact',
                    action='store_true')
parser.add_argument('-s', '--sample',
                    help='use sample data',
                    action='store_true')
parser.add_argument('-t', '--test',
                    help='test, do not send out emails',
                    action='store_true')

args = parser.parse_args()

# Define frequency
freq = None
if args.weekly:
  freq = Frequency.WEEKLY
else:
  freq = Frequency.DAILY

# If you want errors sent to email
if args.emailerrors:
  try:
    email(freq, args.sample, args.test)
  except Exception as err:
    gmail_user = email_config['from']
    gmail_password = email_config['password']

    sent_from = gmail_user
    to = email_config['dev']
    subject = 'SFS Emailer Failure'
    body = err + '\n\n' + traceback.format_exc()

    email_text = '''\
    From: %s
    To: %s
    Subject: %s

    %s
    ''' % (sent_from, ', '.join(to), subject, body)

    try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      server.sendmail(sent_from, to, email_test)
      server.close()
    except Exception as err:
      print('Couldn\'t even email you the error...')
else:
  email(freq, args.sample, args.test)
