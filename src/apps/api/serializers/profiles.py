import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from profiles.models import GithubUserInfo, AccountMergeRequest, Profile, EmailAddress

User = get_user_model()

logger = logging.getLogger(__name__)

ERROR_MESSAGES = {
    'does_not_exist': 'Please make sure the emails you entered are valid and are the primary email '
                      'addresses on the accounts you want to merge.'
}


class AccountMergeRequestSerializer(serializers.ModelSerializer):
    master_account = serializers.SlugRelatedField(
        queryset=EmailAddress.objects.filter(primary=True),
        slug_field='email',
        error_messages=ERROR_MESSAGES
    )
    secondary_account = serializers.SlugRelatedField(
        queryset=EmailAddress.objects.filter(primary=True),
        slug_field='email',
        error_messages=ERROR_MESSAGES
    )

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
        if EmailAddress.objects.filter(
                Q(email=attrs['master_account']) | Q(email=attrs['secondary_account'])
        ).values_list('user', flat=True).distinct().count() != 2:
            # This shouldn't be able to happen anyway, since users should only be able to have one primary email address
            # But checking this anyway for extra bug protection
            raise ValidationError('Master account and secondary account emails must belong to different users')
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
