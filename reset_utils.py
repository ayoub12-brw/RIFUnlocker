import secrets
from notify import send_order_status_email as send_email

def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_reset_email(user_email, username, token):
    reset_link = f"http://localhost:5000/reset-password/confirm?token={token}"
    subject = "استعادة كلمة المرور - RIF Unlocker"
    body = f"مرحباً {username},\n\nلاستعادة كلمة المرور يرجى الضغط على الرابط التالي:\n{reset_link}\n\nإذا لم تطلب ذلك تجاهل الرسالة."
    send_email(user_email, username, subject, body)

if __name__ == '__main__':
    print(generate_reset_token())
