from django.core.mail import send_mail

"""This function is used to send an email through
the local smtp server. All parameters can be filled
using plain text.
e.g. sender = "me@example.com"
receiver = "you@example.com"
subject = "example email message"
text = "this is an example"
"""

def sendEmail(sender, receiver, subject, msg):
	
	send_email (subject, msg, sender, receiver)
	

