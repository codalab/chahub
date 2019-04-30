from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.mixins import BulkSerializerMixin
from api.serializers.producers import ProducerSerializer
from datasets.models import Data, DataGroup


class DataSerializer(BulkSerializerMixin, serializers.ModelSerializer):
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

    def validate_producer(self, producer):
        context_producer = self.context.get(producer)
        if context_producer:
            return context_producer

        if not producer:
            raise ValidationError("Producer not found when creating data entry")
        return producer


class DataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGroup
        fields = [
            'created_by',
            'created_when',
            'name',
            'datas'
        ]
