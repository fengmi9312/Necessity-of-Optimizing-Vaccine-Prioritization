# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 18:36:19 2025

@author: MIFENG
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
import pandas as pd
from model import sir_delta
from data_loader import load_all_data
import func
import basic_params
from copy import deepcopy
import cache_generator

def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    vac_eff = 0.95
    c_perct = 0.1
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    country_data = load_all_data(['United States'], basic_params.group_div)
    calc_params_delta = deepcopy(basic_params.calc_params)
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    calc_params_delta['srv_inf'], calc_params_delta['srv_rem'] = srv_gen, srv_gen
    calc_params_delta['delay'] = 700
    calc_params_delta['eta'] = vac_eff
    calc_params_delta.update({key: country_data['United States'][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params_delta['contacts'] = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    res = {'pre_dist': {}, 'post_dist': {}}
    for r0_idx, r0 in enumerate(np.exp(np.arange(40) * 0.075)):
        print(r0_idx)
        calc_params_delta['k'] = r0 / (np.max(np.linalg.eig(calc_params_delta['populations'][None, :] * calc_params_delta['contacts'])[0]) * func.lambda_eff_srv(calc_params_delta['srv_inf'], calc_params_delta['srv_rem']))
        steady_c = func.get_steady_state(calc_params_delta['k'], calc_params_delta['populations'], calc_params_delta['contacts'], func.lambda_eff_srv(calc_params_delta['srv_inf'], calc_params_delta['srv_rem']), _i = calc_params_delta['i0']) @ calc_params_delta['populations']
        init_c = calc_params_delta['i0'] @ calc_params_delta['populations']
        simu = sir_delta(**calc_params_delta)
        while True:
            simu.spread_once()
            if simu.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
        res['pre_dist'][f'dist_{r0_idx}'] = simu.getc_c()
        for i in range(calc_params_delta['delay']): simu.spread_once()
        res['post_dist'][f'dist_{r0_idx}'] = simu.getc_c()
    return res