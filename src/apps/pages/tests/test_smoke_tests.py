from django.test import TestCase
from django.urls import reverse


class SmokeTests(TestCase):

    def test_index_page(self):
        assert self.client.get(reverse('index')).status_code == 200
