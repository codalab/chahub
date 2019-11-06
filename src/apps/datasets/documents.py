from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from datasets.models import Data


@registry.register_document
class DataDocument(Document):
    hidden = fields.BooleanField()
    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    class Index:
        name = 'data'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Data
        fields = (
            'id',
            'created_by',
            'created_when',
            'name',
            'type',
            'description',
            # 'key',
            'is_public',
        )

    def prepare_hidden(self, instance):
        return not instance.is_public
