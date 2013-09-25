# -*- coding: utf-8 -*-
import time

from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse

from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import (AuthFailed, AuthCanceled, AuthUnknownError,
                                    AuthTokenError, AuthMissingParameter,
                                    AuthAlreadyAssociated,
                                    WrongBackend, NotAllowedToDisconnect,
                                    StopPipeline, AuthStateMissing,
                                    AuthStateForbidden, AuthTokenRevoked)

from urllib2 import urlopen, HTTPError, URLError


def get_avatars(backend, details, response, user=None, is_new=False,
                *args, **kwargs):
    """Update user details using data from provider."""
    if user is None:
        return
    changed = False  # flag to track changes

    try:
        url = None
        if backend.name == 'facebook' and "id" in response:
            url = "http://graph.facebook.com/%s/picture?type=large" \
                  % response["id"]

        elif backend.name == 'twitter':
            url = response.get('profile_image_url', '').replace('_normal', '')

        elif backend.name == 'google-oauth2' and "picture" in response:
            url = response["picture"]

        elif backend.name == 'linkedin' and "picture-url" in response:
            url = response["picture-url"]

        if url:
            avatar = urlopen(url)
            image_basename = slugify(user.username + " social")
            image_name = '%s%s.jpg' % (int(time.time()), image_basename)
            user.avatar.save(image_name, ContentFile(avatar.read()))
            changed = True

    except URLError, HTTPError:
        pass

    if changed:
        user.save()


class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):

    def get_redirect_uri(self, request, exception):
        url = None
        if type(exception) in [AuthFailed, AuthCanceled, AuthUnknownError,
                               AuthTokenError, AuthMissingParameter,
                               AuthAlreadyAssociated,
                               WrongBackend, NotAllowedToDisconnect,
                               StopPipeline, AuthStateMissing,
                               AuthStateForbidden, AuthTokenRevoked]:
            url = reverse('login_error') + '?error=%s' % type(exception).__name__
        if url:
            return url
        else:
            return super(CustomSocialAuthExceptionMiddleware, self)\
                         .get_redirect_uri(request, exception)
