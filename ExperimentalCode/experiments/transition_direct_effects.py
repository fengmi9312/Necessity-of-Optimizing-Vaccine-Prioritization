# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 23:50:29 2025

@author: fengm
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
    if expr_param != 'param' or file_idx != 0: return None
    res = {}
    for r0_idx in range(41):
        r0 = 1.7 + (np.arange(41) / 1000)[r0_idx]
        alpha_val, beta_val = 2.826, 5.665
        srv_func = func.srv_weibull
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
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
        res[str(r0_idx)] = simu._sir_delta__get_eff() * simu._sir_delta__eta
    return {'res': res}
        
        
        