import pytz
import datetime

from django.db import IntegrityError
from django.test import TestCase
from libfaketime import fake_time

from django_multi_factor_authentication.factories.multi_factor_user_factory import MultiFactorUserFactory
from django_multi_factor_authentication.models import MultiFactorToken, MultiFactorAuthenticationUser


class TestMultiFactorToken(TestCase):
    def test_raises_if_no_two_factor_user_provided(self):
        with self.assertRaises(IntegrityError):
            MultiFactorToken.objects.create(code="slow-down-tinkerbell")

    @fake_time("2018-08-20 12:00:00+00:00")
    def test_sets_date_added_to_current_date_time(self):
        mf_user = MultiFactorUserFactory()
        token = MultiFactorToken.objects.create(code="youll-never-sing-the-same", multi_factor_user=mf_user)
        self.assertEqual(token.time_added, datetime.datetime.now(tz=pytz.utc))

    def test_deleting_multi_factor_user_deletes_token(self):
        mf_user = MultiFactorUserFactory()
        MultiFactorToken.objects.create(code="if-your-teeth-aint-your-own", multi_factor_user=mf_user)

        mf_user.delete()
        self.assertEqual(MultiFactorToken.objects.all().count(), 0)

    def test_deleting_token_does_not_delete_multi_factor_user(self):
        mf_user = MultiFactorUserFactory()
        token = MultiFactorToken.objects.create(code="alright-guvnor", multi_factor_user=mf_user)

        token.delete()
        self.assertTrue(MultiFactorAuthenticationUser.objects.filter(user=mf_user.user).exists())
