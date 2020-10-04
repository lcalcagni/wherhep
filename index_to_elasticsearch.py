import requests
import os
import sys, json
from elasticsearch import Elasticsearch, helpers


es = Elasticsearch([os.environ['ELASTICSEARCH_INSTANCE']])

filename = '.output.json'
data = [json.loads(line) for line in open(filename, 'r')]
helpers.bulk(es, data, index='title', doc_type='HEP_papers')

indices = es.indices.get_alias().keys()