# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:23:13 2025

@author: MIFENG
"""


from .analysis_dependencies import required_generated_data as rgd
import numpy as np
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    expr_name = 'optm_transition'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    country = 'United States'
    country_data = data_of_countries[country]
    pop_coef = country_data['populations'] * country_data['ifrs']
    contact_arr = np.sum([data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    anal_data = {'res': {}}
    for file_idx in range(41):
        anal_data['res'][f'corr_{file_idx}'] = []
        anal_data['res'][f'prdt_{file_idx}'] = []
        direct_eff_coef = expr_data['transition_direct_effects_(param)'][0]['res'][str(file_idx)]
        for idx in range(1001):
            alloc = expr_data[task_name][file_idx]['allocs'][f'alloc_{idx}']
            ind_eff = np.arccos(anal_func.cosine_similarity(alloc * country_data['populations'], direct_eff_coef * country_data['populations'] * country_data['ifrs']))
            dir_eff = np.arccos(anal_func.cosine_similarity(alloc * country_data['populations'], contact_arr * country_data['populations']))
            tot_eff = np.arccos(anal_func.cosine_similarity(direct_eff_coef * country_data['populations'] * country_data['ifrs'], contact_arr * country_data['populations']))
            anal_data['res'][f'corr_{file_idx}'].append((ind_eff - dir_eff) / tot_eff)
            anal_data['res'][f'prdt_{file_idx}'].append(expr_data[task_name][file_idx]['dists'][f'dist_{idx}'] @ pop_coef)
    return anal_data
    