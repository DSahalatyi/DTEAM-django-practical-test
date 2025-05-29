import json

from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient

from main.models import LevelChoices, Skill, Project, CV, Contact, ContactChoices


class CVApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cv = CV.objects.create(
            first_name="Test", last_name="Testing", bio="Test bio"
        )
        self.skill = Skill.objects.create(
            cv=self.cv, name="Skill", level=LevelChoices.BASIC
        )
        self.project = Project.objects.create(
            cv=self.cv, name="Test Project", description="Test description"
        )
        self.contact = Contact.objects.create(
            cv=self.cv, type=ContactChoices.PHONE, value="+1234567890"
        )

    def test_get_cvs(self):
        response = self.client.get(reverse("api:cv-list"))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 1)
        cv_data = data[0]
        self.assertEqual(cv_data["first_name"], self.cv.first_name)
        self.assertEqual(cv_data["last_name"], self.cv.last_name)
        self.assertEqual(cv_data["bio"], self.cv.bio)

        self.assertIn("skills", cv_data)
        self.assertEqual(len(cv_data["skills"]), 1)
        self.assertIn(self.skill.name, cv_data["skills"])

    def test_get_cv_detail(self):
        response = self.client.get(reverse("api:cv-detail", kwargs={"pk": self.cv.pk}))
        self.assertEqual(response.status_code, 200)

        cv_data = response.json()

        self.assertEqual(cv_data["first_name"], self.cv.first_name)
        self.assertEqual(cv_data["last_name"], self.cv.last_name)
        self.assertEqual(cv_data["bio"], self.cv.bio)

        self.assertIn("skills", cv_data)
        self.assertEqual(len(cv_data["skills"]), 1)
        self.assertEqual(cv_data["skills"][0]["name"], self.skill.name)
        self.assertEqual(cv_data["skills"][0]["level"], self.skill.level)

        self.assertIn("projects", cv_data)
        self.assertEqual(len(cv_data["projects"]), 1)
        self.assertEqual(cv_data["projects"][0]["name"], self.project.name)
        self.assertEqual(
            cv_data["projects"][0]["description"], self.project.description
        )

        self.assertIn("contacts", cv_data)
        self.assertEqual(len(cv_data["contacts"]), 1)
        self.assertEqual(cv_data["contacts"][0]["type"], self.contact.type)
        self.assertEqual(cv_data["contacts"][0]["value"], self.contact.value)

    def test_post_cv(self):
        data = {
            "first_name": "Post",
            "last_name": "Posting",
            "bio": "Post bio",
            "skills": [{"name": "Skill", "level": LevelChoices.INTERMEDIATE}],
            "projects": [{"name": "Test Project", "description": "Test description"}],
            "contacts": [{"type": ContactChoices.PHONE, "value": "+1234567890"}],
        }
        response = self.client.post(
            reverse("api:cv-list"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        db_cvs = CV.objects.all()
        self.assertEqual(db_cvs.count(), 2)

        db_cv = db_cvs.filter(first_name=data["first_name"]).first()

        self.assert_related_fields(db_cv, data)

    def test_update_cv(self):
        data = {
            "first_name": "Update",
            "last_name": "Updating",
            "bio": "Update bio",
            "skills": [{"name": "Update", "level": LevelChoices.INTERMEDIATE}],
            "projects": [
                {"name": "Updated Project", "description": "Test description"}
            ],
            "contacts": [{"type": ContactChoices.EMAIL, "value": "email@email.com"}],
        }
        response = self.client.put(
            reverse("api:cv-detail", kwargs={"pk": self.cv.pk}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        db_cv = CV.objects.get(pk=self.cv.pk)

        self.assertEqual(db_cv.first_name, data["first_name"])
        self.assertEqual(db_cv.last_name, data["last_name"])
        self.assertEqual(db_cv.bio, data["bio"])

        self.assert_related_fields(db_cv, data)

    def test_delete_cv(self):
        response = self.client.delete(
            reverse("api:cv-detail", kwargs={"pk": self.cv.pk})
        )
        self.assertEqual(response.status_code, 204)

        db_cvs = CV.objects.filter(id=self.cv.pk)
        self.assertEqual(db_cvs.count(), 0)

    def assert_related_fields(self, db_cv, data):
        self.assertEqual(db_cv.skills.count(), 1)
        self.assertEqual(db_cv.skills.first().name, data["skills"][0]["name"])
        self.assertEqual(db_cv.skills.first().level, data["skills"][0]["level"])

        self.assertEqual(db_cv.projects.count(), 1)
        self.assertEqual(db_cv.projects.first().name, data["projects"][0]["name"])

        self.assertEqual(db_cv.contacts.count(), 1)
        self.assertEqual(db_cv.contacts.first().type, data["contacts"][0]["type"])
        self.assertEqual(db_cv.contacts.first().value, data["contacts"][0]["value"])
