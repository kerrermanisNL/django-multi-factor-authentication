import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from django_multi_factor_authentication.models import MultiFactorAuthenticationUser


class MultiFactorToken(models.Model):
    code = models.CharField(max_length=255)
    time_added = models.DateTimeField(auto_now_add=True)
    multi_factor_user = models.ForeignKey(MultiFactorAuthenticationUser, on_delete=models.CASCADE)

    def is_valid(self):
        x_hours_ago = timezone.now() - datetime.timedelta(
            seconds=settings.DMFA_TOKEN_INVALIDATITY_TIME_SECONDS)

        return not MultiFactorToken.objects.filter(
            time_added__gte=x_hours_ago, code=self.code,
            multi_factor_user=self.multi_factor_user).exists()
