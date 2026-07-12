# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 18:22:36 2026

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(code_root)
import numpy as np
from Dependencies.CodeDependencies import func
from Dependencies.CodeDependencies import basic_params
import pandas as pd
from copy import deepcopy
from Dependencies.CodeDependencies.param_data_loader import load_all_data
from Dependencies.CodeDependencies.model import sir_delta

def execute(expr_param, file_idx):
    if expr_param not in ['delay', 'vac_eff', 'vac_avail', 'c_perct', 'vac_dur']: return None
    c_perct = 0.1
    vac_avail = 0.3
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    sttgs = ['min_c', 'max_c', 'min_d', 'max_d', 'no_vac']
    res = {}
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700
        calc_params['eta'] = np.array([0.88, 0.95, 0.96, 0.97, 0.97, 0.96, 0.95, 0.95, 0.94, 0.93, 0.91, 0.88, 0.75, 0.70, 0.65, 0.60])
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        
        
        growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
        mean_gen = mean_func(alpha_val, beta_val)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
        
        for param_idx in range(40):
            calc_params['delay'] = 50 * param_idx
            simu_once = sir_delta(**calc_params)
            if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
                while True:
                    simu_once.spread_once()
                    if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            print(f'Begin excuting {param_name}')
            alloc_map, dist_map = {}, {}
            for sttg in sttgs:
                if sttg != 'no_vac':
                    alloc_map[f'{sttg}_dd'] = simu_once.optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = True, tol=1e-23)['alloc']
                    dist_map[f'{sttg}_dd'] = simu_once.calc_vac_prdt(alloc_map[f'{sttg}_dd'])
                else:
                    dist_map[f'{sttg}_dd'] = simu_once.calc_prdt()
            
            single_res = {'alloc': alloc_map, 'dist': dist_map}
            single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen], index=['r0', 'growth_rate', 't_gen'])}})
            for data_key in single_res.keys():
                if data_key not in res: res[data_key] = {}
                for item_key, item in single_res[data_key].items():
                    res[data_key][f'{item_key}_{{{param_name}}}'] = pd.Series(item)
            print(f'Complete {param_name}')
    print('Return Data')
    return res


res = execute('delay', 10)
