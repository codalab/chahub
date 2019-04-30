import logging
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.serializers.competitions import CompetitionSerializer
from api.serializers.data import DataSerializer
from api.serializers.tasks import TaskSerializer, SolutionSerializer
from competitions.models import Competition, CompetitionParticipant
from profiles.models import GithubUserInfo, LinkedInUserInfo, Profile

User = get_user_model()

logger = logging.getLogger(__name__)

class GithubUserInfoSerializer(ModelSerializer):

    class Meta:
        model = GithubUserInfo
        fields = [
            'uid',
            'login',
            'avatar_url',
            'gravatar_id',
            'html_url',
            'name',
            'company',
            'bio',
            'location',
            'created_at',
            'updated_at',
            'node_id',
            'url',
            'followers_url',
            'following_url',
            'gists_url',
            'starred_url',
            'subscriptions_url',
            'organizations_url',
            'repos_url',
            'events_url',
            'received_events_url'
        ]


class LinkedInUserInfoSerializer(ModelSerializer):

    class Meta:
        model = LinkedInUserInfo
        fields = [
            'uid',
            'firstName',
            'lastName'
        ]


class MyProfileSerializer(serializers.ModelSerializer):
    github_info = GithubUserInfoSerializer(read_only=True, required=False, many=False)
    organized_competitions = CompetitionSerializer(read_only=True, required=False, many=True)
    created_tasks = TaskSerializer(read_only=True, required=False, many=True)
    created_solutions = SolutionSerializer(read_only=True, required=False, many=True)
    created_datasets = DataSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'email',
            'id',
            'github_info',
            'organized_competitions',
            'created_tasks',
            'created_solutions',
            'created_datasets',
        ]

class ProfileSerializer(ModelSerializer):
    from api.serializers.competitions import CompetitionSerializer
    from api.serializers.data import DataSerializer
    from api.serializers.tasks import TaskSerializer
    from api.serializers.tasks import SolutionSerializer

    organized_competitions = CompetitionSerializer(many=True, read_only=True)
    datasets = DataSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    solutions = SolutionSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'remote_id',
            'producer',
            'email',
            'username',
            'details',
            'user',
            'organized_competitions',
            'datasets',
            'tasks',
            'solutions'
        ]
        read_only_fields = [

        ]

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
            instance = Profile.objects.get(
                remote_id=validated_data.get('remote_id'),
                producer=validated_data.get('producer')
            )
            return self.update(instance, validated_data)
        except Profile.DoesNotExist:
            new_instance = super().create(validated_data)
            return new_instance
