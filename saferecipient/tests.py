# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.mail import EmailMultiAlternatives
from django.test import TestCase

from saferecipient import EmailBackend


class TestEmailBackend(TestCase):
    SAFE_EMAIL = 'safe@example.com'

    def test_safeguard(self):
        with self.settings(SAFE_EMAIL_RECIPIENT=self.SAFE_EMAIL):
            message = self._setup_message()
            EmailBackend()._safeguard(message)
            self.assertEquals(message.from_email, 'safe@example.com')
            self.assertEquals(message.to, ['safe@example.com'])
            self.assertEquals(message.cc, ['safe@example.com'])
            self.assertEquals(
                message.attachments[0].get_payload(),
                ("Original From: sender@example.com\nOriginal To: "
                 "['recipient@example.com']\nOriginal CC: "
                 "['cc_recipient@example.com']\nOriginal BCC: []\n"))

    def test_safeguard_with_whitelist(self):
        with self.settings(SAFE_EMAIL_RECIPIENT=self.SAFE_EMAIL), \
             self.settings(SAFE_EMAIL_WHITELIST=[r".*@example\.com",
                                                 r"safe.*@example\.org"]):
            message = self._setup_message(from_email='sender@example.com',
                                          to=['recipient@example.com'],
                                          cc=["safe+safe@example.org"],
                                          bcc=["unsafe@example.net"])
            EmailBackend()._safeguard(message)
            self.assertEquals(message.from_email, 'sender@example.com')
            self.assertEquals(message.to, ['recipient@example.com'])
            self.assertEquals(message.cc, ["safe+safe@example.org"])
            self.assertEquals(message.attachments[0].get_payload(),
                              ("Original From: sender@example.com\n"
                               "Original To: ['recipient@example.com']\n"
                               "Original CC: ['safe+safe@example.org']\n"
                               "Original BCC: ['unsafe@example.net']\n"))

    def test_no_setting(self):
        message = self._setup_message()
        self.assertRaises(
            AttributeError, EmailBackend()._safeguard, message)

    def test_only_safe_emails(self):
        with self.settings(SAFE_EMAIL_RECIPIENT=self.SAFE_EMAIL), \
             self.settings(SAFE_EMAIL_WHITELIST=[r".*@example\.com",
                                                 r"safe.*@example\.org"]):
            eb = EmailBackend()
            self.assertEqual(([], False), eb._only_safe_emails([]))
            self.assertEqual(([self.SAFE_EMAIL], True),
                             eb._only_safe_emails(["unsafe@example.org"]))
            self.assertEqual(([self.SAFE_EMAIL], True),
                             eb._only_safe_emails(["unsafe@example.org",
                                                   "unsafe2@example.org"]))
            self.assertEqual(([self.SAFE_EMAIL], True),
                             eb._only_safe_emails([self.SAFE_EMAIL,
                                                   "unsafe@example.org",
                                                   "unsafe2@example.org"]))
            self.assertEqual((["safe+2@example.com", self.SAFE_EMAIL], True),
                             eb._only_safe_emails(["safe+2@example.com",
                                                   self.SAFE_EMAIL,
                                                   "unsafe@example.org",
                                                   "unsafe2@example.org"]))
            self.assertEqual((["safe+2@example.com",
                               self.SAFE_EMAIL,
                               "safe@example.org"],
                              True),
                             eb._only_safe_emails(["safe+2@example.com",
                                                   self.SAFE_EMAIL,
                                                   "unsafe@example.org",
                                                   "unsafe2@example.org",
                                                   "safe@example.org"]))

    def test_whitelist(self):
        with self.settings(SAFE_EMAIL_WHITELIST=[r".*@example\.com",
                                                 r"safe.*@example\.org"]):
            eb = EmailBackend()
            self.assertTrue(eb._is_whitelisted("example@example.com"))
            self.assertTrue(eb._is_whitelisted("example2@example.com"))
            self.assertTrue(eb._is_whitelisted("safe@example.org"))
            self.assertTrue(eb._is_whitelisted("safe+2@example.org"))
            self.assertFalse(eb._is_whitelisted("unsafe@example.org"))

    def _setup_message(self, from_email='sender@example.com', to=None,
                       cc=None, bcc=None):
        if to is None:
            to = ['recipient@example.com']
        if cc is None:
            cc = ['cc_recipient@example.com']
        if bcc is None:
            bcc = []
        return EmailMultiAlternatives(from_email=from_email, to=to, cc=cc,
                                      bcc=bcc, subject='test', body='TEST')
