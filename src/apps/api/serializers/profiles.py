import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from profiles.models import GithubUserInfo, AccountMergeRequest

User = get_user_model()

logger = logging.getLogger(__name__)


class AccountMergeRequestSerializer(serializers.ModelSerializer):
    master_account = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', error_messages={'does_not_exist': "Bad Request"})
    secondary_account = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', error_messages={'does_not_exist': "Bad Request"})

    class Meta:
        model = AccountMergeRequest
        validators = [
            UniqueTogetherValidator(
                queryset=AccountMergeRequest.objects.all(),
                fields=('master_account', 'secondary_account'),
                message='Merge request already exists'
            )
        ]
        fields = (
            'master_account',
            'secondary_account',
            'created'
        )
        read_only_fields = (
            'created',
        )

    def validate(self, attrs):
        if attrs['master_account'] == attrs['secondary_account']:
            raise ValidationError('Master account and secondary account emails cannot be the same')
        return attrs


class GithubUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubUserInfo
        fields = (
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
        )


class UserDetailSerializer(serializers.ModelSerializer):
    github_user_info = GithubUserInfoSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'id',
            'date_joined',
            'github_user_info',
            'date_joined'
        )


class MyUserDetailSerializer(serializers.ModelSerializer):
    github_user_info = GithubUserInfoSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'date_joined',
            'github_user_info',
            'date_joined'
        )
