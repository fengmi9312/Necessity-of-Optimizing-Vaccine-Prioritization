# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:26:26 2025

@author: MIFENG
"""



from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import itertools

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    country = 'United States'
    country_data = data_of_countries[country]    
    pop_dist = country_data['populations'] 
    ifr_dist = country_data['populations'] * country_data['ifrs']
    expr_name, expr_param = 'necs_from_param', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    example_alloc = {}
    example_res = {}
    example_points = [(8, 8), (28, 8)]
    coef_dist = {'c': pop_dist, 'd': ifr_dist}
    for idx, (r0_idx, delay_idx) in enumerate(example_points):
        dist_data = expr_data[task_name][r0_idx]['dist']
        alloc_data = expr_data[task_name][r0_idx]['alloc']
        append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
        for optm_target, acc_type in itertools.product(['c', 'd'], ['dd', 'gd']):
            example_alloc[f'min_{optm_target}_{idx}_{acc_type}'] = alloc_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() * country_data['populations']
            for res_target in ['c', 'd']:
                example_res[f'min_{optm_target}_res_{res_target}_{idx}_{acc_type}'] = [dist_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() @ coef_dist[res_target]]
        for res_target, acc_type in itertools.product(['c', 'd'], ['dd', 'gd']):
            example_res[f'no_vac_res_{res_target}_{idx}_{acc_type}'] = [dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ coef_dist[res_target]]
    return {'example_alloc': example_alloc, 'example_res': example_res}
