from rest_framework import serializers

from api.serializers.producers import ProducerSerializer
from competitions.models import Competition, Phase, Submission


class CompetitionSerializer(serializers.ModelSerializer):
    # Stop the "uniqueness" validation, we want to be able to update already
    # existing models
    # Also, Producer in this case comes from serializer context
    producer = ProducerSerializer(required=False, validators=[])

    class Meta:
        model = Competition
        fields = (
            'id',
            'remote_id',
            'title',
            'producer',
        )
        validators = []
        extra_kwargs = {
            'producer': {
                'validators': [],
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set producer here... is there a nicer way to do this, like via kwargs?
        if 'producer' in kwargs['context']:
            self.fields['producer'].default = kwargs['context']['producer']

    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        Competition.objects.update_or_create(
            remote_id=validated_data.pop('remote_id'),
            producer=validated_data.pop('producer'),
            defaults=validated_data
        )


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ('competition',)


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('phase',)
