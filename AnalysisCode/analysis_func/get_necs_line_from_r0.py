# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 13:58:26 2025

@author: MIFENG
"""

from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries
country_ifrs = rgd.country_ifrs


def analyze(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    task_names = ['necs_line_from_fatality_(coef_beta_1_0)', 'necs_line_from_fatality_(coef_beta_1_13)', 'necs_line_from_fatality_(coef_beta_1_26)', 'necs_line_from_fatality_(coef_beta_1_39)', 
                  'necs_line_from_param_(delay_10)', 'necs_line_from_param_(delay_8)', 'necs_line_from_param_(delay_13)', 'necs_line_from_param_(delay_26)']
    anal_data = {}
    for task_name, country, target, acc_type, dur in itertools.product(task_names, countries, targets, acc_types, durs):
        expr_name, expr_param = anal_func.get_expr_info(task_name)
        if dur: sheet_name_preppend = f'{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}_dur'
        else: sheet_name_preppend = f'{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}'
        country_data = data_of_countries[country]
        anti_target = 'd' if target == 'c' else 'c'
        val_types = ['max', 'min', 'anti_min', 'no_vac', 'necs', 'cost']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = {'res': []}
        for file_idx, param_idx in itertools.product(range(40), range(40)):
            ifrs = country_ifrs[country][expr_param.split('_')[1]][file_idx * 40 + param_idx][int(expr_param.split('_')[-1])] if expr_name == 'necs_line_from_fatality' else country_data['ifrs']
            pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * ifrs
            dist_data = expr_data[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            max_val = dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            min_val = dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_max']['res'].append(max_val)
            anal_data[f'{sheet_name_preppend}_min']['res'].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs']['res'].append(max_val - min_val)
            anti_min_val = dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            no_vac_val = dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_anti_min']['res'].append(anti_min_val)
            anal_data[f'{sheet_name_preppend}_no_vac']['res'].append(no_vac_val)
            anal_data[f'{sheet_name_preppend}_cost']['res'].append((anti_min_val - min_val) / (no_vac_val - anti_min_val))
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}']['res'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}']['res'])
    return anal_data




