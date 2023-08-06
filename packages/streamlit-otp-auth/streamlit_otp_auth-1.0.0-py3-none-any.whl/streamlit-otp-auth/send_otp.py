from dependencies import *

def send_otp_to_email(email, OTP):
    em = EmailMessage()
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    receiver_email = email
    em["From"] = sender_email
    em["To"] = receiver_email
    em["Subject"] = "OTP Verification"
    em.set_content(MIMEText(f"Your OTP is {OTP}"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())