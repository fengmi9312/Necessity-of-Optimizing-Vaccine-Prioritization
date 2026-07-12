# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:45:33 2024

@author: fengm
"""


import os
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re

def experimental_folder(task_name):
    return os.path.join(code_root, 'ExperimentalDataTmp', ''.join(part.capitalize() for part in re.split(r'_(?![^\(]*\))', task_name)))

def temporary_experimental_file(task_name, file_idx):
    return os.path.join(experimental_folder(task_name), f'Temporary_Data_{task_name}[{file_idx}].xlsx')

def experimental_file(task_name, file_idx):
    return os.path.join(experimental_folder(task_name), f'Data_{task_name}[{file_idx}].xlsx')


def analysis_folder(task_name):
    return os.path.join(code_root, 'ExperimentalData', ''.join(part.capitalize() for part in re.split(r'_(?![^\(]*\))', task_name)))

def analysis_file(task_name, file_idx):
    return os.path.join(analysis_folder(task_name), f'Data_{task_name}[{file_idx}].xlsx')


def refinement_folder(task_name):
    return os.path.join(code_root, 'RefinementData', ''.join(part.capitalize() for part in re.split(r'_(?![^\(]*\))', task_name)))

def refinement_file(task_name, file_idx):
    return os.path.join(refinement_folder(task_name), f'Data_{task_name}[{file_idx}].xlsx')

