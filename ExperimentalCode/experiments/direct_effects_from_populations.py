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
    srv_func = func.srv_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    res = {}
    r0_idx = file_idx
    for country, param_idx in itertools.product(countries, range(40)):
        print(country, r0_idx, param_idx)
        
        alpha_val, beta_val = 2.826, 5.665
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        r0 = np.exp(r0_idx * 0.075)
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700
        calc_params['eta'] = 0.95
        calc_params.update({key: country_data[country][key] for key in ['ifrs', 'ylls']})
        calc_params['populations'] = make_age_dist(param_idx, 40, 16, 0.75)
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        
        simu_once = sir_delta(**calc_params)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), 
                                         _i = calc_params['i0']) @ calc_params['populations']
        
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: 
                    break
                
        s_arr = simu_once.getc_s()
        alloc_coef = simu_once._sir_delta__get_eff() * simu_once._sir_delta__eta
        vac_alloc = func.get_alloc(np.array(s_arr), simu_once.get_populations(), 0.3, basic_params.empirical_groups['all_ages'])
        prdt = simu_once.calc_vac_prdt(vac_alloc)
        sheet_name_0 = f'{basic_params.country_abbr[country]}_{r0_idx}'
        sheet_name_1 = f's_{basic_params.country_abbr[country]}_{r0_idx}'
        sheet_name_2 = f'vac_{basic_params.country_abbr[country]}_{r0_idx}'
        sheet_name_3 = f'prdt_{basic_params.country_abbr[country]}_{r0_idx}'
        if param_idx == 0: 
            res[sheet_name_0] = {}
            res[sheet_name_1] = {}
            res[sheet_name_2] = {}
            res[sheet_name_3] = {}
        res[sheet_name_0][str(param_idx)] = alloc_coef
        res[sheet_name_1][str(param_idx)] = s_arr
        res[sheet_name_2][str(param_idx)] = vac_alloc
        res[sheet_name_3][str(param_idx)] = prdt
        
        
    return {sheet_name: pd.DataFrame(sheet_data) for sheet_name, sheet_data in res.items()} 
