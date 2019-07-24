from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, MultiSearch

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
    # if multi:
    #     s = MultiSearch(using=client)
    # else:
    s = Search(using=client)
    # s = s.filter('term', published=True)
    # s = s.source(excludes=["html_text"])
    s = s.extra(size=size)
    lower_bound = (page-1) * size
    # upper_bound = (page-1) * size * 2 if (page-1 > 1) else size * 2
    upper_bound = lower_bound + size
    print("*************************************")
    print(upper_bound)
    print(lower_bound)
    print("*************************************")
    s = s[lower_bound:upper_bound]
    # {"from": 10, "size": 10}
    return s


def get_results(search):
    results = search.execute()
    # results = search.scan()
    # if multi:
    #     hits = [hit.to_dict() for result in results for hit in result]
    # else:
    # hits = [hit.to_dict() for hit in results]
    hits = [hit.to_dict() for hit in results]
    print(hits)
    return hits


def get_default_search_results():
    s = get_search_client(size=100, page=1)
    matching_types = []
    for object_type in OBJECT_LIST:
        matching_types.append({'match': {'_obj_type': object_type}})
    s = s.query('bool', should=matching_types, minimum_should_match=1)
    print(matching_types)
    # s = s.sort('-start', '-participant_count')
    return get_results(s)
