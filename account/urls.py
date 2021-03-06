from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from account import views

urlpatterns = patterns(
    '',
    url(
        r'^signup/$',
        views.Signup.as_view(),
        name='signup'
    ),
    url(
        r'^activate/retry/(?P<activation_key>\w+)/$',
        views.ActivationRetry.as_view(),
        name='activate_retry'
    ),
    url(
        r'^activate/resend/$',
        views.ActivationResend.as_view(),
        name='activate_resend'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        views.Activation.as_view(),
        name='activate'
    ),
    url(
        r'^signin/$',
        views.Signin.as_view(),
        name='signin'
    ),
    url(
        r'^signin/(?P<backend>[^/]+)/$',
        views.SigninFacebook.as_view(),
        name='signin_social'
    ),
    url(
        r'^signout/$',
        views.Signout.as_view(),
        name='signout'
    ),
    url(
        r'^email/$',
        views.EmailChange.as_view(),
        name='email_change'
    ),
    url(
        r'^confirm-email/(?P<confirmation_key>\w+)/$',
        views.EmailConfirm.as_view(),
        name='email_confirm'
    ),
    url(
        r'^password/set/$',
        views.PasswordSetSocial.as_view(),
        name='password_set'
    ),
    url(
        r'^password/reset/$',
        views.PasswordReset.as_view(),
        name='password_reset'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.PasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^password/$',
        views.PasswordChange.as_view(),
        name='password_change'
    ),
    url(
        r'^profile/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
