from profiles.models import GithubUserInfo, LinkedInUserInfo

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

LINKEDIN_FIELDS = [
    'firstName',
    'lastName'
]


def _create_user_data(user, response, backend_name):
    data = {}
    # --------------------------- Github ----------------------
    if backend_name == 'github':
        data['uid'] = response.get('id')
        for field in GITHUB_FIELDS:
            data[field] = response.get(field)
        if not user.github_info:
            new_github_info = GithubUserInfo.objects.create(**data)
            user.github_info = new_github_info
        else:
            # Only update if they're the same remote id
            if user.github_info.github_uid == data['uid']:
                GithubUserInfo.objects.filter(github_uid=data['uid']).update(**data)
    # --------------------------- Docker ----------------------
    elif backend_name == 'docker':
        pass
    elif backend_name == 'linkedin-oauth2':
        data['uid'] = response.get('id')
        for field in LINKEDIN_FIELDS:
            data[field] = response.get(field)
        if not user.linkedin_info:
            new_linkedin_info = LinkedInUserInfo.objects.create(**data)
            user.linkedin_info = new_linkedin_info
        else:
            # Only update if they're the same remote id
            if user.linkedin_info.linkedin_uid == data['uid']:
                LinkedInUserInfo.objects.filter(linkedin_uid=data['uid']).update(**data)
    user.save()


def user_details(user, **kwargs):
    """Update user details using data from provider."""
    backend = kwargs.get('backend')
    response = kwargs.get('response')

    # If we've been passed a user at this point in the pipeline
    if user:
        _create_user_data(user=user, response=response, backend_name=backend.name)
