# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 11:34:32 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func
from copy import deepcopy



def analyze(expr_data):  
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_from_time_course_(param)']
    
    for country in countries:
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: rgd.data_of_countries[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([rgd.data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        
        coef_target = {'c': calc_params['populations'], 'd': calc_params['populations'] * calc_params['ifrs']}
        
        param_idx = 14
        for task_name, target in itertools.product(task_names, targets):
            expr_name, expr_param = anal_func.get_expr_info(task_name)
            direct_effects_task_name = 'direct_effects_from_param_(delay)'
            append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'optimal_ind': [], 'optimal_dir': [], 'worst_ind': [], 'worst_dir': [], 'effect_corr': [], 'min_max_corr': [], 'optimal_indx': [], 'optimal_dirx': [], 'worst_indx': [], 'worst_dirx': [], 'effect_corrx': []}
            
            if target == 'c': 
                sheet_name_x = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            vac_avail = 0.3
            for file_idx in range(40):
                ifrs = calc_params['ifrs']
                coef_target = {'c': calc_params['populations'], 'd': calc_params['populations'] * ifrs}
                alloc_data = expr_data[task_name][file_idx]['alloc']
                alloc_optimal, alloc_worst = alloc_data[f'min_{target}_{append_name}'].to_numpy(), alloc_data[f'max_{target}_{append_name}'].to_numpy()
                contact_arr = calc_params['contacts'].sum(axis = 1)
                direct_effects_coef = expr_data[direct_effects_task_name][0][f'{basic_params.country_abbr[country]}_{file_idx}']['14']
                
                
                anal_data[sheet_name]['effect_corrx'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_indx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dirx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_indx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dirx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                
                s_vol = expr_data[direct_effects_task_name][0][f's_{basic_params.country_abbr[country]}_{file_idx}']['14'].to_numpy() * calc_params['populations']
                contact_arr = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-contact_arr)) / calc_params['populations']
                direct_effects_coef = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-direct_effects_coef)) / calc_params['populations']
                
                anal_data[sheet_name]['effect_corr'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_ind'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dir'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_ind'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dir'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                
                anal_data[sheet_name]['min_max_corr'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], alloc_worst * calc_params['populations']))
                if target == 'c': anal_data[sheet_name_x]['alloc_corr'].append(anal_func.cosine_similarity(alloc_data[f'min_c_{append_name}'].to_numpy() * calc_params['populations'], alloc_data[f'min_d_{append_name}'].to_numpy() * calc_params['populations']))
    return anal_data



