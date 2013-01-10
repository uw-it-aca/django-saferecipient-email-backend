django-saferecipient-email-backend
==================================

This provides an email backend for Django that will re-route all emails to a safe email address provided by your project's settings.py.  This uses the SMTP email backend to actually send the email.

This makes it so you can use any email address you like during testing, without worrying about spamming people.  The original To:, CC:, BCC: and From: will be attached 

To use this, put this in your settings.py:

    EMAIL_BACKEND='saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT='your email address, or a team testing address'

To install, put this in your requirements.txt:

    -e git://github.com/vegitron/django-saferecipient-email-backend.git#egg=safe_email_backend

