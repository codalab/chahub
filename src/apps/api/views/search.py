import datetime

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rest_framework.decorators import api_view
from rest_framework.response import Response


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

    # Filter on dates...
    # s = s.filter('range', created_when={
    #     'gt': datetime.date(1988, 2, 29),
    #     'lte': 'now'
    # })

    # Get results
    results = s.execute()

    data = {
        "results": [],
        "suggestions": []
    }

    for result in results:
        data["results"].append({key: result[key] for key in result})

    if 'suggest' in results:
        data["suggestions"] = [s.to_dict() for s in results.suggest['suggestions'][0].options]

    return Response(data)
