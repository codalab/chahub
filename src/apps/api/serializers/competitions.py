from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.mixins import ChaHubWritableNestedSerializer
from api.serializers.producers import ProducerSerializer
from api.serializers.tasks import TaskCreationSerializer, TaskSerializer
from competitions.models import Competition, Phase, Submission, CompetitionParticipant
from competitions.tasks import download_competition_image


class CompetitionParticipantSerializer(ChaHubWritableNestedSerializer):
    class Meta:
        model = CompetitionParticipant
        fields = (
            'remote_id',
            'user',
            'status',
        )


class PhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = (
            'id',
            'index',
            'status',
            'start',
            'end',
            'name',
            'description',
            'is_active',
        )


class PhaseCreationSerializer(WritableNestedModelSerializer):
    tasks = TaskCreationSerializer(many=True)

    class Meta:
        model = Phase
        fields = (
            'id',
            'remote_id',
            'index',
            'start',
            'end',
            'name',
            'description',
            'is_active',
            'tasks'
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
            producer=self.context['request'].user
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


class CompetitionCreationSerializer(WritableNestedModelSerializer):
    producer = ProducerSerializer(required=False)
    phases = PhaseCreationSerializer(required=False, many=True)
    participants = CompetitionParticipantSerializer(required=False, many=True)
    logo = serializers.URLField()

    class Meta:
        model = Competition
        fields = (
            'id',
            'remote_id',
            'title',
            'producer',
            'created_by',
            'creator_id',
            'start',
            'logo',
            'url',
            'phases',
            'participants',
            'description',
            'end',
            'admins',
            'is_active',
            'participant_count',
            'html_text',
            'current_phase_deadline',
            'prize',
            'published'
        )
        validators = []

    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """
        logo_url = validated_data.pop('logo', None)
        validated_data['logo_url'] = logo_url
        try:
            comp = Competition.objects.get(
                remote_id=validated_data.get('remote_id'),
                producer=self.context['producer']
            )
            update_logo = logo_url and logo_url != comp.logo_url
            comp = self.update(comp, validated_data)
            if update_logo:
                download_competition_image.apply_async((comp.id,))
        except ObjectDoesNotExist:
            comp = super().create(validated_data)
            comp.producer = self.context['request'].user
            comp.save()
        return comp


class CompetitionListSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer(required=False)
    logo = serializers.URLField()

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
            'description',
            'end',
            'is_active',
            'participant_count',
            'html_text',
            'current_phase_deadline',
            'prize',
            'published'
        )


class CompetitionDetailSerializer(WritableNestedModelSerializer):
    # Also, Producer in this case comes from serializer context
    producer = ProducerSerializer(required=False)
    phases = PhaseSerializer(required=False, many=True)
    participants = CompetitionParticipantSerializer(many=True, read_only=True)
    admins = serializers.StringRelatedField(many=True, read_only=True)
    logo = serializers.URLField()

    class Meta:
        model = Competition
        fields = (
            'id',
            'remote_id',
            'title',
            'producer',
            'created_by',
            'creator_id',
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
