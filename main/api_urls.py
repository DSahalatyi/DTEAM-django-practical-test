from django.urls import path, include
from rest_framework import routers

from main.api_views import CVViewSet

router = routers.DefaultRouter()
router.register("cvs", CVViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
