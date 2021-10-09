import settings
import requests
import json
import re
import time
from log import logger


def get_arxiv_papers(category, date, token):
    base_url = 'http://export.arxiv.org/oai2?verb=ListRecords&'
    url = (base_url +
           f"from={date[0]}&until={date[1]}&" +
           f"metadataPrefix=arXiv&set={category}")
    if token:
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


def get_macademic_papers_title(title):
    headers = {
        'Ocp-Apim-Subscription-Key': f"{settings.MACADEMIC_KEY}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    query = "expr=" + "&".join((f"Ti='{title}'",f"count=1",f"attributes={','.join(settings.papers_attributes)}"))

    try:
        response = requests.post(settings.MACADEMIC, data=query.encode("utf-8"), headers=headers)   
        response = response.json()
    except:
        pass
                     
    return response


def get_macademic_papers_author(author):
    headers = {
        'Ocp-Apim-Subscription-Key': f"{settings.MACADEMIC_KEY}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    query = "expr=" + "&".join((f"AuN='{author}'",f"count=1",f"attributes={','.join(settings.papers_attributes)}"))

    response = requests.post(settings.MACADEMIC, data=query.encode("utf-8"), headers=headers)   
    response = response.json()    

    return response