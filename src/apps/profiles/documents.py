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
    is_active = fields.BooleanField
    is_staff = fields.BooleanField

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

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'profile'