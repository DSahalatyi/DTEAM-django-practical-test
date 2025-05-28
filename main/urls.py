from django.urls import path

from main.views import CVListView, CVDetailView

app_name = 'main'

urlpatterns = [
    path("", CVListView.as_view(), name='cv-list'),
    path("cv/<int:pk>/", CVDetailView.as_view(), name='cv-detail'),
]