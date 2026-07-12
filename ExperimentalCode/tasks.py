# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:55:44 2024

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_root)

from Dependencies.CodeDependencies import func
from Dependencies.FrameDependencies import output_name
import importlib
from task_info import get_file_amount, check_info 
import re
import shutil

def clear_task_data(expr_name, task_param):
    task_name = f'{expr_name}_({task_param})'
    output_path = output_name.experimental_folder(task_name)
    if os.path.exists(output_path):
        try:
            shutil.rmtree(output_path)
            print(f"All data of {task_name} have been removed.")
        except Exception as e:
            print(f"Failed to delete {output_path}. Reason: {e}")
    else:
        print(f"The data folder of {task_name} does not exist.")
    
    pattern = re.compile(rf'cache_{re.escape(task_name)}\[\d+\]$')
    cache_folder_path = os.path.join(code_root, 'ExperimentalCode', 'experiments', 'cache')
    for folder_name in os.listdir(cache_folder_path):
        folder_path = os.path.join(cache_folder_path, folder_name)
        if os.path.isdir(folder_path) and pattern.match(folder_name):
            try:
                shutil.rmtree(folder_path)
                folder_lock_path = f'{folder_path}.lock'
                if os.path.exists(folder_lock_path): os.remove(folder_lock_path)
                print(f"{folder_path} has been removed.")
            except Exception as e:
                print(f"Failed to delete {folder_path}. Reason: {e}")
                
                
def execute_task(expr_name, task_param, task_idx, task_amount):
    task_name = f'{expr_name}_({task_param})'
    if not check_info(expr_name, task_param):
        print(f'{task_name} does not exist.')
        return None
    file_idx = task_idx
    print(f'Begin {task_name} --- task {task_idx} in {task_amount} tasks')
    output_path = output_name.experimental_folder(task_name)
    func.create_folder(output_path)
    file_amount = get_file_amount(expr_name, task_param)
    while True:
        if file_idx >= file_amount: break
        print(f'Begin {task_name}[{file_idx}] of {file_amount} files')
        file_path = output_name.experimental_file(task_name, file_idx)
        if os.path.exists(file_path): 
            print(f'Data_{task_name}[{file_idx}].xlsx already exists.')
            file_idx += task_amount
            continue
        temporary_file_path = output_name.temporary_experimental_file(task_name, file_idx)
        if os.path.exists(temporary_file_path): os.remove(temporary_file_path)
        res = importlib.import_module(f'experiments.{expr_name}').execute(task_param, file_idx)
        func.export_to_file(res, temporary_file_path)
        try:
            os.rename(temporary_file_path, file_path)
        except FileNotFoundError:
            print(f"The file {temporary_file_path} does not exist.")
        except PermissionError:
            print(f"Permission denied: unable to rename {temporary_file_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f'Complete {task_name}[{file_idx}] of {file_amount} files')
        file_idx += task_amount
    folder_lock_path = f'{output_path}.lock'
    if os.path.exists(folder_lock_path): 
        judge_exist = True
        for file_idx in range(task_amount):
            file_path = os.path.join(output_path, f'Data_{task_name}[{file_idx}].xlsx')
            judge_exist = judge_exist and os.path.exists(file_path)
        if judge_exist: os.remove(folder_lock_path)
    print(f'Complete {task_name} --- task {task_idx} in {task_amount} tasks')

