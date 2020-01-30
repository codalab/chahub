import factory
from django.db.models import signals
from django.urls import reverse
from api.urls import router
from django.core.management import call_command
from django.db import connection
from django.test.utils import override_settings
from django.db import reset_queries
from rest_framework.test import APITestCase

LIST_MAX_QUERY_COUNTS = {}
DETAIL_MAX_QUERY_COUNTS = {
    "Competition": 20
}


class MaxQueryTestCase(APITestCase):
    def setUp(self):
        all_urls = router.get_urls()
        self.list_routes = [url for url in all_urls if url.name.split('-')[-1] == 'list']
        self.detail_routes = [url for url in all_urls if url.name.split('-')[-1] == 'detail']

        self._generate_data()

    @factory.django.mute_signals(signals.post_save)
    def _generate_data(self):
        call_command('generate_data')

    def assert_max_query_count(self, url, max_count=5):
        reset_queries()
        self.client.get(url)
        assert len(connection.queries) <= max_count, f"{url} queries: {len(connection.queries)}"


class TestApiQueryCount(MaxQueryTestCase):
    @override_settings(DEBUG=True)
    def test_api_query_count_on_list_endpoints(self):
        for route in self.list_routes:
            # Using object relations, figure out our model for the route
            viewset_class = route.callback.cls
            serializer_class = viewset_class.serializer_class
            model_class = serializer_class.Meta.model

            # Using __name__, get our query count max or default to 5
            max_count = LIST_MAX_QUERY_COUNTS.get(model_class.__name__, 6)

            reversed_url = reverse(route.name, kwargs={'version': 'v1'})
            self.assert_max_query_count(reversed_url, max_count)

    @override_settings(DEBUG=True)
    def test_api_query_count_on_detail_endpoints(self):
        for route in self.detail_routes:
            # Using object relations, figure out our model for the route
            viewset_class = route.callback.cls
            serializer_class = viewset_class.serializer_class
            model_class = serializer_class.Meta.model

            # Using __name__, get our query count max or default to 10
            max_count = DETAIL_MAX_QUERY_COUNTS.get(model_class.__name__, 10)

            # Loop through our objects, and make sure each one is below our threshold
            instance = model_class.objects.first()
            if not instance:
                continue  # Some list data doesn't get created?
            reversed_url = reverse(route.name, kwargs={'version': 'v1', 'pk': instance.pk})
            self.assert_max_query_count(reversed_url, max_count)
