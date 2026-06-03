# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:24:09 2025

@author: MIFENG
"""


from .analysis_dependencies import required_generated_data as rgd
import itertools
from .analysis_dependencies import anal_func
import numpy as np
data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    expr_name = 'necs_space'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {}
    for sheet_idx in range(2):
        anal_data[f'res_{sheet_idx}'] = expr_data[task_name][sheet_idx]['res']
    expr_name = 'optm_transition'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    country = 'United States'
    country_data = data_of_countries[country]
    anal_data['alloc_res'] = {}
    anal_data['alloc_res']['alloc_0_n'] = expr_data[task_name][0]['allocs']['alloc_1000'] * country_data['populations']
    anal_data['alloc_res']['alloc_0_p'] = expr_data[task_name][0]['allocs']['alloc_0'] * country_data['populations']
    anal_data['alloc_res']['alloc_1_n'] = expr_data[task_name][40]['allocs']['alloc_1000'] * country_data['populations']
    anal_data['alloc_res']['alloc_1_p'] = expr_data[task_name][40]['allocs']['alloc_0'] * country_data['populations']
    expr_name = 'transition_direct_effects'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    anal_data['angles'] = {}
    contact_arr = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    for idx in range(2):
        direct_eff_coef = expr_data[task_name][0]['res'][str(idx * 40)]
        for eff in ['n', 'p']:
            anal_data['angles'][f'corr_{idx}_{eff}_ind'] = [np.arccos(anal_func.cosine_similarity(anal_data['alloc_res'][f'alloc_{idx}_{eff}'] * country_data['populations'], direct_eff_coef * country_data['populations'] * country_data['ifrs'])),]
            anal_data['angles'][f'corr_{idx}_{eff}_dir'] = [np.arccos(anal_func.cosine_similarity(anal_data['alloc_res'][f'alloc_{idx}_{eff}'] * country_data['populations'], contact_arr * country_data['populations'])),]
            anal_data['angles'][f'corr_{idx}_{eff}_tot'] = [np.arccos(anal_func.cosine_similarity(direct_eff_coef * country_data['populations'] * country_data['ifrs'], contact_arr * country_data['populations'])),]
    return anal_data