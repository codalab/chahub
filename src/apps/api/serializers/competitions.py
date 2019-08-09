from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.serializers.mixins import BulkSerializerMixin
from competitions.models import Competition, Phase, Submission, CompetitionParticipant
from profiles.models import Profile


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
    phases = PhaseSerializer(required=False, many=True)
    admins = serializers.StringRelatedField(many=True, read_only=True)
    logo = serializers.URLField(required=False)
    # Extra field to mimic ESL results
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
            # 'participants',
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


class CompetitionParticipantCreationSerializer(serializers.ModelSerializer):

    competition = serializers.IntegerField()
    user = serializers.IntegerField()

    class Meta:
        model = CompetitionParticipant
        fields = ['competition', 'user', 'status']
        validators = []
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }

    def validate_competition(self, competition):
        return Competition.objects.get(remote_id=competition, producer=self.context.get('producer'))

    def validate_user(self, user):
        return Profile.objects.get(remote_id=user, producer=self.context.get('producer'))

    # Override mixin
    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """
        try:
            # If we have an existing instance from this producer
            # with the same remote_id, update it instead of making a new one
            if not validated_data.get('user') or not validated_data.get('competition'):
                return None
            instance = self.Meta.model.objects.get(
                user=validated_data.get('user'),
                competition=validated_data.get('competition')
            )
            return self.update(instance, validated_data)
        except self.Meta.model.DoesNotExist:
            new_instance = super().create(validated_data)
            return new_instance


class CompetitionParticipantListSerializer(serializers.ModelSerializer):

    competition = CompetitionSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = CompetitionParticipant
        fields = ['competition', 'user', 'status']
