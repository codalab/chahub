from django.test import TestCase


class SmokeTests(TestCase):

    def test_index_page(self):
        assert self.client.get('/').status_code == 200
