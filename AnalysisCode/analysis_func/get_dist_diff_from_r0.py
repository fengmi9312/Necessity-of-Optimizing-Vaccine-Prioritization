# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:27:32 2025

@author: MIFENG
"""

def analyze(expr_data):
    expr_name, expr_param = 'contact_before_protect', 'param'
    task_name = f'{expr_name}_({expr_param})'
    res = {'dist_diff': {}}
    for idx in range(40):
        res['dist_diff'][f'dist_diff_{idx}'] = (expr_data[task_name][0]['post_dist'][f'dist_{idx}']  - expr_data[task_name][0]['pre_dist'][f'dist_{idx}']) / (1  - expr_data[task_name][0]['pre_dist'][f'dist_{idx}'])
    return res