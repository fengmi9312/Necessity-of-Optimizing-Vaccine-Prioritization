# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:51:03 2025

@author: fengm
"""

import pandas as pd
from . import output_name

def load_edata(expr_name, expr_param, file_amount):
    task_name = f'{expr_name}_({expr_param})'
    res = []
    for file_idx in range(file_amount):
        res.append(pd.read_excel(output_name.analysis_file(task_name, file_idx), index_col = 0, sheet_name = None))
    print(task_name + ' imported')
    return res

def load_certain_edata(key_dict):
    res = {}
    for expr_name, expr_param_infos in key_dict.items():
        for expr_param, file_amount in expr_param_infos.items():
            task_name = f'{expr_name}_({expr_param})'
            res[task_name] = load_edata(expr_name, expr_param, file_amount)
    return res

# def load_all_edata():
#     return load_certain_edata({expr_name: list(task_params.keys()) for expr_name, task_params in info.items()})


     