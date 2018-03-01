from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.producers import ProducerSerializer
from competitions.models import Competition, Phase, Submission, CompetitionParticipant


class CompetitionParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionParticipant
        fields = ('competition', 'user')


class PhaseSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Phase
        fields = (
            'id',
            # 'competition',
            'index',
            'start',
            'end',
            'name',
            'description',
            'is_active',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('phase',)


class CompetitionSerializer(WritableNestedModelSerializer):
    # Stop the "uniqueness" validation, we want to be able to update already
    # existing models
    # Also, Producer in this case comes from serializer context
    producer = ProducerSerializer(required=False, validators=[])
    phases = PhaseSerializer(many=True)
    participants = CompetitionParticipantSerializer(many=True, read_only=True)
    admins = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = (
            'id',
            'remote_id',
            'title',
            'producer',
            'created_by',
            'created_when',
            'logo',
            'url',
            'phases',
            'participants',
            'description',
            'end',
            'admins',
            'is_active',
            'get_active_phase_end',
            'participant_count',
            'deadline',
            'start_date',
            'html_text',
            'phase_deadlines'
        )
        validators = []
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set producer here... is there a nicer way to do this, like via kwargs?
        # if 'context' in kwargs and 'producer' in kwargs['context']:
            # self.fields['producer'].default = kwargs['context']['producer']
            # self.initial_data["producer"] = kwargs["context"]["producer"]

    def create(self, validated_data):
        try:
            temp_instance = Competition.objects.get(remote_id=validated_data['remote_id'],
                                                    producer__id=self.context['producer'].id)
        except ObjectDoesNotExist:
            temp_instance = None
        # If we have an existing instance from this producer
        #  with the same remote_id, update it instead of making a new one
        if temp_instance:
            # Return the updated instance
            return self.update(temp_instance, validated_data)
        else:
            # Get the new instance
            new_instance = super(CompetitionSerializer, self).create(validated_data)
            # Set the producer
            new_instance.producer = self.context['producer']
            # Save it again and return it
            new_instance.save()
            return new_instance

    def validate_producer(self, producer):
        context_producer = self.context.get(producer)
        if context_producer:
            return context_producer

        if not producer:
            raise ValidationError("Producer not found when creating data entry")
        return producer

    # def save(self, **kwargs):
    #     data = dict(self.validated_data.items(), **kwargs)
    #     super().save(**data)
    #
    #     Competition.objects.update_or_create(
    #         remote_id=data.pop('remote_id'),
    #         producer=data.pop('producer'),
    #         defaults=data
    #     )
