import datetime
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

from django_multi_factor_authentication.models import MultiFactorAuthenticationUser


def _uuid_value():
    return uuid4().hex


class MultiFactorAuthenticationToken(models.Model):
    multi_factor_user = models.ForeignKey(MultiFactorAuthenticationUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, default=_uuid_value)
    time_added = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expired_timestamp = self.time_added + datetime.timedelta(
            seconds=settings.DMFA_AUTHENTICATION_TOKEN_VALIDITY_TIME_SECONDS)
        return timezone.now() > expired_timestamp
