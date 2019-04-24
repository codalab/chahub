import logging
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

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

    def create(self, validated_data):
        """
        This creates *AND* updates based on the combination of (remote_id, producer)
        """
        logger.info("**************************************************************************************************")
        logger.info(validated_data)
        logger.info("**************************************************************************************************")
        if self.many:
            last_instance = None
            for profile in validated_data:
                try:
                    # If we have an existing instance from this producer
                    # with the same remote_id, update it instead of making a new one
                    temp_instance = Profile.objects.get(
                        remote_id=validated_data.get('remote_id'),
                        producer__id=validated_data.get('producer')
                    )
                    last_instance = self.update(temp_instance, validated_data)
                except Profile.DoesNotExist:
                    last_instance = super().create(validated_data)
                    # return new_instance
                return last_instance
        else:
            try:
                # If we have an existing instance from this producer
                # with the same remote_id, update it instead of making a new one
                temp_instance = Profile.objects.get(
                    remote_id=validated_data.get('remote_id'),
                    producer__id=validated_data.get('producer')
                )
                return self.update(temp_instance, validated_data)
            except Profile.DoesNotExist:
                new_instance = super().create(validated_data)
                return new_instance
