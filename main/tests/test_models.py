from django.test import TestCase

from main.models import CV


class TestCVModel(TestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            first_name="Test",
            last_name="Testing",
            bio="Test bio",
        )

    def test_cv_absolute_url(self):
        self.assertEqual(self.cv.get_absolute_url(), f"/cv/{self.cv.id}/")
