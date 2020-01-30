from ..utils import SeleniumTestCase


class TestLogin(SeleniumTestCase):

    def test_login_using_selenium(self):
        #  Starts a new window for Chrome and logs in a user
        self.login()
