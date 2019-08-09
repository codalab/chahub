from elasticsearch_dsl import Search
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api.caching import QueryParamsKeyConstructor
from utils.search import get_search_client, get_results, get_default_search_results

# from apps.search.documents import CompetitionDocument, UserDocument, ProfileDocument, TaskDocument, SolutionDocument, DatasetDocument
from apps.search.documents import CompetitionDocument, ProfileDocument

OBJECT_LIST = [
    'profile',
    'competition',
    'task',
    'dataset',
    'solution',
    'user',
]

class SearchView(APIView):
    @cache_response(key_func=QueryParamsKeyConstructor(), timeout=60)
    def get(self, request, version="v1"):
        # Get search data
        query = request.GET.get('q', '')
        object_types = request.GET.get('object_types', 'ALL')
        sorting = request.GET.get('sorting')
        date_flags = request.GET.get('date_flags')
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        producer = request.GET.get('producer')
        page = request.GET.get('page', 1)
        if type(page) != int:
            try:
                page = int(page) if int(page) > 0 else 1
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
            object_types,
        )
        empty_search = all(not f for f in filters)

        # Get results and prepare them
        data = {
            "results": [],
            "showing_default_results": False,
        }

        print("Empty search?: {}".format(empty_search))

        if not empty_search:
                object_types = [obj.strip() for obj in object_types.split(',')]
                s = get_search_client(100, page)
                s = self._search(s, query, object_types)
                s = self._filter(s, date_flags, start, end, producer, object_types)
                s = self._sort(s, sorting, query, object_types)
                matching_types = []
                if object_types and object_types != 'ALL' and 'ALL' not in object_types:
                    for object_type in object_types:
                        matching_types.append({'match': {'_obj_type': object_type}})
                else:
                    for object_type in OBJECT_LIST:
                        matching_types.append({'match': {'_obj_type': object_type}})
                s = s.query('bool', should=matching_types, minimum_should_match=1)
                data["results"] = get_results(s)
        return Response(data)

    def _search(self, search, query, obj_types='ALL'):
        if query and query != ' ':
            fields = []
            if 'competition' in obj_types:
                fields += ["title^3", "description^2", "html_text^2", "created_by"]
            if 'user' in obj_types:
                fields += ["email^3", "username^3", "name^3"]
            if 'profile' in obj_types:
                fields += ["email^3", "username^3", "name^3"]
            if obj_types == 'ALL' or 'ALL' in obj_types:
                fields += ['title^3', 'username^3', 'name^3']
            # Remove duplicates
            fields = list(set(fields))
            search = search.query(
                "multi_match",
                query=query,
                type="best_fields",
                fuzziness=5,
                # We cast to a set first to remove any duplicates.
                fields=fields
            )
        return search

    def _filter(self, search, date_flags, start, end, producer, obj_types='ALL'):
        if 'competition' in obj_types:
            # This month/this year
            if date_flags == "this_month":
                search = search.filter('range', start={
                    'gte': "now/M",
                    'lte': "now/M",
                })
            if date_flags == "this_year":
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

    def _sort(self, search, sorting, query, obj_types='ALL'):
        # Make an empty list for our parameters
        sort_params = []
        if 'competition' in obj_types:
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
