# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:19:02 2025

@author: MIFENG
"""

from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    expr_name = 'necs_from_growth_gen'
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    anal_data = {}
    for expr_param, country, target, acc_type, dur in itertools.product(expr_params, countries, targets, acc_types, durs):
        sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        country_data = data_of_countries[country]
        pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
        task_name = f'{expr_name}_({expr_param})'
        anal_data[sheet_name] = {}
        for r0_idx, file_idx, param_idx in itertools.product(range(4), range(9), range(9)):
            if file_idx == 0 and param_idx == 0: 
                anal_data[sheet_name][f'growth_{r0_idx}'] = []
                anal_data[sheet_name][f'necs_{r0_idx}'] = []
            dist_data = expr_data[task_name][file_idx]['dist']
            param_data = expr_data[task_name][file_idx]['transmission_params']
            append_name = f'{{{basic_params.country_abbr[country]}_{r0_idx}_{param_idx}}}'
            anal_data[sheet_name][f'growth_{r0_idx}'].append(param_data.loc['growth_rate', f'params_{append_name}'] * param_data.loc['t_resp', f'params_{append_name}'])
            anal_data[sheet_name][f'necs_{r0_idx}'].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
        for r0_idx in range(4):
            anal_data[sheet_name][f'growth_{r0_idx}'] = np.array(anal_data[sheet_name][f'growth_{r0_idx}'])
            anal_data[sheet_name][f'necs_{r0_idx}'] = np.array(anal_data[sheet_name][f'necs_{r0_idx}'])
    return anal_data