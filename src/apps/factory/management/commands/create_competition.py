import uuid

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from competitions.models import Competition, Phase, Submission
from datasets.models import DataGroup, Data


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        try:
            new_comp = Competition.objects.create(title="Competition {}".format(uuid.uuid4()),
                                                  created_by="User_{}".format(uuid.uuid4()),
                                                  created_when=timezone.now(), remote_id=999)
            self.stdout.write(self.style.SUCCESS('Successfully created competition "%s"' % new_comp))
        except:
            self.stdout.write(self.style.SUCCESS('Failed to create competition'))
