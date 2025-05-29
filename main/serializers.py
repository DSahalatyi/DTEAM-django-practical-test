from django.db import transaction
from rest_framework import serializers

from main.models import Skill, Project, Contact, CV


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("name", "level")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("name", "description")


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("type", "value")


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = "__all__"


class CVListSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = CV
        fields = ("id", "first_name", "last_name", "bio", "skills")


class CVDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = CV
        fields = "__all__"


class CVCreateUpdateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer(many=True)

    class Meta:
        model = CV
        fields = (
            "id",
            "first_name",
            "last_name",
            "bio",
            "skills",
            "projects",
            "contacts",
        )

    def create(self, validated_data):
        skills_data = validated_data.pop("skills")
        projects_data = validated_data.pop("projects")
        contacts_data = validated_data.pop("contacts")

        with transaction.atomic():
            cv = CV.objects.create(**validated_data)

            for skill in skills_data:
                Skill.objects.create(cv=cv, **skill)
            for project in projects_data:
                Project.objects.create(cv=cv, **project)
            for contact in contacts_data:
                Contact.objects.create(cv=cv, **contact)

        return cv

    def update(self, instance, validated_data):
        skills_data = validated_data.pop("skills")
        projects_data = validated_data.pop("projects")
        contacts_data = validated_data.pop("contacts")

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if skills_data is not None:
                instance.skills.all().delete()
                for s in skills_data:
                    Skill.objects.create(cv=instance, **s)

            if projects_data is not None:
                instance.projects.all().delete()
                for p in projects_data:
                    Project.objects.create(cv=instance, **p)

            if contacts_data is not None:
                instance.contacts.all().delete()
                for c in contacts_data:
                    Contact.objects.create(cv=instance, **c)

        return instance
