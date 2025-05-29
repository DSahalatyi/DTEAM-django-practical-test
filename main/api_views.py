from rest_framework import viewsets

from main.models import CV
from main.serializers import (
    CVSerializer,
    CVListSerializer,
    CVDetailSerializer,
    CVCreateUpdateSerializer,
)


class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = CV.objects.prefetch_related("skills")
        if self.action == "retrieve":
            queryset = CV.objects.prefetch_related("skills", "projects", "contacts")

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = CVListSerializer

        if self.action == "retrieve":
            serializer = CVDetailSerializer

        if self.action in ("create", "update", "partial_update"):
            serializer = CVCreateUpdateSerializer

        return serializer
