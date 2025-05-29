from django.views import generic

from audit.models import RequestLog


class RequestLogListView(generic.ListView):
    model = RequestLog
    queryset = RequestLog.objects.all()[:10]
