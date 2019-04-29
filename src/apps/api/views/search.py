from elasticsearch_dsl import Search
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api.caching import QueryParamsKeyConstructor
from utils.search import get_search_client, get_results, get_default_search_results

# TODO: This is farily UN-DRY so far. We should probably by default exclude published=False...
EXTRA_FILTERS = {
    'competitions': {
        'filter': {
            'args': ('term',),
            'kwargs': {
                'published': True
            }
        },
        'source': {
            'kwargs': {
                'excludes': ["html_text"]
            }
        }
    },
    'tasks': {
        'filter': {
            'args': ('term',),
            'kwargs': {
                'published': True
            }
        }
    },
    'solutions': {
        'filter': {
            'args': ('term',),
            'kwargs': {
                'published': True
            }
        }
    },
    'datasets': {
        'filter': {
            'args': ('term',),
            'kwargs': {
                'published': True
            }
        }
    },
}


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

        # Do we even have anything to search with?
        filters = (
            query,
            sorting,
            date_flags,
            start,
            end,
            producer,
        )
        empty_search = all(not f for f in filters)

        # Get results and prepare them
        data = {
            "results": [],
            "showing_default_results": False,
        }

        if not empty_search:
            # Setup ES connection, excluding HTML text from our results
            if object_types != 'ALL' or 'ALL' not in object_types:
                object_types = [obj.strip() for obj in object_types.split(',')]
                ms = get_search_client(multi=True)
                for obj_type in object_types:
                    new_search = Search(index=obj_type)
                    extra_filters = EXTRA_FILTERS.get(obj_type, {})
                    for filter_type in extra_filters:
                        args = extra_filters[filter_type].get('args', ())
                        kwargs = extra_filters[filter_type].get('kwargs', {})
                        if filter_type == 'filter':
                            new_search.filter(*args, **kwargs)
                        if filter_type == 'source':
                            new_search.source(*args, **kwargs)
                    # Do search/filtering/sorting
                    new_search = self._search(new_search, query, obj_types=[obj_type])
                    new_search = self._filter(new_search, date_flags, start, end, producer, obj_types=[obj_type])
                    new_search = self._sort(new_search, sorting, query, obj_types=[obj_type])
                    ms = ms.add(new_search)
                data["results"] = get_results(ms, multi=True)
            else:
                # Do search/filtering/sorting
                s = get_search_client()
                s = self._search(s, query)
                s = self._filter(s, date_flags, start, end, producer)
                s = self._sort(s, sorting, query)
                data["results"] = get_results(s)

        if not data["results"] or empty_search:
            data["showing_default_results"] = True
            data["results"] = get_default_search_results()

        return Response(data)

    def _search(self, search, query, obj_types='ALL'):
        if query and query != ' ':
            fields = []
            if 'competitions' in obj_types or obj_types == 'ALL':
                fields += ["title^5", "description^3", "html_text^2", "created_by"]
            if 'users' in obj_types or obj_types == 'ALL':
                fields += ["username^5", "name^3", "bio^2", "company"]
            if 'profiles' in obj_types or obj_types == 'ALL':
                fields += ["email", "producer", "remote_id"]
            # Remove duplicates
            fields = list(set(fields))
            search = search.query(
                "multi_match",
                query=query,
                type="best_fields",
                fuzziness=1,
                # We cast to a set first to remove any duplicates.
                fields=fields
            )
            # s = s.highlight('title', fragment_size=50)
            # s = s.suggest('suggestions', query, term={'field': 'title'})
        return search

    def _filter(self, search, date_flags, start, end, producer, obj_types='ALL'):
        if 'competitions' in obj_types or obj_types == 'ALL':
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
        if 'competitions' in obj_types or obj_types=='ALL':
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
