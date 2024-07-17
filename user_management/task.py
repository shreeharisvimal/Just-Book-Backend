# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from django.conf import settings



@shared_task(bind=True)
def send_otp_to_email(self, email, otp):
    subject = 'Your OTP Code for JustBook'
    html_message = render_to_string('OTP_email.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, plain_message, from_email, [email], html_message=html_message)
        return 'Done'
    except Exception as e:
        return str(e)



@shared_task(bind=True)
def send_otp_to_phone(self, phone, otp):
    url = f"https://2factor.in/API/V1/{settings.TWO_FACTOR_AUTH_API_KEY}/SMS/{phone}/{otp}/Just Book Sender"
    response = requests.get(url)
    return "Done"