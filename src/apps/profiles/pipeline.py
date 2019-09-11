from django.contrib.auth import get_user_model
from django.db import IntegrityError
from social_core.pipeline.user import USER_FIELDS

from profiles.models import GithubUserInfo

GITHUB_FIELDS = [
    'login',
    'avatar_url',
    'gravatar_id',
    'html_url',
    'name',
    'company',
    'bio',
    'location',
    'created_at',
    'updated_at',
    'node_id',
    'url',
    'followers_url',
    'following_url',
    'gists_url',
    'starred_url',
    'subscriptions_url',
    'organizations_url',
    'repos_url',
    'events_url',
    'received_events_url'
]

User = get_user_model()


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return
    try:
        user = strategy.create_user(**fields)
    except IntegrityError:
        appended_int = 1
        while User.objects.filter(username=f"{fields['username']}_{appended_int}").exists():
            appended_int += 1
        fields['username'] = f"{fields['username']}_{appended_int}"
        user = strategy.create_user(**fields)
    return {
        'is_new': True,
        'user': user
    }


def user_details(user, **kwargs):
    """Update user details using data from provider."""
    backend = kwargs.get('backend')
    response = kwargs.get('response')
    # Make sure we have a user and a backend
    if user and backend:
        if backend.name == 'github':
            data = {field: response.get(field) for field in GITHUB_FIELDS}
            data['uid'] = response.get('id')
            GithubUserInfo.objects.update_or_create(user=user, defaults=data)
