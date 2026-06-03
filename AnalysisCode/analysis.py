# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 15:44:38 2025

@author: MIFENG
"""


import pandas as pd
import os

def get_anal_data(task_list):
    folder_level = 1
    code_root = os.path.dirname(os.path.abspath(__file__))
    for idx in range(folder_level): code_root = os.path.dirname(code_root)
    anal_data = {}
    for task_name in task_list:
        anal_data[task_name] = pd.read_excel(os.path.join(code_root, 'AnalysisData', f'Data_{task_name}.xlsx'), index_col = 0, sheet_name = None)
    return anal_data