from django.urls import reverse
from rest_framework.test import APITestCase

from factories import UserFactory, ProducerFactory, EmailAddressFactory, ProfileFactory
from profiles.models import EmailAddress


class ChahubAPITestCase(APITestCase):
    def login(self, username, password='test'):
        self.client.logout()
        self.client.login(username=username, password=password)


class TestEmailPermissions(ChahubAPITestCase):
    def setUp(self):
        self.admin = UserFactory(username='admin', is_superuser=True)
        self.user = UserFactory(username='user')
        self.norm = UserFactory(username='norm')

    def add_email(self, email_address, user):
        return self.client.post(
            reverse('user-add_email_address', kwargs={'pk': user.id, 'version': 'v1'}),
            data={'email_address': email_address}
        )

    def remove_email(self, email_address, user):
        email_pk = EmailAddress.objects.get(email=email_address).id
        return self.client.delete(
            reverse('user-remove_email_address', kwargs={'pk': user.id, 'version': 'v1'}),
            data={'email_pk': email_pk}
        )

    def change_primary(self, email_address, user):
        email_pk = EmailAddress.objects.get(email=email_address).id
        return self.client.post(
            reverse('user-change_primary_email', kwargs={'pk': user.id, 'version': 'v1'}),
            data={'email_pk': email_pk}
        )

    def test_add_email_permissions(self):
        email1, email2, email3 = ('email1@example.com', 'email2@example.com', 'email3@example.com')
        emails = self.user.email_addresses.all().values_list('email', flat=True)
        assert email1 not in emails and email2 not in emails and email3 not in emails

        self.login(username='user')
        resp = self.add_email(email1, self.user)
        assert resp.status_code == 201

        self.login(username='admin')
        resp = self.add_email(email2, self.user)
        assert resp.status_code == 201

        self.login(username='norm')
        resp = self.add_email(email3, self.user)
        # must be superuser to add email to a user other than yourself
        assert resp.status_code == 403
        assert resp.json()['detail'] == 'You do not have permission to add an email address to this user'

        emails = self.user.email_addresses.all().values_list('email', flat=True)
        assert email1 in emails
        assert email2 in emails
        assert email3 not in emails

    def test_remove_email_permissions(self):
        email1, email2, email3 = ('email1@example.com', 'email2@example.com', 'email3@example.com')
        for email in [email1, email2, email3]:
            EmailAddressFactory(user=self.user, email=email)
        emails = self.user.email_addresses.all().values_list('email', flat=True)
        assert email1 in emails and email2 in emails and email3 in emails

        self.login(username='user')
        resp = self.remove_email(email1, self.user)
        assert resp.status_code == 200

        self.login(username='admin')
        resp = self.remove_email(email2, self.user)
        assert resp.status_code == 200

        self.login(username='norm')
        resp = self.remove_email(email3, self.user)
        # must be superuser to remove the email of a user other than yourself
        assert resp.status_code == 403
        assert resp.json()['detail'] == 'You do not have permission to remove an email address from this user'

        emails = self.user.email_addresses.all().values_list('email', flat=True)
        assert email1 not in emails
        assert email2 not in emails
        assert email3 in emails

    def test_change_primary_email_permissions(self):
        email1, email2, email3 = ('email1@example.com', 'email2@example.com', 'email3@example.com')
        for email in [email1, email2, email3]:
            EmailAddressFactory(user=self.user, email=email, verified=True)
        assert self.user.primary_email not in [email1, email2, email3]

        self.login(username='user')
        resp = self.change_primary(email1, self.user)
        assert resp.status_code == 200
        assert self.user.primary_email == email1

        self.login(username='admin')
        resp = self.change_primary(email2, self.user)
        assert resp.status_code == 200
        assert self.user.primary_email == email2

        self.login(username='norm')
        resp = self.change_primary(email3, self.user)
        # must be superuser to change the primary email of a user other than yourself
        assert resp.status_code == 403
        assert resp.json()['detail'] == "You do not have permission to change this user's primary email"
        assert self.user.primary_email == email2  # didn't change


class TestEmails(APITestCase):
    def setUp(self):
        self.producer = ProducerFactory()
        self.user = UserFactory(username='user')
        self.profile = ProfileFactory()

    def test_email_does_not_connects_profiles_to_users_until_email_is_verified(self):
        email = EmailAddressFactory(email=self.profile.email, user=self.user)
        assert not self.user.profiles.filter(id=self.profile.id).exists()
        self.client.get(email.verification_url)
        assert self.user.profiles.filter(id=self.profile.id).exists()
