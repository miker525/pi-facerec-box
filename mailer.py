"""Raspberry Pi Face Recognition Treasure Box
Email Script
Script & implementation by Michael Rosenberg
Project by Tony DiCola
"""

import smtplib
import datetime
import config
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

# Set now to whatever time it currently is
now = datetime.datetime.now()

def email(filename):
	# Define the email subject
	SUBJECT = "Unknown intruder on " + str(now.day)+"-"+str(now.month)+"-"+str(now.year)
	# Create a variable based on the configuration recipient
	RECIPIENT_EMAIL = config.RECIPIENT_EMAIL
	# If the recipient field is blank in the config the email should go to the sender
	if (RECIPIENT_EMAIL == ''):
		RECIPIENT_EMAIL = config.SENDER_EMAIL
	# Create the email
	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT 
	msg['From'] = config.SENDER_EMAIL
	msg['To'] = RECIPIENT_EMAIL
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filename, "rb").read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')
	msg.attach(part)
	# Connect to the email server
	server = smtplib.SMTP(config.SMTP_SERVER)
	server.ehlo()
	server.starttls()
	# Log into the sender email address and send the email
	try:
		server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
		server.sendmail(config.SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
		print "Email Sent!"
	except Exception:
		print('Login Failed!')
		print(traceback.format_exc())
	# Close server connection
	server.quit
