import traceback
import logging

from django.db import models

logger = logging.getLogger(__name__)

class EmailTemplate(models.Model):
    key = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    subject = models.CharField(max_length = 255)
    plain_text = models.TextField()
    html = models.TextField(null = True, blank = True)

    attachment = models.FileField(upload_to="email_template_attachments", null = True, blank = True)

    language_code = models.CharField(max_length = 16, default = "en")

    def __unicode__(self): return self.key