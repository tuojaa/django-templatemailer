import traceback
import logging
from django.contrib import admin

# Register your models here.
from .models import EmailTemplate

admin.site.register(EmailTemplate)

logger = logging.getLogger(__name__)