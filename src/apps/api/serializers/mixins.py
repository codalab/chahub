from rest_framework.exceptions import ValidationError


class ProducerValidationSerializerMixin():
    def get_unique_together_validators(self):
        '''
        Overriding method to disable unique together checks
        '''
        return []

    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """
        remote_id = validated_data.pop('remote_id', None)
        producer = validated_data.pop('producer', None)
        if not remote_id or not producer:
            raise self.Meta.model.DoesNotExist("Producer and or remote_id are None!")
        instance, _ = self.Meta.model.objects.update_or_create(
            remote_id=remote_id,
            producer=producer,
            defaults=validated_data
        )
        return instance

    def validate_producer(self, producer):
        context_producer = self.context.get(producer)
        if context_producer:
            return context_producer

        if not producer:
            raise ValidationError("Producer not found when creating data entry")
        return producer
