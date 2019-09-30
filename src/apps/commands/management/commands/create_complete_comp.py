import datetime
import random
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone
from termcolor import colored

from competitions.models import Competition, Phase, CompetitionParticipant
from factories import UserFactory
from profiles.models import User as CodalabUser

from tqdm import tqdm

from faker import Faker
fake = Faker()


class Command(BaseCommand):
    help = 'Creates a specific dummy competition'

    def add_arguments(self, parser):
        parser.add_argument(
            '--owner',
            type=str,
            dest='owner',
            help='Creator of the comp',
        )
        parser.add_argument(
            '--title',
            type=str,
            dest='title',
            help='Title of the competition',
        )
        parser.add_argument(
            '--desc',
            type=str,
            dest='desc',
            help='Description of the competition',
        )
        parser.add_argument(
            '--num-phases',
            type=int,
            dest='num-phases',
            help='How many phases to create for this comp',
        )
        parser.add_argument(
            '--num-participants',
            type=int,
            dest='num-parts',
            help='How many participants to create',
        )
        parser.add_argument(
            '--num-admins',
            type=int,
            dest='num-admins',
            help='How many admins to create',
        )
        parser.add_argument(
            '--random-participants',
            type=bool,
            dest='rand-parts',
            help='Enter true for a random amount of participants. Still requires `num-parts`.',
        )
        parser.add_argument(
            '--random-admins',
            type=bool,
            dest='rand-admins',
            help='Enter true for a random amount of admins. Still requires `num-admins`.',
        )

    def handle(self, *args, **options):
        # Init specific vars
        temp_user = None  # Email of creator
        temp_title = None  # Title of Comp
        temp_desc = None
        new_comp = None  # Init this so we can check if we actually got it
        temp_admin_count = None

        if options['num-admins']:
            if options['rand-admins']:
                temp_admin_count = random.randint(0, 7)
            else:
                temp_admin_count = options['num-admins']

        # If we have a title inputed, set our title to that
        if options['title']:
            temp_title = options['title']
        else:
            temp_title = "Competition {}".format(uuid.uuid4())

        if options['desc']:
            temp_desc = options['desc']
        else:
            temp_desc = "A description for competition {}".format(temp_title)

        # If we are given a user
        if options['owner']:
            # Try to grab them and say whether we found them, alert on fail
            try:
                temp_user = CodalabUser.objects.get(email=options['owner'])
                print(colored('Succesfully found user with email: {}'.format(options['owner']), 'green'))
            except ObjectDoesNotExist:
                print(colored('Failed to find user with email: {}'.format(options['owner']), 'red'))
                raise ValueError(
                    'The user with email: `{}` was not found. Breaking...'.format(
                        options['owner']))

        # First create our competition
        try:
            new_comp = Competition.objects.create(
                title=temp_title,
                created_by=temp_user.username,
                producer=None,
                remote_id=999,
                description=temp_desc,
                published=True,
            )
            new_comp.created_when = timezone.now() + datetime.timedelta(days=random.randint(-465, 465))
            new_comp.save()
            print(colored('Succesfully created competition {}'.format(new_comp.pk), 'green'))
        except:
            print(colored('Failed to create new comp', 'red'))
            raise KeyError("Could not create competition! Breaking...")

        if options['num-phases']:
            # Create a phase for how many we have

            # Init a timeframe of a month long for phases
            temp_phase_start_date = timezone.now()
            temp_phase_end_date = timezone.now() + datetime.timedelta(days=30)

            for i in tqdm(range(options['num-phases']), ncols=100):
                # Init Phase specific vars
                temp_phase_name = "Phase_{}".format(uuid.uuid4())
                temp_phase_description = "Description for phase {}".format(temp_phase_name)

                try:
                    new_phase = Phase.objects.create(
                        name=temp_phase_name,
                        description=temp_phase_description,
                        competition=new_comp,
                        index=i,
                        start=temp_phase_start_date,
                        end=temp_phase_end_date,
                    )
                    # Increment our dates for the next phase by 1 month.
                    temp_phase_start_date = temp_phase_end_date
                    temp_phase_end_date += datetime.timedelta(random.randint(7, 45))

                except:
                    print(colored("Failed to create phase. An exception has occured.", 'red'))
                    raise KeyError("Could not create phases! Breaking...")
        else:
            temp_phase_name = "Phase_{}".format(uuid.uuid4())
            temp_phase_description = "Description for phase {}".format(temp_phase_name)

            try:
                # Create a phase that is a month long.
                new_phase = Phase.objects.create(
                    name=temp_phase_name,
                    description=temp_phase_description,
                    competition=new_comp,
                    index=0,
                    start=timezone.now(),
                    end=timezone.now() + datetime.timedelta(random.randint(7, 45)),
                )

                print(
                    colored(
                        "Succesfully created phase {0} with index {1} for competition {2} "
                        "with start-date of {3} and end-date of {4}".format(
                            new_phase.pk, new_phase.index, new_comp.pk, new_phase.start, new_phase.end
                        ),
                        'green'
                    )
                )
            except:
                print(colored("Failed to create phase. An exception has occured.", 'red'))
                raise KeyError("Could not create phases! Breaking...")

        # Create participant from Owner
        # This filter should either return an object or None!
        if len(CompetitionParticipant.objects.filter(user=temp_user, competition=new_comp)) == 0:
            try:
                new_part = CompetitionParticipant.objects.create(
                    competition=new_comp,
                    user=temp_user
                )
                print(
                    colored(
                        "Succesfully made competition participant {} for competition owner".format(new_part),
                        'green'
                    )
                )
            except:
                print(colored("Failed to create participant for competition owner.", 'red'))

        # Create `other` participants
        if options['num-parts']:
            temp_part_count = None
            if options['rand-parts']:
                # Just a random range of participants
                if temp_admin_count:
                    temp_part_count = random.randint(temp_admin_count, 57)
                else:
                    temp_part_count = random.randint(3, 57)
            else:
                temp_part_count = options['num-parts']
            print("Creating {0} participants and {1} admins...".format(temp_part_count, temp_admin_count))
            try:
                print(colored('Number of participants arg received. Creating fake participants.', 'yellow'))
                for i in tqdm(range(temp_part_count), ncols=100):

                    # Append a bit of UUID to help us get uniques
                    temp_bot_username = "{0}_{1}_{2}".format(fake.user_name(), str(uuid.uuid4())[0:8], str(uuid.uuid4())[0:8])
                    temp_bot_email = fake.email()

                    temp_bot = UserFactory(username=temp_bot_username, email=temp_bot_email)

                    # Grab our succesfully made user
                    new_bot_part = CompetitionParticipant.objects.create(
                        competition=new_comp,
                        user=temp_bot
                    )

                    if temp_admin_count:
                        if temp_admin_count > 0:
                            new_comp.admins.add(new_bot_part)
                            new_comp.save()
                            temp_admin_count -= 1
                print(
                    colored("Successfully created all participants")
                )
            except:
                print(
                    colored(
                        'Failed to make fake bot participants!',
                        'red'
                    )
                )

        print(colored("Completed all operations succesfully.", 'green'))
