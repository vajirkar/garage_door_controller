# Import smtplib for the actual sending function
import smtplib
import gdc_settings as config

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email_notification(subject, textmsg):
	msg = MIMEText(textmsg)
	msg['Subject'] = subject
	msg['From'] = config.email_from
	msg['To'] = config.email_to[0]
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.login(config.gmail_user, config.gmail_pass)
	s.sendmail(config.email_from, config.email_to, msg.as_string())
	s.close()
