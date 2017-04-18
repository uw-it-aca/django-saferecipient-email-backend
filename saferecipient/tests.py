from django.test import TestCase
from django.core.mail import EmailMultiAlternatives
from saferecipient import EmailBackend


class TestEmailBackend(TestCase):
    def test_safeguard(self):
        with self.settings(SAFE_EMAIL_RECIPIENT='safe@example.com'):
            message = self._setup_message()
            EmailBackend()._safeguard(message)
            self.assertEquals(message.from_email, 'safe@example.com')
            self.assertEquals(message.to, ['safe@example.com'])
            self.assertEquals(message.cc, [])
            self.assertEquals(
                message.attachments[0].get_payload(),
                ("Original From: sender@example.com\nOriginal To: "
                 "['recipient@example.com']\nOriginal CC: "
                 "['cc_recipient@example.com']\nOriginal BCC: []\n"))

    def test_no_setting(self):
        message = self._setup_message()
        self.assertRaises(
            AttributeError, EmailBackend()._safeguard, message)

    def _setup_message(self):
        return EmailMultiAlternatives(
            subject='test', body='TEST', from_email='sender@example.com',
            to=['recipient@example.com'], cc=['cc_recipient@example.com'])
