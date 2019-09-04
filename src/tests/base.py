import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth import get_user_model

User = get_user_model()


class ChahubTestHelpersMixin:

    def login(self):
        User.objects.create_user(username='test', password='test')
        self.get(reverse('login'))
        self.find("#id_username").send_keys("test")
        self.find("#id_password").send_keys("test")
        self.find(".submit.button").click()
        self.assertTrue(self.selenium.find_element_by_css_selector('#searchbar > input[type="text"]'))


@pytest.mark.e2e
class SeleniumTestCase(ChahubTestHelpersMixin, StaticLiveServerTestCase):
    urls = 'urls'  # TODO: what the F is this???
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        # Wait 10 seconds for elements to appear, always
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.selenium.set_window_size(800, 600)

    def get(self, url):
        #  live_server_url will be a random localhost:5digits/
        return self.selenium.get('%s%s' % (self.live_server_url, url))

    def find(self, selector):
        return self.selenium.find_element_by_css_selector(selector)

    def circleci_screenshot(self, name="screenshot.png"):
        circle_dir = os.environ.get('CIRCLE_ARTIFACTS')
        assert circle_dir, "Could not find CIRCLE_ARTIFACTS environment variable!"
        self.selenium.get_screenshot_as_file(os.path.join(circle_dir, name))

    def assertCurrentUrl(self, url):
        # url = 'your/site/here/'  and live_server_url = http://localhost:5digits
        return self.assertEquals(self.selenium.current_url, f"{self.live_server_url}{url}")

    def assertLinkTextExists(self, text):
        self.assertTrue(self.selenium.find_element_by_link_text(text))
