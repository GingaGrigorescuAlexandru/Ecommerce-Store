from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(session):
    customer_email = session.get('customer_email')  # Adjust based on your session data
    subject = 'Payment Confirmation'
    message = 'Thank you for your payment! Your transaction was successful.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer_email])