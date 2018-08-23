# Generated by Django 2.0.6 on 2018-08-23 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templatemailer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='email_template_attachments'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='language_code',
            field=models.CharField(default='en', max_length=16),
        ),
    ]