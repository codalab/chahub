from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.serializers.data import DataSerializer
from api.serializers.mixins import ChaHubWritableNestedSerializer
from tasks.models import Task, Solution

TASK_DATA_FIELDS = [
    'ingestion_program',
    'input_data',
    'reference_data',
    'scoring_program',
]


class TaskSerializer(serializers.ModelSerializer):
    ingestion_program = DataSerializer(required=False)
    input_data = DataSerializer(required=False)
    scoring_program = DataSerializer(required=False)
    reference_data = DataSerializer(required=False)

    class Meta:
        model = Task
        fields = (
            'remote_id',
            'producer',
            'created_by',
            'creator_id',
            'created_when',
            'name',
            'description',
            'key',
            'is_public',
            'ingestion_program',
            'input_data',
            'ingestion_only_during_scoring',
            'reference_data',
            'scoring_program',
        )


class TaskCreationSerializer(ChaHubWritableNestedSerializer):
    ingestion_program = DataSerializer(required=False)
    input_data = DataSerializer(required=False)
    scoring_program = DataSerializer(required=False)
    reference_data = DataSerializer(required=False)

    class Meta:
        model = Task
        fields = (
            'producer',
            'id',
            'remote_id',
            'created_by',
            'creator_id',
            'created_when',
            'name',
            'description',
            'key',
            'is_public',
            'ingestion_program',
            'input_data',
            'ingestion_only_during_scoring',
            'reference_data',
            'scoring_program',
        )

    # def create(self, validated_data):
    #     print(validated_data)
    #     solution = validated_data.pop('solution', None)
    #     for field in TASK_DATA_FIELDS:
    #         data = validated_data.get(field)
    #         if data:
    #             serializer = DataSerializer(data=data, context=self.context)
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()
    #             validated_data[field] = serializer.data['id']
    #
    #     print(validated_data)
    #     obj, created = Task.objects.update_or_create(
    #         producer=self.context['request'].user,
    #         remote_id=validated_data.pop('remote_id'),
    #         defaults=validated_data
    #     )
    #
    #     if solution:
    #         serializer = SolutionCreationSerializer(data=solution, context=self.context)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     return obj


class SolutionCreationSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Solution
        fields = (
            'remote_id',
        )
