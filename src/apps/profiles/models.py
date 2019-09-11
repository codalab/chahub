import uuid

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.db import models
from django.urls import reverse

from .utils import send_templated_email


class User(AbstractBaseUser, PermissionsMixin):
    # Social needs the below setting. Username is not really set to UID.
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # User Attributes
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True, null=True, blank=True)

    # Utility Attributes
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Required for social auth and such to create users
    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username


class GithubUserInfo(models.Model):
    # Required Info
    uid = models.CharField(max_length=30, unique=True)

    user = models.OneToOneField('User', related_name='github_user_info', null=True, blank=True, on_delete=models.CASCADE)

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

    def __str__(self):
        return f"{getattr(self, 'user', self.login)} GitHub user info"


class AccountMergeRequest(models.Model):
    master_account = models.ForeignKey(User, related_name='primary_merge_requests', on_delete=models.CASCADE)
    secondary_account = models.ForeignKey(User, related_name='secondary_merge_requests', on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, unique=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['master_account', 'secondary_account']

    @property
    def absolute_url(self):
        return f'{settings.SITE_DOMAIN}{reverse("profiles:finalize_merge", kwargs={"merge_key": self.key})}'

    def save(self, *args, **kwargs):
        subject = f'Chahub Account Merge Request From: {self.master_account.email}'
        recipient_list = [self.secondary_account.email],
        context = {
            'user': self.secondary_account,
            'requester': self.master_account,
            'merge': self,
            'static': f'{settings.SITE_DOMAIN}/static',
            'signature_img': f'{settings.SITE_DOMAIN}/static/img/temp_chahub_logo_beta.png'
        }
        template_name = 'email/merge/merge_request'
        send_templated_email(template_name, context, subject, recipient_list)

        return super().save(*args, **kwargs)

    def merge_accounts(self):
        if hasattr(self.secondary_account, 'github_user_info'):
            git_info = self.secondary_account.github_user_info
            git_info.user = self.master_account
            git_info.save()
