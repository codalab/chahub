from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, MultiSearch


def get_search_client(size=100, multi=False):
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    if multi:
        s = MultiSearch(using=client)
    else:
        s = Search(using=client)
        # s = s.filter('term', published=True)
        # s = s.source(excludes=["html_text"])
    s = s.extra(size=size)
    return s


def get_results(search, multi=False):
    results = search.execute()
    if multi:
        hits = [hit.to_dict() for result in results for hit in result]
    else:
        hits = [hit.to_dict() for hit in results]
    return hits


def get_default_search_results():
    s = get_search_client()
    s = s.sort('-start', '-participant_count')
    return get_results(s)
