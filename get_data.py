import config
from endpoints import *
import xml.etree.ElementTree as ET


def get_arxiv_data():
    while True:
        papers = get_papers(config.arxiv_category, config.arxiv_date, token=None)
        papers = ET.fromstring(papers.text)

        for record in papers.find(config.OAI+'ListRecords').findall(config.OAI+"record"):

            meta = record.find(config.OAI+'metadata')
            info = meta.find(config.ARXIV+"arXiv")
            categories = info.find(config.ARXIV+"categories").text
            doi = info.find(config.ARXIV+"doi")

            if doi:
                doi = doi.text.split()[0]
                
            paper_data = {'title'         : info.find(config.ARXIV+"title").text,
                          'abstract'      : info.find(config.ARXIV+"abstract").text.strip(),
                          'categories'    : categories.split(),
                          'doi'           : doi
                        }
        token = papers.find(config.OAI+'ListRecords').find(config.OAI+"resumptionToken")
        if not token:
            break