import logging

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

from apps import app

logger = logging.getLogger('django')


@app.task
def send_email(subject, message, email_to):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=f'Apptimizm<{EMAIL_HOST_USER}>',
        bcc=[email_to],
    )

    try:
        email.send()
    except Exception as e:
        logger.error(f'Ошибка при отсылке письма {e}')
