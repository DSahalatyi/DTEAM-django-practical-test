from django.db import models


class LevelChoices(models.TextChoices):
    BASIC = "basic", "Basic"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"


class ContactChoices(models.TextChoices):
    PHONE = "phone", "Phone number"
    EMAIL = "email", "Email address"
    TELEGRAM = "telegram", "Telegram"
    LINKEDIN = "linkedin", "LinkedIn"
    GITHUB = "github", "Github"
    WEBSITE = "website", "Website"


class CV(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    bio = models.TextField()


class Skill(models.Model):
    cv = models.ForeignKey(CV, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    level = models.CharField(max_length=31, choices=LevelChoices.choices)


class Project(models.Model):
    cv = models.ForeignKey(CV, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()


class Contact(models.Model):
    cv = models.ForeignKey(CV, related_name="contacts", on_delete=models.CASCADE)
    type = models.CharField(max_length=63, choices=ContactChoices.choices)
    value = models.CharField(max_length=127)
