from django.urls import path

from audit.views import RequestLogListView

app_name = "audit"

urlpatterns = [
    path("logs/", RequestLogListView.as_view(), name="logs"),
]
