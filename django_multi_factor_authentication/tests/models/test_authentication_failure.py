import datetime

import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from libfaketime import fake_time

from django_multi_factor_authentication.models.authentication_failure import AuthenticationFailure


class TestAuthenticationFailure(TestCase):
    def test_username_is_set_to_none_by_default(self):
        authentication_failre = AuthenticationFailure.objects.create(ip='1.2.3.4')
        self.assertIsNone(authentication_failre.username)

    @fake_time("2018-08-20 12:00:00+00:00")
    def test_sets_time_added_to_current_time_by_default(self):
        authentication_failre = AuthenticationFailure.objects.create(ip='1.2.3.4')
        self.assertEqual(authentication_failre.time_added, datetime.datetime.now(tz=pytz.utc))

    def test_username_can_be_none(self):
        # Sometimes people might not want to specifically have a username set to the login failures, but just want
        # to do things based on IP. Of course an empty username '' would also work then, but why limit ourselves?
        AuthenticationFailure.objects.create(ip='1.2.3.4', username=None)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    def test_limit_exceeded_returns_true_if_amount_of_login_failures_for_ip_user_combination_exceeds_x(self):
        AuthenticationFailure.objects.create(ip='1.2.3.4', username='johnny-quid')

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='johnny-quid')

        self.assertTrue(ret)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    def test_limit_exceeded_returns_true_if_amount_of_login_failures_for_ip_exceeds_x(self):
        AuthenticationFailure.objects.create(ip='1.2.3.4', username='mumbles')

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertTrue(ret)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=1)
    def test_limit_exceeded_returns_false_if_amount_of_login_failures_for_ip_user_combination_does_not_exceed_x(self):
        AuthenticationFailure.objects.create(ip='1.2.3.4', username='one-two')

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='one-two')

        self.assertFalse(ret)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=1)
    def test_limit_exceeded_returns_false_if_amount_of_login_failures_for_ip_does_not_exceed_x(self):
        AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertFalse(ret)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=1)
    def test_limit_exceeded_returns_false_if_amount_of_login_failures_for_ip_user_combination_less_than_x(self):
        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='one-two')

        self.assertFalse(ret)

    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=1)
    def test_limit_exceeded_returns_false_if_amount_of_login_failures_for_ip_less_than_x(self):
        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertFalse(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_removes_authentication_failures_exceeding_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2592001)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertFalse(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_does_not_remove_authentication_failures_matching_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2592000)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertTrue(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_does_not_remove_authentication_failures_not_exceeding_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2591999)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4')

        self.assertTrue(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_removes_user_failures_exceeding_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2592001)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='handsome-bob')

        self.assertFalse(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_does_not_remove_user_failures_matching_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2592000)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='handsome-bob')

        self.assertTrue(ret)

    @fake_time("2018-08-20 12:00:00+00:00")
    @override_settings(DMFA_AUTHENTICATION_FAILURE_LIMIT=0)
    @override_settings(DMFA_AUTHENTICATION_FAILURE_RETENTION_TIME_SECONDS=2592000)
    def test_does_not_remove_user_failures_not_exceeding_retention_limit_before_checking_limit_exceeded(self):
        failure = AuthenticationFailure.objects.create(ip='1.2.3.4', username='handsome-bob')
        failure.time_added = timezone.now() - datetime.timedelta(seconds=2591999)
        failure.save()

        ret = AuthenticationFailure.limit_exceeded('1.2.3.4', username='handsome-bob')

        self.assertTrue(ret)
