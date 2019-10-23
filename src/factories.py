import random
import uuid
from urllib.parse import urljoin

import factory
from dateutil.tz import UTC
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast
from django.db.models.signals import post_save
from factory import DjangoModelFactory, post_generation
from faker import Faker

from competitions.models import Competition, Phase
from datasets.models import Data
from producers.models import Producer
from profiles.models import User, EmailAddress, Profile
from tasks.models import Task

fake = Faker()

SAFE_PRODUCER_DOMAINS = [
    'http://chalab.lri.fr',
    'http://competitions.codalab.org/competitions/',
    'http://codalab.lri.fr',
    'http://example.com',
]

DATA_FILE_TYPES = [
    'ingestion_program',
    'input_data',
    'ingestion_only_during_scoring',
    'reference_data',
    'scoring_program',
]


def get_next_remote_id(qs):
    max_id = qs.annotate(remote_id_int=Cast('remote_id', IntegerField())).aggregate(max=Max('remote_id_int')).get('max')
    return max_id + 1 if max_id is not None else 0


def get_next_phase_index(phase):
    max_index = phase.competition.phases.aggregate(Max('index')).get('index__max')
    return max_index + 1 if max_index is not None else 0


def get_next_phase_start(phase):
    if phase.index == 0:
        return phase.competition.start
    else:
        return phase.competition.phases.get(index=phase.index - 1).end + fake.time_delta()


def random_phase_end(phase):
    return phase.start + fake.time_delta()


def random_prize_money():
    return random.randint(10, 100) * 100 if random.choice([True, False]) else None


def random_producer():
    return random.choice(Producer.objects.all())


def random_creator_id(obj):
    try:
        return random.choice(obj.producer.profiles.values_list('remote_id', flat=True))
    except IndexError:
        return ProfileFactory(producer=obj.producer).remote_id


def get_created_by(obj):
    return Profile.objects.get(remote_id=obj.creator_id, producer=obj.producer).username


# Muting signals on User and EmailAddresses so factories don't try and send verification emails
@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    class Params:
        super_user = factory.Trait(
            is_superuser=True,
            is_staff=True
        )
        enabled = True

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = "test"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


@factory.django.mute_signals(post_save)
class EmailAddressFactory(DjangoModelFactory):
    class Meta:
        model = EmailAddress

    user = factory.SubFactory(UserFactory)
    email = factory.Faker('safe_email')


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    producer = factory.LazyFunction(random_producer)
    remote_id = factory.LazyAttribute(lambda p: get_next_remote_id(p.producer.profiles.all()))
    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')


class ProducerFactory(DjangoModelFactory):
    class Meta:
        model = Producer

    name = factory.Faker('company')
    contact = factory.Faker('safe_email')
    url = factory.Iterator(SAFE_PRODUCER_DOMAINS)

    @post_generation
    def api_key(self, created, extracted, **kwargs):
        if extracted:
            if not isinstance(extracted, uuid.UUID):
                extracted = uuid.UUID(extracted)
            self.api_key = extracted
            if created:
                self.save()


class DataFactory(DjangoModelFactory):
    class Meta:
        model = Data

    producer = factory.LazyFunction(random_producer)
    creator_id = factory.LazyAttribute(random_creator_id)
    created_by = factory.LazyAttribute(get_created_by)
    remote_id = factory.LazyAttribute(lambda t: get_next_remote_id(t.producer.datasets.all()))
    created_when = factory.Faker('date_time_this_year', tzinfo=UTC)
    type = factory.Iterator(DATA_FILE_TYPES)
    name = factory.Faker('catch_phrase')
    description = factory.Faker('bs')
    is_public = factory.Faker('boolean', chance_of_getting_true=80)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task
    producer = factory.LazyFunction(random_producer)
    remote_id = factory.LazyAttribute(lambda t: get_next_remote_id(t.producer.tasks.all()))
    creator_id = factory.LazyAttribute(random_creator_id)
    created_by = factory.LazyAttribute(get_created_by)
    created_when = factory.Faker('date_time_this_year', tzinfo=UTC)
    name = factory.Faker('catch_phrase')
    description = factory.Faker('bs')
    is_public = factory.Faker('boolean', chance_of_getting_true=80)
    ingestion_program = factory.SubFactory(DataFactory, type='ingestion_program')
    input_data = factory.SubFactory(DataFactory, type='input_data')
    reference_data = factory.SubFactory(DataFactory, type='reference_data')
    scoring_program = factory.SubFactory(DataFactory, type='scoring_program')
    ingestion_only_during_scoring = factory.Faker('boolean', chance_of_getting_true=20)


class PhaseFactory(DjangoModelFactory):
    class Meta:
        model = Phase
    competition = None
    remote_id = factory.LazyAttribute(lambda p: get_next_remote_id(p.competition.phases.all()))
    index = factory.LazyAttribute(get_next_phase_index)
    start = factory.LazyAttribute(get_next_phase_start)
    end = factory.LazyAttribute(random_phase_end)
    name = factory.Faker('catch_phrase')
    description = factory.Faker('bs')

    @post_generation
    def tasks(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            if hasattr(extracted, '__iter__'):
                for t in extracted:
                    self.tasks.add(t)
            else:
                self.tasks.add(extracted)
        else:
            for _ in range(random.randint(1, 3)):
                self.tasks.add(TaskFactory(producer=self.competition.producer))


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = Competition

    title = factory.Faker('catch_phrase')
    description = factory.Faker('bs')
    producer = factory.LazyFunction(random_producer)
    remote_id = factory.LazyAttribute(lambda c: get_next_remote_id(Competition.objects.filter(producer=c.producer)))
    creator_id = factory.LazyAttribute(random_creator_id)
    created_by = factory.LazyAttribute(get_created_by)
    created_when = factory.Faker('date_time_this_year', tzinfo=UTC)
    prize = factory.LazyFunction(random_prize_money)
    url = factory.LazyAttribute(lambda c: urljoin(c.producer.url, fake.uri_path()))
    participant_count = factory.LazyFunction(lambda: random.randint(1, 500))
    published = factory.Faker('boolean')
    start = factory.Faker('date_time_this_year', tzinfo=UTC)
    phases = factory.RelatedFactoryList(PhaseFactory, 'competition', size=lambda: random.randint(1, 4))

    @post_generation
    def endless(self, created, extracted, **kwargs):
        if extracted or random.random() <= .25:
            final_phase = self.phases.order_by('index').last()
            final_phase.end = None
            final_phase.save()

    @post_generation
    def end(self, created, extracted, **kwargs):
        self.end = extracted if extracted else self.phases.order_by('index').last().end
        self.save()
