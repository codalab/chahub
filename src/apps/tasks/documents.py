from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from tasks.models import Task


@registry.register_document
class TaskDocument(Document):
    hidden = fields.BooleanField()
    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    class Index:
        name = 'tasks'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Task
        fields = (
            'remote_id',
            'created_by',
            'created_when',
            'name',
            'description',
            # 'key',
            'is_public',
        )

    def prepare_hidden(self, instance):
        return not instance.is_public
