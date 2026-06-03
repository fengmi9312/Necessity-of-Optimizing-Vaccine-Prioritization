# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:59:31 2024

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
import itertools

def execute(expt_param, file_idx):
    func_type, func_idx = expt_param.split('_')
    mean_inf, mean_rem = [[1.5, 3.5], [2, 3], [2.5, 2.5]][int(func_idx)]
    srv_func = {'weibull': func.srv_weibull, 'gamma': func.srv_gamma, 'lognormal': func.srv_lognormal}[func_type]
    pow_list = {'weibull': np.arange(-6, 31, 6), 'gamma': np.arange(-6, 31, 6), 'lognormal': np.arange(5, 36, 5)}[func_type]
    pow_special = list(itertools.product(pow_list[::3], pow_list[::3]))
    beta_func = {'weibull': func.get_beta_from_weibull, 'gamma': func.get_beta_from_gamma, 'lognormal': func.get_beta_from_lognormal}[func_type]
    param_func = {'weibull': lambda _val_pow: np.exp(_val_pow * 0.05), 'gamma': lambda _val_pow: np.exp(_val_pow * 0.1), 'lognormal': lambda _val_pow: _val_pow * 0.05}[func_type]
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'contacts', 'ifrs', 'ylls']})
        g, _ = func.fit_g(country_data[country]['confirmed'][:90] / country_data[country]['total_population'], basic_params.beginning[country])
        r0 = func.calc_r0(g, 2.826, 5.665)
        for inf_idx, inf_pow in enumerate(pow_list):
            for rem_idx, rem_pow in enumerate(pow_list):
                param_idx = f'{basic_params.country_abbr[country]}_{inf_idx}_{rem_idx}'
                if not cache_generator.check_cache(expt_param, file_idx, param_idx):
                    print(f'Begin excuting {param_idx}')
                    alpha_inf, alpha_rem = param_func(inf_pow), param_func(rem_pow)
                    beta_inf, beta_rem = beta_func(alpha_inf, mean_inf), beta_func(alpha_rem, mean_rem)
                    srv_inf, srv_rem = srv_func(alpha_inf, beta_inf, basic_params.srv_length, calc_params['step']), srv_func(alpha_rem, beta_rem, basic_params.srv_length, calc_params['step'])
                    calc_params['srv_inf'], calc_params['srv_rem'] = srv_inf, srv_rem
                    single_res = simu_once.simulate(calc_params, imm_params=('delay', file_idx * basic_params.day_div), r0 = r0, get_curve = True if (inf_pow, rem_pow) in pow_special and file_idx == 3 else False)
                    mean_gen = func.get_mean_from_srv(func.get_gen_srv(srv_inf, srv_rem, calc_params['step']), calc_params['step'])
                    growth_rate = func.find_g(srv_inf, srv_rem, r0, calc_params['step'])
                    delay_day = file_idx
                    single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, delay_day, mean_gen], index=['r0', 'growth_rate', 't_resp', 't_gen'])}})
                    cache_generator.add_cache(expt_param, file_idx, param_idx, single_res)
                    print(f'Complete {param_idx}')
    print('Gather Data')
    res = {}
    for country_idx, country in enumerate(countries):
        for inf_idx, inf_pow in enumerate(pow_list):
            for rem_idx, rem_pow in enumerate(pow_list):
                param_idx = f'{basic_params.country_abbr[country]}_{inf_idx}_{rem_idx}'
                single_res = cache_generator.get_cache(expt_param, file_idx, param_idx)
                for data_key in single_res.keys():
                    if data_key not in res: res[data_key] = {}
                    for key, item in single_res[data_key].items():
                        res[data_key][f'{key}_{{{param_idx}}}'] = pd.Series(item)
    cache_generator.del_cache(expt_param, file_idx)
    print('Return Data')
    return res
