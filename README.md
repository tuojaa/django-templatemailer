# django-templatemailer

This package provides a Django component that can be used to send HTML and plain text emails rendered with the Django template engine. The email templates are store in the database.

The package supports sending emails via Celery or Zappa delay functionality.

## Installation

Add templatemailer to INSTALLED_APPS


## Settings

Asynchronous email sending can be configured with the TEMPLATEMAILER_ASYNC setting. If it is not set, no async queue is used.

```python
TEMPLATEMAILER_ASYNC = "CELERY"
TEMPLATEMAILER_ASYNC = "ZAPPA"
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
