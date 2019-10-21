from django.conf import settings
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.serializers.mixins import ChaHubWritableNestedSerializer
from datasets.models import Data, DataGroup


class DataSerializer(ChaHubWritableNestedSerializer):
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
        )


class DataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGroup
        fields = (
            'created_by',
            'created_when',
            'name',
            'datas',
        )
