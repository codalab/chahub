import factory
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from termcolor import colored

from factories import ProducerFactory, UserFactory, ProfileFactory, CompetitionFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--size',
            type=int,
            default=3,
            help='The number of each type of item to create',
        )

        parser.add_argument(
            '-n',
            '--no-admin',
            action='store_true',
            help='Do not create a superuser with username admin (to avoid collisions)',
        )

    def handle(self, *args, **kwargs):
        print(colored(f'Generating Data', 'cyan'))
        size = kwargs.get('size')
        with factory.django.mute_signals(post_save):
            for i in range(size):
                if i == 0 and not kwargs.get('no_admin'):
                    UserFactory(super_user=True, username='admin', password='admin')
                else:
                    UserFactory()

            producers = [ProducerFactory() for _ in range(size)]
            for producer in producers:
                for _ in range(size):
                    ProfileFactory(producer=producer)
                for _ in range(size):
                    CompetitionFactory(producer=producer)
        print(colored(f'Data generated successfully', 'green'))
