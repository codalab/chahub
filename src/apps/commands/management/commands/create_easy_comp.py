import datetime
import random
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone
from termcolor import colored

from competitions.models import Competition
from factories import UserFactory


class Command(BaseCommand):
    help = 'Creates a dummy competition'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--number',
            type=int,
            dest='amount',
            help='Amount of comps/users to create',
        )

    def handle(self, *args, **options):
        count = 1
        if options['amount']:
            count = options['amount']

        for i in range(count):
            try:
                # Setup a temp user
                temp_user = UserFactory()

                temp_title = "New Competition_{}".format(str(uuid.uuid4()))
                temp_desc = temp_title + "'s description"
                # Setup a new comp
                new_comp = Competition.objects.create(
                    title=temp_title,
                    description=temp_desc,
                    created_by=temp_user.username,
                    remote_id=999,
                    published=True
                )
                new_comp.created_when = timezone.now() + datetime.timedelta(days=random.randint(-15, 15))
                new_comp.save()
                print(colored('Successfully created new user and competition: {0}, {1}'.format(temp_user, new_comp),
                              'green'))
            except:
                print(colored('Failed to create competition', 'red'))
