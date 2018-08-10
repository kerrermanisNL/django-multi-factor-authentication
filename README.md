# django-multi-factor-authentication
Django module for providing multi-factor authentication on your views.


# Settings
All settings for this module are prefixed with the `DMFA_` prefix.

`DMFA_TOKEN_INVALIDATITY_TIME_SECONDS`: Indicates how long a token used to identify a certain user's login attempt 
should remain invalid. Default is 24 hours (86400 seconds). This would prevent cases in, for example, time-based
one-time-password (TOTP) scenarios where a nefarious person could intercept the TOTP code and re-use it quickly after
the original user to gain access to the system.

`DMFA_AUTHENTICATION_TOKEN_VALIDITY_TIME_SECONDS`: Indicates how long an authentication token should remain valid in
seconds. Default is 5 minutes (300 seconds). If a user has not authenticated with a form of multi factor authentication
within this time the user will be redirected back to wherever he came from to let them try again. Could prevent 
situations in which a user walks away from their screen and a nefarious person gains access
to their computer while they are away.


`DMFA_AUTHENTICATION_FAILURE_LIMIT`: Indicates how many authentication failures are allowed to happen before a user/ip
is no longer allowed to authenticate. Depending on the chosen solution this can be remedied by using Google NoCaptcha
for example. Default is 5.
