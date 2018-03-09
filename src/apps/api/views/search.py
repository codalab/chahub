from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api.caching import QueryParamsKeyConstructor


class SearchView(APIView):

    def _search(self, search, query):
        if query and query != ' ':
            search = search.query(
                "multi_match",
                query=query,
                type="best_fields",
                fuzziness='auto',
                fields=["title^5", "description", "html_text", "created_by"]
            )
            # s = s.highlight('title', fragment_size=50)
            # s = s.suggest('suggestions', query, term={'field': 'title'})
        return search

    def _filter(self, search, date_flags, start, end):
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
        return search

    def _sort(self, search, sorting, query):
        if sorting == 'participant_count':
            if query:
                search = search.sort('_score', '-participant_count')
            else:
                search = search.sort('-participant_count')
        elif sorting == 'prize':
            if query:
                search = search.sort('_score', '-prize')
            else:
                search = search.sort('-prize')
        elif sorting == 'deadline':
            if query:
                search = search.sort('_score', 'current_phase_deadline')
            else:
                search = search.sort('current_phase_deadline')
        return search


    @cache_response(key_func=QueryParamsKeyConstructor(), timeout=60)
    def get(self, request, version="v1"):
        if 'q' not in request.GET:
            return Response()

        SIZE = 20

        # Get search data
        query = request.GET.get('q')
        sorting = request.GET.get('sorting')
        date_flags = request.GET.get('date_flags')
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')

        # Setup ES connection, excluding HTML text from our results
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        s = Search(using=client)
        s = s.extra(size=SIZE)
        s = s.source(excludes=["html_text"])
        data = {
            "results": [],
            "showing_default_results": False,
        }

        # Do search/filtering/sorting
        s = self._search(s, query)
        s = self._filter(s, date_flags, start, end)
        s = self._sort(s, sorting, query)

        # Get results and prepare them
        results = s.execute()

        if not results:
            data["showing_default_results"] = True
            s = Search(using=client)
            s = s.extra(size=SIZE)
            s = s.source(excludes=["html_text"])
            results = s.execute()

        data["results"] = [hit.to_dict() for hit in results]

        # print(results)
        #
        # comp_ids = [r.meta["id"] for r in results if r.meta["id"].isdigit()]
        # competitions = []
        # if comp_ids:
        #     # The below preserves the ordering elastic search gives us
        #     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(comp_ids)])
        #     competitions = Competition.objects.filter(pk__in=comp_ids).order_by(preserved)
        #
        # if not competitions:
        #     competitions = Competition.objects.all()[:SIZE]
        #     data['showing_default_results'] = True
        #
        # data["results"] = [CompetitionSimpleSearchSerializer(c).data for c in competitions]

        return Response(data)
