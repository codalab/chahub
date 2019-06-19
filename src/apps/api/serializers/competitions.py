from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.mixins import BulkSerializerMixin
from api.serializers.producers import ProducerSerializer
from competitions.models import Competition, Phase, Submission, CompetitionParticipant


class CompetitionParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionParticipant
        fields = ['competition', 'user']


class PhaseSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Phase
        fields = [
            'id',
            # 'competition',
            'index',
            'start',
            'end',
            'name',
            'description',
            'is_active'
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    competition = serializers.IntegerField(min_value=1, write_only=True, required=True)
    phase_index = serializers.IntegerField(min_value=1, write_only=True, required=True)

    class Meta:
        model = Submission
        fields = [
            'remote_id',
            'competition',  # on write only
            'phase_index',  # on write this is the phase index within the competition, NOT a PK
            'submitted_at',
            'participant'
        ]

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


class CompetitionSerializer(BulkSerializerMixin, WritableNestedModelSerializer):
    # Stop the "uniqueness" validation, we want to be able to update already
    # existing models
    # Also, Producer in this case comes from serializer context
    # producer = ProducerSerializer(required=False, validators=[])
    phases = PhaseSerializer(required=False, many=True)
    participants = CompetitionParticipantSerializer(many=True, read_only=True)
    admins = serializers.StringRelatedField(many=True, read_only=True)
    logo = serializers.URLField()
    _object_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Competition
        fields = [
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
            'published',
            'user',
            '_object_type'
        ]
        validators = []
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }

    def get__object_type(self, obj):
        return "competition"

    def validate_description(self, description):
        if description:
            description = description.replace("<p>", "").replace("</p>", "")
        return description
