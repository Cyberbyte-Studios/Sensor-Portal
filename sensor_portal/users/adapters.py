# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.signals import user_signed_up


class AccountAdapter(DefaultAccountAdapter):
    def login(self, request, user):
        # Require two-factor authentication if it has been configured.
        if user.totpdevice_set.filter(confirmed=True).all():
            request.session['allauth_2fa_user_id'] = user.id
            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(
                    reverse('two-factor-authenticate')
                )
            )

        # Otherwise defer to the original allauth adapter.
        return super(AccountAdapter, self).login(request, user)

    def is_open_for_signup(self, request):
        if getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True) is False:
            return False

        if hasattr(request, 'session') and request.session.get(
                'account_verified_email'):
            return True
        elif getattr(settings, 'INVITATION_ONLY', False):
            # Site is ONLY open for invites
            return False
        # Site is open to signup
        return True

    def get_user_signed_up_signal(self):
        return user_signed_up


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True) and getattr(settings, 'INVITATION_ONLY', True)
