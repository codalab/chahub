from django.conf import settings
from rest_framework import serializers

from api.serializers.mixins import BulkSerializerMixin
from datasets.models import Data, DataGroup


class DataSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    # data_file = FileField(allow_empty_file=False)

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

    # def get_unique_together_validators(self):
    #     '''
    #     Overriding method to disable unique together checks
    #     '''
    #     return []
    #
    # def create(self, validated_data):
    #     """
    #     This creates *AND* updates based on the combination of (remote_id, producer)
    #     """
    #
    #     try:
    #         # If we have an existing instance from this producer
    #         # with the same remote_id, update it instead of making a new one
    #         instance = Data.objects.get(
    #             remote_id=validated_data.get('remote_id'),
    #             producer=validated_data.get('producer')
    #         )
    #         return self.update(instance, validated_data)
    #     except Data.DoesNotExist:
    #         new_instance = super().create(validated_data)
    #         return new_instance

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #
    #     # Should only be changing data_file if we're using local storage!!!
    #
    #     # Fix the URL, should be the full URL with correct path
    #     upload_path = '{}{}'.format(settings.MEDIA_URL, instance.data_file)
    #     representation["data_file"] = self.context['request'].build_absolute_uri(upload_path)
    #
    #     return representation

    # def create(self, validated_data):
    #     validated_data["created_by"] = self.context['request'].user
    #     return super().create(validated_data)


class DataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGroup
        fields = [
            'created_by',
            'created_when',
            'name',
            'datas'
        ]
