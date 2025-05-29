import io

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import View, TemplateView
from xhtml2pdf import pisa

from main.models import CV


class CVListView(generic.ListView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")


class CVDetailView(generic.DetailView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")


class CVDownloadPDFView(View):
    def get(self, request, pk):
        cv = CV.objects.prefetch_related("skills", "projects", "contacts").get(pk=pk)
        html = render_to_string("main/cv_pdf.html", {"cv": cv})
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = (
                f"attachment; filename={cv.first_name}_{cv.last_name}_cv.pdf"
            )
            return response
        return HttpResponse("Error rendering PDF", status=500)


class SettingsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "main/settings.html"

    def test_func(self):
        return self.request.user.is_superuser
