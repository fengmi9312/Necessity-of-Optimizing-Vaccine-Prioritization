# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 14:06:52 2025

@author: MIFENG
"""

from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func
from copy import deepcopy
from scipy.stats import pearsonr



def analyze(expr_data):  
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_from_param_by_eta_(delay)']
    vac_avail = 0.3
    eta_arr = np.array([0.88, 0.95, 0.96, 0.97, 0.97, 0.96, 0.95, 0.95, 0.94, 0.93, 0.91, 0.88, 0.75, 0.70, 0.65, 0.60])
    for country in countries:
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: rgd.data_of_countries[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([rgd.data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        
        for task_name, param_idx, target in itertools.product(task_names, range(40), targets):
            expr_name, expr_param = anal_func.get_expr_info(task_name)
            direct_effects_task_name = f'direct_effects_from_param_({expr_param})'
            append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'min_max_corr': [], 'optimal_ind': [], 'optimal_dir': [], 'worst_ind': [], 'worst_dir': [], 'effect_corr': [], 'optimal_indx': [], 'optimal_dirx': [], 'worst_indx': [], 'worst_dirx': [], 'effect_corrx': []}
            if target == 'c': 
                sheet_name_x = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            for file_idx in range(40):
                ifrs = calc_params['ifrs']
                coef_target = {'c': calc_params['populations'], 'd': calc_params['populations'] * ifrs}
                alloc_data = expr_data[task_name][file_idx]['alloc']
                direct_effects_coef = expr_data[direct_effects_task_name][0][f'{basic_params.country_abbr[country]}_{file_idx}'][str(param_idx)] * eta_arr / 0.95
                contact_arr = calc_params['contacts'].sum(axis = 1)
                alloc_optimal, alloc_worst = alloc_data[f'min_{target}_{append_name}'].to_numpy(), alloc_data[f'max_{target}_{append_name}'].to_numpy()
                
                
                anal_data[sheet_name]['effect_corrx'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_indx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dirx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_indx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dirx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                
                s_vol = expr_data[direct_effects_task_name][0][f's_{basic_params.country_abbr[country]}_{file_idx}'][str(param_idx)].to_numpy() * calc_params['populations']
                contact_arr = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-contact_arr)) / calc_params['populations']
                direct_effects_coef = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-direct_effects_coef)) / calc_params['populations']
                
                anal_data[sheet_name]['effect_corr'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_ind'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dir'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_ind'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dir'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['min_max_corr'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], alloc_worst * calc_params['populations']))
                if target == 'c': anal_data[sheet_name_x]['alloc_corr'].append(pearsonr(alloc_data[f'min_c_{append_name}'].to_numpy() * calc_params['populations'], alloc_data[f'min_d_{append_name}'].to_numpy() * calc_params['populations'])[0])
    return anal_data



