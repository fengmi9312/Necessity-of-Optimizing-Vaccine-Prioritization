# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:57:57 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import load_experimental_data
from task_info import info
import numpy as np
from data_loader import load_all_data
import basic_params
from copy import deepcopy
import func

edata = {}
task_list = {'necs_from_example': ['delay'],
             'necs_from_param': ['delay', 'vac_eff', 'vac_avail', 'c_perct', 'vac_dur'],
             'necs_from_growth_gen': ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2'],
             'necs_from_fatality': ['coef'],
             'necs_from_contact': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
             'necs_from_country': ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']}

edata = load_experimental_data.load_certain_edata(task_list)


from scipy.stats import ks_2samp

target = 'c'
country = 'United States'
acc_type = 'dd'

country_data = load_all_data([country], basic_params.group_div)[country]    
res = {}
optm_alloc = {}
worst_alloc = {}
pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']

contact_arr = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
expr_name, expr_param = 'necs_from_param', 'delay'
task_name = f'{expr_name}_({expr_param})'
res = []
alloc_diff = []
for file_idx in range(info[expr_name][expr_param]):
    res.append([])
    for param_idx in range(40):
        if file_idx == 0: alloc_diff.append([])
        dist_data = edata[task_name][file_idx]['dist']
        append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
        res[-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
        alloc_data = edata[task_name][file_idx]['alloc']
        x, y = alloc_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() * country_data['populations'], alloc_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() * country_data['populations']
        alloc_diff[param_idx].append(abs(np.dot(x, contact_arr) / (np.linalg.norm(x) * np.linalg.norm(contact_arr)) - np.dot(contact_arr, y) / (np.linalg.norm(contact_arr) * np.linalg.norm(y))))
res = np.array(res)







# min_arg = []
# for i in range(40):
#     min_arg.append(np.argmin(alloc_diff[i]))

# m_val = []
# for i in range(40):
#     m_val.append([])
#     for j in range(1, 39):
#         if (res[j][i] - res[j - 1][i]) * (res[j][i] - res[j + 1][i]) > 0:
#             m_val[-1].append(j)



expr_name, expr_param = 'necs_from_example', 'delay'
task_name = f'{expr_name}_({expr_param})'
example_res = []
country = 'United States'
for r0_idx in range(3):
    example_res.append([])
    for delay_idx in range(3):
        example_res[-1].append({})
        example_res[-1][-1][f'time_line_max_{target}'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_max_{target}_{acc_type}'][f'time_line_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        example_res[-1][-1][f'curve_max_{target}'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_max_{target}_{acc_type}'][f'curve_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        example_res[-1][-1][f'time_line_min_{target}'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_min_{target}_{acc_type}'][f'time_line_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        example_res[-1][-1][f'curve_min_{target}'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_min_{target}_{acc_type}'][f'curve_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        example_res[-1][-1]['time_line_no_vac'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_no_vac_{acc_type}'][f'time_line_{{{expr_param}_{basic_params.country_abbr[country]}}}']
        example_res[-1][-1]['curve_no_vac'] = edata[task_name][r0_idx * 3 + delay_idx][f'curve_no_vac_{acc_type}'][f'curve_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']


import matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 3)
for r0_idx in range(3):
    for delay_idx in range(3):
        plt.sca(axes[r0_idx][delay_idx])
        plt.plot(example_res[r0_idx][delay_idx]['time_line_no_vac'], example_res[r0_idx][delay_idx]['curve_no_vac'], color = 'black')
        plt.plot(example_res[r0_idx][delay_idx][f'time_line_min_{target}'], example_res[r0_idx][delay_idx][f'curve_min_{target}'], color = 'tab:red')
        plt.plot(example_res[r0_idx][delay_idx][f'time_line_max_{target}'], example_res[r0_idx][delay_idx][f'curve_max_{target}'], color = 'tab:blue')
        plt.ylim(0, 1)




expr_name = 'necs_from_growth_gen'
res_growth = []
for r0_idx in range(4):
    res_growth.append({})
    for expr_param in task_list[expr_name]:
        task_name = f'{expr_name}_({expr_param})'
        res_growth[-1][f'{expr_param}_growth'] = []
        res_growth[-1][f'{expr_param}_necs'] = []
        for file_idx in range(info[expr_name][expr_param]):
            for param_idx in range(9):
                dist_data = edata[task_name][file_idx]['dist']
                param_data = edata[task_name][file_idx]['transmission_params']
                append_name = f'{{{basic_params.country_abbr[country]}_{r0_idx}_{param_idx}}}'
                res_growth[-1][f'{expr_param}_growth'].append(param_data.loc['growth_rate', f'params_{append_name}'] * param_data.loc['t_resp', f'params_{append_name}'])
                res_growth[-1][f'{expr_param}_necs'].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
                


calc_params = deepcopy(basic_params.calc_params)
calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
alpha_val, beta_val = 2.826, 5.665
srv_gen = func.srv_weibull(alpha_val, beta_val, basic_params.srv_length, basic_params.step)

expr_name, expr_param = 'necs_from_fatality', 'coef'
task_name = f'{expr_name}_({expr_param})'
fatality_res = []
for file_idx in range(info[expr_name][expr_param]):
    fatality_res.append([])
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(srv_gen, srv_gen))
    steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(srv_gen, srv_gen), _i = calc_params['i0']) * calc_params['populations']
    steady_d = steady_c_arr @ country_data['ifrs']
    equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
    diff_ifr = country_data['ifrs'] - equal_ifr
    for param_idx, param_val in enumerate(np.arange(40) / 40):
        ifr_tmp = equal_ifr + param_val * diff_ifr 
        pop_coef = country_data['populations'] * ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp) 
        dist_data = edata[task_name][file_idx]['dist']
        append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
        fatality_res[-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
fatality_res = np.array(fatality_res)



target = 'd'
expr_name = 'necs_from_contact'
pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
for expr_param_idx in range(14):
    expr_param = str(expr_param_idx)
    task_name = f'{expr_name}_({expr_param})'
    contact_res = []
    for file_idx in range(info[expr_name][expr_param]):
        contact_res.append([])
        for param_idx, param_val in enumerate(np.arange(40) / 40):
            dist_data = edata[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            contact_res[-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
    contact_res = np.array(contact_res)
    
    
    

target = 'd'
expr_name = 'necs_from_param'
pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
param_res = {}
for expr_param in  ['vac_eff', 'vac_avail', 'c_perct', 'vac_dur']:
    task_name = f'{expr_name}_({expr_param})'
    param_res[expr_name] = []
    for file_idx in range(info[expr_name][expr_param]):
        param_res[expr_name].append([])
        for param_idx, param_val in enumerate(np.arange(40) / 40):
            dist_data = edata[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            param_res[expr_name][-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
    param_res[expr_name] = np.array(param_res[expr_name])
    plt.figure()
    plt.imshow(param_res[expr_name].T)
    plt.gca().invert_yaxis()


    


target = 'c'
pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
expr_name = 'necs_from_country'
country_res = {}
for expr_param in x_countries:
    task_name = f'{expr_name}_({expr_param})'
    country_res[expr_param] = []
    for file_idx in range(info[expr_name][expr_param]):
        for param_idx in range(25):
            dist_data = edata[task_name][file_idx]['dist']
            append_name = f'{{{param_idx}}}'
            country_res[expr_param].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)

import seaborn as sns
import pandas as pd

df = pd.DataFrame([(key, val) for key, values in country_res.items() for val in values], columns=["Country", "Value"])

# Create a violin plot
sns.violinplot(x="Country", y="Value", data=df)




                
import matplotlib.pyplot as plt
fig, axes = plt.subplots(4, 5)
colors = ['tab:red', 'tab:blue']
for i in range(2):
    for j, idx in enumerate([2, 10, 16, 26, 32]):
        plt.sca(axes[i * 2][j])
        plt.bar(np.arange(16), alloc[i]['optm'][idx], color = colors[0])
        plt.sca(axes[i * 2 + 1][j])
        plt.bar(np.arange(16), alloc[i]['worst'][idx], color = colors[1])


fig = plt.figure()
ax = fig.add_subplot(111)
plt.sca(ax)
r0_idx = 0
for idx, expr_param in enumerate(task_list[expr_name]):
    task_name = f'{expr_name}_({expr_param})'
    plt.plot(res_growth[r0_idx][f'{expr_param}_growth'], res_growth[r0_idx][f'{expr_param}_necs'], '.')
