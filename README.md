[![Build Status](https://github.com/uw-it-aca/django-saferecipient-email-backend/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/django-saferecipient-email-backend/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/django-saferecipient-email-backend/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/django-saferecipient-email-backend?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/django-safe-emailbackend.svg)](https://pypi.python.org/pypi/django-safe-emailbackend)
![Python versions](https://img.shields.io/pypi/pyversions/django-safe-emailbackend.svg)


django-saferecipient-email-backend
==================================

This app provides an email backend for Django that will re-route all emails to a safe email address provided by your project's settings.py.  This uses the SMTP email backend to actually send the email.

This makes it so you can use any email address you like during testing, without worrying about spamming people.  The original To:, CC:, BCC: and From: will be attached.

Specific email addresses, domains, etc. that will bypass the safe email routing can be added via a regex-based safelist.

### Configuration

To use this, put these in your settings.py:

    EMAIL_BACKEND='saferecipient.EmailBackend'
    SAFE_EMAIL_RECIPIENT='your email address, or a team testing address'

    # Optional
    SAFE_EMAIL_SAFELIST = []
