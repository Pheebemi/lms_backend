import os
import tempfile
from io import StringIO
from unittest import mock
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from authentication.models import User
from .models import Certificate, Course, Enrollment


def stored_files(root):
    return [os.path.join(d, f) for d, _, files in os.walk(root) for f in files]


class CertificateOnDemandTests(APITestCase):
    """Student course-completion certificates are drawn on demand, never stored."""

    @classmethod
    def setUpTestData(cls):
        tutor = User.objects.create(
            username='tutor', email='tutor@example.com', role='tutor', is_verified=True,
        )
        cls.student = User.objects.create(
            username='stu', email='stu@example.com', first_name='Jane', last_name='Doe',
            role='student', is_verified=True,
        )
        cls.course = Course.objects.create(
            title='Web Development', description='Learn the web', instructor=tutor,
        )
        cls.enrollment = Enrollment.objects.create(
            student=cls.student, course=cls.course, is_completed=True, completed_at=timezone.now(),
        )

    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        override = override_settings(MEDIA_ROOT=self.media.name)
        override.enable()
        self.addCleanup(override.disable)
        self.client.force_authenticate(self.student)

    def generate(self):
        return self.client.post(f'/api/courses/student/certificates/generate/{self.enrollment.id}/')

    def test_generating_saves_a_record_but_no_file(self):
        response = self.generate()
        self.assertEqual(response.status_code, 201)

        certificate = Certificate.objects.get()
        self.assertFalse(certificate.image_file)
        self.assertEqual(stored_files(self.media.name), [])
        self.assertIn('/certificates/render/', response.json()['certificate']['image_file_url'])

    def test_the_link_draws_a_png_on_demand_without_logging_in(self):
        url = self.generate().json()['certificate']['image_file_url']

        response = APIClient().get(urlparse(url).path)  # anonymous, like an <img src>

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertTrue(response.content.startswith(b'\x89PNG'))
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(stored_files(self.media.name), [])

    def test_tampered_link_is_not_found(self):
        url = self.generate().json()['certificate']['image_file_url']
        path = urlparse(url).path
        self.assertEqual(APIClient().get(path.replace('/render/', '/render/x')).status_code, 404)
        self.assertEqual(APIClient().get(path[:-2] + 'zz/').status_code, 404)

    def test_expired_link_is_not_found(self):
        url = self.generate().json()['certificate']['image_file_url']
        with mock.patch('courses.certificate_views.CERTIFICATE_IMAGE_MAX_AGE', -1):
            self.assertEqual(APIClient().get(urlparse(url).path).status_code, 404)

    def test_list_and_detail_return_full_working_links(self):
        self.generate()
        certificate = Certificate.objects.get()

        listed = self.client.get('/api/courses/student/certificates/').json()
        detail = self.client.get(f'/api/courses/student/certificates/{certificate.id}/').json()

        for url in (listed[0]['image_file_url'], detail['image_file_url']):
            self.assertTrue(url.startswith('http'), url)
            self.assertEqual(APIClient().get(urlparse(url).path).status_code, 200)

    def test_purge_command_deletes_old_files_and_keeps_certificates_working(self):
        self.generate()
        certificate = Certificate.objects.get()
        certificate.image_file.save('old.png', ContentFile(b'not really a png'), save=True)
        self.assertEqual(len(stored_files(self.media.name)), 1)

        call_command('purge_certificate_images', '--dry-run', stdout=StringIO())
        certificate.refresh_from_db()
        self.assertTrue(certificate.image_file)
        self.assertEqual(len(stored_files(self.media.name)), 1)

        out = StringIO()
        call_command('purge_certificate_images', stdout=out)
        certificate.refresh_from_db()
        self.assertIn('Deleted 1 certificate image file', out.getvalue())
        self.assertFalse(certificate.image_file)
        self.assertEqual(stored_files(self.media.name), [])

        url = self.client.get('/api/courses/student/certificates/').json()[0]['image_file_url']
        self.assertEqual(APIClient().get(urlparse(url).path).status_code, 200)
