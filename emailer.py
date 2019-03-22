import sys
import argparse
import smtplib

from enums import Frequency
from config import email_config
from create_email import createEmail

from sample_data import sample_data

# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument("frequency", help="'daily' or 'weekly'", type=str)
args = parser.parse_args()
if args.frequency != 'daily' and args.frequency != 'weekly':
  sys.exit('format: python emailer.py <daily/weekly>')

frequency = None
if args.frequency == 'daily':
  frequency = Frequency.DAILY
else:
  frequency = Frequency.WEEKLY

# Get data from Google Sheet

data = sample_data

# Transform data into markdown

raw_markdown = createEmail(frequency, data)

# Transform markdown into rich text and plaintext



'''
# Create email

sent_from = email_config['from']
to = email_config['to']
subject = 'test'
body = 'Sent an email from Python' + args.frequency

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

# Send email

gmail_user = email_config['from']
gmail_password = email_config['password']

try:
  server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
  server_ssl.ehlo()
  server_ssl.login(gmail_user, gmail_password)
  server_ssl.sendmail(sent_from, to, email_text)
  server_ssl.close()
  print('Email sent!')
except Exception as e:
  print('Something went wrong...')
  print(e)
'''
