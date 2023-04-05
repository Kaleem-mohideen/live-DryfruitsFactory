from django.conf import settings
import smtplib

def send_mail(subject, email_body, from_addr, to_addr_list):
    SMTP_SESSION = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIT_PORT)
    SMTP_SESSION.ehlo()
    SMTP_SESSION.starttls()
    SMTP_SESSION.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    headers = "\r\n".join(["from: " + 'Dry Fruits Factory', "subject: " + subject, "mime-version: 1.0", "content-type: text/html"])
    content = headers + "\r\n\r\n" + email_body
    SMTP_SESSION.sendmail(from_addr, to_addr_list, content)
