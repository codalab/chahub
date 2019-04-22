
from django.contrib.auth import get_user_model
from rest_framework import serializers

from competitions.models import Competition, CompetitionParticipant

User = get_user_model()


class MyProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source="github_info.bio")

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'bio',
            'id',
            'github_info',
        )


class ProfileCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = (
            'id',
            # 'remote_id',
            'title',
            'producer',
            # 'created_by',
            'start',
            'logo',
            'url',
            # 'phases',
            # 'participants',
            'description',
            'end',
            # 'admins',
            'is_active',
            # 'get_active_phase_end',
            'participant_count',
            'html_text',
            'current_phase_deadline',
            'prize',
            'published',
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    competitions = serializers.SerializerMethodField()
    bio = serializers.CharField(source="github_info.bio", allow_null=True)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'bio',
            'id',
            'competitions',
        )

    def get_competitions(self, user):
        qs = CompetitionParticipant.objects.filter(user=user)
        competition_list = [comp.competition for comp in qs]
        competitions = ProfileCompetitionSerializer(competition_list, many=True)

        return competitions.data
