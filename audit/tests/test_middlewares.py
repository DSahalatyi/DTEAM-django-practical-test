from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from audit.models import RequestLog


class RequestLogMiddlewareTest(TestCase):
    TEST_URL = reverse("api:cv-list")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

    def test_log_is_created_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.TEST_URL, {"search": "test"})
        self.assertEqual(response.status_code, 200)

        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), 1)

        log = logs.first()
        self.assertEqual(log.http_method, "GET")
        self.assertTrue(log.path.endswith(self.TEST_URL))
        self.assertEqual(log.query_string, "search=test")
        self.assertEqual(log.user, self.user)

    def test_log_is_created_for_anonymous_user(self):
        response = self.client.get(self.TEST_URL, {"search": "test"})
        self.assertEqual(response.status_code, 200)

        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), 1)

        log = logs.first()
        self.assertEqual(log.http_method, "GET")
        self.assertTrue(log.path.endswith(self.TEST_URL))
        self.assertEqual(log.query_string, "search=test")
        self.assertEqual(log.user, None)
