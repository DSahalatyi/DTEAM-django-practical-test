from django.test import TestCase

from main.models import CV, Skill, LevelChoices


class BaseModelTest(TestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            first_name="Test",
            last_name="Testing",
            bio="Test bio",
        )


class TestCVModel(BaseModelTest):
    def test_cv_absolute_url(self):
        self.assertEqual(self.cv.get_absolute_url(), f"/cv/{self.cv.id}/")


class TestSkillModel(BaseModelTest):
    def setUp(self):
        super().setUp()
        self.name = "Test skill"
        self.skill = Skill.objects.create(
            cv=self.cv, name=self.name, level=LevelChoices.BASIC
        )

    def test_skill_str(self):
        self.assertEqual(str(self.skill), self.name)
