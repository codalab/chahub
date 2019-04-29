from django_elasticsearch_dsl import DocType, Index, fields

from datasets.models import Data

datasets = Index('datasets')
datasets.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# TODO:
# - Include github_info on UserDocument + Set-up to index right

@datasets.doc_type
class DatasetDocument(DocType):
    class Meta:
        model = Data

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
