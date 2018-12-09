from tests.base import SeleniumTestCase
from producers.models import Producer
from competitions.models import Competition
from django.urls import reverse
from time import sleep


class TestChangingProviderAndResultsChange(SeleniumTestCase):

    def test_setup_and_login_as_user(self):
        #  Starts a new window for Chrome
        #  Assures they can login
        self.get(reverse('login'))
        self.login()
        self.assertCurrentUrl('/?')

    def test_logging_in_as_producer(self):
        #  Discovered how to do so on accident, might as well go with it now wheee
        self.get(reverse('producers:management'))
        self.login()
        self.assertCurrentUrl(reverse('producers:management'))

    def test_changing_provider_changes_url(self):
        #  Creates Two Providers, and Two Competitions
        #  Assign Competitions to the two separate Providers - "tag" them through the url
        prod1 = Producer.objects.create(name='Prod1Testing')
        comp1 = Competition.objects.create(title='Fake Competition1',
                                           producer=prod1,
                                           is_active=True,
                                           published=True,
                                           url='http://www.test.org')
        prod2 = Producer.objects.create(name='Prod2Testing')
        comp2 = Competition.objects.create(title='Even Faker Competition2',
                                           producer=prod2,
                                           is_active=True,
                                           published=True,
                                           url='http://www.test2.org')
        #  Go to the homepage and assert that the URL is correct - index without any producers selected
        self.get('/')
        self.assertCurrentUrl('/?')
        #  Click the Producer drop-down bar and click the 4th child - Producer1
        #  Need a half second to load the dropdown bar
        self.find('#advanced_search_button[ref="producer_filter"]').click()
        sleep(.5)
        self.find('#advanced_search_button[ref="producer_filter"] *:nth-child(4)').click()
        #  Confirm that the URL at index loads the proper competition
        #  Assert that the URL has changed to the producer1's number, and that producer2 doesn't show up
        self.assertIsNot(self.selenium.find_element_by_link_text('test.org'), self.selenium.current_url)
        self.assertIn(f"/?producer={prod1.pk}", self.selenium.current_url)
        #  Chigga chigga now flip it and reverse it
        #  Need a half second to load the dropdown bar
        self.find('#advanced_search_button[ref="producer_filter"]').click()
        sleep(.5)
        self.find('#advanced_search_button[ref="producer_filter"] *:nth-child(5)').click()
        self.assertIsNot(self.selenium.find_element_by_link_text('test2.org'), self.selenium.current_url)
        self.assertIn(f"/?producer={prod2.pk}", self.selenium.current_url)


