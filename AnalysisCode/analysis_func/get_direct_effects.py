# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 14:06:52 2025

@author: MIFENG
"""

from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from copy import deepcopy



def analyze(expr_data):  
    targets = ['c', 'd']
    anal_data = {}
    data_types = ['delay', 'coef_beta_1']
    
    country = 'United States'
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: rgd.data_of_countries[country][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([rgd.data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    
    coef_target = {'c': calc_params['populations'], 'd': calc_params['populations'] * calc_params['ifrs']}
    for data_type, param_idx, target in itertools.product(data_types, range(40), targets):
        direct_effects_task_name = f'direct_effects_from_param_({data_type})'
        sheet_name = f'{data_type}_{param_idx}_{target}'
        anal_data[sheet_name] = {}
        for file_idx in range(40):
            if data_type == 'delay': ifrs = calc_params['ifrs']
            else: ifrs = rgd.country_ifrs[country][data_type.split('_')[1]][file_idx * 40][param_idx]
            coef_target = {'c': 1, 'd': ifrs}
            direct_effects_coef = expr_data[direct_effects_task_name][0][f'{basic_params.country_abbr[country]}_{file_idx}'][str(param_idx)]
            anal_data[sheet_name][str(file_idx)] = direct_effects_coef * coef_target[target]
                
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
    





