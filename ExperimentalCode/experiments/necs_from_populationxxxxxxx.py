# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 17:11:33 2024

@author: 20481756
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm
import func
import basic_params
import cache_generator
from .elements import simu_once
import pandas as pd
from copy import deepcopy
from data_loader import load_all_data


def generate_dist(peak = 30, equity = 0.2, group_amount = basic_params.group_amount):
    tau_step = 80 / group_amount
    if equity == 0:
        return np.ones(group_amount) / group_amount
    if equity == 1:
        return np.eye(group_amount)[peak // group_amount]
    
    def get_normal_dist(sigma):
        dist = [norm.sf((i + 1) * tau_step, peak, sigma) - norm.sf(i * tau_step, peak, sigma) for i in range(group_amount)]
        return np.array(dist) / np.sum(dist)
    
    def equation(x):
        return equity - func.calc_equity(get_normal_dist(x[0]))
    
    param = fsolve(equation, [1,])[0]
    return get_normal_dist(param)



def execute(expr_param, file_idx):
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    param_list = np.linspace(0, 0.8775, 40) if expr_param == 'equity' else np.linspace(0, 78, 40)
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        for param_idx, param_val in enumerate(param_list):
            calc_params['populations'] = generate_dist(**{expr_param: param_val})
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            if not cache_generator.check_cache(expr_param, file_idx, param_name):
                print(f'Begin excuting {param_name}')
                single_res = simu_once.simulate(calc_params, r0 = r0, optm_targets=['c', 'd'])
                growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
                mean_gen = mean_func(alpha_val, beta_val)
                single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen], index=['r0', 'growth_rate', 't_gen'])}})
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

























