from tests.base import SeleniumTestCase
from producers.models import Producer
from competitions.models import Competition
from time import sleep
from django.test.utils import override_settings


@override_settings(DEBUG=True)
class TestChangingProviderAndResultsChange(SeleniumTestCase):

    def test_setup_and_login_as_user(self):
        #  Starts a new window for Chrome
        self.login()

    def test_changing_provider_changes_url_and_search_results(self):
        #  Creates Two Providers, and Two Competitions
        #  Assign Competitions to the two separate Providers - "tag" them through the url
        prod1 = Producer.objects.create(
            name='Prod1Testing'
        )
        comp1 = Competition.objects.create(
            title='Fake Competition1',
            producer=prod1,
            is_active=True,
            published=True,
            url='http://www.test.org'
                                           )
        prod2 = Producer.objects.create(
            name='Prod2Testing'
        )
        comp2 = Competition.objects.create(
            title='Even Faker Competition2',
            producer=prod2,
            is_active=True,
            published=True,
            url='http://www.test2.org'
        )

        #  Go to the homepage and assert that the URL is correct - index without any producers selected
        self.get('')
        self.circleci_screenshot('After_getting_webpage.png')

        sleep(.5)

        #  Click the Producer drop-down bar and click the 4th child - Producer1
        #  Need a half second to load the dropdown bar
        self.circleci_screenshot('Before_clicking_Prod1.png')
        self.find('#advanced_search_button[ref="producer_filter"]').click()
        self.circleci_screenshot('After_clicking_Prod1.png')
        sleep(.5)
        self.find('#advanced_search_button[ref="producer_filter"] *:nth-child(4)').click()

        #  Confirm that the URL at index loads the proper competition
        #  Assert that the URL has changed to the producer1's search results and filtered out unwanted search results
        self.assertIn(f"producer={prod1.pk}", self.selenium.current_url)
        self.assertLinkTextExists('test.org')

        #  Click the Producer drop-down bar and click the 4th child - Producer1
        #  Need a half second to load the dropdown bar
        sleep(.5)
        self.find('#advanced_search_button[ref="producer_filter"]').click()
        sleep(.5)
        self.find('#advanced_search_button[ref="producer_filter"] *:nth-child(5)').click()

        #  Assert that the URL has changed to the producer2's search results and filtered out unwanted search results
        self.assertIn(f"producer={prod2.pk}", self.selenium.current_url)
        self.assertLinkTextExists('test2.org')
