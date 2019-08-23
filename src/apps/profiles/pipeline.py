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


def _handle_external_user_data(user, data, response, fields_list, data_field_name, data_model):
    data['uid'] = response.get('id')
    for field in fields_list:
        data[field] = response.get(field)
    object, created = data_model.objects.get_or_create(user=user, defaults=data)
    if not created:
        data_model.objects.filter(pk=object.pk).update(**data)
    user.save()


def _create_user_data(user, response, backend_name):
    data = {}
    # --------------------------- Github ----------------------
    if backend_name == 'github':
        _handle_external_user_data(user=user, data=data, response=response, fields_list=GITHUB_FIELDS,
                                   data_field_name='github_info', data_model=GithubUserInfo)
    # --------------------------- Docker ----------------------
    elif backend_name == 'docker':
        pass
    elif backend_name == 'linkedin-oauth2':
        _handle_external_user_data(user=user, data=data, response=response, fields_list=LINKEDIN_FIELDS,
                                   data_field_name='linkedin_info', data_model=LinkedInUserInfo)


def user_details(user, **kwargs):
    """Update user details using data from provider."""
    backend = kwargs.get('backend')
    response = kwargs.get('response')

    # If we've been passed a user at this point in the pipeline
    if user:
        _create_user_data(user=user, response=response, backend_name=backend.name)
