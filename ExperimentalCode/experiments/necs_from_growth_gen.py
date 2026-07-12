# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 19:00:40 2024

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
    func_type, func_idx = expr_param.split('_')
    alpha_val = {'weibull':[0.7, 1, 2], 'gamma':[0.7, 1, 2], 'lognormal':[0.15, 0.45, 1.35]}[func_type][int(func_idx)]
    srv_func = {'weibull': func.srv_weibull, 'gamma': func.srv_gamma, 'lognormal': func.srv_lognormal}[func_type]
    beta_func = {'weibull': func.get_beta_from_weibull, 'gamma': func.get_beta_from_gamma, 'lognormal': func.get_beta_from_lognormal}[func_type]
    mean_func = {'weibull': func.get_mean_from_weibull, 'gamma': func.get_mean_from_gamma, 'lognormal': func.get_mean_from_lognormal}[func_type]
    delay = file_idx * basic_params.day_div
    mean_list = np.arange(1, 10)
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        for r0_idx, r0_pow in enumerate(np.array([8, 16, 24, 32]) * 0.075):
            r0 = np.exp(r0_pow)
            for mean_idx, mean_val in enumerate(mean_list):
                param_name = f'{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}'
                if not cache_generator.check_cache(expr_param, file_idx, param_name):
                    print(f'Begin excuting {param_name}')
                    beta_val = beta_func(alpha_val, mean_val)
                    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
                    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
                    single_res = simu_once.simulate(calc_params, imm_params=('delay', delay), r0 = r0, optm_targets = ['c', 'd'])
                    mean_gen = mean_func(alpha_val, beta_val)
                    growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
                    delay_day = delay * calc_params['step']
                    single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, delay_day, mean_gen], index=['r0', 'growth_rate', 't_resp', 't_gen'])}})
                    cache_generator.add_cache(expr_param, file_idx, param_name, single_res)
                    print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for country_idx, country in enumerate(countries):
        for r0_idx, r0_pow in enumerate(np.array([8, 16, 24, 32]) * 0.075):
            for mean_idx, mean_val in enumerate(mean_list):
                param_name = f'{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}'
                single_res = cache_generator.get_cache(expr_param, file_idx, param_name)
                for data_key in single_res.keys():
                    if data_key not in res: res[data_key] = {}
                    for key, item in single_res[data_key].items():
                        res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expr_param, file_idx)
    print('Return Data')
    return res

