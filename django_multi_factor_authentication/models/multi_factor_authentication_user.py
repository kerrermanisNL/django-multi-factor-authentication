from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import OneToOneField


class MultiFactorAuthenticationUser(models.Model):
    user = OneToOneField(get_user_model(), on_delete=models.CASCADE)
    multi_factor_authentication_enabled = models.BooleanField(default=False)
