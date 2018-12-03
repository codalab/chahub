from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def get_search_client():
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    s = Search(using=client)
    # s = s.extra(size=size)  # default was 'size=35' -- we're displaying all competitions all the time now
    s = s.filter('term', published=True)
    s = s.source(excludes=["html_text"])
    return s


def get_results(search):
    results = search.execute()
    return [hit.to_dict() for hit in results]


def get_default_search_results():
    s = get_search_client()
    s = s.filter('term', published=True)
    s = s.extra(size=50)
    s = s.sort('-start', '-participant_count')
    return get_results(s)
