from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.serializers.producers import ProducerSerializer
from datasets.models import Data, DataGroup


class DataSerializer(WritableNestedModelSerializer):
    producer = ProducerSerializer(required=False)
    tasks_using = serializers.SerializerMethodField()

    class Meta:
        model = Data
        fields = (
            'id',
            'creator_id',
            'remote_id',
            'created_by',
            'created_when',
            'name',
            'type',
            'description',
            'key',
            'is_public',
            'producer',
            'tasks_using',
        )

    def get_tasks_using(self, instance):
        from api.serializers.tasks import TaskSimpleSerializer
        # TODO Figure out a way to break up this giant line
        qs = instance.task_ingestion_programs.all() | instance.task_scoring_programs.all() | instance.task_reference_datas.all() | instance.task_input_datas.all()
        return [task if task['is_public'] else {'is_public': False} for task in
                TaskSimpleSerializer(qs, many=True).data]

    def create(self, validated_data):
        obj, created = Data.objects.update_or_create(
            remote_id=validated_data.pop('remote_id'),
            producer=self.context['request'].user,
            defaults=validated_data
        )
        return obj


class DataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGroup
        fields = (
            'created_by',
            'created_when',
            'name',
            'datas',
        )
