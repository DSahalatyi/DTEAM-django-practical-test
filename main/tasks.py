from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from main.models import CV
from main.utilities import html_to_pdf


@shared_task
def send_cv_email(cv_id, recipient_email):
    try:
        cv = CV.objects.prefetch_related("skills", "projects", "contacts").get(pk=cv_id)
        html = render_to_string("main/cv_pdf.html", {"cv": cv})
        pdf_data = html_to_pdf(html)
        if not pdf_data:
            raise Exception("PDF generation failed")

        filename = f"{cv.first_name}_{cv.last_name}_cv.pdf"
        email = EmailMessage(
            subject="Your CV PDF",
            body="Please find your CV attached.",
            from_email="your-email@example.com",
            to=[recipient_email],
        )
        email.attach(filename, pdf_data, "application/pdf")
        email.send()
    except CV.DoesNotExist:
        pass
