from rest_framework import serializers
from api.serializers.mixins import BulkSerializerMixin
from api.serializers.producers import ProducerSerializer
from datasets.models import Data, DataGroup


class DataSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    # producer = ProducerSerializer(required=False, validators=[])

    class Meta:
        model = Data
        fields = [
            'creator_id',
            'remote_id',
            'producer',
            'user',
            'name',
            'type',
            'description',
            'is_public'
        ]
        read_only_fields = (
            'owner',
            'key',
            'created_by',
            'created_when',
            'uploaded_when'
        )


class DataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGroup
        fields = [
            'created_by',
            'created_when',
            'name',
            'datas'
        ]
