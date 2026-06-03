# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 19:59:12 2025

@author: fengm
"""



import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
import pandas as pd
from .elements import simu_once
from Dependencies.FrameDependencies.data_loader import load_all_data
import func
import basic_params
from copy import deepcopy
from Dependencies.FrameDependencies import cache_generator

def execute(expr_param, file_idx):
    if expr_param != 'delay': return None
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    param_idx, r0 = [(10, 1.01), (10, 1.8), (10, 4.8), (10, 12), (10, 30), (10, 2), (8, 1.05), (8, 1.8), (8, 5.5), (8, 16), (8, 50), (10, 5.5)][file_idx]
    param_val = np.arange(0, 2000, 50)[param_idx]
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}'
        if not cache_generator.check_cache(expr_param, file_idx, param_name):
            print(f'Begin excuting {param_name}')
            srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
            calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
            if expr_param == 'delay': single_res = simu_once.simulate(calc_params, imm_params=('delay', param_val), r0 = r0, get_curve = True, optm_targets = ['c', 'd'])
            else: single_res = simu_once.simulate(calc_params, r0 = r0, **{expr_param: param_val})
            growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
            mean_gen = mean_func(alpha_val, beta_val)
            single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen, param_val], index=['r0', 'growth_rate', 't_gen', expr_param])}})
            cache_generator.add_cache(expr_param, file_idx, param_name, single_res)
            print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for country_idx, country in enumerate(countries):
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}'
        single_res = cache_generator.get_cache(expr_param, file_idx, param_name)
        for data_key in single_res.keys():
            if data_key not in res: res[data_key] = {}
            for key, item in single_res[data_key].items():
                res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expr_param, file_idx)
    print('Return Data')
    return res