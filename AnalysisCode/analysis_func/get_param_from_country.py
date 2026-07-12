# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:49:56 2025

@author: fengm
"""

import itertools

def analyze(expr_data):
    x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    expr_name = 'necs_from_country'
    anal_data = {}
    for param in ['r0', 'growth_rate', 'alpha', 'beta']:
        sheet_name = param
        anal_data[sheet_name] = {}
        for expr_param in x_countries:
            task_name = f'{expr_name}_({expr_param})'
            key = expr_param
            anal_data[sheet_name][key] = []
            for file_idx, param_idx in itertools.product(range(40), range(25)):
                param_data = expr_data[task_name][file_idx]['transmission_params']
                anal_data[sheet_name][key].append(param_data.loc[param, f'params_{{none_{param_idx}}}'])
    return anal_data