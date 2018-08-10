from uuid import uuid4
from django.db import models

from django_multi_factor_authentication.models import MultiFactorAuthenticationUser


def _uuid_value():
    return uuid4().hex


class MultiFactorAuthenticationToken(models.Model):
    multi_factor_user = models.ForeignKey(MultiFactorAuthenticationUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, default=_uuid_value)
    time_added = models.DateTimeField(auto_now_add=True)
