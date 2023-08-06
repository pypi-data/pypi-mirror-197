from . import *;
from lib import fn;
import smtplib;
from email.mime.text import MIMEText;
from email.utils import formatdate;
from email.utils import parseaddr;
import re;

host_email = fn.config['MAIL_EMAIL'];
def send(subject, msg, target=None):
	if target == None:
		target = fn.config['DEBUG_NOTIFY_EMAIL'].strip().split(';');
	try:
		username = fn.config['MAIL_USERNAME'];
		host = fn.config['MAIL_SERVER'];
		host_port = int(fn.config['MAIL_PORT']);
		host_password = fn.config['MAIL_PASSWORD'];
		server = smtplib.SMTP(host, host_port);
		#server.set_debuglevel(1);
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, host_password);
		valid_target = isValid(target);
		if valid_target:
			email = generateEmail(valid_target, subject, msg);
			server.sendmail(host_email, valid_target, email);

		server.quit();
	except Exception as ex:
		Logger.e(ex);
		#send(None, 'Something wrong for email', fn.dumps(msg));
		return False;
	#print('msg sent.');
	return True;

def generateEmail(target=[], subject='', msg=''):
	to_emails = ",".join(target);
	args = {
		'From':host_email,
		'To': to_emails,
		'Subject':subject,
		'Date':formatdate(localtime=True),
	};
	message =  MIMEText(str(msg).replace('\n','<br/>'),'html');
	for key in args.keys():
		value = args[key];
		message[key] = value;

	return message.as_string();

def generateMessage(msg):
	return msg;

def isValid(email):
	if not email:
		return False;
		
	if ',' in email: # split multiple emails into list
		email = email.split(',');

	if type(email) == str: #force email become list
		email = [email];

	pattern = re.compile(r"^[\w\.\+\-]+\@[\w.-]+\.[a-z]{2,3}$");
	valid_email = [];
	for e in email:
		if not re.match(pattern, e.strip()):
			return False;
		valid_email.append(e.strip());
	return valid_email;

#send(['daniel@webqlo.com'], 'Testing', 'This is a system generated email');