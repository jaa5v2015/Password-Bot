from email.message import EmailMessage
import rpyc
import datetime as dt
import imaplib
from os import path
from datetime import timezone
import email
import time
import smtplib


AD_SERVER_IP = "10.170.139.191"
AD_BOT_PORT = 19961
domain_controller = "DC=net,DC=ads,DC=state,DC=tn,DC=us"
users_ou = 'OU=Users and Groups, OU=11975, OU=STATE, {}'.format(domain_controller)
groups_ou = 'OU=State, {}'.format(domain_controller)
conn = rpyc.connect(AD_SERVER_IP,AD_BOT_PORT)


### Connect to ut look to get user name and password
user = "helpdesktwrabot@gmail.com"
app_password = "Wildlife2022"
gmail_host = 'imap.gmail.com'

while(True):
    mail_con = imaplib.IMAP4_SSL(host = gmail_host)
    mail_con.login(user, app_password)
    mail_con.select("INBOX")

    tmp, data = mail_con.search(None, 'ALL')

    def send_commands(command):
        try:
            conn = rpyc.connect(AD_SERVER_IP,AD_BOT_PORT)
            conn.root.run_commands(command)
        except Exception as Err:
            print(str(Err))

    def change_password(username, new_password):
            dn = 'CN={},{}'.format(username, users_ou)
            cmd='dsmod user "{}" -pwd {}'.format(dn, new_password)
            send_commands(cmd)
            print(username, " Password changed too:", new_password)
    
    def emailPassword(username, password, user,new_password):
        email_text = "Changed password to: " + new_password
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(username, password)
            smtp_server.sendmail(username, user, email_text)
            smtp_server.close()
            print("Email Sent")
        except:
            print("Couldnt send email")
    for num in data[0].split():
        tmp, data = mail_con.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        fromMsg = str(msg["From"])
        r = fromMsg.replace('"', '')
        fromMsg = r.split("<")
        emailUser = fromMsg[1].replace(">", '')
        print(emailUser)
        username = fromMsg[0].strip(" ")
        for part in msg.walk():

            if part.get_content_type() == 'text/plain':

                l = part.get_payload()
                
                new_password = l.strip("\n")
                r =new_password.split()
                
                new_password=r[0]
            
                change_password(username, new_password)
                emailPassword(user, app_password, emailUser,new_password)
                break
        mail_con.store(num, '+FLAGS', '\\Deleted')
    mail_con.expunge()
    time.sleep(10)