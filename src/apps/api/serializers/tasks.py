from django.conf import settings
from rest_framework import serializers

from tasks.models import Task, Solution

class TaskSerializer(serializers.ModelSerializer):
    # data_file = FileField(allow_empty_file=False)

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


class SolutionSerializer(serializers.ModelSerializer):

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
