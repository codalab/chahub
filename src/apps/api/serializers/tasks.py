from rest_framework import serializers

from api.serializers.data import DataSerializer
from api.serializers.mixins import ChaHubWritableNestedSerializer
from api.serializers.producers import ProducerSerializer
from datasets.models import Data
from tasks.models import Task, Solution


class TaskSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer(required=False)
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


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'remote_id',
            'name',
            'is_public',
        )


class SolutionCreationSerializer(ChaHubWritableNestedSerializer):
    producer = ProducerSerializer(required=False)
    data = DataSerializer(required=False, allow_null=True)

    class Meta:
        model = Solution
        fields = (
            'remote_id',
            'producer',
            'data',
            'name',
            'description',
            'key',
            'producer',
        )

    def create(self, validated_data):
        producer = self.context['request'].user
        data = validated_data.pop('data')
        if data:
            obj, created = Data.objects.update_or_create(
                remote_id=data.pop('remote_id'),
                producer=producer,
                defaults=data
            )
            validated_data['data'] = obj
        obj, created = Solution.objects.update_or_create(
            remote_id=validated_data.pop('remote_id'),
            producer=producer,
            defaults=validated_data
        )
        return obj


class TaskCreationSerializer(ChaHubWritableNestedSerializer):
    ingestion_program = DataSerializer(required=False, allow_null=True)
    input_data = DataSerializer(required=False, allow_null=True)
    scoring_program = DataSerializer(required=False, allow_null=True)
    reference_data = DataSerializer(required=False, allow_null=True)
    solutions = SolutionCreationSerializer(required=False, allow_null=True, many=True)

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
            'solutions'
        )

    def create(self, validated_data):
        solutions = validated_data.pop('solutions')
        serializer = SolutionCreationSerializer(data=solutions, context=self.context, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super().create(validated_data)
