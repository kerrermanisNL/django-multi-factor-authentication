from unittest.mock import patch
from django.utils import timezone
from django.db import IntegrityError
from django.test import TestCase
from libfaketime import fake_time

from django_multi_factor_authentication.factories.multi_factor_user_factory import MultiFactorUserFactory
from django_multi_factor_authentication.models import MultiFactorAuthenticationUser
from django_multi_factor_authentication.models.multi_factor_authentication_token import MultiFactorAuthenticationToken


class TestAuthenticationToken(TestCase):
    def setUp(self):
        self.mf_user = MultiFactorUserFactory()

    def test_raises_error_if_no_multi_factor_user_supplied(self):
        with self.assertRaises(IntegrityError):
            MultiFactorAuthenticationToken.objects.create()

    def test_deleting_multi_factor_user_deletes_token(self):
        MultiFactorAuthenticationToken.objects.create(code="hooks-is-extra", multi_factor_user=self.mf_user)

        self.mf_user.delete()
        self.assertEqual(MultiFactorAuthenticationToken.objects.all().count(), 0)

    def test_deleting_token_does_not_delete_multi_factor_user(self):
        token = MultiFactorAuthenticationToken.objects.create(code="on-gp", multi_factor_user=self.mf_user)

        token.delete()
        self.assertTrue(MultiFactorAuthenticationUser.objects.filter(user=self.mf_user.user).exists())

    @patch('django_multi_factor_authentication.models.multi_factor_authentication_token.uuid4')
    def test_creates_code_with_default_uuid4_value(self, uuid4):
        uuid4.return_value.hex = 'continuum-transfunctioner'
        token = MultiFactorAuthenticationToken.objects.create(multi_factor_user=self.mf_user)

        self.assertEqual(token.code, uuid4.return_value.hex)

    @fake_time("2018-08-20 12:00:00+00:00")
    def test_time_added_field_is_set_to_current_time_by_default(self):
        token = MultiFactorAuthenticationToken.objects.create(multi_factor_user=self.mf_user)

        self.assertEqual(token.time_added, timezone.now())
