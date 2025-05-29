from django.contrib.auth.models import User
from django.db import models


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    http_method = models.CharField(max_length=15)
    path = models.CharField(max_length=127)
    query_string = models.TextField(blank=True)
    remote_ip = models.CharField(max_length=63)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="request_logs",
    )

    class Meta:
        ordering = ("-timestamp",)
