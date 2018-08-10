import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone


class AuthenticationFailure(models.Model):
    """
    Log failed logins based on IP and optionally per username.
    """
    username = models.CharField(max_length=255, null=True, default=None)
    ip = models.CharField(max_length=46, null=False)
    time_added = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def limit_exceeded(ip, username=None):
        kwargs = {'ip': ip, 'username': username} if username else {'ip': ip}

        AuthenticationFailure._reset_failures(**kwargs)
        failures = AuthenticationFailure.objects.filter(**kwargs)

        return failures.count() > settings.DMFA_AUTHENTICATION_FAILURE_LIMIT

    @staticmethod
    def _reset_failures(**kwargs):
        exceeding_retention = timezone.now() - datetime.timedelta(
            seconds=settings.DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS)
        kwargs.update({'time_added__lt': exceeding_retention})
        AuthenticationFailure.objects.filter(**kwargs).delete()
