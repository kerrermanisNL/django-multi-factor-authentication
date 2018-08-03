from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from django_multi_factor_authentication.models.multi_factor_authentication_user import MultiFactorAuthenticationUser


class TestMultiFactorAuthenticationUser(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Geralt')

    def test_gets_created_with_mfa_enabled_false(self):
        user = MultiFactorAuthenticationUser.objects.create(user=self.user)
        self.assertFalse(user.multi_factor_authentication_enabled)

    def test_raises_if_no_user_supplied(self):
        with self.assertRaises(IntegrityError):
            MultiFactorAuthenticationUser.objects.create()

    def test_deletes_mfa_user_if_user_is_deleted(self):
        self.user.delete()

        self.assertEqual(MultiFactorAuthenticationUser.objects.all().count(), 0)

    def test_does_not_delete_user_if_mfa_user_is_deleted(self):
        mfa_user = MultiFactorAuthenticationUser.objects.create(user=self.user)
        mfa_user.delete()

        self.assertTrue(get_user_model().objects.filter(username=self.user.username).exists())
