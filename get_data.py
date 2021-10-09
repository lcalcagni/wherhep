import settings
from endpoints import *
from utils import *
import xml.etree.ElementTree as ET
import pandas as pd
import os
from alphabet_detector import AlphabetDetector


def get_arxiv_data():
    """Get paper's information from arXiV

    This function extracts the following fields for each paper from the arXiv site:
    title
    abstract
    categories
    doi

    The output is then saved in a .csv file
    """
    df = pd.DataFrame(columns=("title", "abstract", "categories",  "doi"))

    while True:
        papers = get_arxiv_papers(settings.arxiv_category, settings.arxiv_date, token=None)
        papers = ET.fromstring(papers.text)
        
        for record in papers.find(settings.OAI+'ListRecords').findall(settings.OAI+"record"):

            meta = record.find(settings.OAI+'metadata')
            info = meta.find(settings.ARXIV+"arXiv")
            categories = info.find(settings.ARXIV+"categories").text
            doi = info.find(settings.ARXIV+"doi")

            if doi is not None:
                doi = doi.text

                
            paper_data = {'title'         : info.find(settings.ARXIV+"title").text,
                          'abstract'      : info.find(settings.ARXIV+"abstract").text.strip(),
                          'categories'    : categories.split(),
                          'doi'           : doi
                        }
                        
            df = df.append(paper_data, ignore_index=True)

        token = papers.find(settings.OAI+'ListRecords').find(settings.OAI+"resumptionToken")
        if not token:
            break
        
        else:
            url = base_url + "resumptionToken=%s"%(token.text)
            
    return df


def get_grid_df(path, columns):
    df = pd.read_csv(path)[columns]     
    return df


def get_grid_data():
    grid_folder = get_grid_folder()
    general_path = f"{settings.data_folder}/{grid_folder}/{settings.grid_file}"
    coordinates_path = f"{settings.data_folder}/{grid_folder}/full_tables/addresses.csv"

    df_grid_ids = get_grid_df(general_path,['ID', 'Name'])
    df_grid_latlong = get_grid_df(coordinates_path,['grid_id', 'lat', 'lng'])
    df_grid_latlong.rename(index=str,columns = {'grid_id':'ID'}, inplace=True)

    # Combine dfs
    df_grid = pd.merge(df_grid_ids, df_grid_latlong, on='ID')
    df_up = df_grid.copy() 
    df_up.to_csv('df_up.csv', sep=',', encoding='utf-8')
    df_grid['Name']=df_grid['Name'].str.lower()
    
    return df_grid


class TitleProcessor(AlphabetDetector):
    def process_title(self, title):
        result = "".join([x
                        if len(self.detect_alphabet(x)) > 0
                        or x.isnumeric()
                        else " " for x in title.lower()])
        while "  " in result:
            result = result.replace("  "," ")        
        return result



def get_macademic_data():
    df_output = pd.DataFrame(columns=("Title", "Abstract", "Categories", "Date", "doi", "Authors", "Institutions"))

    df = pd.read_csv('df_hep_ph.csv', index_col=0, comment='#')
    df_grid = pd.read_csv('df_grid.csv', index_col=0, comment='#')
    df_up = pd.read_csv('df_up.csv', index_col=0, comment='#')

    HEADERS = {
        'Ocp-Apim-Subscription-Key': os.getenv('MACADEMIC_KEY'),
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    fields_or = ["Id","Ti","D","AA.AuN","AA.DAuN","AA.AuId","F.FId","C.CN","J.JId","AA.AfId","CC","ECC","AA.AfN","J.JN"]


    def getbytitle(title, query_count):

        query = f"expr=Ti='{title}'&count={query_count}&attributes={','.join(fields_or)}"

        r = requests.post('https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate', data=query.encode("utf-8"), headers=HEADERS)
        try:
            js = r.json()
        except json.decoder.JSONDecodeError as err:
            print("Error with status code ",r.status_code)
            print(r.text)
            raise err
                
        print(js)
        print("Got",len(js["entities"]),"titles results")
        return js


    def getbyauthor(auth, query_count):

        query = f"expr=Composite(AA.AuN='{auth}')&count={query_count}&attributes={','.join(fields_or)}"

        print("----query", query)

        r = requests.post('https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate', data=query.encode("utf-8"), headers=HEADERS)
        try:
            js_a = r.json()
        except json.decoder.JSONDecodeError as err:
            print("Error with status code ",r.status_code)
            print(r.text)
            raise err
            
        return js_a


    query_count = 1



    for i in range(len(df)):

        title = df['title'].values[i]  
        doi = df['doi'].values[i]
        abstract =  df['abstract'].values[i]
        categories = df['categories'].values[i]
        
        print(f"Processing title {title}")  
        tp = TitleProcessor()
        title_lower = tp.process_title(title)
                
        js = getbytitle(title_lower, query_count)    
        print(js)  

        auth=[]
        inst=set([])
        
        start = '"AfN":"'
        end = '"'
        
        for row in js['entities']:
            date = row['D']
        
        ####Get affiliation if paper has
        for row in js["entities"]:
            for author in row['AA']:
                auth.append(author['AuN'])
                if "AfN" in author:
                    inst.add(author['AfN'])
        
        
        ####If paper has not affiliation, get affiliation by authors
        if len(inst)==0:
            found=False
            print("paper with no affiliation, searching by authors")
            for a in auth:
                js_a = getbyauthor(a,query_count)
                print("---------------------author")
                print(js_a)
                for row in js_a["entities"]:
                    print("row", row)
            
                    if row.get('AA'):
                        for i in row['AA']: 
                            if "AfN" in i and "AuN" in i:
                                if a == i['AuN']:
                                    inst.add(i['AfN'])
                                    found = True
                                    print("--------------------INST")
                                    print(inst)
                                    break
                    
                    if found:
                        break
                if found:
                    break
            if found:
                break

                            # inst.add((row['E'].split(start))[1].split(end)[0])
                            # break
        
    #
        total_inst_coord=[]

    #get coordinates of institutions
        for i in inst:
            institute=[]
            a=df_grid.loc[df_grid['Name'] == i, 'lat']
        
            if (len(a)!=0):
                lat = df_grid.loc[df_grid['Name'] == i, 'lat'].iloc[0]  
                lng = df_grid.loc[df_grid['Name'] == i, 'lng'].iloc[0] 
                
                idx = df_grid.index[df_grid['Name'] == i].tolist()
                
    #            print("idx:  ", idx)
                instit = df_up.iloc[idx]['Name'].iloc[0]

    #            print("instit:  ", instit)
                coord = str(lat)+','+str(lng)

                print("lat:    ",lat)
                print("long:    ",lng)
                print("lat:    ",coord)
                institute.append(instit)
                institute.append(coord)

                
                total_inst_coord.append(institute)
    #            print(total_inst_coord)
        
            else:
                lat=0
                lng=0
        
        if (total_inst_coord != []):
            
            contents = {'Title': title, 
                        'Abstract': abstract, 
                        'Categories': categories,
                        'Date': date,
                        'doi': doi,
                        'Authors': auth,
                        'Institutions':total_inst_coord,
                        }


            df_output = df_output.append(contents, ignore_index=True)
            
            
    print(df_output)
    df_output.to_csv('df_output.csv', sep=',', encoding='utf-8')
    df_output.to_json('output.json', orient='records', lines=True)