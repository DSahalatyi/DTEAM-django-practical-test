import threading

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from audit.models import RequestLog

_thread_locals = threading.local()


class RequestLogMiddleware(MiddlewareMixin):
    BATCH_SIZE = 10

    def process_request(self, request):
        if request.path.startswith(
            ("/static/", "/media/", "/favicon.ico", "/__debug__")
        ):
            return

        request._log_data = {
            "http_method": request.method,
            "path": request.path,
            "query_string": request.META.get("QUERY_STRING", ""),
            "remote_ip": request.META.get("REMOTE_ADDR", ""),
            "user": getattr(request, "user", None)
            if request.user.is_authenticated
            else None,
        }

    def process_response(self, request, response):
        data = getattr(request, "_log_data", None)
        if data is None:
            return response

        log = RequestLog(
            http_method=data["http_method"],
            path=data["path"],
            query_string=data["query_string"],
            remote_ip=data["remote_ip"],
            user=data["user"],
        )

        if settings.TESTING:
            log.save()
            return response

        buffer = getattr(_thread_locals, "buffer", [])
        buffer.append(log)

        if len(buffer) >= self.BATCH_SIZE:
            RequestLog.objects.bulk_create(buffer)
            buffer.clear()

        _thread_locals.buffer = buffer
        return response
