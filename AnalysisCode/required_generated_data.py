# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 00:39:57 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
import numpy as np
from data_loader import load_all_data
import basic_params
from copy import deepcopy
import func
import itertools

data_of_countries = load_all_data(['United States', 'United Kingdom', 'Ireland', 'France', 'Germany', 'Spain', 'Austria', 'Israel', 'Japan', 'South Korea'], basic_params.group_div)
country_ifrs = {}
alpha_val, beta_val = 2.826, 5.665
srv_func = func.srv_weibull
for country in ['United States', 'United Kingdom', 'Ireland', 'France', 'Germany', 'Spain', 'Austria', 'Israel', 'Japan', 'South Korea']:
    country_ifrs[country] = {'alpha': [], 'beta': []}
    country_data = data_of_countries[country]
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
    calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    for file_idx, param_idx, in itertools.product(range(40), range(40)):
        country_ifrs[country]['alpha'].append([])
        country_ifrs[country]['beta'].append([])
        r0 = np.exp((file_idx + param_idx / 40) * 0.075)
        k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
        steady_d = steady_c_arr @ country_data['ifrs']
        equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
        diff_ifr = country_data['ifrs'] - equal_ifr
        for equity_idx in range(40):
            ifr_tmp = equal_ifr + equity_idx * diff_ifr / 39
            country_ifrs[country]['alpha'][-1].append(ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp))
            country_ifrs[country]['beta'][-1].append(ifr_tmp)
    print(f'IFRs of {country} are completed')