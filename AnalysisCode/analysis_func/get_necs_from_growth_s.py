# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:19:47 2025

@author: MIFENG
"""

from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries

def analyze(expr_data): 
    expr_name = 'necs_from_growth_s'
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    anal_data = {}
    growth_left_list = np.arange(0, 13)
    for expr_param, country, target, acc_type, dur in itertools.product(expr_params, countries, targets, acc_types, durs):
        sheet_name_prepend = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        country_data = data_of_countries[country]
        pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
        task_name = f'{expr_name}_({expr_param})'
        for growth_left in growth_left_list:
            sheet_name = f'{sheet_name_prepend}_{growth_left}'
            anal_data[sheet_name] = {}
            anal_data[sheet_name]['r0'] = []
            anal_data[sheet_name]['necs'] = []
            for r0_idx, file_idx, mean_idx in itertools.product(range(40), range(40), range(3)):
                dist_data = expr_data[task_name][file_idx]['dist']
                param_data = expr_data[task_name][file_idx]['transmission_params']
                append_name = f'{{{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}}}'
                growth = param_data.loc['growth_rate', f'params_{append_name}'] * param_data.loc['t_resp', f'params_{append_name}']
                if growth_left <= growth <= growth_left + 0.1:
                    anal_data[sheet_name]['r0'].append(param_data.loc['r0', f'params_{append_name}'])
                    anal_data[sheet_name]['necs'].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
            anal_data[sheet_name]['r0'] = np.array(anal_data[sheet_name]['r0'])
            anal_data[sheet_name]['necs'] = np.array(anal_data[sheet_name]['necs'])
    return anal_data