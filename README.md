# django-templatemailer

This package provides a Django component that can be used to send HTML and plain text emails rendered with the Django template engine. The email templates are store in the database.

The package supports sending emails directle or via Celery tasks.

## Installation

Add templatemailer to INSTALLED_APPS


## Settings

Configure templatemailer with the TEMPLATEMAILER dict in settings

```python
TEMPLATEMAILER = {
    "FROM": "noreply@liberaalipuolue.fi",
    "DEBUG_RECIPIENTS": ["tuomas.tiainen@liberaalipuolue.fi"],
    "USE_CELERY": False
}

```

## Usage

```python
from templatemailer.mailer import send_email

context = {}

send_email(
    "email_address@example.com",
    "template:name",
    context,
    email_from="From Name <from@example.com>"
)
```
