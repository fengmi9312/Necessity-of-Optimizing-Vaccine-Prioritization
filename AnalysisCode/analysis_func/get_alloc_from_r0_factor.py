# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:17:24 2025

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
    task_names = ['necs_from_param_(delay)',  'necs_from_param_(c_perct)',  'necs_from_param_(vac_avail)',  'necs_from_param_(vac_dur)',  'necs_from_param_(vac_eff)', 'necs_from_fatality_(coef_alpha_0)', 'necs_from_fatality_(coef_alpha_1)', 'necs_from_fatality_(coef_beta_0)', 'necs_from_fatality_(coef_beta_1)']
    anal_data = {}
    for country, task_name, param_idx, target in itertools.product(countries, task_names, range(40), targets):
        expr_name, expr_param = anal_func.get_expr_info(task_name)
        append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        anal_data[sheet_name] = {}
        for file_idx in range(40):
            alloc_data = expr_data[task_name][file_idx]['alloc']
            anal_data[sheet_name][f'min_{target}_{append_name}'] = alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations']
            anal_data[sheet_name][f'max_{target}_{append_name}'] = alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations']
    return anal_data

