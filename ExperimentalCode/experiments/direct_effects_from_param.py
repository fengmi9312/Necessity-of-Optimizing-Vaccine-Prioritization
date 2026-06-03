# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 23:24:42 2025

@author: fengm
"""


import os
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Dependencies.CodeDependencies import basic_params, func
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.FrameDependencies.data_loader import load_all_data
import numpy as np
import itertools
from copy import deepcopy
import pandas as pd

def execute(expr_param, file_idx):
    if file_idx != 0: return None
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    param_vals = {'delay': 700, 'k_val': None, 'vac_eff': 0.95, 'vac_avail': 0.3, 'c_perct': 0.1}
    param_list_dict = {'delay': np.arange(0, 2000, 50), 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 'c_perct': np.linspace(0.215, 0.8, 40)}
    countries = ['United States', 'Ireland', 'Japan']
    country_data = load_all_data(countries, basic_params.group_div)
    res = {}
    for country, r0_idx, param_idx in itertools.product(countries, range(40), range(40)):
        print(country, r0_idx, param_idx)
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        r0 = np.exp(r0_idx * 0.075)
        if expr_param in ['delay', 'c_perct', 'vac_avail', 'vac_eff']: param_vals[expr_param] = param_list_dict[expr_param][param_idx]
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        
        param_vals['k_val'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        calc_params_delta = deepcopy(calc_params)
        if expr_param in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']:
            if expr_param.split('_')[1] == 'alpha':
                steady_c_arr = func.get_steady_state(param_vals['k_val'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
                steady_d = steady_c_arr @ calc_params['ifrs']
            equal_ifr = np.ones(basic_params.group_amount) * calc_params['ifrs'].sum() / basic_params.group_amount
            diff_ifr = calc_params['ifrs'] - equal_ifr
            ifr_tmp = equal_ifr + param_idx * diff_ifr / 40
            if expr_param.split('_')[1] == 'alpha': calc_params_delta['ifrs'] = ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp)
            else: calc_params_delta['ifrs'] = ifr_tmp
            if expr_param.split('_')[-1] == '1': param_vals['delay'] = 0
        
        calc_params_delta['k'] = param_vals['k_val']
        calc_params_delta['eta'] = param_vals['vac_eff']
        calc_params_delta['delay'] = param_vals['delay']
        steady_c = func.get_steady_state(param_vals['k_val'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
        init_c = calc_params['i0'] @ calc_params['populations']
        
        simu_once = sir_delta(**calc_params_delta)
        if simu_once.getc_c_tot() < param_vals['c_perct'] * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                if simu_once.getc_c_tot() >= param_vals['c_perct'] * (steady_c - init_c) + init_c: break
        
        s_arr = simu_once.getc_s()
        alloc_coef = simu_once._sir_delta__get_eff() * simu_once._sir_delta__eta
        vac_alloc = func.get_alloc(np.array(s_arr), simu_once.get_populations(), param_vals['vac_avail'], basic_params.empirical_groups['all_ages'])
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

