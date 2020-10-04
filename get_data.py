import config
from endpoints import *
from utils import *
import xml.etree.ElementTree as ET
import pandas as pd


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


def get_grid_df(path, columns):
    df = pd.read_csv(path)[columns]     
    return df


def get_grid_data():
    grid_folder = get_grid_folder()
    general_path = f"{config.data_folder}/{grid_folder}/{config.grid_file}"
    coordinates_path = f"{config.data_folder}/{grid_folder}/full_tables/addresses.csv"

    df_grid_ids = get_grid_df(general_path,['ID', 'Name'])
    df_grid_latlong = get_grid_df(coordinates_path,['grid_id', 'lat', 'lng'])
    df_grid_latlong.rename(index=str,columns = {'grid_id':'ID'}, inplace=True)

    # Combine dfs
    df_grid = pd.merge(df_grid_ids, df_grid_latlong, on='ID')
    df_grid['Name']=df_grid['Name'].str.lower()

    return df_grid

