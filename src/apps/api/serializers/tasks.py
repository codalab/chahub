from rest_framework import serializers

from api.serializers.mixins import BulkSerializerMixin
from api.serializers.producers import ProducerSerializer
from tasks.models import Task, Solution


class TaskSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    producer = ProducerSerializer(required=False, validators=[])

    class Meta:
        model = Task
        fields = [
            'creator_id',
            'remote_id',
            'producer',
            'name',
            'description',
            'user',
            'is_public',
            'ingestion_program',
            'input_data',
            'ingestion_only_during_scoring',
            'reference_data',
            'scoring_program'
        ]
        read_only_fields = [
            'owner',
            'key',
            'created_by',
            'created_when',
            'uploaded_when',
        ]


class SolutionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    producer = ProducerSerializer(required=False, validators=[])
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Solution
        fields = [
            'creator_id',
            'remote_id',
            'user',
            'created_by',
            'producer',
            'key',
            'uploaded_when',
            'tasks',
            'data',
            'is_public'
        ]
