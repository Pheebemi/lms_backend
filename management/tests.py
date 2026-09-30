from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

from authentication.models import User
from .models import CourseCatalog, ManualCertificate

GENERATE_URL = '/api/management/certificates/generate/'
EMAIL_URL = '/api/management/certificates/email/'
LIST_URL = '/api/management/certificates/'


@override_settings(CONTACT_EMAIL_HOST_USER='')  # send_from_info falls back to the default connection
class ManualCertificateHistoryTests(APITestCase):
    """Generate -> history -> download/email flow for manually issued certificates."""

    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create(
            username='mgr', email='mgr@example.com', role='management', is_verified=True,
        )
        cls.student = User.objects.create(
            username='stu', email='stu@example.com', role='student', is_verified=True,
        )
        cls.course = CourseCatalog.objects.create(
            sn=1, name='Web Development', duration='3 months', price=50000,
        )

    def setUp(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post(
            GENERATE_URL,
            {'recipient_name': 'Jane Doe', 'course': self.course.id, 'grade': 'distinction'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.certificate = ManualCertificate.objects.get(recipient_name='Jane Doe')

    def test_generate_saves_a_record_and_returns_the_image(self):
        self.assertEqual(self.certificate.emailed_to, '')
        self.assertIsNone(self.certificate.emailed_at)

    def test_regenerate_by_id_keeps_the_same_certificate_id(self):
        response = self.client.post(GENERATE_URL, {'id': str(self.certificate.id)}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response['X-Certificate-Id'], self.certificate.certificate_id)
        self.assertEqual(ManualCertificate.objects.count(), 1)

    def test_regenerate_rejects_bad_and_unknown_ids(self):
        self.assertEqual(self.client.post(GENERATE_URL, {'id': 'nope'}, format='json').status_code, 400)
        unknown = '00000000-0000-0000-0000-000000000000'
        self.assertEqual(self.client.post(GENERATE_URL, {'id': unknown}, format='json').status_code, 404)

    def test_email_sends_the_png_and_records_the_recipient(self):
        response = self.client.post(
            EMAIL_URL, {'id': str(self.certificate.id), 'email': 'jane@example.com'}, format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True, 'emailed_to': 'jane@example.com'})

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ['jane@example.com'])
        self.assertIn('Web Development', message.subject)
        self.assertIn('Dear Jane Doe', message.body)
        filename, content, mimetype = message.attachments[0]
        self.assertEqual(mimetype, 'image/png')
        self.assertTrue(filename.startswith(f'certificate_{self.certificate.certificate_id}_'))
        self.assertTrue(content.startswith(b'\x89PNG'))

        self.certificate.refresh_from_db()
        self.assertEqual(self.certificate.emailed_to, 'jane@example.com')
        self.assertIsNotNone(self.certificate.emailed_at)

    def test_email_uses_custom_subject_and_message_when_given(self):
        self.client.post(
            EMAIL_URL,
            {'id': str(self.certificate.id), 'email': 'jane@example.com',
             'subject': 'Custom subject', 'message': 'Custom note.'},
            format='json',
        )
        self.assertEqual(mail.outbox[0].subject, 'Custom subject')
        self.assertEqual(mail.outbox[0].body, 'Custom note.')

    def test_email_failure_returns_502_and_does_not_record_a_send(self):
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                               EMAIL_HOST='127.0.0.1', EMAIL_PORT=1):
            response = self.client.post(
                EMAIL_URL, {'id': str(self.certificate.id), 'email': 'jane@example.com'}, format='json',
            )
        self.assertEqual(response.status_code, 502)
        self.certificate.refresh_from_db()
        self.assertEqual(self.certificate.emailed_to, '')
        self.assertIsNone(self.certificate.emailed_at)

    def test_email_validates_input(self):
        body = {'id': str(self.certificate.id), 'email': 'not-an-email'}
        self.assertEqual(self.client.post(EMAIL_URL, body, format='json').status_code, 400)
        unknown = {'id': '00000000-0000-0000-0000-000000000000', 'email': 'a@b.com'}
        self.assertEqual(self.client.post(EMAIL_URL, unknown, format='json').status_code, 404)

    def test_only_management_can_email(self):
        body = {'id': str(self.certificate.id), 'email': 'jane@example.com'}
        self.client.force_authenticate(self.student)
        self.assertEqual(self.client.post(EMAIL_URL, body, format='json').status_code, 403)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.post(EMAIL_URL, body, format='json').status_code, 401)
        self.assertEqual(len(mail.outbox), 0)

    def test_history_list_exposes_last_emailed(self):
        self.client.post(EMAIL_URL, {'id': str(self.certificate.id), 'email': 'jane@example.com'}, format='json')
        data = self.client.get(LIST_URL).json()
        rows = data['results'] if isinstance(data, dict) else data
        self.assertEqual(rows[0]['emailed_to'], 'jane@example.com')
        self.assertIsNotNone(rows[0]['emailed_at'])
