import config
from endpoints import *

def get_arxiv_data():
    get_papers(config.arxiv_category, config.arxiv_date)