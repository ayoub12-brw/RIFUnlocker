import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import sqlite3

def send_order_status_email(user_email, username, subject, body):
    sender_email = 'noreply@yourdomain.com'
    sender_name = 'RIF Unlocker'
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = user_email
    msg['Subject'] = subject
    try:
        with smtplib.SMTP('smtp.yourdomain.com', 587) as server:
            server.starttls()
            server.login('your_smtp_user', 'your_smtp_password')
            server.sendmail(sender_email, [user_email], msg.as_string())
        print('Email sent!')
    except Exception as e:
        print('Email error:', e)

if __name__ == '__main__':
    # مثال تجريبي
    send_order_status_email('test@example.com', 'username', 123, 'تم')
