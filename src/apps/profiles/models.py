import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Case, When, Value, F, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from utils.email import send_templated_email


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

    def add_email(self, email, primary=False):
        # TODO: add catch integrity error from already existing email address
        self.email_addresses.create(email=email, primary=primary)
        self.refresh_profiles()

    def resend_verification_email(self, email_pk):
        email = get_object_or_404(EmailAddress, user=self, id=email_pk)
        email.send_verification_email()

    def refresh_profiles(self):
        Profile.objects.filter(
            Q(email__in=self.email_addresses.filter(verified=True).values_list('email', flat=True)) |
            Q(user=self)
        ).distinct().update(user=Case(
            When(email__in=self.email_addresses.filter(verified=True).values_list('email', flat=True), then=Value(self.id)),
            default=None
        ))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Make sure an email address object exists for this users email address
        if not self.email_addresses.filter(email=self.email).exists():
            self.add_email(self.email, primary=True)


class EmailAddress(models.Model):
    user = models.ForeignKey(User, related_name='email_addresses', on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    verification_key = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.verified:
            self.send_verification_email()

    @property
    def absolute_url(self):
        return reverse("profiles:verify_email", kwargs={"verification_key": self.verification_key})

    def send_verification_email(self):
        template_name = "email/email_verification/verification_request"
        context = {
            "absolute_url": self.absolute_url,
            "user": self.user,
        }
        subject = "Verify Email Address"
        recipient_list = [self.email]
        send_templated_email(
            template_name=template_name,
            context=context,
            subject=subject,
            recipient_list=recipient_list
        )

    def make_primary(self):
        if not self.verified:
            raise Exception('Primary emails must be verified')
        self.user.email_addresses.update(primary=Case(
            When(id=F('id'), then=Value(True)),
            default=False
        ))

    def verify(self):
        self.verified = True
        self.save()
        self.user.refresh_profiles()


class Profile(models.Model):
    remote_id = models.IntegerField()
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150)  # Required, but not unique
    email = models.EmailField(max_length=200, null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', related_name='profiles', on_delete=models.CASCADE)
    details = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ['remote_id', 'producer']

    def __str__(self):
        return f"{self.user.username if self.user else self.username}'s {self.producer.name} Profile"

    def save(self, *args, **kwargs):
        if not hasattr(self, 'user') and EmailAddress.objects.filter(email=self.email).exists():
            self.user = EmailAddress.objects.get(email=self.email).user
        super().save(*args, **kwargs)


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
        return reverse("profiles:finalize_merge", kwargs={"merge_key": self.key})

    def save(self, *args, **kwargs):
        subject = f'Chahub Account Merge Request From: {self.master_account.email}'
        recipient_list = [self.secondary_account.email],
        context = {
            'user': self.secondary_account,
            'requester': self.master_account,
            'absolute_url': self.absolute_url,
        }
        template_name = 'email/merge/merge_request'
        send_templated_email(template_name, context, subject, recipient_list)

        return super().save(*args, **kwargs)

    def merge_accounts(self):
        if hasattr(self.secondary_account, 'github_user_info'):
            git_info = self.secondary_account.github_user_info
            git_info.user = self.master_account
            git_info.save()
        self.secondary_account.email_addresses.update(user=self.master_account)
        self.secondary_account.profiles.update(user=self.master_account)
