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
from Dependencies.CodeDependencies.model import sir_delta


def make_age_dist(
    idx: int,
    n: int,
    n_group: int,
    sigma_rel: float = 0.5,
) -> np.ndarray:
    """
    Generate an age distribution.

    idx = 0      -> concentrated in young age groups
    idx = n - 1  -> concentrated in old age groups

    sigma_rel controls relative spread on [0, 1].
    """
    if not 0 <= idx < n:
        raise ValueError("idx must be in range(n)")
    if n <= 1:
        raise ValueError("n must be greater than 1")
    if n_group <= 1:
        raise ValueError("n_group must be greater than 1")
    if sigma_rel <= 0:
        raise ValueError("sigma_rel must be positive")

    age_pos = np.linspace(0, 1, n_group)
    center = idx / (n - 1)

    weights = np.exp(-0.5 * ((age_pos - center) / sigma_rel) ** 2)
    age_dist = weights / weights.sum()

    return age_dist

def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    c_perct = 0.1
    vac_avail = 0.3
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx // 40]
    pop_idx = file_idx % 40
    sttgs = ['min_c', 'max_c', 'min_d', 'max_d', 'no_vac']
    res = {}
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700
        calc_params['eta'] = 0.95
        calc_params.update({key: country_data[country][key] for key in ['ifrs', 'ylls']})
        calc_params['populations'] = make_age_dist(pop_idx, 40, 16, 0.5)
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        
        simu_once = sir_delta(**calc_params)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
        
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
        
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{pop_idx}'
        print(f'Begin excuting {param_name}')
        alloc_map, dist_map = {}, {}
        for sttg in sttgs:
            print('Strategy:', sttg)
            if sttg != 'no_vac':
                alloc_map[f'{sttg}_dd'] = simu_once.optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = True, tol=1e-20)['alloc']
                dist_map[f'{sttg}_dd'] = simu_once.calc_vac_prdt(alloc_map[f'{sttg}_dd'])
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






