import secrets
from urllib.parse import urlencode
from notify import send_order_status_email as send_email
import sqlite3

def generate_activation_token():
    return secrets.token_urlsafe(32)

def send_activation_email(user_email, username, token):
    activation_link = f"http://localhost:5000/activate?token={token}"
    subject = "تفعيل حسابك في RIF Unlocker"
    body = f"مرحباً {username},\n\nيرجى تفعيل حسابك عبر الرابط التالي:\n{activation_link}\n\nمع تحيات فريق الدعم."
    send_email(user_email, username, 'تفعيل الحساب', body)

if __name__ == '__main__':
    print(generate_activation_token())
