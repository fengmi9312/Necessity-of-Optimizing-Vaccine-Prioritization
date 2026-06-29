# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 18:47:19 2024

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
from Dependencies.FrameDependencies.data_loader import load_all_data
from Dependencies.CodeDependencies.model_time_course import sir_delta

def get_vac_gap(vac_dur: int, cur_len: int) -> int:
    """
    Return the smallest integer vac_gap >= 1 such that:
    (vac_dur - 1) * vac_gap >= 100
    """
    if vac_dur <= 1:
        raise ValueError("vac_dur must be greater than 1")

    denominator = vac_dur - 1
    vac_gap = (cur_len + denominator - 1) // denominator  # ceiling division

    return max(1, vac_gap)


def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    c_perct = 0.1
    c_perct_mid = 0.3
    c_perct_end = 0.5
    vac_avail = 0.3
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx // 40]
    sttgs = ['min_d', 'max_d', 'no_vac']
    res = {}
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700
        calc_params['eta'] = 0.95
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ylls']})
        
        equal_ifr = np.ones(basic_params.group_amount) * country_data[country]['ifrs'].sum() / basic_params.group_amount
        diff_ifr = country_data[country]['ifrs'] - equal_ifr
        param_idx = file_idx % 40
        param_val = param_idx / 39
        calc_params['ifrs'] = equal_ifr + param_val * diff_ifr
        
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        
        simu_once = sir_delta(**calc_params)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), 
                                         _i = calc_params['i0']) @ calc_params['populations']
        init_mark = True
        mid_mark = True
        time_int = 0
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                time_int = time_int + 1
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c and init_mark: 
                    init_time_int = time_int
                    init_mark = False
                if simu_once.getc_c_tot() >= c_perct_mid * (steady_c - init_c) + init_c and mid_mark: 
                    mid_time_int = time_int
                    mid_mark = False
                if simu_once.getc_c_tot() >= c_perct_end * (steady_c - init_c) + init_c: 
                    end_time_int = time_int
                    break
        
        vac_dur = 30
        vac_gap = get_vac_gap(vac_dur, 100)
        time_scale = (vac_dur - 1) * vac_gap / (end_time_int - init_time_int)
        beta_val = beta_val * time_scale
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['delay'] = int(700 * time_scale)
        simu_once = sir_delta(**calc_params)
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
        print(vac_dur, vac_gap, init_time_int, end_time_int, calc_params['delay'], time_scale)
        
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{vac_dur}'
        print(f'Begin excuting {param_name}')
        alloc_map, dist_map = {}, {}
        for sttg in sttgs:
            print('Strategy:', sttg)
            if sttg != 'no_vac':
                alloc_map[f'{sttg}_dd'] = simu_once.optimize_time_course_vac_alloc(vac_avail = vac_avail, vac_dur = vac_dur, vac_gap = vac_gap, optm_dir = (sttg[:3] == 'min'), 
                                                                                   target = sttg[-1], disp = True, tol=1e-20)['alloc']
                dist_map[f'{sttg}_dd'] = simu_once.calc_time_course_vac_prdt(alloc_map[f'{sttg}_dd'], vac_dur = vac_dur, vac_gap = vac_gap)
            else:
                dist_map[f'{sttg}_dd'] = simu_once.calc_prdt()
        
        single_res = {'alloc': alloc_map, 'dist': dist_map}
        for data_key in single_res.keys():
            if data_key not in res: res[data_key] = {}
            for item_key, item in single_res[data_key].items():
                res[data_key][f'{item_key}_{{{param_name}}}'] = pd.Series(item)
            print(f'Complete {param_name}')
    print('Return Data')
    return res









