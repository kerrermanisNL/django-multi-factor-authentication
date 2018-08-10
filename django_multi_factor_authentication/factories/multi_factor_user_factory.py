import factory
from django.contrib.auth import get_user_model

from django_multi_factor_authentication.models import MultiFactorAuthenticationUser


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'Jango Fett {}'.format(n))


class MultiFactorUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = MultiFactorAuthenticationUser

    user = factory.SubFactory(UserFactory)
