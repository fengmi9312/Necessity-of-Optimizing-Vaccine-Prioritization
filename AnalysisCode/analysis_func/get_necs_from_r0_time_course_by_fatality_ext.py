# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 11:38:13 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries


def analyze(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd']

    task_names = ['necs_from_time_course_fixd_by_fatality_ext_(param)']
    anal_data = {}
    r0_amount = 40
    param_amount = 40

    for task_name, country, target, acc_type in itertools.product(task_names, countries, targets, acc_types):
        expr_name, expr_param = anal_func.get_expr_info(task_name)
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}"
        country_data = data_of_countries[country]
        anti_target = 'd' if target == 'c' else 'c'
        val_types = ['max', 'min', 'anti_min', 'no_vac', 'necs', 'cost']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = []

        for r0_idx in range(r0_amount):
            param_idx = 'ext'
            equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
            diff_ifr = country_data['ifrs'] - equal_ifr
            param_val = 1.05
            ifrs = equal_ifr + param_val * diff_ifr
            
            pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * ifrs
            
            for val_type in val_types:
                anal_data[f'{sheet_name_preppend}_{val_type}'].append([])

            file_idx = r0_idx
            dist_data = expr_data[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            max_val = dist_data[f"max_{target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            min_val = dist_data[f"min_{target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            anti_min_val = dist_data[f"min_{anti_target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            no_vac_val = dist_data[f"no_vac_{acc_type}_{append_name}"].to_numpy() @ pop_coef

            anal_data[f'{sheet_name_preppend}_max'][-1].append(max_val)
            anal_data[f'{sheet_name_preppend}_min'][-1].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs'][-1].append(max_val - min_val)
            anal_data[f'{sheet_name_preppend}_anti_min'][-1].append(anti_min_val)
            anal_data[f'{sheet_name_preppend}_no_vac'][-1].append(no_vac_val)
            anal_data[f'{sheet_name_preppend}_cost'][-1].append((anti_min_val - min_val) / (no_vac_val - min_val))

        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}'])
    return anal_data
