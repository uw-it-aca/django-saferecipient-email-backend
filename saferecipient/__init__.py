# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
import ssl
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
from django.utils.functional import cached_property
from email.mime.text import MIMEText


class EmailBackend(SMTPEmailBackend):
    """
    An SMTP email backend class that only sends email to a safe email address.

    Re-routes email, so it goes to, and comes from
    settings.SAFE_EMAIL_RECIPIENT.

    The original to and from are added to a text file
    that is attached to the message.
    """

    @cached_property
    def ssl_context(self):
        """
        See https://code.djangoproject.com/ticket/34504
        """
        try:
            ssl_context = super().ssl_context
        except AttributeError:  # Django < 4
            ssl_context = ssl.SSLContext()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def send_messages(self, email_messages):
        for message in email_messages:
            self._safeguard(message)
        return super().send_messages(email_messages)

    def _safeguard(self, message):
        originals = ("Original From: {}\nOriginal To: {}\nOriginal CC: {}\n"
                     "Original BCC: {}\n").format(
                         message.from_email, message.to,
                         message.cc, message.bcc)

        from_modified = False
        if not self._is_safelisted(message.from_email):
            from_modified = True
            message.from_email = settings.SAFE_EMAIL_RECIPIENT

        message.to, to_modified = self._only_safe_emails(message.to)
        message.cc, cc_modified = self._only_safe_emails(message.cc)
        message.bcc, bcc_modified = self._only_safe_emails(message.bcc)

        if from_modified or to_modified or cc_modified or bcc_modified:
            text_attachment = MIMEText(originals)
            text_attachment.add_header(
                'Content-disposition',
                'attachment; filename="original_emails.txt"')
            message.attach(text_attachment)

    def _only_safe_emails(self, emails):
        """"
        Given a list of emails, checks whether they are all in the safe list.
        """
        email_modified = False
        if any(not self._is_safelisted(email) for email in emails):
            email_modified = True
            emails = [email for email in emails if self._is_safelisted(email)]
            if settings.SAFE_EMAIL_RECIPIENT not in emails:
                emails.append(settings.SAFE_EMAIL_RECIPIENT)
        return emails, email_modified

    def _is_safelisted(self, email):
        """
        Check if an email is in the safelist. If there's no safelist,
        it's assumed it's not safelisted.
        """
        return (hasattr(settings, "SAFE_EMAIL_SAFELIST") and
                any(re.match(m, email) for m in settings.SAFE_EMAIL_SAFELIST))
