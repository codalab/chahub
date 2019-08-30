import uuid

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse

from apps.profiles.utils import send_templated_email

from producers.models import Producer


class User(AbstractBaseUser, PermissionsMixin):
    # Social needs the below setting. Username is not really set to UID.
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # Any User Attributes
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True, default='')

    github_info = models.OneToOneField('GithubUserInfo', related_name='user', null=True, blank=True, on_delete=models.CASCADE)
    docker_info = models.OneToOneField('DockerUserInfo', related_name='user', null=True, blank=True, on_delete=models.CASCADE)
    linkedin_info = models.OneToOneField('LinkedInUserInfo', related_name='user', null=True, blank=True, on_delete=models.CASCADE)

    # Utility Attributes
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Profile Fields
    brief_description = models.CharField(max_length=300, null=True, blank=True)

    edu_institution = models.CharField(max_length=60, null=True, blank=True)
    edu_degree = models.CharField(max_length=40, null=True, blank=True)
    edu_years = models.CharField(max_length=40, null=True, blank=True)
    edu_awards = models.CharField(max_length=40, null=True, blank=True)

    org_image = models.ImageField(null=True, blank=True)
    org_name = models.CharField(max_length=60, null=True, blank=True)
    org_type = models.CharField(max_length=40, null=True, blank=True)
    org_description = models.CharField(max_length=300, null=True, blank=True)

    event_name = models.CharField(max_length=60, null=True, blank=True)
    event_dates = models.CharField(max_length=50, null=True, blank=True)
    event_description = models.CharField(max_length=300, null=True, blank=True)
    event_url = models.CharField(max_length=100, null=True, blank=True)

    dataset = models.FileField(null=True, blank=True)

    # Required for social auth and such to create users
    objects = UserManager()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    @property
    def organized_competitions_count(self):
        return self.organized_competitions.count() if self.organized_competitions else 0

    @property
    def datasets_count(self):
        return self.created_datasets.count() if self.created_datasets else 0

    @property
    def tasks_count(self):
        return self.created_tasks.count() if self.created_tasks else 0

    @property
    def solutions_count(self):
        return self.created_solutions.count() if self.created_solutions else 0


class Profile(models.Model):
    """
    Keeps track of remote users from producers
    """

    remote_id = models.IntegerField()
    producer = models.ForeignKey(Producer, related_name='profiles', on_delete=models.CASCADE)
    email = models.EmailField()
    username = models.CharField(max_length=150)  # Required, but not unique

    user = models.ForeignKey(User, related_name='profiles', on_delete=models.SET_NULL, null=True, blank=True)

    details = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ['remote_id', 'producer']

    @property
    def organized_competitions(self):
        from competitions.models import Competition
        return Competition.objects.filter(producer=self.producer, creator_id=self.remote_id)

    @property
    def datasets(self):
        from datasets.models import Data
        return Data.objects.filter(producer=self.producer, creator_id=self.remote_id)

    @property
    def tasks(self):
        from tasks.models import Task
        return Task.objects.filter(producer=self.producer, creator_id=self.remote_id)

    @property
    def solutions(self):
        from tasks.models import Solution
        return Solution.objects.filter(producer=self.producer, creator_id=self.remote_id)


# WILL BE VERY USEFUL
class GithubUserInfo(models.Model):
    # Required Info
    uid = models.CharField(max_length=30, unique=True)

    # Misc/Avatar/Profile
    login = models.CharField(max_length=100, null=True, blank=True)  # username
    avatar_url = models.URLField(max_length=100, null=True, blank=True)
    gravatar_id = models.CharField(max_length=100, null=True, blank=True)
    html_url = models.URLField(max_length=100, null=True, blank=True)  # Profile URL
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=2000, null=True, blank=True)
    location = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # API Info
    node_id = models.CharField(unique=True, max_length=50, default='')
    url = models.URLField(max_length=100, null=True, blank=True)  # Base API URL
    followers_url = models.URLField(max_length=100, null=True, blank=True)
    following_url = models.URLField(max_length=100, null=True, blank=True)
    gists_url = models.URLField(max_length=100, null=True, blank=True)
    starred_url = models.URLField(max_length=100, null=True, blank=True)
    subscriptions_url = models.URLField(max_length=100, null=True, blank=True)
    organizations_url = models.URLField(max_length=100, null=True, blank=True)
    repos_url = models.URLField(max_length=100, null=True, blank=True)
    events_url = models.URLField(max_length=100, null=True, blank=True)
    received_events_url = models.URLField(max_length=100, null=True, blank=True)


# No use yet
class DockerUserInfo(models.Model):
    uid = models.CharField(max_length=30, unique=True)


# Not so useful
class LinkedInUserInfo(models.Model):
    uid = models.CharField(max_length=30, unique=True)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)


class AccountMergeRequest(models.Model):
    master_account = models.ForeignKey(User, related_name='primary_merge_requests', on_delete=models.CASCADE)
    secondary_account = models.ForeignKey(User, related_name='secondary_merge_requests', on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, unique=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['master_account', 'secondary_account']

    def clean(self, *args, **kwargs):
        # add custom validation here
        if self.master_account == self.secondary_account:
            raise ValidationError("Cannot create a merge request between the same account")
        super().clean(*args, **kwargs)

    @property
    def absolute_url(self):
        return f'{settings.SITE_DOMAIN}{reverse("profiles:merge", kwargs={"merge_key": self.key})}'

    def save(self, *args, **kwargs):
        email_kwargs = {
            'subject': f'Chahub Account Merge Request From: {self.master_account.email}',
            'recipient_list': [self.secondary_account.email],
            'fail_silently': False
        }
        context = {
            'user': self.secondary_account,
            'requester': self.master_account,
            'merge': self,
            'static': f'{settings.SITE_DOMAIN}/static',
            'signature_img': f'{settings.SITE_DOMAIN}/static/img/temp_chahub_logo_beta.png'
        }
        template_name = 'email/merge/merge_request'
        send_templated_email(template_name, context, **email_kwargs)

        return super(AccountMergeRequest, self).save(*args, **kwargs)

    def merge_accounts(self):
        merge_fields = ['organized_competitions', 'datasets', 'tasks', 'profiles']
        for field in merge_fields:
            qs = getattr(self.secondary_account, field)
            qs.update(user=self.master_account)
            # for obj in getattr(self.secondary_account, field):
            #     obj.user = self.master_account
            #     obj.save()
