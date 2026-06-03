# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:19:16 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    targets = ['w', 'x']
    countries = ['United States']
    acc_types = ['dd']
    durs = [False]
    
    task_names = ['necs_from_fatality_by_contact_(coef_beta_1)']
    anal_data = {}
    for task_name, country, target, acc_type, dur in itertools.product(task_names, countries, targets, acc_types, durs):
        expr_name, expr_param = anal_func.get_expr_info(task_name)
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        val_types = ['max', 'min', 'no_vac', 'necs', 'anti_min', 'cost']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = []
        for file_idx, param_idx in itertools.product(range(40), range(40)):
            if param_idx == 0: 
                for val_type in val_types:
                    anal_data[f'{sheet_name_preppend}_{val_type}'].append([])
            
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_0}}' if target == 'w' else f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            anti_append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}' if target == 'w' else f'{{{expr_param}_{basic_params.country_abbr[country]}_0}}'
            pop_coef = data_of_countries['United States']['populations'] if target == 'w' else expr_data[task_name][file_idx]['weights'][f"max_x_{acc_type}{'_dur' if dur else ''}_{append_name}"] * data_of_countries['United States']['populations']
            dist_data = expr_data[task_name][file_idx]['dist']
            max_val = dist_data[f"max_x_{acc_type}{'_dur' if dur else ''}_{append_name}"].to_numpy() @ pop_coef
            min_val = dist_data[f"min_x_{acc_type}{'_dur' if dur else ''}_{append_name}"].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_max'][-1].append(max_val)
            anal_data[f'{sheet_name_preppend}_min'][-1].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs'][-1].append(max_val - min_val)
            anti_min_val = dist_data[f"min_x_{acc_type}{'_dur' if dur else ''}_{anti_append_name}"].to_numpy() @ pop_coef
            no_vac_val = dist_data[f"no_vac_{acc_type}_{append_name}"].to_numpy() @ pop_coef 
            anal_data[f'{sheet_name_preppend}_no_vac'][-1].append(no_vac_val)
            anal_data[f'{sheet_name_preppend}_anti_min'][-1].append(anti_min_val)
            anal_data[f'{sheet_name_preppend}_cost'][-1].append((anti_min_val - min_val) / (no_vac_val - min_val))
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}'])
    return anal_data
