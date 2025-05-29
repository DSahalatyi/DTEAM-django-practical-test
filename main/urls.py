from django.urls import path

from main.views import (
    CVListView,
    CVDetailView,
    CVDownloadPDFView,
    SettingsView,
    CVSendEmailView,
)

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv-list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv-detail"),
    path("cv/<int:pk>/download/", CVDownloadPDFView.as_view(), name="cv-download"),
    path("cv/<int:pk>/send-email/", CVSendEmailView.as_view(), name="cv-send-email"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
