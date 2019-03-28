import sys
import smtplib
import traceback
import datetime

import markdown

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .enums import Frequency
from .config import email_config
from .create_email import createEmail
from .addresses import addresses
from .rota import get_call 

def email(frequency, sample, test):
  # Get data from Google Sheet
  data = get_call(frequency, sample)
  if data == None:
    if frequency == Frequency.DAILY:
      print('no show')
      return
  
  # Transform data into markdown
  markdown_content = ''
  if data == None: # Must be weekly in this case
    markdown_content = 'No shows this week!'
  else:
    markdown_content = createEmail(frequency, data)
  html_content = markdown.markdown(markdown_content)

  # Format subject line
  subject = ' call - '
  if frequency == Frequency.DAILY:
    now = datetime.datetime.now().strftime('%B %d')
    subject = 'Daily' + subject + now
  else:
    now = datetime.datetime.now().strftime('%B %d')
    then = (datetime.datetime.now() + datetime.timedelta(weeks=1)).strftime('%B %d')
    subject = 'Weekly' + subject + now + '-' + then

  # If it's a test, just print it out. Don't send out email
  if test:
    print(markdown_content)
    return

  # Create email

  email = MIMEMultipart('alternative')
  email['From'] = email_config['from']
  email['To'] = addresses() if not sample else email_config['dev']
  email['Subject'] = subject

  email.attach(MIMEText(markdown_content, 'plain'))
  email.attach(MIMEText(html_content, 'html'))

  # Send email

  gmail_user = email_config['from']
  gmail_password = email_config['password']

  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    server_ssl.ehlo()
    server_ssl.login(gmail_user, gmail_password)
    server_ssl.sendmail(email['From'],
                        email['To'],
                        email.as_string())
    server_ssl.close()
    print('Email sent!')
    print(email['To'])
  except Exception as err:
    print('Something went wrong...')
    print(err)
    traceback.print_exc()
