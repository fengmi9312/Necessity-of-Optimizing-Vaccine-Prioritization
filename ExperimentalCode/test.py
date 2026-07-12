# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:05:15 2023

@author: admin
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_root)

import numpy as np
from Dependencies.CodeDependencies.model import sir_delta
from Dependencies.FrameDependencies.data_loader import load_all_data
import Dependencies.CodeDependencies.func as func
import Dependencies.CodeDependencies.basic_params as basic_params
from copy import deepcopy


def calc_vac_prdt_grad(self, vac_alloc, mem = True, init_c = None, ctol = 1e-6, gtol = 1e-6, vac_compr = False):
    _vac_alloc = np.minimum(vac_alloc, self._sir_delta__s[self._sir_delta__current_time_int]) * self._sir_delta__eta * self._sir_delta__get_eff()
    lams = self.calc_lams(mem = mem)
    pos = self._sir_delta__time_int
    rt= self._sir_delta__r[pos]
    svu_tmp = self._sir_delta__sv[pos] + self._sir_delta__u[pos] - _vac_alloc
    totmat_tmp = self._sir_delta__contacts * self._sir_delta__populations[None, :] * self._sir_delta__k  
    lam, mem_eff = lams['lambda_eff'], lams['memory_eff']
    c_arr = self.calc_vac_prdt(vac_alloc)
    c_grad_tmp = np.ones([self._sir_delta__group_amount, self._sir_delta__group_amount])
    while True:
        c_grad = - np.eye(self._sir_delta__group_amount) \
        + np.eye(self._sir_delta__group_amount) * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff))[:,None] \
        + (totmat_tmp * (svu_tmp * lam * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff)))[:,None]) @ c_grad_tmp
        if np.all(abs(c_grad-c_grad_tmp) <= abs(c_grad_tmp) * (np.ones([self._sir_delta__group_amount, self._sir_delta__group_amount])*gtol)): break
        else: c_grad_tmp = c_grad
    return c_grad * (self._sir_delta__eta * self._sir_delta__get_eff())[None, :]

sir_delta.calc_vac_prdt_grad = calc_vac_prdt_grad

country = 'United States'
country_data = load_all_data([country], basic_params.group_div)

alpha_val, beta_val = 2.826, 5.665
srv_func = func.srv_weibull
calc_params = deepcopy(basic_params.calc_params)
calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
calc_params['eta'] = 0.95
calc_params['delay'] = 4 * basic_params.day_div

import matplotlib.pyplot as plt
fig0, axes0 = plt.subplots(5, 8)
fig1, axes1 = plt.subplots(5, 8)
fig2, axes2 = plt.subplots(5, 8)
fig3, axes3 = plt.subplots(5, 8)
for idx in range(40):
    r0 = np.exp(idx * 0.075)
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    simu = sir_delta(**calc_params)
    steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    while True:
        simu.spread_once()
        if simu.getc_c_tot() >= 0.1 * (steady_c - init_c) + init_c: break
    grad = simu.calc_vac_prdt_grad(np.zeros(16))
    ax = axes0[idx // 8][idx % 8]
    plt.sca(ax)
    plt.bar(np.arange(16), -calc_params['populations'] @ grad / calc_params['populations'])
    for i in range(10000):
        simu.spread_once()


fig3, axes3 = plt.subplots(4, 4)
res = np.array(simu.get_c()).T
for idx in range(16):
    ax = axes1[idx // 4][idx % 4]
    plt.sca(ax)
    plt.plot(simu.get_time_line(), res[idx])
    plt.xlim(0, 2000)
    
    # ax = axes1[idx // 8][idx % 8]
    # plt.sca(ax)
    # plt.imshow(-calc_params['populations'][:, None] * grad / calc_params['populations'][None, :])
    # ax.invert_yaxis()
    
    # ax = axes2[idx // 8][idx % 8]
    # plt.sca(ax)
    # plt.bar(np.arange(16), -(calc_params['populations'] * calc_params['ifrs']) @ grad / calc_params['populations'])
    
    # ax = axes3[idx // 8][idx % 8]
    # plt.sca(ax)
    # plt.imshow(-(calc_params['populations'] * calc_params['ifrs'])[:, None] * grad / calc_params['populations'][None, :])
    # ax.invert_yaxis()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    