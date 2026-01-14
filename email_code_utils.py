import random
import string
from notify import send_order_status_email as send_email

def generate_email_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_verification_code(user_email, username, code):
    subject = "كود التحقق من البريد الإلكتروني - RIF Unlocker"
    body = f"مرحباً {username},\n\nكود التحقق الخاص بك هو: {code}\n\nيرجى إدخاله في الموقع لإتمام العملية."
    send_email(user_email, username, subject, body)

if __name__ == '__main__':
    print(generate_email_code())
