from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def get_search_client(size=35):
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    s = Search(using=client)
    s = s.extra(size=size)
    s = s.filter('term', published=True)
    s = s.source(excludes=["html_text"])
    return s


def get_results(search):
    results = search.execute()
    return [hit.to_dict() for hit in results]


def get_default_search_results():
    s = get_search_client()
    s = s.filter('term', published=True)
    s = s.sort('_score', 'start:desc')
    return get_results(s)
