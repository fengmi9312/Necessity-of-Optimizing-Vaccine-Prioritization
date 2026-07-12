# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 14:06:52 2025

@author: MIFENG
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Dependencies.CodeDependencies import basic_params, func
from Dependencies.CodeDependencies.model import sir_delta
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func
from copy import deepcopy
from scipy.stats import pearsonr



def analyze(expr_data):  
    targets = ['w', 'x']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_from_fatality_by_contact_(coef_beta_1)']
    vac_avail = 0.3
    for country in countries:
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: rgd.data_of_countries[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([rgd.data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        
        for task_name, param_idx, target in itertools.product(task_names, range(40), targets):
            expr_name, expr_param = anal_func.get_expr_info(task_name)
            direct_effects_task_name = f'direct_effects_from_param_({expr_param})'
            if target == 'x': append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            else: append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_0}}'
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'min_max_corr': [], 'optimal_ind': [], 'optimal_dir': [], 'worst_ind': [], 'worst_dir': [], 'effect_corr': [], 'optimal_indx': [], 'optimal_dirx': [], 'worst_indx': [], 'worst_dirx': [], 'effect_corrx': []}
            if target == 'w': 
                sheet_name_x = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            for file_idx in range(40):
                alloc_data = expr_data[task_name][file_idx]['alloc']
                weights = expr_data[task_name][file_idx]['weights'][f'min_x_{append_name}']
                coef_target = {'w': calc_params['populations'], 'x': calc_params['populations'] * weights}
                direct_effects_coef = expr_data[direct_effects_task_name][0][f'{basic_params.country_abbr[country]}_{file_idx}'][str(param_idx)]
                if target == 'x': alloc_optimal, alloc_worst = alloc_data[f'min_x_{append_name}'].to_numpy(), alloc_data[f'max_x_{append_name}'].to_numpy()
                else: alloc_optimal, alloc_worst = alloc_data[f'min_x_{append_name}'].to_numpy(), alloc_data[f'max_x_{append_name}'].to_numpy()
                contact_arr = calc_params['contacts'].sum(axis = 1)
                
                anal_data[sheet_name]['effect_corrx'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_indx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dirx'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_indx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dirx'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                
                s_vol = expr_data[direct_effects_task_name][0][f's_{basic_params.country_abbr[country]}_{file_idx}'][str(param_idx)].to_numpy() * calc_params['populations']
                contact_arr = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-contact_arr)) / calc_params['populations']
                direct_effects_coef = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-direct_effects_coef)) / calc_params['populations']
                
                anal_data[sheet_name]['min_max_corr'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], alloc_worst * calc_params['populations']))
                anal_data[sheet_name]['effect_corr'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], calc_params['populations'] * contact_arr))
                anal_data[sheet_name]['optimal_ind'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['optimal_dir'].append(anal_func.cosine_similarity(alloc_optimal * calc_params['populations'], direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_ind'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], contact_arr * calc_params['populations']))
                anal_data[sheet_name]['worst_dir'].append(anal_func.cosine_similarity(alloc_worst * calc_params['populations'], direct_effects_coef * coef_target[target]))
                if target == 'w': anal_data[sheet_name_x]['alloc_corr'].append(pearsonr(alloc_data[f'min_x_dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'].to_numpy() * calc_params['populations'], alloc_data[f'min_x_{append_name}'].to_numpy() * calc_params['populations'])[0])
    return anal_data











# def get_eff_prop(vac_allocs, calc_params, expr_param, param_idx, file_idx):
#     r0 = np.exp(file_idx * 0.075)
#     param_vals = {'delay': 700, 'k_val': None, 'vac_eff': 0.95, 'vac_avail': 0.3, 'c_perct': 0.1}
#     param_list_dict = {'delay': np.arange(0, 2000, 50), 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 'c_perct': np.linspace(0.215, 0.8, 40)}
#     if expr_param in ['delay', 'c_perct', 'vac_avail', 'vac_eff']: param_vals[expr_param] = param_list_dict[expr_param][param_idx]
    
    
#     alpha_val, beta_val = 2.826, 5.665
#     srv_func = func.srv_weibull
#     srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#     calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
#     if param_vals['k_val'] is None:
#         param_vals['k_val'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
#     calc_params_delta = deepcopy(calc_params)
#     if expr_param in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']:
#         if expr_param.split('_')[1] == 'alpha':
#             steady_c_arr = func.get_steady_state(param_vals['k_val'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
#             steady_d = steady_c_arr @ calc_params['ifrs']
#         equal_ifr = np.ones(basic_params.group_amount) * calc_params['ifrs'].sum() / basic_params.group_amount
#         diff_ifr = calc_params['ifrs'] - equal_ifr
#         ifr_tmp = equal_ifr + param_idx * diff_ifr / 40
#         if expr_param.split('_')[1] == 'alpha': calc_params_delta['ifrs'] = ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp)
#         else: calc_params_delta['ifrs'] = ifr_tmp
    
#     calc_params_delta['k'] = param_vals['k_val']
#     calc_params_delta['eta'] = param_vals['vac_eff']
#     calc_params_delta['delay'] = param_vals['delay']
#     steady_c = func.get_steady_state(param_vals['k_val'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
#     init_c = calc_params['i0'] @ calc_params['populations']
    
#     simu_once = sir_delta(**calc_params_delta)
#     if simu_once.getc_c_tot() < param_vals['c_perct'] * (steady_c - init_c) + init_c:
#         while True:
#             simu_once.spread_once()
#             if simu_once.getc_c_tot() >= param_vals['c_perct'] * (steady_c - init_c) + init_c: break
    
#     coef_target = {'c': calc_params['populations'], 'd': calc_params['populations'] * calc_params['ifrs']}
#     time_int = simu_once._sir_delta__time_int
#     hidden_svu = simu_once._sir_delta__sv[time_int] + simu_once._sir_delta__u[time_int]
#     hidden_c = simu_once._sir_delta__c[time_int]
#     steady_non = simu_once.calc_prdt()
#     alloc_coef = simu_once._sir_delta__get_eff() * simu_once._sir_delta__eta
#     res = {'c': [], 'd': []}
#     alloc_all_ages = func.get_alloc(np.array(simu_once.getc_s()), simu_once.get_populations(), param_vals['vac_avail'], basic_params.empirical_groups['all_ages'])
#     if (file_idx, param_idx) in [(4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (5, 1), (6, 1), (7, 1), (4, 2), (5, 2), (6, 2), (7, 2), (6, 3)]:
#         print(vac_allocs['d']['optimal'])
    
#     for target in ['c', 'd']:
#         tot_eff_arr_optimal = steady_non - simu_once.calc_vac_prdt(vac_allocs[target]['optimal'])
#         tot_eff_arr_worst = steady_non - simu_once.calc_vac_prdt(vac_allocs[target]['worst'])
#         tot_eff_arr_all_ages = steady_non - simu_once.calc_vac_prdt(alloc_all_ages)
#         dir_eff_arr_optimal = (steady_non - hidden_c) * vac_allocs[target]['optimal'] * alloc_coef/ hidden_svu
#         dir_eff_arr_worst = (steady_non - hidden_c) * vac_allocs[target]['worst'] * alloc_coef / hidden_svu
#         dir_eff_arr_all_ages = (steady_non - hidden_c) * alloc_all_ages * alloc_coef / hidden_svu
#         optimal_corr = pearsonr(alloc_coef * coef_target[target], vac_allocs[target]['optimal'] * calc_params['populations'])[0] - pearsonr(calc_params['contacts'].sum(axis = 0) * calc_params['populations'], vac_allocs[target]['optimal'] * calc_params['populations'])[0]
#         worst_corr = pearsonr(alloc_coef * coef_target[target], vac_allocs[target]['worst'] * calc_params['populations'])[0] - pearsonr(calc_params['contacts'].sum(axis = 0) * calc_params['populations'], vac_allocs[target]['worst'] * calc_params['populations'])[0]
#         res[target] = [[tot_eff_arr_optimal @ coef_target[target], dir_eff_arr_optimal @ coef_target[target]], 
#                       [tot_eff_arr_worst @ coef_target[target], dir_eff_arr_worst @ coef_target[target]],
#                       [tot_eff_arr_all_ages @ coef_target[target], dir_eff_arr_all_ages @ coef_target[target]], [optimal_corr, worst_corr]]
#     return res


# def get_ifrs(vac_allocs, calc_params, expr_param, param_idx, file_idx):
#     if expr_param in ['delay', 'c_perct', 'vac_avail', 'vac_eff']: return calc_params['ifrs']
#     if expr_param in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']:
#         r0 = np.exp(file_idx * 0.075)
#         param_vals = {'delay': 700, 'k_val': None, 'vac_eff': 0.95, 'vac_avail': 0.3, 'c_perct': 0.1}
#         alpha_val, beta_val = 2.826, 5.665
#         srv_func = func.srv_weibull
#         srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#         calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
#         param_vals['k_val'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
#         if expr_param.split('_')[1] == 'alpha':
#             steady_c_arr = func.get_steady_state(param_vals['k_val'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
#             steady_d = steady_c_arr @ calc_params['ifrs']
#         equal_ifr = np.ones(basic_params.group_amount) * calc_params['ifrs'].sum() / basic_params.group_amount
#         diff_ifr = calc_params['ifrs'] - equal_ifr
#         ifr_tmp = equal_ifr + param_idx * diff_ifr / 40
#         if expr_param.split('_')[1] == 'alpha': return ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp)
#         else: return ifr_tmp
    





