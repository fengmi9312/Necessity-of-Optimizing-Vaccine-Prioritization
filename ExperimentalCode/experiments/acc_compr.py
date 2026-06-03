# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 19:01:52 2024

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


def execute(expt_param, file_idx):
    acc_param_list = {'var': np.linspace(1.5 / 21, 0.5, 20), 'delay': np.arange(3, 23) * basic_params.day_div, 'half_domain': np.arange(0, 20) * 50}[expt_param][file_idx::5]
    calc_params = deepcopy(basic_params.calc_params)
    country = 'United States'
    alpha, beta = 2.826, 5.665
    srv_func = func.srv_weibull
    country_data = load_all_data([country], basic_params.group_div)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'contacts', 'ifrs', 'ylls']})
    g, _ = func.fit_g(country_data[country]['confirmed'][:90] / country_data[country]['total_population'], basic_params.beginning[country])
    for param_idx, acc_param in enumerate(acc_param_list):
        if not cache_generator.check_cache(expt_param, file_idx, param_idx):
            print(f'Begin excuting {param_idx}')
            srv_gen = srv_func(alpha, beta, basic_params.srv_length, calc_params['step'])
            calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
            r0 = func.calc_r0(g, alpha, beta)
            single_res = simu_once.simulate(calc_params, imm_params=(expt_param, acc_param), r0 = r0, gg = True)
            mean_gen = func.get_mean_from_srv(srv_gen, calc_params['step'])
            single_res.update({'transmission_params': {'params': pd.Series([r0, g, acc_param, mean_gen], index=['r0', 'growth_rate', expt_param, 't_gen'])}})
            cache_generator.add_cache(expt_param, file_idx, param_idx, single_res)
            print(f'Complete {param_idx}')
    print('Gather Data')
    res = {}
    for param_idx, acc_param in enumerate(acc_param_list):
        single_res = cache_generator.get_cache(expt_param, file_idx, param_idx)
        for data_key in single_res.keys():
            if data_key not in res: res[data_key] = {}
            for key, item in single_res[data_key].items():
                res[data_key][f'{key}_{{{param_idx}}}'] = pd.Series(item)
    cache_generator.del_cache(expt_param, file_idx)
    print('Return Data')
    return res