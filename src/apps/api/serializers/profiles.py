import logging
from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.serializers.mixins import BulkSerializerMixin
from api.serializers.producers import ProducerSerializer
from profiles.models import GithubUserInfo, LinkedInUserInfo, Profile, AccountMergeRequest

from api.serializers.competitions import CompetitionSerializer, CompetitionParticipantListSerializer
from api.serializers.data import DataSerializer
from api.serializers.tasks import TaskSerializer
from api.serializers.tasks import SolutionSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class AccountMergeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMergeRequest
        fields = [
            'master_account',
            'secondary_account',
            'created'
        ]
        read_only_fields = [
            'created'
        ]


class GithubUserInfoSerializer(serializers.ModelSerializer):

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


class LinkedInUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkedInUserInfo
        fields = [
            'uid',
            'firstName',
            'lastName'
        ]


class UserProfileDetailSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    organized_competitions = CompetitionSerializer(many=True, read_only=True)
    datasets = DataSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    solutions = SolutionSerializer(many=True, read_only=True)
    participants = CompetitionParticipantListSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id',
            'remote_id',
            'producer',
            'email',
            'username',
            'details',
            'user',
            'organized_competitions',
            'datasets',
            'tasks',
            'solutions',
            'participants',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }


class MyProfileDetailSerializer(serializers.ModelSerializer):
    github_info = GithubUserInfoSerializer(read_only=True, required=False, many=False)
    organized_competitions = CompetitionSerializer(read_only=True, required=False, many=True)
    created_tasks = TaskSerializer(read_only=True, required=False, many=True)
    created_solutions = SolutionSerializer(read_only=True, required=False, many=True)
    created_datasets = DataSerializer(read_only=True, required=False, many=True)
    profiles = UserProfileDetailSerializer(read_only=True, required=False, many=True)


    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'email',
            'id',
            'date_joined',
            'github_info',
            'organized_competitions',
            'created_tasks',
            'created_solutions',
            'created_datasets',
            'profiles',
        ]


class MyProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'email',
            'id',
            'date_joined',
            'github_info',
            'organized_competitions',
            'created_tasks',
            'created_solutions',
            'created_datasets',
        ]


# Different Profile Serializers
class ProfileDetailSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    organized_competitions = CompetitionSerializer(many=True, read_only=True)
    datasets = DataSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    solutions = SolutionSerializer(many=True, read_only=True)
    # TODO: Look more into the effects of removing this. I believe we added it so we could display details
    user = MyProfileDetailSerializer(many=False, read_only=True)
    participants = CompetitionParticipantListSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id',
            'remote_id',
            'producer',
            'email',
            'username',
            'details',
            'user',
            'organized_competitions',
            'datasets',
            'tasks',
            'solutions',
            'participants',
        ]
        read_only_fields = ['id']


class ProfileCreateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    organized_competitions = CompetitionSerializer(many=True, read_only=True)
    datasets = DataSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    solutions = SolutionSerializer(many=True, read_only=True)
    # TODO: Look more into the effects of removing this. I believe we added it so we could display details
    participants = CompetitionParticipantListSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id',
            'remote_id',
            'producer',
            'email',
            'username',
            'details',
            'user',
            'organized_competitions',
            'datasets',
            'tasks',
            'solutions',
            'participants',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }


class BaseProfileSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    producer = ProducerSerializer(required=False, validators=[])

    class Meta:
        model = Profile
        fields = [
            'id',
            'remote_id',
            'producer',
            'email',
            'username',
            'details',
            'user',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'producer': {
                # UniqueTogether validator messes this up
                'validators': [],
            }
        }
