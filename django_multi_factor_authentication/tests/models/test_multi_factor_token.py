import datetime
import pytz
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import IntegrityError
from django.test import TestCase, override_settings
from libfaketime import fake_time

from django_multi_factor_authentication.factories.multi_factor_user_factory import MultiFactorUserFactory
from django_multi_factor_authentication.models import MultiFactorToken, MultiFactorAuthenticationUser


class TestMultiFactorToken(TestCase):
    def setUp(self):
        self.mf_user = MultiFactorUserFactory()

    def test_raises_if_no_two_factor_user_provided(self):
        with self.assertRaises(IntegrityError):
            MultiFactorToken.objects.create(code="slow-down-tinkerbell")

    @fake_time("2018-08-20 12:00:00+00:00")
    def test_sets_date_added_to_current_date_time(self):
        token = MultiFactorToken.objects.create(code="youll-never-sing-the-same", multi_factor_user=self.mf_user)
        self.assertEqual(token.time_added, datetime.datetime.now(tz=pytz.utc))

    def test_deleting_multi_factor_user_deletes_token(self):
        MultiFactorToken.objects.create(code="if-your-teeth-aint-your-own", multi_factor_user=self.mf_user)

        self.mf_user.delete()
        self.assertEqual(MultiFactorToken.objects.all().count(), 0)

    def test_deleting_token_does_not_delete_multi_factor_user(self):
        token = MultiFactorToken.objects.create(code="alright-guvnor", multi_factor_user=self.mf_user)

        token.delete()
        self.assertTrue(MultiFactorAuthenticationUser.objects.filter(user=self.mf_user.user).exists())

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_TOKEN_INVALIDATITY_TIME_SECONDS=86400)
    def test_is_valid_returns_true_if_token_in_database_with_same_code_more_than_x_seconds_ago(self):
        old_token = MultiFactorToken.objects.create(code='fancy-a-run-around', multi_factor_user=self.mf_user)
        old_token.time_added = timezone.now() - datetime.timedelta(seconds=86401)
        old_token.save()
        new_token = MultiFactorToken(code='fancy-a-run-around', multi_factor_user=self.mf_user)

        ret = new_token.is_valid()

        self.assertTrue(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_TOKEN_INVALIDATITY_TIME_SECONDS=86400)
    def test_is_valid_returns_false_if_token_in_database_with_same_code_x_seconds_ago(self):
        old_token = MultiFactorToken.objects.create(code='with-the-chancellor', multi_factor_user=self.mf_user)
        old_token.time_added = timezone.now() - datetime.timedelta(seconds=86400)
        old_token.save()
        new_token = MultiFactorToken(code='with-the-chancellor', multi_factor_user=self.mf_user)

        ret = new_token.is_valid()

        self.assertFalse(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_TOKEN_INVALIDATITY_TIME_SECONDS=86400)
    def test_is_valid_returns_false_if_token_in_database_with_same_code_less_than_x_seconds_ago(self):
        old_token = MultiFactorToken.objects.create(code='olright-mate', multi_factor_user=self.mf_user)
        old_token.time_added = timezone.now() - datetime.timedelta(seconds=86399)
        old_token.save()
        new_token = MultiFactorToken(code='olright-mate', multi_factor_user=self.mf_user)

        ret = new_token.is_valid()

        self.assertFalse(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_TOKEN_INVALIDATITY_TIME_SECONDS=86400)
    def test_is_valid_returns_true_if_code_was_used_by_different_user_within_x_seconds(self):
        other_user = MultiFactorUserFactory()
        old_token = MultiFactorToken.objects.create(code='snag-on-the-barbee', multi_factor_user=other_user)
        old_token.time_added = timezone.now() - datetime.timedelta(seconds=86399)
        old_token.save()
        new_token = MultiFactorToken(code='snag-on-the-barbee', multi_factor_user=self.mf_user)

        ret = new_token.is_valid()

        self.assertTrue(ret)
