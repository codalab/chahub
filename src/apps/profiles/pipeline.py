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


def user_details(user, **kwargs):
    """Update user details using data from provider."""
    backend = kwargs.get('backend')
    response = kwargs.get('response')
    # If we've been passed a user at this point in the pipeline
    if user and backend:
        if backend.name == 'github':
            data = {field: response.get(field) for field in GITHUB_FIELDS}
            data['uid'] = response.get('id')
            GithubUserInfo.objects.update_or_create(user=user, defaults=data)
