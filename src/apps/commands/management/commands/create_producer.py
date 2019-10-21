from django.core.management.base import BaseCommand
from termcolor import colored

from factories import ProducerFactory


class Command(BaseCommand):
    help = 'Add a producer.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--name',
            type=str,
            help='Producer Name (optional)',
        )

        parser.add_argument(
            '-c',
            '--contact-email',
            type=str,
            help='Producer contact email (optional)',
        )

        parser.add_argument(
            '-u',
            '--url',
            type=str,
            help='Producer URL (optional)',
        )

        parser.add_argument(
            '-k',
            '--api-key',
            type=str,
            help='Api key for Producer (optional)',
        )

    def handle(self, *args, **options):
        name = options.get('name')
        contact = options.get('contact_email')
        url = options.get('url')
        api_key = options.get('api_key')
        options = {}
        if name:
            options['name'] = name
        if contact:
            options['contact'] = contact
        if url:
            options['url'] = url
        if api_key:
            options['api_key'] = api_key

        producer = ProducerFactory(**options)
        print(colored(f'Successfully created Producer <{producer.name}> with API Key <{str(producer.api_key)}>', 'green'))
