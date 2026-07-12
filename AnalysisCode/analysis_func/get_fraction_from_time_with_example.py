# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:20:40 2025

@author: MIFENG
"""


from Dependencies.CodeDependencies import basic_params
import itertools

def analyze(expr_data):
    expr_name, expr_param = 'necs_from_example', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {}
    country = 'United States'
    sttgs = ['no_vac', 'max_c', 'min_c', 'max_d', 'min_d', 'under_20', '20-49', '20+', '60+', 'all_ages']
    for delay_idx, r0_idx, sttg, acc_type, dur in itertools.product(range(1), range(5, 12), sttgs, ['dd', 'gd'], [False, True]):
        sheet_name = f"{delay_idx}_{r0_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"
        anal_data[sheet_name] = {'time_line': expr_data[task_name][r0_idx + delay_idx * 3][f"curve_{sttg}_{acc_type}{'_dur' if dur else ''}"][f'time_line_{{{expr_param}_{basic_params.country_abbr[country]}}}']}
        for target in ['s', 'i', 'r', 'c', 'd']:
            anal_data[sheet_name][f'curve_{target}'] = expr_data[task_name][r0_idx + delay_idx * 3][f"curve_{sttg}_{acc_type}{'_dur' if dur else ''}"][f'curve_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        for target in ['c', 'd']:
            if acc_type == 'dd': anal_data[sheet_name][f'prdt_{target}'] = expr_data[task_name][r0_idx + delay_idx * 3][f"curve_{sttg}_{acc_type}{'_dur' if dur else ''}"][f'prdt_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']
    return anal_data