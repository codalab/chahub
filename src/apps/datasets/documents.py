from django_elasticsearch_dsl import DocType, Index, fields

from datasets.models import Data

data = Index('data')
data.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@data.doc_type
class DataDocument(DocType):
    class Meta:
        model = Data

    created_by = fields.TextField()
    created_when = fields.DateField()
    name = fields.TextField()
    type = fields.TextField()
    description = fields.TextField()
    key = fields.TextField()
    is_public = fields.BooleanField()

    def prepare_created_by(self, instance):
        return instance.created_by
