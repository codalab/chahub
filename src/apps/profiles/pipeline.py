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


def _handle_external_user_data(user, response, fields_list, data_model):
    data = {
        'uid': response.get('id')
    }
    for field in fields_list:
        data[field] = response.get(field)
    instance, created = data_model.objects.update_or_create(user=user, defaults=data)


def _create_user_data(user, response, backend_name):
    # --------------------------- Github ----------------------
    if backend_name == 'github':
        _handle_external_user_data(
            user=user,
            response=response,
            fields_list=GITHUB_FIELDS,
            data_model=GithubUserInfo
        )
    # --------------------------- Docker ----------------------
    elif backend_name == 'docker':
        pass
    # --------------------------- LinkedIn ----------------------
    elif backend_name == 'linkedin-oauth2':
        _handle_external_user_data(
            user=user,
            response=response,
            fields_list=LINKEDIN_FIELDS,
            data_model=LinkedInUserInfo
        )


def user_details(user, **kwargs):
    """Update user details using data from provider."""
    backend = kwargs.get('backend')
    response = kwargs.get('response')

    # If we've been passed a user at this point in the pipeline
    if user:
        _create_user_data(user=user, response=response, backend_name=backend.name)
