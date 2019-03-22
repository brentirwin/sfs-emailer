import sys
import smtplib
import traceback

import markdown

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .enums import Frequency
from .config import email_config
from .create_email import createEmail

from .sample_data import sample_data

def email(frequency):

  # Get data from Google Sheet
  data = sample_data

  # Transform data into markdown
  markdown_content = createEmail(frequency, data)
  html_content = markdown.markdown(markdown_content)
  subject = ' call - ' + data[0]['date']
  if frequency == Frequency.DAILY:
    subject = 'Daily' + subject
  else:
    subject = 'Weekly' + subject

  print(email_config['to'])

  email = MIMEMultipart('alternative')
  email['From'] = email_config['from']
  email['To'] = ','.join(email_config['to'])
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
  except Exception as err:
    print('Something went wrong...')
    print(err)
    traceback.print_exc()

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
'''
 
