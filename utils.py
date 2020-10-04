import os 
import re
import config

def get_grid_folder():
    grid_folder = []
    reg_compile = re.compile("grid")
    for dirpath, dirnames, filenames in os.walk(config.data_folder, topdown = False):
        grid_folder = grid_folder + [dirname for dirname in dirnames if  reg_compile.match(dirname)]       
    return grid_folder[0]