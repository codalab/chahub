import datetime
import random
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from competitions.models import Competition


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            new_comp = Competition.objects.create(title="Competition {}".format(uuid.uuid4()),
                                                  created_by="User_{}".format(uuid.uuid4()), remote_id=999)
            new_comp.created_when = timezone.now() + datetime.timedelta(days=random.randint(-15, 15))
            new_comp.save()
            self.stdout.write(self.style.SUCCESS('Successfully created competition "%s"' % new_comp))
        except:
            self.stdout.write(self.style.SUCCESS('Failed to create competition'))
