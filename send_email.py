# Import smtplib for the actual sending function
import smtplib
import gdc_settings as config

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# Create a text/plain message
msg = MIMEText("The Garage Door has been open since ."  )

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = "Garage Door Open Notification!"
msg['From'] = config.email_from
msg['To'] = config.email_to[0]

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.login(config.gmail_user, config.gmail_pass)
s.sendmail(config.email_from, config.email_to, msg.as_string())
s.close()
