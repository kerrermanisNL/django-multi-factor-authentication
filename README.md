# django-multi-factor-authentication
Django module for providing multi-factor authentication on your views.


# Settings
All settings for this module are prefixed with the `DMFA_` prefix.

`DMFA_TOKEN_INVALIDATITY_TIME_SECONDS`: Indicates how long a token used to identify a certain user's login attempt 
should remain invalid. Default is 24 hours (86400 seconds). This would prevent cases in, for example, time-based
one-time-password (TOTP) scenarios where a nefarious person could intercept the TOTP code and re-use it quickly after
the original user to gain access to the system.
