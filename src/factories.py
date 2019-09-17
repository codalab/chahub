import factory
from django.db.models.signals import post_save
from factory import DjangoModelFactory, post_generation

from producers.models import Producer
from profiles.models import User, EmailAddress, Profile


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = "test"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)

    @post_generation
    def super_user(self, created, extracted, **kwargs):
        if extracted:
            self.is_superuser = True
            self.is_staff = True


@factory.django.mute_signals(post_save)
class EmailAddressFactory(DjangoModelFactory):
    class Meta:
        model = EmailAddress

    user = factory.SubFactory(UserFactory)
    email = factory.Faker('safe_email')


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    remote_id = factory.Sequence(lambda n: n)
    producer = factory.Iterator(Producer.objects.all())
    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')


class ProducerFactory(DjangoModelFactory):
    class Meta:
        model = Producer

    name = factory.Faker('company')
    contact = factory.Faker('safe_email')
    url = 'example.com'
