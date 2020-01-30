from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Competition


@registry.register_document
class CompetitionDocument(Document):
    hidden = fields.BooleanField()
    participant_count = fields.IntegerField()
    producer = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'url': fields.TextField(),
        'name': fields.TextField()
    })

    class Index:
        name = 'competitions'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Competition
        fields = (
            'id',
            'remote_id',
            'created_by',
            'title',
            'description',
            'html_text',
            'is_active',
            'prize',
            'url',
            'logo_url',
            'logo',
            'start',
            'end',
            'published',
        )

    # TODO: add "active" boolean field so we can add this to queries and not have a special case

    def prepare_hidden(self, instance):
        return not instance.published or instance.deleted

    def prepare_logo(self, instance):
        return instance.logo.url if instance.logo else ''

    def prepare_participant_count(self, instance):
        return instance.participants.count()
