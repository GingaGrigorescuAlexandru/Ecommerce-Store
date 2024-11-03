from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_confirmation_email(customer_email,
                            cart_items_with_totals,
                            total_price,
                            client_instance,
                            billing_address_info,
                            shipping_address_info):

    subject = 'Payment Confirmation'

    context = {
        'cart_items_with_totals': cart_items_with_totals,
        'total_price': total_price,
        'client': client_instance,
        'billing_address_info': billing_address_info,
        'shipping_address_info': shipping_address_info,
    }

    html_message = render_to_string('app/email_order_confirmation.html', context=context)
    message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer_email],
    )


    email.attach_alternative(html_message, "text/html")

    email.send()