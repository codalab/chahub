from django.urls import reverse
from api.urls import router as Router
from django.core.management import call_command
from django.db import connection
from django.test.utils import override_settings
from django.db import reset_queries
from rest_framework.test import APITestCase

LIST_MAX_QUERY_COUNTS = {}
DETAIL_MAX_QUERY_COUNTS = {
    "Competition": 20
}


class MaxQueryTestCase(object):
    def setUp(self):
        all_urls = Router.get_urls()
        self.list_routes = [url for url in all_urls if url.name.split('-')[-1] == 'list']
        self.detail_routes = [url for url in all_urls if url.name.split('-')[-1] == 'detail']

        self._generate_data()

    def _generate_data(self):
        pass

    def _assert_max_query_count(self, reversed_url, max_count=5):
        reset_queries()
        self.client.get(reversed_url)
        print("Connection queries length for api endpoint {0}: {1}".format(reversed_url, len(connection.queries)))
        assert len(connection.queries) <= max_count


class TestApiQueryCount(MaxQueryTestCase, APITestCase):

    def _generate_data(self):
        call_command('create_competition', amount=50, fill_all_details=True, fail_on_exception=True)

    @override_settings(DEBUG=True)
    def test_api_query_count_on_list_endpoints(self):
        for route in self.list_routes:
            # Using object relations, figure out our model for the route
            viewset_class = route.callback.cls
            serializer_class = viewset_class.serializer_class
            model_class = serializer_class.Meta.model

            # Using __name__, get our query cout max or default to 5
            max_count = LIST_MAX_QUERY_COUNTS.get(model_class.__name__, 6)

            reversed_url = reverse('api:{}'.format(route.name), kwargs={'version': 'v1'})

            self._assert_max_query_count(reversed_url, max_count)

    @override_settings(DEBUG=True)
    def test_api_query_count_on_detail_endpoints(self):
        for route in self.detail_routes:
            # Using object relations, figure out our model for the route
            viewset_class = route.callback.cls
            serializer_class = viewset_class.serializer_class
            model_class = serializer_class.Meta.model

            # Using __name__, get our query cout max or default to 10
            max_count = DETAIL_MAX_QUERY_COUNTS.get(model_class.__name__, 10)

            # Loop through our objects, and make sure each one is below our threshold
            for instance in model_class.objects.all():
                reversed_url = reverse('api:{}'.format(route.name), kwargs={'version': 'v1', 'pk': instance.pk})
                self._assert_max_query_count(reversed_url, max_count)
