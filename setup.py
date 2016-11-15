from setuptools import setup

setup(name='django-templatemailer',
      version='0.0.7',
      description='Django component that is used to send emails using template engine',
      author='Tuomas Jaanu',
      author_email='tuomas@jaa.nu',
      url='https://github.com/tuomasjaanu/django-templatemailer',
      packages=['templatemailer', 'templatemailer.migrations'],
      install_requires=[
          "django-celery",
          "django",
      ],
      )
