import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Case, When, Value, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now

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
        if not EmailAddress.objects.filter(email=email).exists():
            email = EmailAddress.objects.create(user=self, email=email, primary=primary)
            self.refresh_profiles()
            return email
        else:
            return False

    def resend_verification_email(self, email_pk):
        # TODO: add celery and handle sending emails as a celery task
        email = get_object_or_404(EmailAddress, user=self, id=email_pk)
        email.send_verification_email()

    def refresh_profiles(self):
        Profile.objects.filter(
            Q(email__in=self.email_addresses.filter(verified=True).values_list('email', flat=True)) | Q(user=self)
        ).distinct().update(user=Case(
            When(email__in=self.email_addresses.filter(verified=True).values_list('email', flat=True), then=Value(self.id)),
            default=None
        ))

    @property
    def primary_email(self):
        return self.email_addresses.filter(primary=True).values_list('email', flat=True).first()

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

    @property
    def verification_url(self):
        return reverse("profiles:verify_email", kwargs={"verification_key": self.verification_key})

    def send_verification_email(self):
        # TODO: add celery and handle sending emails as a celery task
        template_name = "email/email_verification/verification_request"
        context = {
            "verification_url": self.verification_url,
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
        # TODO: decide if we want this to also change the email address field on the user model.
        if not self.verified:
            raise Exception('Primary emails must be verified')
        self.user.email_addresses.update(primary=Case(
            When(id=self.id, then=Value(True)),
            default=False
        ))

    def verify(self):
        self.verified = True
        self.save()


class Profile(models.Model):
    remote_id = models.IntegerField()
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)  # Required, but not unique
    email = models.EmailField(max_length=200, null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', related_name='profiles', on_delete=models.CASCADE)
    details = JSONField(null=True, blank=True)
    scrubbed = models.BooleanField(default=False)

    # Todo: do this with an annotation on the user queryset? or maybe serializer context?
    @property
    def submission_count(self):
        return self.producer.competition_participants.filter(user=self.remote_id).count()

    @property
    def participating_count(self):
        return self.producer.competitions.filter(participants__user=self.remote_id).count()

    class Meta:
        unique_together = ['remote_id', 'producer']

    def __str__(self):
        return f"{self.user.username if self.user else self.username or self.remote_id}'s {self.producer.name} Profile"

    def save(self, *args, **kwargs):
        if self.scrubbed:
            self.user = None
            self.username = None
            self.email = None
            self.details = None
        elif not self.user and EmailAddress.objects.filter(email=self.email, verified=True).exists():
            self.user = EmailAddress.objects.get(email=self.email, verified=True).user
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
    master_account = models.ForeignKey('EmailAddress', related_name='primary_merge_requests', on_delete=models.SET_NULL, null=True)
    secondary_account = models.ForeignKey('EmailAddress', related_name='secondary_merge_requests', on_delete=models.SET_NULL, null=True)
    master_key = models.UUIDField(default=uuid.uuid4, unique=True)
    secondary_key = models.UUIDField(default=uuid.uuid4, unique=True)
    master_confirmation = models.BooleanField(default=False)
    secondary_confirmation = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    emails_sent = models.BooleanField(default=False)

    # these record the email addresses of master and secondary account, so that if the email address object is deleted,
    # we can still see what email addresses were involved in the merge
    master_email = models.EmailField()
    secondary_email = models.EmailField()

    def __str__(self):
        return f"Merge Request ({self.pk}) for master account ({self.master_account.email})"

    class Meta:
        unique_together = ['master_account', 'secondary_account']

    @property
    def master_verification_url(self):
        return reverse("profiles:confirm_merge", kwargs={"merge_key": self.master_key})

    @property
    def secondary_verification_url(self):
        return reverse("profiles:confirm_merge", kwargs={"merge_key": self.secondary_key})

    def send_confirmation_email(self, recipient, verification_url):
        subject = f'Chahub Account Merge Request'
        recipient_list = [recipient.email],
        context = {
            'secondary_account': self.secondary_account,
            'master_account': self.master_account,
            'verification_url': verification_url,
        }
        template_name = 'email/merge/merge_request'
        send_templated_email(template_name, context, subject, recipient_list)

    def save(self, *args, **kwargs):
        if not self.emails_sent:
            self.send_confirmation_email(self.master_account, self.master_verification_url)
            self.send_confirmation_email(self.secondary_account, self.secondary_verification_url)
            self.emails_sent = True

        if not self.master_email:
            self.master_email = self.master_account.email

        if not self.secondary_email:
            self.secondary_email = self.secondary_account.email

        return super().save(*args, **kwargs)

    def merge_accounts(self):
        secondary_user = self.secondary_account.user
        master_user = self.master_account.user
        if hasattr(secondary_user, 'github_user_info'):
            git_info = secondary_user.github_user_info
            git_info.user = master_user
            git_info.save()
        secondary_user.email_addresses.update(user=master_user, primary=False)
        secondary_user.profiles.update(user=master_user)
        secondary_user.delete()
        self.completed_at = now()
        self.save()


@receiver(post_save, sender=EmailAddress)
def email_save_handler(sender, instance, **kwargs):
    if instance.verified:
        instance.user.refresh_profiles()
    else:
        instance.send_verification_email()
