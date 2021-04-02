# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""SMTP email backend class that only sends email to a safe email address"""
import re
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
from email.mime.text import MIMEText


class EmailBackend(SMTPEmailBackend):
    """
    Re-routes email, so it goes to, and comes from
    settings.SAFE_EMAIL_RECIPIENT.

    The original to and from are added to a text file
    that is attached to the message.
    """

    def send_messages(self, email_messages):
        for message in email_messages:
            self._safeguard(message)
        return super(EmailBackend, self).send_messages(email_messages)

    def _safeguard(self, message):
        originals = ("Original From: {}\nOriginal To: {}\nOriginal CC: {}\n"
                     "Original BCC: {}\n").format(
                         message.from_email, message.to,
                         message.cc, message.bcc)

        from_modified = False
        if not self._is_whitelisted(message.from_email):
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
        """"Given a list of emails, checks whether they are all in the white
        list."""

        email_modified = False
        if any(not self._is_whitelisted(email) for email in emails):
            email_modified = True
            emails = [email for email in emails if self._is_whitelisted(email)]
            if settings.SAFE_EMAIL_RECIPIENT not in emails:
                emails.append(settings.SAFE_EMAIL_RECIPIENT)
        return emails, email_modified

    def _is_whitelisted(self, email):
        """Check if an email is in the whitelist. If there's no whitelist,
        it's assumed it's not whitelisted."""

        return hasattr(settings, "SAFE_EMAIL_WHITELIST") and \
            any(re.match(m, email) for m in settings.SAFE_EMAIL_WHITELIST)
