import smtplib
from config import CONFIG

sent_from = CONFIG['from']
to = CONFIG['to']
subject = 'test'
body = 'Sent an email from Python'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

gmail_user = CONFIG['from']
gmail_password = CONFIG['password']

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
