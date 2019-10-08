from django.core.management.base import BaseCommand
from termcolor import colored

from factories import UserFactory


class Command(BaseCommand):
    help = 'Add a user. Takes positional args, username, email, password.'

    def add_arguments(self, parser):
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
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        su = options.get('super_user')
        options = {
            'username': username,
            'email': email,
            'password': password
        }
        if su:
            options['super_user'] = True

        user = UserFactory(**options)
        print(colored(f'Successfully created {"super user" if su else "user"} <{user.username}> with password <{password}>', 'green'))
