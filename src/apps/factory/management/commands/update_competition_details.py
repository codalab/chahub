from django.core.management.base import BaseCommand
from termcolor import colored
from tqdm import tqdm

from competitions.models import Competition


class Command(BaseCommand):
    help = 'Updates competition details in ES'

    def handle(self, *args, **options):

        for comp in tqdm(Competition.objects.all()):
            try:
                old_deadline, old_is_active = comp.current_phase_deadline, comp.is_active
                comp.current_phase_deadline = comp.get_current_phase_deadline()
                comp.is_active = comp.get_is_active()
                if comp.is_active != old_is_active or comp.current_phase_deadline != old_deadline:
                    comp.save()
                    print("Updating competition: {}".format(comp.pk))
            except:
                print(colored("Failed to save/update competition.", 'red'))
        print(colored("Competition details finished updating.", 'green'))
