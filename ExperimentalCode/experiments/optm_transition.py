# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 15:00:18 2025

@author: MIFENG
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta
from Dependencies.FrameDependencies.data_loader import load_all_data
import func
import basic_params
from copy import deepcopy

country = 'United States'
country_data = load_all_data([country], basic_params.group_div)

def execute(expr_param, file_idx):
    from scipy.stats import pearsonr
    if expr_param != 'param': return None
    r0 = 1.7 + (np.arange(41) / 1000)[file_idx]
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
    contact_arr = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params['eta'] = 0.95
    calc_params['delay'] = 4 * basic_params.day_div
    simu = sir_delta(**calc_params)
    steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    while True:
        simu.spread_once()
        if simu.getc_c_tot() >= 0.1 * (steady_c - init_c) + init_c: break
    res = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = True, target = 'd', double_optm=True)
    corr_0 = pearsonr(res[0]['alloc'] * country_data[country]['populations'], contact_arr)[0]
    corr_1 = pearsonr(res[1]['alloc'] * country_data[country]['populations'], contact_arr)[0]
    if corr_0 * corr_1 >= 0:
        while True:
            if corr_0 < 0: init_strategy = np.minimum(simu.getc_s(),  simu.get_contacts().sum(axis = 1) * np.random.rand() / simu.get_populations())
            else: init_strategy = np.minimum(simu.getc_s(), simu.get_ifrs() * np.random.rand() / simu.get_populations())
            res_tmp = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = True, target = 'd', double_optm=True, init_strategy = init_strategy)[0]
            corr_test = pearsonr(res_tmp['alloc'] * country_data[country]['populations'], contact_arr)[0]
            if corr_0 < 0 and corr_test > 0:
                res[0] = res_tmp
                break
            elif corr_1 > 0 and corr_test < 0:
                res[1] = res_tmp
                break
            else: pass
        
    alloc_diff = res[1]['alloc'] - res[0]['alloc']
    alloc_amount = 1001
    allocs = {}
    dists = {}
    for idx in range(alloc_amount):
        alloc = res[0]['alloc'] + alloc_diff * idx / (alloc_amount - 1)
        allocs[f'alloc_{idx}'] = alloc
        dists[f'dist_{idx}'] = simu.calc_vac_prdt(alloc)
    return {'allocs': allocs, 'dists': dists}
        
        
        
        
        
        
        
        
        
        
        
        