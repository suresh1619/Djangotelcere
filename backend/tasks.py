from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_welcome_email(user_email):
    subject = 'Registraion is successful!'
    message = (
        "Hello there! 👋\n\n"
        "Thanks for registering with us. 🚀\n"
        "We're excited to have you onboard! 🤝\n"
        "Stay tuned for updates and awesome features. 🌟\n"
        "Cheers, Team Clopileta 💌"
    )
    from_email = 'clopileta8@gmail.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

