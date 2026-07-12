# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 00:19:24 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
import numpy as np
import func
import basic_params
import cache_generator
from .elements import simu_once
import pandas as pd
from copy import deepcopy
from data_loader import load_all_data

def execute(expr_param, file_idx):
    if '_'.join(expr_param.split('_')[:-1]) not in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']: return None
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    r0_head = file_idx
    param_val = int(expr_param.split('_')[-1]) / 39
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        equal_ifr = np.ones(basic_params.group_amount) * country_data[country]['ifrs'].sum() / basic_params.group_amount
        diff_ifr = country_data[country]['ifrs'] - equal_ifr
        ifr_tmp = equal_ifr + param_val * diff_ifr
        for r0_tail in range(40):
            r0 = np.exp((r0_head + r0_tail / 40) * 0.075)
            if expr_param.split('_')[1] == 'alpha':
                k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
                steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
                steady_d = steady_c_arr @ country_data[country]['ifrs']
                calc_params['ifrs'] = ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp)
            else: calc_params['ifrs'] = ifr_tmp
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{r0_tail}'
            if not cache_generator.check_cache(expr_param, file_idx, param_name):
                print(f'Begin excuting {param_name}')
                single_res = simu_once.simulate(calc_params, imm_params = ('delay', 700) if expr_param.split('_')[-2] == '1' else ('delay', 0), r0 = r0, optm_targets=['c', 'd'])
                growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
                mean_gen = mean_func(alpha_val, beta_val)
                single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen], index=['r0', 'growth_rate', 't_gen'])}})
                cache_generator.add_cache(expr_param, file_idx, param_name, single_res)
                print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for country_idx, country in enumerate(countries):
        for r0_tail in range(40):
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{r0_tail}'
            single_res = cache_generator.get_cache(expr_param, file_idx, param_name)
            for data_key in single_res.keys():
                if data_key not in res: res[data_key] = {}
                for key, item in single_res[data_key].items():
                    res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expr_param, file_idx)
    print('Return Data')
    return res




