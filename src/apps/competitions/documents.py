from django_elasticsearch_dsl import DocType, Index, fields

from .models import Competition

competitions = Index('competitions')
competitions.settings(
    number_of_shards=1,
    number_of_replicas=0
)


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

    # TODO: add "active" boolean field so we can add this to queries and not have a special case

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""

    def prepare_logo(self, instance):
        return instance.logo.url if instance.logo else ''
