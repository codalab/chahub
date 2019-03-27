from django_elasticsearch_dsl import DocType, Index, fields

from tasks.models import Task, Solution

tasks = Index('tasks')
tasks.settings(
    number_of_shards=1,
    number_of_replicas=0
)

solutions = Index('solutions')
solutions.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# TODO:
# - Should we be indexing the actual related objects for ingestion/scoring? Or how should that work out?
#   * Would that search fields such as name/description?

@tasks.doc_type
class TaskDocument(DocType):
    class Meta:
        model = Task

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
    # ingestion_program = fields.TextField()

    remote_input_data = fields.TextField()
    # input_data = fields.TextField()

    ingestion_only_during_scoring = fields.BooleanField()

    remote_reference_data = fields.TextField()
    # reference_data = fields.TextField()

    remote_scoring_program = fields.TextField()
    # scoring_program = fields.TextField()

    _obj_type = fields.TextField()

    def prepare__obj_type(self, instance):
        return 'task'

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""


@solutions.doc_type
class SolutionDocument(DocType):
    class Meta:
        model = Solution

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

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""
