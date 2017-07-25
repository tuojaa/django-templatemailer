import logging

from django.core import mail
from django.conf import settings
from .tasks import task_email_user

logger = logging.getLogger(__name__)


def send_email(user,
               template,
               context,
               attachments=None,
               delete_attachments_after_send=False,
               language_code=None,
               email_from=None):
    '''
    Send email to user

    :param user: User instance or recipient email addres
    :param template: Template to use for email
    :param context: Context for email
    :param attachments: List of attachments
    :param delete_attachments_after_send: If true, delete attachments from storage after sending
    :param language_code: Language code for template
    :param email_from: Optional override for email FROM field
    :return:
    '''

    send_email_f = task_email_user

    if settings.TEMPLATEMAILER_ASYNC == "CELERY":
        send_email_f = task_email_user.delay
    elif settings.TEMPLATEMAILER_ASYNC == "ZAPPA":
        send_email_f = task_email_user

    try:
        user_email = user.email
    except AttributeError:
        user_email = user

    ### send email
    send_email_f(
        user_email,
        template,
        context,
        attachments=attachments,
        delete_attachments_after_send=delete_attachments_after_send,
        language_code=language_code,
        email_from=email_from
    )
