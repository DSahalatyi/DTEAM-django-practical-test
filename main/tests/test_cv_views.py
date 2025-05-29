from django.test import TestCase
from django.urls.base import reverse

from main.models import CV


class BaseCVTests(TestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            first_name="Test", last_name="Testing", bio="Test bio"
        )


class CVListTests(BaseCVTests):
    CV_LIST_URL = reverse("main:cv-list")

    def test_cv_list_uses_correct_template(self):
        response = self.client.get(self.CV_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cv_list.html")


class CVDetailTests(BaseCVTests):
    def test_cv_detail_uses_correct_template(self):
        response = self.client.get(self.cv.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cv_detail.html")
