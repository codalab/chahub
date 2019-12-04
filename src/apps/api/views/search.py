from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api.caching import QueryParamsKeyConstructor
from utils.search import get_search_client, get_results, get_default_search_results


class SearchView(APIView):

    @cache_response(key_func=QueryParamsKeyConstructor(), timeout=60)
    def get(self, request, version="v1"):
        # Get search data
        query = request.query_params.get('q', '')
        sorting = request.query_params.get('sorting')
        date_flags = request.query_params.get('date_flags')
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')
        producer = request.query_params.get('producer')
        index = request.query_params.getlist('index[]')
        page = request.query_params.get('page', 1)
        try:
            page = max(int(page), 1)
        except ValueError:
            page = 1

        # Do we even have anything to search with?
        filters = (
            query,
            sorting,
            date_flags,
            start,
            end,
            producer,
            index,
        )
        empty_search = not any(filters)

        # Get results and prepare them
        data = {
            "results": [],
            "showing_default_results": False,
        }

        if not empty_search:
            # Setup ES connection, excluding HTML text from our results
            s = get_search_client(page=page, index=index)

            # Do search/filtering/sorting
            s = self._search(s, query)
            s = self._filter(s, date_flags, start, end, producer)
            s = self._sort(s, sorting, query)
            search_results = get_results(s)
        else:
            data["showing_default_results"] = True
            search_results = get_default_search_results()

        data["results"] = search_results["results"]
        data["total"] = search_results["total"]
        return Response(data)

    def _search(self, search, query):
        if query and query != ' ':
            search = search.query(
                "multi_match",
                query=query,
                type="best_fields",
                fuzziness=1,
                fields=["title^5", "name^5", "description^3", "html_text^2", "created_by"]
            )
        return search

    def _filter(self, search, date_flags, start, end, producer):
        # This month/this year
        if date_flags == "this_month":
            search = search.filter('range', start={
                'gte': "now/M",
                'lte': "now/M",
            })
        elif date_flags == "this_year":
            search = search.filter('range', start={
                'gte': "now/y",
                'lte': "now/y",
            })

        # Start/end range
        date_args = {}
        if start:
            date_args['gte'] = start
        if end:
            date_args['lte'] = end
        if date_args:
            date_args['format'] = 'date_optional_time'
            search = search.filter('range', start=date_args)

        # Active competitions, ones with submissions in the last 30 days
        if date_flags and date_flags == "active":
            search = search.filter('term', is_active=True)
        if producer:
            search = search.filter('term', producer__id=producer)
        return search

    def _sort(self, search, sorting, query):
        # Make an empty list for our parameters
        sort_params = []
        if sorting == 'participant_count':
            sort_params.append('-participant_count')
        elif sorting == 'prize':
            sort_params.append('-prize')
        elif sorting == 'deadline':
            sort_params.append('current_phase_deadline')

        # If '_score' is the first sort parameter, the participant sorting gets overridden and the results are mostly
        # relevancy based instead of being based on whatever sorting we desire. Append it last here.
        if query:
            sort_params.append('_score')
        return search.sort(*sort_params)
