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

    query = request.GET.get('q')
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    s = Search(using=client)

    if query:
        # Do keyword search
        s = s.query("match_phrase_prefix", title=query)
        s = s.highlight('title', fragment_size=50)
        s = s.suggest('suggestions', query, term={'field': 'title'})
        # s = s.slop(1)

    # Do filters
    # ...

    date_flags = request.GET.get('date_flags')
    if date_flags:
        print("We received date_flags and they are {}".format(date_flags))
        if date_flags == "active":
            # Do something
            print("We have date flags for active")
        if date_flags == "last_month":
            # Do something
            s = s.filter('range', created_when={
                'gt': datetime.date.today() - datetime.timedelta(days=30),  # I think..
                "format": "yyyy-MM-dd",
                'lte': datetime.date.today()
            })
        if date_flags == "last_year":
            # Do something
            s = s.filter('range', created_when={
                'gt': datetime.date.today() - datetime.timedelta(days=365),  # I think..
                "format": "yyyy-MM-dd",
                'lte': datetime.date.today()
            })
        # ELSE DO NOTHING

    # Filter on dates...
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        s = s.filter('range', created_when={
            'gte': start_date,  # I think..
            "format": "yyyy-MM-dd",
            'lte': end_date
        })
    elif start_date:
        s = s.filter('range', created_when={
            'gt': start_date,  # I think..
            "format": "yyyy-MM-dd",
            'lte': datetime.date.today() + datetime.timedelta(days=999)
        })
    elif end_date:
        s = s.filter('range', created_when={
            'gte': datetime.date.today() - datetime.timedelta(days=999),
            "format": "yyyy-MM-dd",
            'lt': end_date
        })

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

    comp_ids = [r.meta["id"] for r in results]
    comps = Competition.objects.filter(id__in=comp_ids)

    data["results"] = [CompetitionSerializer(c).data for c in comps]

    # OLD WAY THAT WORKS!
    # for result in results:
    #     data["results"].append({key: result[key] for key in result})

    if 'suggest' in results:
        data["suggestions"] = [s.to_dict() for s in results.suggest['suggestions'][0].options]

    return Response(data)
