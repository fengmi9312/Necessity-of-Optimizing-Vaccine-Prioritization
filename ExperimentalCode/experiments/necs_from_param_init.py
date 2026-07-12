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

def execute(expr_param, file_idx):
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    param_list = {'delay': np.arange(0, 2000, 50), 
                  'vac_eff': np.linspace(0.22, 1, 40), 
                  'vac_avail': np.linspace(0.12, 0.9, 40), 
                  'c_perct': np.linspace(0.215, 0.8, 40), 
                  'vac_dur': np.arange(1, 41)}[expr_param]
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        for param_idx, param_val in enumerate(param_list):
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            if not cache_generator.check_cache(expr_param, file_idx, param_name):
                print(f'Begin excuting {param_name}')
                srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
                calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
                if expr_param == 'delay': single_res = simu_once.simulate(calc_params, imm_params=('delay', param_val), r0 = r0, optm_targets=['c', 'd'], c_perct = 0)
                else: single_res = simu_once.simulate(calc_params, r0 = r0, **{expr_param: param_val}, optm_targets=['c', 'd'], c_perct = 0)
                growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
                mean_gen = mean_func(alpha_val, beta_val)
                single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen, param_val], index=['r0', 'growth_rate', 't_gen', expr_param])}})
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


