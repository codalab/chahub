from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def get_search_client(size=100, index=None):
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    search_kwargs = {
        'using': client,
    }
    if index is not None:
        search_kwargs['index'] = index
    s = Search(**search_kwargs)
    s = s.extra(size=size)
    # s = s.filter('term', published=True)
    s = s.source(excludes=["html_text"])
    return s


def serialize_hit(hit):
    d = hit.to_dict()
    d['index_type'] = hit.meta.index
    return d


def get_results(search):
    results = search.execute()
    return [serialize_hit(hit) for hit in results]


def get_default_search_results():
    s = get_search_client(index='competitions')
    s = s.sort('-start', '-participant_count')
    return get_results(s)
