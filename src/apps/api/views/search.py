import datetime

from django.conf import settings
from django.utils.timezone import now
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api.caching import QueryParamsKeyConstructor
from api.serializers.competitions import CompetitionSerializer, CompetitionSimpleSearchSerializer
from competitions.models import Competition, CompetitionParticipant, Phase


class SearchView(APIView):
    @cache_response(key_func=QueryParamsKeyConstructor(), timeout=60)
    def get(self, request, version="v1"):
        if 'q' not in request.GET:
            return Response()

        SIZE = 20

        query = request.GET.get('q')
        sorting = request.GET.get('sorting')
        date_flags = request.GET.get('date_flags')
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        s = Search(using=client).extra(size=SIZE)
        data = {
            "results": [],
            "suggestions": [],
            "showing_default_results": False,
        }

        if query and query != ' ':
            s = s.query(
                "multi_match",
                query=query,
                type="best_fields",
                fuzziness='auto',
                fields=["title^3", "description", "html_text", "created_by"]
            )
            # s = s.highlight('title', fragment_size=50)
            # s = s.suggest('suggestions', query, term={'field': 'title'})

        # Do filters
        if date_flags == "this_month":
            s = s.filter('range', created_when={
                'gte': "now/M",
                'lte': "now/M",
            })
        if date_flags == "this_year":
            s = s.filter('range', created_when={
                'gte': "now/y",
                'lte': "now/y",
            })

        # Filter on specified start/end range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        date_args = {}
        if start_date:
            date_args['gte'] = start_date
        if end_date:
            date_args['lte'] = end_date
        if date_args:
            date_args['format'] = 'date_optional_time'
            s = s.filter('range', created_when=date_args)

        # Get results
        results = s.execute()



        # Sort out results into each class type, then query to get each of those models
        # model_queries = {}
        # for r in results:
        #     # import ipdb; ipdb.set_trace()
        #     ## model_class = r._doc_type.model
        #     # model_class = s._doc_type_map.get(r.meta.doc_type)
        #     # print(s._doc_type_map)
        #     # if model_class not in model_queries:
        #     #     model_queries[model_class] = []
        #     # model_queries[model_class].append(r.meta["id"])
        #
        # for model_class, ids in model_queries.items():
        #     print(model_class.objects.filter(id__in=ids))

        comp_ids = [r.meta["id"] for r in results if r.meta["id"].isdigit()]
        competitions = []
        if comp_ids:
            competitions = Competition.objects.filter(id__in=comp_ids)
            if sorting == 'participant_count':
                competitions = competitions.order_by('-participant_count')
            elif sorting == 'prize':
                competitions = competitions.order_by('-prize')
            elif sorting == 'deadline':
                phases = Phase.objects.filter(
                    competition_id__in=comp_ids,
                    end__gte=now()
                )
                phases = phases.order_by('end').select_related('competition')
                competitions = [phase.competition for phase in phases]
            else:
                # TODO: This is horribly inefficient.. need to make this sort like a real engineer would!
                # default sorting for relevance -- we have to get database objects but they
                # aren't in the order we received comp_ids, yet
                new_sorted_competitions = []
                for id in comp_ids:
                    for competition in competitions:
                        if id == str(competition.id):
                            new_sorted_competitions.append(competition)
                            break
                competitions = new_sorted_competitions

            if date_flags and date_flags == "active":
                competitions = [comp for comp in competitions if comp.is_active]

        if not competitions:
            competitions = Competition.objects.all()[:SIZE]
            data['showing_default_results'] = True

        data["results"] = [CompetitionSimpleSearchSerializer(c).data for c in competitions]

        if 'suggest' in results:
            if len(results.suggest['suggestions']) > 0:
                data["suggestions"] = [s.to_dict() for s in results.suggest['suggestions'][0].options]

        return Response(data)
