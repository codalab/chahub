import datetime
import random
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone
from termcolor import colored
from tqdm import tqdm

from competitions.models import Competition
from profiles.models import User as CodalabUser


class Command(BaseCommand):
    help = 'Updates competition details in ES'

    # def add_arguments(self, parser):
        # Named (optional) arguments
        # parser.add_argument(
        #     '--number',
        #     type=int,
        #     dest='amount',
        #     help='Amount of comps/users to create',
        # )

    def handle(self, *args, **options):

        for comp in tqdm(Competition.objects.all()):
            try:
                comp.save()
            except:
                print(colored("Failed to save/update competition.", 'red'))
        print(colored("Competition details finished updating.", 'green'))
