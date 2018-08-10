from django.conf import settings
from django.db import models


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
        failures = AuthenticationFailure.objects.filter(**kwargs)
        return failures.count() > settings.DMFA_AUTHENTICATION_FAILURE_LIMIT
