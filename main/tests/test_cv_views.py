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


class CDDownloadTests(BaseCVTests):
    CV_DOWNLOAD_URL = reverse("main:cv-download", kwargs={"pk": 1})

    def test_pdf_download_returns_pdf(self):
        response = self.client.get(self.CV_DOWNLOAD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_pdf_download_has_correct_filename(self):
        response = self.client.get(self.CV_DOWNLOAD_URL)
        content_disposition = response["Content-Disposition"]
        self.assertIn("attachment", content_disposition)
        self.assertIn(
            f"{self.cv.first_name}_{self.cv.last_name}_cv.pdf", content_disposition
        )
