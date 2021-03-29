from datetime import datetime
import ssl, smtplib
from email.mime.text import MIMEText
import base64
import reverb_price_finder.db_mod as db


def email_info_db():
    info = []
    data = db.Data_Base('data')
    email_s = data.query_all('email_s')
    email_r = data.query_all('email_r')
    data.close()
    for i in email_s[0]:
        info.append(i)
    info.append(email_r[0][0])
    return info

def construct_txt_message(q):
    plural = ''
    message_text = ''
    if len(q[0]) > 1:
        plural = 's'

    for i in range(len(q[0])):
        message_text += 'Product: {:71}| Price: {:15} \nCondition: {} \nCheck it out at this link: {} \n \n'.format(q[0][i][:70], q[1][i], q[3][i], q[2][i])

    return message_text

def construct_message_email(q):
    plural = ''
    message_text = ''
    if len(q[0]) > 1:
        plural = 's'

    for i in range(len(q[0])):
        message_text += 'Product: {:71}| Price: {:15} \nCondition: {} \nCheck it out at this link: {} \n \n'.format(q[0][i][:70], q[1][i], q[3][i], q[2][i])

        message = MIMEText(message_text)
    email_info = email_info_db()
    message['to'] = email_info[2]
    message['from'] = email_info[0]
    message['subject'] = 'New Reverb Item{} Within Budget \n \n'.format(plural)
    return message.as_string()

def notify_action(q):
    #1 = send | 2 = dont send
    data = db.Data_Base('data')
    email_setting = data.query_all('email_toggle')
    data.close()
    if email_setting[0][0] == '1':
        send_email(q)
    write_to_file(q)

def send_email(q):
    port = 587 #for ssl
    email_info = email_info_db()
    email_s = email_info[0]
    send_pass = email_info[1]
    email_r = email_info[2]

    #run construct message and assign 
    message = construct_message_email(q)

    #login and send email
    server = smtplib.SMTP('smtp.gmail.com', port)
    server.ehlo()
    server.starttls()
    server.login(email_s, send_pass)
    server.sendmail(email_s, email_r, message)
    server.quit()

def write_to_file(q):
    message = construct_txt_message(q)
    time_log = datetime.now()
    message = ('Date and Time of Results: {} \n \n{} \n'.format(time_log, message))
    file1 = open('results_log.txt', 'a')
    file1.write(message) 
    file1.close() 





def main():
    #this is only for testing
    q = [['d','f'],['d','f'],['d','f'],['d','f']]
    notify_action(q)

if __name__ == '__main__':
    main()