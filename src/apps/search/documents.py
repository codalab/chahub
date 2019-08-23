from django_elasticsearch_dsl import DocType, Index, fields

from competitions.models import Competition
from datasets.models import Data
from profiles.models import User, Profile
from tasks.models import Task, Solution

chahub_index = Index('chahub')
chahub_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@chahub_index.doc_type
class CompetitionDocument(DocType):
    class Meta:
        model = Competition

    class Index:
        name = 'chahub'

    remote_id = fields.IntegerField
    created_by = fields.TextField()
    title = fields.TextField()
    description = fields.TextField()
    html_text = fields.TextField()

    participant_count = fields.IntegerField()
    is_active = fields.BooleanField()
    prize = fields.IntegerField()
    current_phase_deadline = fields.DateField()
    url = fields.TextField()
    logo_url = fields.TextField()
    logo = fields.TextField()

    start = fields.DateField()
    end = fields.DateField()

    published = fields.BooleanField()

    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'competition'

    def prepare_logo(self, instance):
        return instance.logo.url if instance.logo else ''


@chahub_index.doc_type
class DatasetDocument(DocType):
    class Meta:
        model = Data

    class Index:
        name = 'chahub'

    creator_id = fields.IntegerField()
    remote_id = fields.IntegerField()

    created_by = fields.TextField()

    created_when = fields.DateField()
    uploaded_when = fields.DateField()

    name = fields.TextField()
    type = fields.TextField()
    description = fields.TextField()
    key = fields.TextField()

    is_public = fields.BooleanField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'dataset'

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""


@chahub_index.doc_type
class UserDocument(DocType):
    class Meta:
        model = User

    class Index:
        name = 'chahub'

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

    organized_competitions_count = fields.IntegerField()
    datasets_count = fields.IntegerField()
    tasks_count = fields.IntegerField()
    solutions_count = fields.IntegerField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'user'


@chahub_index.doc_type
class ProfileDocument(DocType):
    class Meta:
        model = Profile

    class Index:
        name = 'chahub'

    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })
    remote_id = fields.IntegerField()
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
        return instance.organized_competitions.count()

    def prepare_datasets_count(self, instance):
        return instance.datasets.count()

    def prepare_tasks_count(self, instance):
        return instance.tasks.count()

    def prepare_solutions_count(self, instance):
        return instance.solutions.count()


@chahub_index.doc_type
class TaskDocument(DocType):
    class Meta:
        model = Task

    class Index:
        name = 'chahub'

    creator_id = fields.IntegerField()
    remote_id = fields.IntegerField

    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    name = fields.TextField()
    description = fields.TextField()
    key = fields.TextField()

    created_by = fields.TextField()

    created_when = fields.DateField()
    uploaded_when = fields.DateField()

    is_public = fields.BooleanField()

    remote_ingestion_program = fields.IntegerField()

    remote_input_data = fields.TextField()

    ingestion_only_during_scoring = fields.BooleanField()

    remote_reference_data = fields.TextField()

    remote_scoring_program = fields.TextField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'task'

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""


@chahub_index.doc_type
class SolutionDocument(DocType):
    class Meta:
        model = Solution

    class Index:
        name = 'chahub'

    creator_id = fields.IntegerField()
    remote_id = fields.IntegerField

    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    # These fields come from datasets. Should we just have this be an (ObjectField?) to Datasets?
    name = fields.TextField()
    description = fields.TextField()
    key = fields.TextField()

    created_by = fields.TextField()

    uploaded_when = fields.DateField()

    is_public = fields.BooleanField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'solution'

    def prepare_created_by(self, instance):
        return instance.created_by
