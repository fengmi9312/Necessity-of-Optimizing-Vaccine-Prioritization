# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:34:19 2025

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
import basic_params
import numpy as np


info = {}

key_list = []
for optm_dir in ['max', 'min']:
    for target in ['c', 'd']:
        for acc_type in ['gd', 'dd']:
            for get_dur in [True, False]:
                if get_dur: key_list.append(f'{optm_dir}_{target}_{acc_type}_dur')
                else: key_list.append(f'{optm_dir}_{target}_{acc_type}')

for acc_type in ['gd', 'dd']:
    key_list.append(f'no_vac_{acc_type}')

expr_info = {'necs_from_contact': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
             'necs_from_population': ['peak', 'equity'],
             'necs_line_from_param': ['delay_8', 'delay_10', 'delay_0', 'delay_13', 'delay_26', 'delay_39'],
             'necs_from_fatality': ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1'],
             'necs_from_fatality_init': ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1'],
             'necs_line_from_fatality': ['coef_alpha_0_0', 'coef_alpha_0_13', 'coef_alpha_0_26', 'coef_alpha_0_39',
                                         'coef_alpha_1_0', 'coef_alpha_1_13', 'coef_alpha_1_26', 'coef_alpha_1_39',
                                         'coef_beta_0_0', 'coef_beta_0_13', 'coef_beta_0_26', 'coef_beta_0_39',
                                         'coef_beta_1_0', 'coef_beta_1_13', 'coef_beta_1_26', 'coef_beta_1_39'],
             'necs_from_param': ['delay', 'vac_eff', 'vac_avail', 'c_perct', 'vac_dur'],
             'necs_from_param_init': ['delay', 'vac_eff', 'vac_avail', 'c_perct', 'vac_dur'],
             'necs_from_example': ['delay'], 'necs_line_from_add': ['param']}

for expr_name, expr_param_list in expr_info.items():
    info[expr_name] = {}
    countries = ['United States']
    r0_list = np.exp(np.arange(40) * 0.075)
    for expr_param in expr_param_list:
        info[expr_name][expr_param] = []
        for r0_idx, r0 in enumerate(r0_list):
            info[expr_name][expr_param].append({})
            for data_key in ['dist', 'alloc']:
                info[expr_name][expr_param][-1][data_key] = []
                list_tmp = info[expr_name][expr_param][-1][data_key]
                for country_idx, country in enumerate(countries):
                    for param_idx in range(40):
                        param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
                        for key in key_list:
                            if data_key == 'alloc' and key[:6] == 'no_vac': continue
                            if data_key == 'dist': 
                                list_tmp.append(f'{key}_{{{param_name}}}')
                            else: 
                                if key[-3:] != 'dur': list_tmp.append(f'{key}_{{{param_name}}}')

expr_info = {'necs_from_example': ['delay']}
curve_types = []
for sttg in ['max_c', 'max_d', 'min_c', 'min_d', 'no_vac', 'under_20', '20-49', '20+', '60+', 'all_ages']:
    for acc_type in ['dd', 'gd']:
        curve_types.append(f'curve_{sttg}_{acc_type}')
        curve_types.append(f'curve_{sttg}_{acc_type}_dur')
        

for expr_name, expr_param_list in expr_info.items():
    info[expr_name] = {}
    countries = ['United States']
    for expr_param in expr_param_list:
        info[expr_name][expr_param] = []
        for idx in range(10):
            info[expr_name][expr_param].append({})
            for data_key in ['dist', 'alloc'] + curve_types:
                info[expr_name][expr_param][-1][data_key] = []
                list_tmp = info[expr_name][expr_param][-1][data_key]
                for country_idx, country in enumerate(countries):
                    param_name = f'{expr_param}_{basic_params.country_abbr[country]}'
                    if data_key == 'dist': 
                        for key in key_list: list_tmp.append(f'{key}_{{{param_name}}}')
                    elif data_key == 'alloc': 
                        for key in key_list:
                            if key[-3:] != 'dur' and key[:6] != 'no_vac': list_tmp.append(f'{key}_{{{param_name}}}')
                    else:
                        list_tmp.append(f'time_line_{{{param_name}}}')
                        for target in ['s', 'i', 'r', 'c', 'd']:
                            list_tmp.append(f'curve_{target}_{{{param_name}}}')
                        for target in ['c', 'd']:
                            if 'dd' in data_key.split('_'): list_tmp.append(f'prdt_{target}_{{{param_name}}}')
                

