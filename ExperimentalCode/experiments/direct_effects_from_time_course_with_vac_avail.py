# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 23:24:42 2025

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
import itertools

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
    c_perct_end = 0.9
    srv_func = func.srv_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    res = {}
    r0_idx = file_idx
    for country, param_idx in itertools.product(countries, range(1)):
        print(country, r0_idx, param_idx)
        
        alpha_val, beta_val = 2.826, 5.665
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        r0 = np.exp(r0_idx * 0.075)
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700
        calc_params['eta'] = 0.95
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        
        simu_once = sir_delta(**calc_params)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), 
                                         _i = calc_params['i0']) @ calc_params['populations']
        init_mark = True
        time_int = 0
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                time_int = time_int + 1
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c and init_mark: 
                    init_time_int = time_int
                    init_mark = False
                if simu_once.getc_c_tot() >= c_perct_end * (steady_c - init_c) + init_c: 
                    end_time_int = time_int
                    break
                
        vac_dur = 80
        vac_gap = get_vac_gap(vac_dur, 300)
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
        
        
        s_arr = simu_once.getc_s()
        alloc_coef = simu_once._sir_delta__get_eff() * simu_once._sir_delta__eta
        sheet_name_0 = f'{basic_params.country_abbr[country]}_{r0_idx}'
        sheet_name_1 = f's_{basic_params.country_abbr[country]}_{r0_idx}'
        if param_idx == 0: 
            res[sheet_name_0] = {}
            res[sheet_name_1] = {}
        res[sheet_name_0][str(param_idx)] = alloc_coef
        res[sheet_name_1][str(param_idx)] = s_arr
        
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 
