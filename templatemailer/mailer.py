import traceback
import logging

from django.core import mail
from django.core.mail import send_mail

from dashboard import settings
from .tasks import task_email_user
from .models import EmailTemplate
from django.template import Template, Context

logger = logging.getLogger(__name__)

def email_user(user, template, context, attachments = None, delete_attachments_after_send = False, send_to = None, language_code = None):
    '''
    Send email to user

    :param user: User instance or None if no DB user is used
    :param template: Template to use for email
    :param context: Context for email
    :param attachments: List of attachments
    :param delete_attachments_after_send: If true, delete attachments from storage after sending
    :param send_to: email address to send (or None, to use user email address)
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

    ### send email
    send_email_f(
        user.pk if user else None,
        template,
        context,
        attachments = attachments,
        delete_attachments_after_send = delete_attachments_after_send,
        send_to=send_to,
        language_code =language_code
    )