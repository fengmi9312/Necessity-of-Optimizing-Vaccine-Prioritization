# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 21:51:18 2020

@author: Tingting
"""

import pandas as pd

def write_to_file(data, file_dir):
    with pd.ExcelWriter(file_dir) as writer:
        for key in data.keys():
            pd.DataFrame(data[key]).to_excel(writer, sheet_name = key)













        
        
    