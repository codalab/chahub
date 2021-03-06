from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def get_search_client(size=30, page=1, index=None):
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    if index:
        query = {
            "query": {
                "terms": {
                    "_index": index
                }
            }
        }
        s = Search.from_dict(query)
    else:
        s = Search()
    s.using(client)
    s = s.extra(size=size)
    s = s.filter('term', hidden=False)
    s = s.source(excludes=["html_text"])
    _to = size * page
    _from = _to - size
    s = s[_from: _to]
    return s


def serialize_hit(hit):
    d = hit.to_dict()
    d['index_type'] = hit.meta.index
    return d


def get_results(search):
    results = search.execute()
    return {
        "results": [serialize_hit(hit) for hit in results],
        "total": results.hits.total.value,
    }


def get_default_search_results():
    s = get_search_client(index=['competitions'])
    s = s.sort('-start', '-participant_count')
    return get_results(s)
