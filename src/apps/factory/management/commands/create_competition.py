import datetime
import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone
from termcolor import colored

from competitions.models import Competition, Phase, CompetitionParticipant
from profiles.models import User as CodalabUser

from tqdm import tqdm

from faker import Faker
fake = Faker()


def _create_fake_user():
    try:
        # Usernames will be in the format <some_username><some_number> IE: shieldshannah53
        temp_email = fake.safe_email()
        temp_email = "{0}{1}{2}".format(temp_email.split('@')[0] + "@", random.randint(1, 9999), temp_email.split('@')[1])
        new_user = CodalabUser.objects.create(
            username="{0}{1}".format(fake.user_name(), random.randint(1, 9999)),
            name=fake.name(),
            email=temp_email,
        )
        # print(colored("Successfully created new user!", 'green'))
        return new_user
    except:
        print(colored("Could not create fake user! Operation failed!", 'red'))
        raise ObjectDoesNotExist("Could not create fake user! Operation failed!")


def _create_fake_participant(competition):
    try:
        new_user = _create_fake_user()
        new_part = CompetitionParticipant.objects.create(
            competition=competition,
            user=new_user
        )
        # print(colored("Successfully created new participant!", 'green'))
        return new_part
    except:
        print(colored("Could not create fake participant! Operation failed!", 'red'))
        raise ObjectDoesNotExist("Could not create fake participant! Operation failed!")


def _stringdate_to_datetime(str_date):
    datetime_object = datetime.datetime.strptime(str_date, "%m-%d-%Y:%H-%M-%S")
    return datetime_object


# Function should take some defaults, options dictionary,
#  and dictionary key and set a value accordingly in the data dictionary.
def _check_data_key(options, options_key, data, data_key, default_value, is_date=False):
    # If we're not passed options or we don't have an options key to check, set value to default
    if not options or not options_key:
        data[data_key] = default_value
    # If options contains the key we're looking for
    elif options.get(options_key):
        # If it's a date try to format it, else just set to value
        if is_date:
            data[data_key] = _stringdate_to_datetime(options[options_key])
        else:
            data[data_key] = options[options_key]
    # Else if we don't have anything in the data for the object, set it to the default value
    elif not data.get(data_key):
        data[data_key] = default_value


def _create_competition(full_details, data):
    if full_details:
        # should_have_prize = random.randint(1, 4) == 4
        # if not should_have_prize:
        #     data['prize'] = None
        fake_url = 'competitions/{0}/'.format(random.randint(0, 9999))
        temp_competition = Competition.objects.create(
            created_by=data['creator'].username,
            created_when=data['created_when'],
            start=data['start'],
            title=data['title'],
            description=data['desc'],
            end=data['end'],
            prize=data['prize'],
            url="{0}://{1}/{2}".format('http', fake.domain_name(), fake_url),
            remote_id=999,
            is_active=True,
            published=True,
        )
    else:
        temp_competition = Competition.objects.create(
            created_by=data['creator'].username,
            title=data['title'],
            description=data['desc'],
            remote_id=999,
            published=True,
        )
    # print(colored("Successfully created new competition", 'green'))
    return temp_competition


