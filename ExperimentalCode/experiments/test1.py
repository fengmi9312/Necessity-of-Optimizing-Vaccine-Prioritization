# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:07:24 2024

@author: 20481756
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta
from data_loader import load_all_data
import func
import basic_params
from scipy.stats import spearmanr, pearsonr
from copy import deepcopy
from scipy.stats import pearsonr

country = 'United States'
country_data = load_all_data([country], basic_params.group_div)

alpha_val, beta_val = 2.826, 5.665
srv_func = func.srv_weibull
mean_func = func.get_mean_from_weibull
calc_params = deepcopy(basic_params.calc_params)
calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
calc_params['eta'] = 0.95
calc_params['delay'] = 0 * basic_params.day_div
contact_arr = calc_params['contacts'].sum(axis = 1)
o, w = [], []
for i in range(1):
    
    r0 = np.exp(20 * 3 * 0.075)
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    simu = sir_delta(**calc_params)
    steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    c_perct = 0
    optimal_res = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = True, target = 'c', disp = True, tol=1e-23)
    worst_res = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = False, target = 'c', disp = True, tol=1e-23)