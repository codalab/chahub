from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

OBJECT_LIST = [
    'profile',
    'competition',
    'task',
    'dataset',
    'solution',
    'user'
]


def get_search_client(size=100, page=1):
    client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
    s = Search(using=client)
    # s = s.filter('term', published=True)
    # s = s.source(excludes=["html_text"])
    s = s.extra(size=size)
    lower_bound = (page-1) * size
    upper_bound = lower_bound + size
    s = s[lower_bound:upper_bound]
    return s


def get_results(search):
    results = search.execute()
    hits = [hit.to_dict() for hit in results]
    return hits


def get_default_search_results():
    s = get_search_client(size=100, page=1)
    matching_types = []
    for object_type in OBJECT_LIST:
        matching_types.append({'match': {'_obj_type': object_type}})
    s = s.query('bool', should=matching_types, minimum_should_match=1)
    return get_results(s)
