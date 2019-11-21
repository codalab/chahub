from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested import WritableNestedModelSerializer


class ChaHubWritableNestedSerializer(WritableNestedModelSerializer):
    """
    Extending create() and update() of WritableNested so that we correctly call update when needed on Post requests
    and so we can pass request.user as producer.
    """
    def create(self, validated_data):
        validated_data['producer'] = self.context['request'].user
        try:
            obj = self.Meta.model.objects.get(
                remote_id=validated_data['remote_id'],
                producer=validated_data['producer']
            )
            return self.update(obj, validated_data)
        except ObjectDoesNotExist:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['producer'] = self.context['request'].user
        return super().update(instance, validated_data)
