import getopt, sys
from time import process_time

from log import logger
from get_data import *

OPTIONS_LONG = [
            "arxiv",
            "grid",
            "macademic"
        ]

if __name__ == "__main__":
    try:
        arguments, values = getopt.getopt(sys.argv[1:],"", OPTIONS_LONG)
    except getopt.error as e:
        print(e)
        sys.exit()

    tic = process_time()

    for argument, value in arguments:

        if argument == "--arxiv":            
            logger.info("🚀  Processing ArXiv data ...")
            df_arxiv = get_arxiv_data()
            print(df_arxiv)
            df_arxiv.to_csv('df_hep_ph.csv', sep=',', encoding='utf-8')

        if argument == "--grid":    
            logger.info("🚀  Processing GRID data ...")
            df_grid = get_grid_data()
            print(df_grid)
            df_grid.to_csv('df_grid.csv', sep=',', encoding='utf-8')

        if argument == "--macademic":    
            logger.info("🚀  Processing Microsoft Academic data ...")
            get_macademic_data()

    toc = process_time()
    elapsed_time = toc-tic
    logger.info(f"⏲  Elapsed time= {elapsed_time}") 
