import sys
import smtplib
import traceback

import markdown

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .enums import Frequency
from .config import email_config
from .create_email import createEmail
from .addresses import addresses
from .rota import get_call 

from .sample_data import sample_data

def email(frequency):
  # Get data from Google Sheet
  data = get_call(frequency)
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
  subject = ' call'
  if frequency == Frequency.DAILY:
    subject = 'Daily' + subject
  else:
    subject = 'Weekly' + subject

  print(markdown_content)

'''
  email = MIMEMultipart('alternative')
  email['From'] = email_config['from']
  email['To'] = addresses()
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
'''
