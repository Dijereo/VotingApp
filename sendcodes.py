import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'dion.recai@my.uwi.edu'
PASSWORD = '19991215'
with open('email_content.txt') as fp:
    EMAIL_CONTENT = fp.read()

def sendEmail(users_data):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    for email, passcode in users_data:
        msg = MIMEMultipart()
        message = EMAIL_CONTENT.format(passcode)
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Election Notification'
        
        msg.attach(MIMEText(message, 'plain'))
        
        s.send_message(msg)
        del msg
    
    s.quit()
