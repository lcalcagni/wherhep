from config import *
import requests
import json
import re
import time
from log import logger


def get_papers(category, date, token):
    base_url = 'http://export.arxiv.org/oai2?verb=ListRecords&'
    url = (base_url +
           f"from={date[0]}&until={date[1]}&" +
           f"metadataPrefix=arXiv&set={category}")
    if token:
        print("there is token")
        url = base_url + f"resumptionToken={token}"   
    try:
        response = requests.get(url)
        logger.debug(f" ⚙ fetching... {url}")           
        if response.status_code == 503:
            pattern = "Retry after (.*?) seconds"
            seconds_wait = int(re.search(pattern, response.text).group(1))
            logger.debug(f"    💤 Got 503. Retrying after {seconds_wait} seconds")
            time.sleep(seconds_wait)
    except Exception as e:
        print(e)
    return response