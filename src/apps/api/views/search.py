import datetime

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.competitions import CompetitionSerializer
from competitions.models import Competition, CompetitionParticipant


@api_view(['GET'])
def query(request, version="v1"):
    if 'q' not in request.GET:
        return Response()

    SIZE = 100

    query = request.GET.get('q')
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    s = Search(using=client).extra(size=SIZE)

    if query:
        # Do keyword search
        # s = s.query("match_phrase_prefix", title=query)
        s = s.query(
            "multi_match",
            query=query,
            type="best_fields",
            fuzziness=1,
            fields=["title^3", "description^2", "html_text", "created_by"]
        )
        s = s.highlight('title', fragment_size=50)
        s = s.suggest('suggestions', query, term={'field': 'title'})
        # s = s.slop(1)

    # Do filters
    # ...

    date_flags = request.GET.get('date_flags')
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

    data = {
        "results": [],
        "suggestions": []
    }

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

    comps = Competition.objects.filter(id__in=comp_ids)

    # data["results"] = [CompetitionSerializer(c).data for c in comps]

    # WE NEED THE ABOVE SO WE CAN ACTUALLY DO THIS OPERATION
    if len(comps) == 0:
        data['show_default_results'] = True
        comps = Competition.objects.all()[:SIZE]
    else:
        # If we're filtering by active, return only active
        if date_flags and date_flags == "active":
            comps = (comp for comp in comps if comp.is_active)
        data["show_default_results"] = False

    data["results"] = [CompetitionSerializer(c).data for c in comps]

    # OLD WAY THAT WORKS!
    # for result in results:
    #     data["results"].append({key: result[key] for key in result})

    if 'suggest' in results:
        if len(results.suggest['suggestions']) > 0:
            data["suggestions"] = [s.to_dict() for s in results.suggest['suggestions'][0].options]

    return Response(data)
