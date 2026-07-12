# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:25:18 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import pandas as pd
import func
import output_name
from refinement_info import check_info, get_file_amount, info

def execute_refinement(expr_name, task_param, task_idx, task_amount):
    task_name = f'{expr_name}_({task_param})'
    if not check_info(expr_name, task_param):
        print(f'{task_name} does not exist.')
        return None
    file_idx = task_idx
    refinement_path = output_name.refinement_folder(task_name)
    func.create_folder(refinement_path)
    file_amount = get_file_amount(expr_name, task_param)
    while True:
        if file_idx >= file_amount: break
        data = pd.read_excel(output_name.experimental_file(task_name, file_idx), index_col = 0, sheet_name = None)
        res = {}
        for sheet_key, sheet_item in info[expr_name][task_param][file_idx].items():
            res[sheet_key] = {}
            for key in sheet_item:
                res[sheet_key][key] = data[sheet_key][key]
        func.export_to_file(res, output_name.refinement_file(task_name, file_idx))
        file_idx += task_amount
    folder_lock_path = f'{refinement_path}.lock'
    if os.path.exists(folder_lock_path): 
        judge_exist = True
        for file_idx in range(task_amount):
            file_path = os.path.join(refinement_path, f'Data_{task_name}[{file_idx}].xlsx')
            judge_exist = judge_exist and os.path.exists(file_path)
        if judge_exist: os.remove(folder_lock_path)
    print(f'Complete {task_name} --- task {task_idx} in {task_amount} tasks')