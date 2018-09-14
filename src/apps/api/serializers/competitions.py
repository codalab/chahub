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
    competition = serializers.IntegerField(min_value=1, write_only=True, required=True)
    phase_index = serializers.IntegerField(min_value=1, write_only=True, required=True)

    class Meta:
        model = Submission
        fields = (
            'remote_id',
            'competition',  # on write only
            'phase_index',  # on write this is the phase index within the competition, NOT a PK
            'submitted_at',
            'participant',
        )

    def validate(self, attrs):
        competition = Competition.objects.get(
            remote_id=attrs.pop('competition'),
            producer=self.context.get('producer')
        )
        attrs['phase'] = competition.phases.get(index=attrs.pop('phase_index'))
        return attrs

    def create(self, validated_data):
        instance, _ = Submission.objects.update_or_create(
            remote_id=validated_data.pop('remote_id'),
            phase=validated_data.pop('phase'),
            defaults=validated_data
        )
        return instance


class CompetitionSerializer(WritableNestedModelSerializer):
    # Stop the "uniqueness" validation, we want to be able to update already
    # existing models
    # Also, Producer in this case comes from serializer context
    producer = ProducerSerializer(required=False, validators=[])
    phases = PhaseSerializer(required=False, many=True)
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
            'start',
            'logo',
            'url',
            'phases',
            'participants',
            'description',
            'end',
            'admins',
            'is_active',
            # 'get_active_phase_end',
            'participant_count',
            'html_text',
            'current_phase_deadline',
            'prize',
            'published'
        )
        validators = []
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }

    def validate_description(self, description):
        if description:
            description = description.replace("<p>", "").replace("</p>", "")
        return description

    def validate_producer(self, producer):
        context_producer = self.context.get(producer)
        if context_producer:
            return context_producer

        if not producer:
            raise ValidationError("Producer not found when creating data entry")
        return producer

    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """
        try:
            temp_instance = Competition.objects.get(
                remote_id=validated_data.get('remote_id'),
                producer__id=self.context['producer'].id
            )
        except ObjectDoesNotExist:
            temp_instance = None

        if temp_instance:
            # If we have an existing instance from this producer
            # with the same remote_id, update it instead of making a new one
            return self.update(temp_instance, validated_data)
        else:
            new_instance = super().create(validated_data)
            new_instance.producer = self.context['producer']
            new_instance.save()
            return new_instance