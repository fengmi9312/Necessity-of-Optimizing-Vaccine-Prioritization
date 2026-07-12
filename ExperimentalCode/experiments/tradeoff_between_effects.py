# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:53:23 2025

@author: fengm
"""


if __name__ == '__main__':
    import os
    import sys
    root_level = 2
    code_root = os.path.dirname(os.path.abspath(__file__))
    for i in range(root_level): code_root = os.path.dirname(code_root)
    sys.path.append(code_root)

import numpy as np
import pandas as pd
from Dependencies.FrameDependencies.data_loader import load_all_data
from Dependencies.CodeDependencies.model_test import sir_delta
from Dependencies.CodeDependencies import basic_params, func
from copy import deepcopy

from scipy.stats import pearsonr

def get_direct_eff(self):
    vac_tmp = np.ones(len(self.get_populations())) / self.get_populations() * self._sir_delta__get_eff()
    pos = self._sir_delta__time_int
    svu_arr = self._sir_delta__sv[pos] + self._sir_delta__u[pos]
    c_arr = self._sir_delta__c[pos]
    c_prdt_add = self.calc_prdt() - c_arr
    return np.diag(c_prdt_add * vac_tmp / svu_arr)

sir_delta.get_direct_eff = get_direct_eff


def execute(expr_param, file_idx):
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    country = 'United States'
    countries = [country]
    c_perct = 0.1
    country_data = load_all_data(countries, basic_params.group_div)
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    calc_params['eta'] = 0.95
    calc_params['delay'] = 1800
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    target_coef = {'c': calc_params['populations'], 'd':calc_params['populations'] * calc_params['ifrs'], 'y': calc_params['populations'] * calc_params['ifrs'] * calc_params['ylls']}
    group_amount = len(calc_params['populations'])
    res_ind, res_dir = [], []
    for r0_idx, r0 in enumerate(np.exp(np.arange(40) * 0.075)):
        print(r0_idx)
        calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
        init_c = calc_params['i0'] @ calc_params['populations']
        simu = sir_delta(**calc_params)
        while True:
            if simu.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
            simu.spread_once()
        for target in ['c']:
            dir_res_tmp = (target_coef[target][:, None] * simu.get_direct_eff()).sum(axis = 0)
            res_tmp = (-target_coef[target][:, None] * simu.calc_steady_grad(np.zeros(group_amount)) / calc_params['populations'][None, :]).sum(axis = 0)
            ind_res_tmp = res_tmp - dir_res_tmp
            res_ind.append(pearsonr(ind_res_tmp, calc_params['contacts'].sum(axis = 0))[0])
            res_dir.append(pearsonr(dir_res_tmp, calc_params['contacts'].sum(axis = 0))[0])
    return np.exp(np.arange(40) * 0.075), res_ind, res_dir

if __name__ == '__main__':
    res = execute('param', 0)
    
    import matplotlib.pyplot as plt
    plt.plot(res[0], np.array(res[1]), color = 'tab:red')
    plt.plot(res[0], res[2], color = 'tab:blue')
    plt.xscale('log')