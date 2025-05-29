from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import View, TemplateView

from main.models import CV
from main.tasks import send_cv_email
from main.utilities import html_to_pdf


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
        pdf_data = html_to_pdf(html)

        if pdf_data:
            response = HttpResponse(pdf_data, content_type="application/pdf")
            response["Content-Disposition"] = (
                f"attachment; filename={cv.first_name}_{cv.last_name}_cv.pdf"
            )
            return response
        return HttpResponse("Error rendering PDF", status=500)


class SettingsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "main/settings.html"

    def test_func(self):
        return self.request.user.is_superuser


class CVSendEmailView(View):
    def post(self, request, pk):
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email address is required.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        cv = get_object_or_404(CV, pk=pk)
        send_cv_email.delay(cv.id, email)
        messages.success(request, "CV is being sent to the specified email.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
