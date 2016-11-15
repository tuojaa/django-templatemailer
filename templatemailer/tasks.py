from __future__ import absolute_import

import logging
import mimetypes
from os.path import basename

from celery import shared_task
from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import Template, Context

from .models import EmailTemplate

logger = logging.getLogger(__name__)


@shared_task
def task_email_user(
        user_pk,
        template_key,
        context,
        attachments=None,
        delete_attachments_after_send=True,
        language_code=None,
        email_from=None):
    '''
    Task to send email to user

    :param user_pk: User primary key (or None if no DB user is used)
    :param template_key: Template key
    :param context: Context variables as a dictionary
    :param attachments: Attachments as list of tuples (name, mimetype)
    :param delete_attachments_after_send: True = delete attachments from storage after sending email
    :param language_code: Language code for email template
    :return:
    '''
    headers = {}

    try:
        mailer_settings = settings.TEMPLATEMAILER
    except:
        mailer_settings = {}

    DEFAULT_LANGUAGE_CODE = mailer_settings.get("DEFAULT_LANGUAGE_CODE", "en")

    if attachments is None:
        attachments = []

    recipients = [user_pk, ]

    if settings.DEBUG and not mailer_settings.get("FORCE_DEBUG_OFF"):
        headers['X-DjangoTemplateMailer-Original-Recipients'] = ','.join(recipients)
        recipients = mailer_settings.get("DEBUG_RECIPIENTS", map(lambda (name, email): email, settings.ADMINS))

    try:
        email_template = EmailTemplate.objects.get(key=template_key, language_code=language_code)
    except:
        email_template = EmailTemplate.objects.get(key=template_key, language_code=DEFAULT_LANGUAGE_CODE)

    text_template = Template(email_template.plain_text)
    template_context = Context(context)

    text_body = text_template.render(template_context)

    if email_template.html:
        html_template = Template(email_template.html)
        html_body = html_template.render(template_context)
    else:
        html_body = None

    subject_template = Template(email_template.subject)
    subject = subject_template.render(template_context)

    email_from = email_from or mailer_settings.get("FROM", map(lambda (name, email): email, settings.ADMINS)[0])

    connection = get_connection()
    mail = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=email_from,
        to=recipients,
        connection=connection)

    if html_body:
        mail.attach_alternative(html_body, 'text/html')

    storage = DefaultStorage()

    if email_template.attachment:
        mimetype, att_encoding = mimetypes.guess_type(email_template.attachment.name)
        name = email_template.attachment.name
        f = storage.open(name)
        mail.attach(basename(name), f.read(), mimetype)

    for (name, mimetype) in attachments:
        f = storage.open(name)
        mail.attach(basename(name), f.read(), mimetype)
        if delete_attachments_after_send:
            storage.delete(name)

    mail.send()
