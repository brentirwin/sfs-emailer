import sys
import argparse
import smtplib
import traceback

from src import *
from src.enums import Frequency
from src.emailer import email

parser = argparse.ArgumentParser()
parser.add_argument("frequency", help="'daily' or 'weekly'", type=str)
parser.add_argument('-e', '--emailerrors', help='email errors to emergency contact', action='store_true')
args = parser.parse_args()
if args.frequency != 'daily' and args.frequency != 'weekly':
  sys.exit('format: python emailer.py <daily/weekly>')

freq = None
if args.frequency == 'daily':
  freq = Frequency.DAILY
else:
  freq = Frequency.WEEKLY

if args.emailerrors:
  try:
    email(freq)
  except Exception as err:
    gmail_user = email_config['from']
    gmail_password = email_config['password']

    sent_from = gmail_user
    to = email_config['emergency']
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
  email(freq)
