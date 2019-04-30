from rest_framework.exceptions import ValidationError

from api.serializers.producers import ProducerSerializer


class BulkSerializerMixin(object):

    producer = ProducerSerializer(required=False, validators=[])

    def get_unique_together_validators(self):
        '''
        Overriding method to disable unique together checks
        '''
        return []

    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """

        try:
            # If we have an existing instance from this producer
            # with the same remote_id, update it instead of making a new one
            instance = self.Meta.model.objects.get(
                remote_id=validated_data.get('remote_id'),
                producer=validated_data.get('producer')
            )
            return self.update(instance, validated_data)
        except self.Meta.model.DoesNotExist:
            new_instance = super().create(validated_data)
            return new_instance
