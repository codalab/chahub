from django_elasticsearch_dsl import DocType, Index, fields

from profiles.models import User, Profile

users = Index('users')
users.settings(
    number_of_shards=1,
    number_of_replicas=0
)

profiles = Index('profiles')
profiles.settings(
    number_of_shards=1,
    number_of_replicas=0
)


# TODO:
# - Include github_info on UserDocument + Set-up to index right

@users.doc_type
class UserDocument(DocType):
    class Meta:
        model = User

    username = fields.TextField()
    date_joined = fields.DateField()
    is_active = fields.BooleanField()
    is_staff = fields.BooleanField()

    github_info = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'uid': fields.IntegerField(),
        'login': fields.TextField(),  # username
        'avatar_url': fields.TextField(),
        'gravatar_id': fields.TextField(),
        'html_url': fields.TextField(),  # Profile URL
        'name': fields.TextField(),
        'company': fields.TextField(),
        'bio': fields.TextField(),
        'location': fields.TextField(),
        'created_at': fields.DateField(),
        'updated_at': fields.DateField(),
        'node_id': fields.TextField(),
        'url': fields.TextField(),  # Base API URL
        'followers_url': fields.TextField(),
        'following_url': fields.TextField(),
        'gists_url': fields.TextField(),
        'starred_url': fields.TextField(),
        'subscriptions_url': fields.TextField(),
        'organizations_url': fields.TextField(),
        'repos_url': fields.TextField(),
        'events_url': fields.TextField(),
        'received_events_url': fields.TextField()
    })

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'user'


@profiles.doc_type
class ProfileDocument(DocType):
    class Meta:
        model = Profile

    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })
    # remote_id = fields.IntegerField()
    remote_id = fields.TextField
    email = fields.TextField()
    username = fields.TextField()

    user = fields.ObjectField(properties={
        'username': fields.TextField(),
        'email': fields.TextField(),
        'name': fields.TextField(),
        'github_info': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'uid': fields.IntegerField(),
            'login': fields.TextField(),  # username
            'avatar_url': fields.TextField(),
            'gravatar_id': fields.TextField(),
            'html_url': fields.TextField(),  # Profile URL
            'name': fields.TextField(),
            'company': fields.TextField(),
            'bio': fields.TextField(),
            'location': fields.TextField(),
            'created_at': fields.DateField(),
            'updated_at': fields.DateField(),
            'node_id': fields.TextField(),
            'url': fields.TextField(),  # Base API URL
            'followers_url': fields.TextField(),
            'following_url': fields.TextField(),
            'gists_url': fields.TextField(),
            'starred_url': fields.TextField(),
            'subscriptions_url': fields.TextField(),
            'organizations_url': fields.TextField(),
            'repos_url': fields.TextField(),
            'events_url': fields.TextField(),
            'received_events_url': fields.TextField()
        })

        # 'docker_info':,
        # 'linkedin_info':,
    })

    organized_competitions_count = fields.IntegerField()
    datasets_count = fields.IntegerField()
    tasks_count = fields.IntegerField()
    solutions_count = fields.IntegerField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'profile'

    def prepare_organized_competitions_count(self, instance):
        return instance.organized_competitions.count() if instance.organized_competitions else 0

    def prepare_datasets_count(self, instance):
        return instance.datasets.count() if instance.datasets else 0

    def prepare_tasks_count(self, instance):
        return instance.tasks.count() if instance.tasks else 0

    def prepare_solutions_count(self, instance):
        return instance.solutions.count() if instance.solutions else 0
