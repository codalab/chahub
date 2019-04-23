from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from profiles.models import GithubUserInfo, LinkedInUserInfo, Profile

User = get_user_model()

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


class MyProfileSerializer(ModelSerializer):

    github_info = GithubUserInfoSerializer(many=False, required=False, read_only=True)
    linkedin_info = LinkedInUserInfoSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'github_info',
            'linkedin_info'
        )

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'remote_id',
            'producer',
            'email',
            'details'
        ]
