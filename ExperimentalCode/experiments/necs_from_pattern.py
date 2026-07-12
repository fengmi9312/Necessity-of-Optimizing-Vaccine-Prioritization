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

def generate_contacts(diff_group = 0.005, cross_group = 0.3, intra_group = 0.001, group_amount = 16, family_diff = 25, age_peak = 16):
    tau_step = 80 / group_amount
    contacts = [[(np.exp(- diff_group * abs(i - j) * tau_step) + cross_group * np.exp(- diff_group * abs(abs(i - j)  * tau_step - family_diff))) 
                 * np.exp(- intra_group * (abs(i * tau_step - age_peak) + abs(j  * tau_step - age_peak))) for j in range(group_amount)] 
                for i in range(group_amount)]
    return np.array(contacts) / np.sum(contacts)


def generate_dist(peak = 30, equity = 0.2, group_amount = 16):
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



def execute(expt_param, file_idx):
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    param_list = {'diff_group': np.linspace(0.005, 0.2, 40), 
                  'cross_group': np.linspace(0.025, 1, 40), 
                  'intra_group': np.linspace(0.001, 0.04, 40), 
                  'pop_peak': np.linspace(0, 78, 40),
                  'pop_equity': np.linspace(0, 0.8775, 40)}[expt_param]
    r0 = np.linspace(1.05, 3, 40)[file_idx]
    calc_params = deepcopy(basic_params.calc_params)
    country_data = load_all_data(['United States'], basic_params.group_div)['United States']
    calc_params.update({'populations': generate_dist(30, 0, group_amount = basic_params.group_amount), 'contacts': generate_contacts(diff_group = 0.1, cross_group = 0.3, intra_group = 0.02, group_amount = basic_params.group_amount), 
                        'ifrs': country_data['ifrs'], 'ylls': country_data['ylls']})
    for param_idx, param_val in enumerate(param_list):
        param_name = f'{expt_param}_{param_idx}'
        if not cache_generator.check_cache(expt_param, file_idx, param_name):
            print(f'Begin excuting {param_name}')
            if expt_param in ['diff_group', 'intra_group', 'cross_group']: calc_params['contacts'] = generate_contacts(**{expt_param: param_val, 'group_amount': basic_params.group_amount})
            else: calc_params['populations'] = generate_dist(**{expt_param.split('_')[-1]: param_val})
            srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
            calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
            single_res = simu_once.simulate(calc_params, r0 = r0, get_dur = False, empirical_group_keys = [], optm_targets = ['c'])
            growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
            mean_gen = mean_func(alpha_val, beta_val)
            single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen, param_val], index=['r0', 'growth_rate', 't_gen', expt_param])}})
            cache_generator.add_cache(expt_param, file_idx, param_name, single_res)
            print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for param_idx, param_val in enumerate(param_list):
        param_name = f'{expt_param}_{param_idx}'
        single_res = cache_generator.get_cache(expt_param, file_idx, param_name)
        for data_key in single_res.keys():
            if data_key not in res: res[data_key] = {}
            for key, item in single_res[data_key].items():
                res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expt_param, file_idx)
    print('Return Data')
    return res

























