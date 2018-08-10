from django.db import models

from django_multi_factor_authentication.models import MultiFactorAuthenticationUser


class MultiFactorToken(models.Model):
    code = models.CharField(max_length=255)
    time_added = models.DateTimeField(auto_now_add=True)
    multi_factor_user = models.ForeignKey(MultiFactorAuthenticationUser, on_delete=models.CASCADE)
