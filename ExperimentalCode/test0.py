# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:07:24 2024

@author: 20481756
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta
from data_loader import load_all_data
import func
import basic_params
from copy import deepcopy


country = 'United States'
country_data = load_all_data([country], basic_params.group_div)

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

def calc_vac_prdt_grad_dis(self, vac_alloc, step = 0.001):
    prdt = self.calc_vac_prdt(vac_alloc)
    group_amount = self._sir_delta__group_amount
    return np.array([(self.calc_vac_prdt(vac_alloc + np.eye(group_amount)[i] * step) - prdt) / step for i in range(group_amount)]).T
    
    

sir_delta.calc_vac_prdt_grad = calc_vac_prdt_grad
sir_delta.calc_vac_prdt_grad_dis = calc_vac_prdt_grad_dis

def find_x(v1, v2, v3, allowed_indices):
    from scipy.optimize import minimize
    v3_tmp = v3 / np.linalg.norm(v3)
    
    def objective(x):
        return -np.dot(v3_tmp, x)
    
    constraints = [{'type': 'eq', 'fun': lambda x: np.dot(x, v1)}, 
                   {'type': 'eq', 'fun': lambda x: np.dot(x, v2)},
                   {'type': 'eq', 'fun': lambda x: np.linalg.norm(x) - 1}]
    bounds = [(0 if i not in allowed_indices else -np.inf, 0 if i not in allowed_indices else np.inf) for i in range(16)]
    
    x0 = np.ones(16)
    while True:
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints, 
                          options = {'maxiter': 10000})
        if result.success:
            print("sucess:", result.x)
            return result.x
        else:
            print("failure:", result.message)
            x0 = np.random.rand(16)

alloc_step = 0.002
alpha_val, beta_val = 2.826, 5.665
srv_func = func.srv_weibull
calc_params = deepcopy(basic_params.calc_params)
calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
calc_params['eta'] = 0.95
calc_params['delay'] = 4 * basic_params.day_div
target0, target1 = [], []
r0_list = []

from scipy.stats import pearsonr
contact_arr = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)

import matplotlib.pyplot as plt
import seaborn as sns
cmap = sns.color_palette("coolwarm", as_cmap=True)
corrs = []
prdts = []



r0_arr = np.arange(0, 11) / 200 + 1.7
for r0_idx, r0 in enumerate(r0_arr):
    r0_list.append(r0)
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    simu = sir_delta(**calc_params)
    steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    while True:
        simu.spread_once()
        if simu.getc_c_tot() >= 0.1 * (steady_c - init_c) + init_c: break
    res = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = True, target = 'd', double_optm=True)
    target0.append(res[0]['target'])
    target1.append(res[1]['target'])
    diff_alloc = res[1]['alloc'] - res[0]['alloc']
    print(r0, res[0]['target'], res[1]['target'])
    corrs.append([])
    prdts.append([])
    for i in range(101):
        alloc = res[0]['alloc'] + diff_alloc * i / 100
        corrs[-1].append(pearsonr(alloc, contact_arr)[0])
        prdts[-1].append(simu.calc_vac_prdt_target(alloc, target = 'd'))

plt.figure()
for r0_idx, r0 in enumerate(r0_list):
    plt.plot(corrs[r0_idx], prdts[r0_idx], color = cmap(r0_idx / 7))

plt.figure()
plt.plot(r0_list, target0, '*', color = 'tab:red')
plt.plot(r0_list, target1, 'o', color = 'tab:blue')

# alloc_idx = [i for i in range(16) if 0.1 < res[0]['alloc'][i] < 0.9 * simu.getc_s()[i]]
# u1 = (res[1]['alloc'] - res[0]['alloc']) / np.linalg.norm(res[1]['alloc'] - res[0]['alloc'])
# u2 = find_x(res[1]['alloc'] - res[0]['alloc'], calc_params['populations'], calc_params['populations'] @ simu.calc_vac_prdt_grad(res[0]['alloc']), alloc_idx)
# u2 /= np.linalg.norm(u2)

# alloc_coefs = []
# prdts = []
# idx = 0
# y_coef_idx = 0
# coef_idx_line_a = []
# while True:
#     y_coef = alloc_step * y_coef_idx
#     x_coef_idx = idx
#     x_coef = alloc_step * x_coef_idx
#     alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
#     if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
#     alloc_coefs.append([x_coef_idx, y_coef_idx])
#     prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
#     coef_idx_line_a.append([x_coef_idx, y_coef_idx])
#     print(x_coef, y_coef)
#     idx += 1

# for coef_idx_i, coef_idxes in enumerate(coef_idx_line_a):
#     if coef_idx_i == 0: coef_idx_line_b = []
#     elif coef_idx_i == len(coef_idx_line_a) - 1: coef_idx_line_c = []
#     else: pass
#     x_coef_idx = coef_idxes[0]
#     x_coef = alloc_step * x_coef_idx
#     for i in [True, False]:
#         idx = -1 if i else 0
#         while True:
#             y_coef_idx = idx
#             y_coef = alloc_step * y_coef_idx
#             alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
#             if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
#             alloc_coefs.append([x_coef_idx, y_coef_idx])
#             prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
#             if coef_idx_i == 0: coef_idx_line_b.append([x_coef_idx, y_coef_idx])
#             if coef_idx_i == len(coef_idx_line_a) - 1: coef_idx_line_c.append([x_coef_idx, y_coef_idx])
#             else: pass
#             print(x_coef, y_coef)
#             if i: idx -= 1
#             else: idx += 1

# for coef_idx_line_idx, coef_idx_line in enumerate([coef_idx_line_b, coef_idx_line_c]):
#     if len(coef_idx_line) <= 1: continue
#     for coef_idx_i, coef_idxes in enumerate(coef_idx_line):
#         y_coef_idx = coef_idxes[1]
#         idx = -1 if coef_idx_line_idx == 0 else 1
#         while True:
#             x_coef_idx = idx
#             x_coef = (coef_idxes[0] + x_coef_idx) * alloc_step
#             alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
#             if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
#             alloc_coefs.append([x_coef_idx, y_coef_idx])
#             prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
#             print(x_coef, y_coef)
#             if coef_idx_line_idx == 0: idx -= 1
#             else: idx += 1    
# return {'res':{'x_coef': np.array(alloc_coefs)[:, 0], 'y_coef': np.array(alloc_coefs)[:, 1], 'prdt': prdts}}







