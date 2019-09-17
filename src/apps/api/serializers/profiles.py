import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from profiles.models import GithubUserInfo, AccountMergeRequest, Profile, EmailAddress

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


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'remote_id',
            'email',
            'username',
            'producer',
            'details',
        )
        # TODO: this has to be a bad idea, right?
        validators = []
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        instance, created = Profile.objects.update_or_create(
            remote_id=validated_data.pop('remote_id'),
            producer=validated_data.pop('producer'),
            defaults=validated_data
        )
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(source='producer.name')

    class Meta:
        model = Profile
        fields = (
            'id',
            'remote_id',
            'username',
            'producer'
        )


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = (
            'id',
            'email',
            'verified',
            'primary',
            'user',
        )
        extra_kwargs = {
            'user': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    github_user_info = GithubUserInfoSerializer(read_only=True, required=False)
    profiles = ProfileSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'date_joined',
            'github_user_info',
            'profiles',
        )


class MyUserSerializer(serializers.ModelSerializer):
    github_user_info = GithubUserInfoSerializer(read_only=True, required=False)
    profiles = ProfileSerializer(read_only=True, many=True)
    email_addresses = EmailAddressSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'date_joined',
            'github_user_info',
            'profiles',
            'email_addresses',
        )
