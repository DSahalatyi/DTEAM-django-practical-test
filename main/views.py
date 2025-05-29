from django.views import generic

from main.models import CV


class CVListView(generic.ListView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")


class CVDetailView(generic.DetailView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")