expr_info = {'necs_from_growth_gen': ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']}
mean_list = np.arange(1, 10)

for expr_name, expr_param_list in expr_info.items():
    info[expr_name] = {}
    countries = ['United States', 'Ireland', 'Japan']
    r0_list = np.exp(np.arange(40) * 0.075)
    for expr_param in expr_param_list:
        info[expr_name][expr_param] = []
        for file_idx in range(9):
            info[expr_name][expr_param].append({})
            for data_key in ['dist', 'transmission_params']:
                info[expr_name][expr_param][-1][data_key] = []
                list_tmp = info[expr_name][expr_param][-1][data_key]
                for country_idx, country in enumerate(countries):
                    for r0_idx, r0_pow in enumerate(np.array([8, 16, 24, 32]) * 0.075):
                        for mean_idx, mean_val in enumerate(mean_list):
                            param_name = f'{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}'
                            if data_key == 'dist':
                                for key in key_list:
                                    list_tmp.append(f'{key}_{{{param_name}}}')
                            else:
                                list_tmp.append(f'params_{{{param_name}}}')

expr_info = {'necs_from_growth_s': ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']}
for expr_name, expr_param_list in expr_info.items():
    info[expr_name] = {}
    countries = ['United States']
    for expr_param in expr_param_list:
        info[expr_name][expr_param] = []
        for file_idx in range(40):
            mean_list = np.arange(1, 11, 4) + (file_idx % 4)
            info[expr_name][expr_param].append({})
            for data_key in ['dist', 'transmission_params']:
                info[expr_name][expr_param][-1][data_key] = []
                list_tmp = info[expr_name][expr_param][-1][data_key]
                for country_idx, country in enumerate(countries):
                    for r0_idx, r0 in enumerate(np.exp(np.arange(40) * 0.075)):
                        for mean_idx, mean_val in enumerate(mean_list):
                            param_name = f'{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}'
                            if data_key == 'dist':
                                for key in key_list:
                                    list_tmp.append(f'{key}_{{{param_name}}}')
                            else:
                                list_tmp.append(f'params_{{{param_name}}}')




expr_info = {'necs_from_country': ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']}
mean_list = np.arange(1, 10)

for expr_name, expr_param_list in expr_info.items():
    info[expr_name] = {}
    for expr_param in expr_param_list:
        info[expr_name][expr_param] = []
        for file_idx in range(40):
            info[expr_name][expr_param].append({})
            for data_key in ['dist', 'alloc', 'transmission_params']:
                info[expr_name][expr_param][-1][data_key] = []
                list_tmp = info[expr_name][expr_param][-1][data_key]
                for contact_type in ['none', 's', 'w', 'o', 'swo']:
                    for param_idx in range(25):
                        param_name = f'{contact_type}_{param_idx}'
                        if data_key == 'dist':
                            for key in key_list:
                                list_tmp.append(f'{key}_{{{param_name}}}')
                        elif data_key == 'alloc':
                            if key[-3:] != 'dur' and key[:6] != 'no_vac': list_tmp.append(f'{key}_{{{param_name}}}')
                        else:
                            list_tmp.append(f'params_{{{param_name}}}')

def check_info(func_name, task_param):
    if func_name not in info:
        return False
    else:
        if task_param not in info[func_name]: return False
        else: return True
        
def get_file_amount(func_name, task_param):
    return len(info[func_name][task_param])














