from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import View, TemplateView

from main.forms import TranslateCVForm
from main.models import CV
from main.tasks import send_cv_email
from main.utilities import html_to_pdf, translate_text


class CVListView(generic.ListView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")


class CVDetailView(generic.DetailView):
    model = CV
    queryset = CV.objects.prefetch_related("skills", "projects", "contacts")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["translate_form"] = TranslateCVForm()
        ctx["translated_fields"] = {}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TranslateCVForm(request.POST)
        context = self.get_context_data()
        context["translate_form"] = form

        if form.is_valid():
            lang = form.cleaned_data["language"]

            if lang == "en":
                return redirect("main:cv-detail", pk=self.object.pk)

            data = {
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "bio": self.object.bio,
                "skills": [
                    {"name": skill.name, "level": skill.get_level_display()}
                    for skill in self.object.skills.all()
                ],
                "projects": [
                    {"name": project.name, "description": project.description}
                    for project in self.object.projects.all()
                ],
                "contacts": [
                    {"type": contact.get_type_display(), "value": contact.value}
                    for contact in self.object.contacts.all()
                ],
                "headings": {
                    "skills": "Skills",
                    "projects": "Projects",
                },
            }

            translated = {}
            for key, value in data.items():
                if isinstance(value, list):
                    if all(isinstance(item, str) for item in value):
                        translated[key] = [translate_text(item, lang) for item in value]
                    elif all(isinstance(item, dict) for item in value):
                        translated[key] = []
                        for item in value:
                            translated_item = {
                                k: translate_text(v, lang) for k, v in item.items()
                            }
                            translated[key].append(translated_item)
                elif isinstance(value, dict):
                    translated[key] = {
                        k: translate_text(v, lang) for k, v in value.items()
                    }
                else:
                    translated[key] = translate_text(value, lang)

            context["translated_fields"] = translated

        return self.render_to_response(context)


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


# Remove restrictions for testing/demonstration purposes
class SettingsView(
    # LoginRequiredMixin,
    # UserPassesTestMixin,
    TemplateView
):
    template_name = "main/settings.html"

    # def test_func(self):
    #     return self.request.user.is_superuser


class CVSendEmailView(View):
    def post(self, request, pk):
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email address is required.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        cv = get_object_or_404(CV, pk=pk)
        print("Creating send mail task")
        send_cv_email.delay(cv.id, email)
        messages.success(request, "CV is being sent to the specified email.")
        return redirect(request.META.get("HTTP_REFERER", "/"))
