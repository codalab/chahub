from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.serializers.producers import ProducerSerializer
from datasets.models import Data, DataGroup


class DataSerializer(WritableNestedModelSerializer):
    producer = ProducerSerializer(required=False)

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
            'download_url',
        )

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
