# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 21:51:18 2020

@author: Tingting
"""

import numpy as np
import scipy.special as sc
import pandas as pd
from filelock import FileLock
import os

def create_folder(folder_path):
    lock = FileLock(folder_path + '.lock')
    with lock:
        os.makedirs(folder_path, exist_ok=True)
    return None

def export_to_file(data, file_dir):
    with pd.ExcelWriter(file_dir) as writer:
        for key in data.keys():
            pd.DataFrame(data[key]).to_excel(writer, sheet_name = key)













        
        
    