class Command(BaseCommand):
    help = 'Your one stop shop for creating test competitions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            dest='amount',
            help='Amount of competitions to create. If creating multiple title/desc/owner/start/end/created_when are ignored as are phases.'
        )

        parser.add_argument(
            '--fail-on-exception',
            type=bool,
            dest='fail-on-exception',
            help='Should this command fail if it hits a minor exception? (Not providing number of phases/etc, else default to 1)'
        )

        parser.add_argument(
            '--owner-email',
            type=str,
            dest='owner-email',
            help='A users email to designate them as the creator',
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
            dest='phases',
            help='How many phases to create for this comp. If not supplied will generate a random amount.',
        )

        parser.add_argument(
            '--num-participants',
            type=int,
            dest='participants',
            help='How many participants to create for this comp. If not supplied will generate a random amount.',
        )

        parser.add_argument(
            '--num-admins',
            type=int,
            dest='admins',
            help='How many admins to create for this comp. If not supplied will generate a random amount.',
        )

        parser.add_argument(
            '--created-when',
            type=str,
            dest='created-when',
            help='String date of when competition should be marked as created. Leave blank for today/now. Format: DD-MM-YYYY:HH-MM-SS',
        )

        parser.add_argument(
            '--start',
            type=str,
            dest='start',
            help='String starting date of the competition. Leave blank for random date in the future. Format: DD-MM-YYYY:HH-MM-SS',
        )

        parser.add_argument(
            '--end',
            type=str,
            dest='end',
            help='String ending date of the competition. Leave blank for random date in the future. Format: DD-MM-YYYY:HH-MM-SS',
        )

        parser.add_argument(
            '--prize',
            type=int,
            dest='prize',
            help='Prize amount. Usually dollars/euros. Leave blank for a random number between $100 and $5000'
        )

        parser.add_argument(
            '--fill-all-details',
            type=bool,
            dest='fill-all-details',
            help="Boolean: False for simple competitions, True for filling in all the details"
        )

    def handle(self, *args, **options):
        # Check whether we're creating multiple competitions or one
        if options['amount'] and options['amount'] > 0:
            # We're creating multiple competitions
            # print("Do somethign")

            for i in tqdm(range(options['amount']), ncols=100):
                # Reset our data each time
                data = {
                    'creator': None,
                    'admin_count': None,
                    'part_count:': None,
                    'desc': None,
                    'title': None,
                    'phase_count': None,
                    'created_when': None,
                    'start': None,
                    'end': None,
                    'prize': None
                }

                if not data['creator']:
                    data['creator'] = _create_fake_user()

                # def _check_data_key(options, options_key, data, data_key, default_value, is_date=False):

                _check_data_key(options, 'title', data, 'title', fake.catch_phrase())

                _check_data_key(options, 'desc', data, 'desc', fake.text(max_nb_chars=200, ext_word_list=None))

                _check_data_key(options, 'phases', data, 'phase_count', random.randint(1, 7))

                _check_data_key(options, 'participants', data, 'part_count', random.randint(5, 17))

                _check_data_key(options, 'admins', data, 'admin_count', random.randint(1, 5))

                _check_data_key(options, 'created-when', data, 'created_when', timezone.now())

                _check_data_key(options, 'start', data, 'start',
                                timezone.now() + datetime.timedelta(days=random.randint(1, 35)), is_date=True)

                _check_data_key(options, 'end', data, 'end',
                                data['start'] + datetime.timedelta(days=random.randint(7, 475)), is_date=True)

                # if we don't pass prize parameter
                if not options.get('prize'):
                    # 1 in 4 will randomly get a prize, else None
                    should_have_prize = random.randint(1, 4) == 4
                    if should_have_prize:
                        data['prize'] = random.randint(100, 5000)
                    else:
                        data['prize'] = None
                else:
                    data['prize'] = options['prize']

                # _check_data_key(None, None, data, 'prize', random.randint(100, 5000))

                competition = _create_competition(options['fill-all-details'], data)

                for i in tqdm(range(data['part_count']), ncols=100):
                    _create_fake_participant(competition)

                for i in tqdm(range(data['admin_count']), ncols=100):
                    temp_part = _create_fake_participant(competition)
                    competition.admins.add(temp_part)

                competition.participant_count = CompetitionParticipant.objects.filter(competition=competition).count()

                # Init some random dates for our first phase
                temp_phase_start = timezone.now() + datetime.timedelta(days=random.randint(1, 35))
                temp_phase_end = temp_phase_start + datetime.timedelta(days=random.randint(1, 35))

                for i in tqdm(range(data['phase_count']), ncols=100):
                    try:
                        Phase.objects.create(
                            name=fake.company_suffix(),
                            description=fake.catch_phrase(),
                            competition=competition,
                            index=i,
                            start=temp_phase_start,
                            end=temp_phase_end,
                        )
                        # Subsequent phases will start when the last ended, and have a random end-date up to 35 days after
                        temp_phase_start = temp_phase_end
                        temp_phase_end = temp_phase_start + datetime.timedelta(days=random.randint(1, 35))
                    except:
                        print(colored("Could not create phase! Operation failed!", 'red'))
                        raise ObjectDoesNotExist("Could not create phase! Operation failed!")
                competition.save()

        else:

            data = {
                'creator': None,
                'admin_count': None,
                'part_count:': None,
                'desc': None,
                'title': None,
                'phase_count': None,
                'created_when': None,
                'start': None,
                'end': None,
                'prize': None
            }

            # We're only creating one competition. If owner-email arg is used, find that user.
            # If not found create a random user if we're not failing easy
            if options['owner-email']:
                try:
                    data['creator'] = CodalabUser.objects.get(email=options['owner-email'])
                except ObjectDoesNotExist:
                    # We failed to find that user, check fail easy
                    if options['fail-on-exception']:
                        print(colored("Could not find a user associated with that email!", 'red'))
                        raise ObjectDoesNotExist("Could not find a user associated with the supplied email!")
            # We either have a found user, failed to find a user, or have not done anything yet.
            # Double check that we assign a value to temp_creator at this point if it doesn't exist
            if not data['creator']:
                data['creator'] = _create_fake_user()

            _check_data_key(options, 'title', data, 'title', fake.catch_phrase())

            _check_data_key(options, 'desc', data, 'desc', fake.text(max_nb_chars=200, ext_word_list=None))

            _check_data_key(options, 'phases', data, 'phase_count', random.randint(1, 7))

            _check_data_key(options, 'participants', data, 'part_count', random.randint(5, 17))

            _check_data_key(options, 'admins', data, 'admin_count', random.randint(1, 5))

            _check_data_key(options, 'created-when', data, 'created_when', timezone.now(), True)

            _check_data_key(options, 'start', data, 'start', timezone.now() + datetime.timedelta(days=random.randint(1, 35)), True)

            _check_data_key(options, 'end', data, 'end', data['start'] + datetime.timedelta(days=random.randint(7, 475)), True)

            # Check Prize data. Default 100-5000

            _check_data_key(options, 'prize', data, 'prize', random.randint(100, 5000))

            competition = _create_competition(options['fill-all-details'], data)

            for i in tqdm(range(data['part_count']), ncols=100):
                _create_fake_participant(competition)

            for i in tqdm(range(data['admin_count']), ncols=100):
                temp_part = _create_fake_participant(competition)
                competition.admins.add(temp_part)

            competition.participant_count = CompetitionParticipant.objects.filter(competition=competition).count()

            # Init some random dates for our first phase
            temp_phase_start = timezone.now() + datetime.timedelta(days=random.randint(1, 35))
            temp_phase_end = temp_phase_start + datetime.timedelta(days=random.randint(1, 35))

            for i in tqdm(range(data['phase_count']), ncols=100):
                try:
                    Phase.objects.create(
                        name=fake.company_suffix(),
                        description=fake.catch_phrase(),
                        competition=competition,
                        index=i,
                        start=temp_phase_start,
                        end=temp_phase_end,
                    )
                    # Subsequent phases will start when the last ended, and have a random end-date up to 35 days after
                    temp_phase_start = temp_phase_end
                    temp_phase_end = temp_phase_start + datetime.timedelta(days=random.randint(1, 35))
                    # print(colored("Successfully created a phase!", 'green'))
                except:
                    print(colored("Could not create phase! Operation failed!", 'red'))
                    raise ObjectDoesNotExist("Could not create phase! Operation failed!")
            competition.save()
