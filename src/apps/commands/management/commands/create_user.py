from django.core.management.base import BaseCommand
from termcolor import colored

from profiles.models import User as CodalabUser


class Command(BaseCommand):
    help = 'Add a user. Takes positional args, username, email, password.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            'email',
            type=str,
            help='New users email (required)',
        )

        parser.add_argument(
            'username',
            type=str,
            help='New users username (required)',
        )

        parser.add_argument(
            'password',
            type=str,
            help='New users password (required)',
        )
        parser.add_argument(
            '-su',
            '--super-user',
            action='store_true',
            help='Created user will be super user')

    def handle(self, *args, **options):
        # These are the only 2 required fields.
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        su = options.get('super_user')
        try:
            temp_user = CodalabUser.objects.create(email=email, username=username)
            temp_user.set_password(password)
            if su:
                temp_user.is_staff = True
                temp_user.is_superuser = True
            temp_user.save()
            print(colored(f'Successfully created {"super user" if su else "user"} <{temp_user.username}> with password <{password}>', 'green'))
        except:
            print(colored('Failed to create user', 'red'))
