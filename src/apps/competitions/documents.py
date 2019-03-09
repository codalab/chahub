from django_elasticsearch_dsl import DocType, Index, fields

from profiles.models import User
from .models import Competition

competitions = Index('competitions')
competitions.settings(
    number_of_shards=1,
    number_of_replicas=0
)

users = Index('users')
users.settings(
    number_of_shards=1,
    number_of_replicas=0
)


# class ModelDocMixin():
#     """
#     This mixin provides some utility function for documents,
#     simplifying access to related model information.
#     """
#     @property
#     def pk(self):
#         return self.meta["id"]
#
#     def get_model_class(self):
#         # return self.get_queryset().model
#         return self._doc_type.model
#
#     def get_model_instance(self):
#         return self.get_queryset().get(pk=self.pk)


@users.doc_type
class UserDocument(DocType):
    class Meta:
        model = User

    github_uid = fields.TextField()
    avatar_url = fields.TextField()
    url = fields.TextField()
    html_url = fields.TextField()
    name = fields.TextField()
    company = fields.TextField()
    bio = fields.TextField()
    username = fields.TextField()
    # email = fields.TextField()
    date_joined = fields.DateField()
    is_active = fields.BooleanField
    is_staff = fields.BooleanField

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'user'


@competitions.doc_type
class CompetitionDocument(DocType):
    class Meta:
        model = Competition

    remote_id = fields.TextField()
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

    # TODO: add "active" boolean field so we can add this to queries and not have a special case

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""

    def prepare_logo(self, instance):
        return instance.logo.url if instance.logo else ''
