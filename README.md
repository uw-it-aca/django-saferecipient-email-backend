[![Build Status](https://api.travis-ci.org/uw-it-aca/django-saferecipient-email-backend.svg?branch=master)](https://travis-ci.org/uw-it-aca/django-saferecipient-email-backend)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/django-saferecipient-email-backend/badge.png?branch=master)](https://coveralls.io/r/uw-it-aca/django-saferecipient-email-backend?branch=master)


django-saferecipient-email-backend
==================================

This provides an email backend for Django that will re-route all emails to a safe email address provided by your project's settings.py.  This uses the SMTP email backend to actually send the email.

This makes it so you can use any email address you like during testing, without worrying about spamming people.  The original To:, CC:, BCC: and From: will be attached

To use this, put this in your settings.py:

    EMAIL_BACKEND='saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT='your email address, or a team testing address'
