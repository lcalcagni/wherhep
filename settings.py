from dotenv import load_dotenv
import os

load_dotenv()

data_folder      = 'data'


# arXiv
OAI              = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV            = "{http://arxiv.org/OAI/arXiv/}"

arxiv_date       = ['2012-01-01', '2012-01-04']  #from, to
arxiv_category   = 'physics:hep-ph'


# GRID
grid_file        = 'grid.csv'


# Microsoft Academic
MACADEMIC_KEY    = os.getenv('MACADEMIC_KEY')
MACADEMIC        = 'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate'
paper_attributes = ['AA.AfId',
                    'AA.AfN',
                    'AA.AuN',
                    'AA.AuId',
                    'D',
                    'E',
                    'Id',                    
                    'Ti']