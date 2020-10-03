from config import *
import requests


def get_papers(category, date):
    date = ['2012-01-01', '2012-02-01']
    category = 'physics:hep-ph'
    base_url = 'http://export.arxiv.org/oai2?verb=ListRecords&'
    url = (base_url +
           f"from={date[0]}&until={date[1]}&" +
           "metadataPrefix=arXiv&set={category}")
    while True:
        papers = requests.get(url)
    return papers