# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:01:13 2025

@author: MIFENG
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
from .analysis_dependencies import anal_func
import numpy as np
import itertools


def analyze(expr_data):
    vac_avail = 0.3
    data_of_countries = rgd.data_of_countries
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_line_from_fatality_(coef_beta_1_0)', 'necs_line_from_fatality_(coef_beta_1_13)', 'necs_line_from_fatality_(coef_beta_1_26)', 'necs_line_from_fatality_(coef_beta_1_39)', 
                  'necs_line_from_param_(delay_10)', 'necs_line_from_param_(delay_8)', 'necs_line_from_param_(delay_13)', 'necs_line_from_param_(delay_26)']
    for country in countries:
        for task_name, target in itertools.product(task_names, targets):
            expr_name, expr_param = anal_func.get_expr_info(task_name)
            sheet_name = f'{task_name}_{target}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'optimal_ind': [], 'worst_ind': [], 'optimal_dir': [], 'worst_dir': [], 'effect_corr': [], 'max_min_corr': [], 'optimal_indx': [], 'optimal_dirx': [], 'worst_indx': [], 'worst_dirx': [], 'effect_corrx': []}
            if target == 'c': 
                sheet_name_x = f'{task_name}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            for file_idx, param_idx in itertools.product(range(40), range(40)):
                if expr_name == 'necs_line_from_param': ifrs = data_of_countries[country]['ifrs']
                else: ifrs = rgd.country_ifrs[country][expr_param.split('_')[1]][file_idx * 40 + param_idx][int(expr_param.split('_')[-1])]
                coef_target = {'c': data_of_countries[country]['populations'], 'd': data_of_countries[country]['populations'] * ifrs}
                append_name = f"dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}"
                alloc_data = expr_data[task_name][file_idx]['alloc']
                direct_effects_coef = expr_data[f'direct_effects_line_from_param_({expr_param})'][0][f'{basic_params.country_abbr[country]}'][str(file_idx * 40 + param_idx)].to_numpy()
                contact_arr = np.sum([data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
                
                anal_data[sheet_name]['effect_corrx'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], data_of_countries[country]['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_indx'].append(anal_func.cosine_similarity(alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], contact_arr * data_of_countries[country]['populations']))
                anal_data[sheet_name]['worst_indx'].append(anal_func.cosine_similarity(alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], contact_arr * data_of_countries[country]['populations']))
                anal_data[sheet_name]['optimal_dirx'].append(anal_func.cosine_similarity(alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], coef_target[target] * direct_effects_coef))
                anal_data[sheet_name]['worst_dirx'].append(anal_func.cosine_similarity(alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], coef_target[target] * direct_effects_coef))
                
                s_vol = expr_data[f'direct_effects_line_from_param_({expr_param})'][0][f's_{basic_params.country_abbr[country]}'][str(file_idx * 40 + param_idx)].to_numpy() * data_of_countries[country]['populations']
                contact_arr = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-contact_arr)) / data_of_countries[country]['populations']
                direct_effects_coef = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-direct_effects_coef)) / data_of_countries[country]['populations']
                
                anal_data[sheet_name]['effect_corr'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], data_of_countries[country]['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_ind'].append(anal_func.cosine_similarity(alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], contact_arr * data_of_countries[country]['populations']))
                anal_data[sheet_name]['worst_ind'].append(anal_func.cosine_similarity(alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], contact_arr * data_of_countries[country]['populations']))
                anal_data[sheet_name]['optimal_dir'].append(anal_func.cosine_similarity(alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], coef_target[target] * direct_effects_coef))
                anal_data[sheet_name]['worst_dir'].append(anal_func.cosine_similarity(alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], coef_target[target] * direct_effects_coef))
                anal_data[sheet_name]['max_min_corr'].append(anal_func.cosine_similarity(alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations'], alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations']))
                if target == 'c': anal_data[sheet_name_x]['alloc_corr'].append(anal_func.cosine_similarity(alloc_data[f'min_c_{append_name}'].to_numpy() * data_of_countries[country]['populations'], alloc_data[f'min_d_{append_name}'].to_numpy() * data_of_countries[country]['populations']))
    return anal_data
