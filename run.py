import getopt, sys
from time import process_time


from log import logger
from get_data import *

if __name__ == "__main__":
    try:
        shortops, args = getopt.getopt(sys.argv[1:]," ")
    except getopt.error as e:
        print(e)
        sys.exit()
    
    for arg in args:
        if arg == "arxiv":
            tic = process_time()
            logger.info("🚀  Processing ArXiv data ...")
            get_arxiv_data()

            logger.info("🚀  Processing GRID data ...")
            get_grid_data()
            toc = process_time()
            elapsed_time = toc-tic
            logger.info(f"⏲  Elapsed time= {elapsed_time}")