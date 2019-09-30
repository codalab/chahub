from django.core.management.base import BaseCommand
from faker import Faker
from termcolor import colored
from tqdm import tqdm

from factories import UserFactory

fake = Faker()


class Command(BaseCommand):
    help = 'Creates a simple user, or multiple'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--number',
            type=int,
            dest='amount',
            help='Amount of users to create',
        )

    def handle(self, *args, **options):
        count = 1
        if options['amount']:
            count = options['amount']
        for i in tqdm(range(count), ncols=100):
            try:
                # Create a random user
                UserFactory()
            except:
                print(colored('Failed to create user', 'red'))
        print(
            colored("Operation completed succesfully! {} users created!".format(count))
        )
