import logging

from django.core import mail

from .tasks import task_email_user

logger = logging.getLogger(__name__)


def send_email(user, template, context, attachments=None, delete_attachments_after_send=False,
               language_code=None):
    '''
    Send email to user

    :param user: User instance or recipient email addres
    :param template: Template to use for email
    :param context: Context for email
    :param attachments: List of attachments
    :param delete_attachments_after_send: If true, delete attachments from storage after sending
    :param language_code: Language code for template
    :return:
    '''

    ### check if we are using test framework
    if hasattr(mail, 'outbox'):
        ### if yes, do not defer sending email
        send_email_f = task_email_user
    else:
        ### otherwise, defer sending email to celery
        send_email_f = task_email_user.delay

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
        language_code=language_code
    )
