# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:47:19 2024

@author: fengm
"""



import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
import pandas as pd
from .elements import simu_once
from data_loader import load_all_data
import func
import basic_params
from copy import deepcopy
import cache_generator
from itertools import combinations

def execute(expr_param, file_idx):
    coef_pos_list = []
    for r in range(1, 4):
        for combo in combinations([0, 1, 2, 3], r):
            coef_pos_list.append(list(combo))
    coef_pos = coef_pos_list[int(expr_param)]
    expr_param_name = ''.join(['hswo'[i] for i in coef_pos])
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    param_list = np.arange(40) / 40
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        for param_idx, param_val in enumerate(param_list):
            contacts_total = np.array([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']])
            k_val = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * contacts_total.sum(axis = 0))[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
            contacts_total[coef_pos] *= param_val
            calc_params['contacts'] = contacts_total.sum(axis = 0)
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            if not cache_generator.check_cache(expr_param, file_idx, param_name):
                print(f'Begin excuting {param_name}')
                single_res = simu_once.simulate(calc_params, imm_params = ('delay', 700), k_val = k_val, optm_targets=['c', 'd'])
                growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
                mean_gen = mean_func(alpha_val, beta_val)
                single_res.update({f'transmission_params_{expr_param_name}': {'params': pd.Series([r0, growth_rate, mean_gen], index=['r0', 'growth_rate', 't_gen'])}})
                cache_generator.add_cache(expr_param, file_idx, param_name, single_res)
                print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for country_idx, country in enumerate(countries):
        for param_idx, param_val in enumerate(param_list):
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            single_res = cache_generator.get_cache(expr_param, file_idx, param_name)
            for data_key in single_res.keys():
                if data_key not in res: res[data_key] = {}
                for key, item in single_res[data_key].items():
                    res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expr_param, file_idx)
    print('Return Data')
    return res


