# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:21:57 2025

@author: MIFENG
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import itertools

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    expr_name, expr_param = 'necs_from_example', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {'alloc': {}}
    country = 'United States'
    sttgs = ['max_c', 'min_c', 'max_d', 'min_d']
    for delay_idx, r0_idx, sttg in itertools.product(range(1), range(5, 12), sttgs):
        anal_data['alloc'][f"{delay_idx}_{r0_idx}_{sttg}"] = expr_data[task_name][r0_idx + delay_idx * 3]['alloc'][f'{sttg}_dd_{{{expr_param}_{basic_params.country_abbr[country]}}}'] * data_of_countries[country]['populations']
    return anal_data
