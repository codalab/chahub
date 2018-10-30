from time import sleep

import traceback
from django.core.management.base import BaseCommand
from termcolor import colored
from tqdm import tqdm

from competitions.models import Competition


import logging
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    help = 'Updates competition details in ES'

    def handle(self, *args, **options):
        qs = Competition.objects.exclude(is_active=False)
        qs = qs.prefetch_related('phases')
        for comp in tqdm(qs):
            try:
                old_deadline, old_is_active = comp.current_phase_deadline, comp.is_active
                comp.current_phase_deadline = comp.get_current_phase_deadline()
                comp.is_active = comp.get_is_active()
                if comp.is_active != old_is_active or comp.current_phase_deadline != old_deadline:
                    comp.save()
                    print("Updating competition: {}".format(comp.pk))
            except:
                traceback.print_exc()
                print(colored("Failed to save/update competition.", 'red'))
        print(colored("Competition details finished updating.", 'green'))
