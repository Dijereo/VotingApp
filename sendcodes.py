import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'v-elect@outlook.com'
PASSWORD = 'votingapp1'
with open('email_content.txt') as fp:
    EMAIL_CONTENT = fp.read()

def sendEmail(users_data, election_id):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    for email, passcode in users_data:
        msg = MIMEMultipart()
        print('msg', msg)
        message = EMAIL_CONTENT.format(passcode, election_id)
        print('mess', message)
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Election Notification'
        print('data', msg)
        msg.attach(MIMEText(message, 'plain'))
        print('att', msg)
        s.send_message(msg)
        print('Sent')
        del msg
    s.quit()
