# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:09:10 2024

@author: 20481756
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import load_experimental_data
from task_info import info
import re
from scipy.stats import norm
import numpy as np
import func
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from data_loader import load_all_data
import basic_params

edata = {}
task_list = {'necs_from_param': ['delay']}

for idx, task_param in enumerate(task_list['necs_from_param']):
    edata.update(load_experimental_data.load_certain_edata({'necs_from_param': [task_param]}))

'''
def generate_dist(peak = 30, equity = 0.5, group_amount = 16):
    tau_step = 80 / group_amount
    
    def get_normal_dist(sigma):
        dist = [norm.sf((i + 1) * tau_step, peak, sigma) - norm.sf(i * tau_step, peak, sigma) for i in range(group_amount)]
        return np.array(dist) / np.sum(dist)
    
    def equation(x):
        return equity - func.calc_equity(get_normal_dist(x[0]))
    
    param = fsolve(equation, [1,])[0]
    return get_normal_dist(param)

target = 'c'
pop_coef = generate_dist(30, 0.2)
min_c, max_c, all_ages, no_vac = [], [], [], []
for i in range(40):
    one_data = edata['necs_from_pattern_(diff_group)'][i]['dist']
    max_c.append(one_data[f'max_{target}_dd_{{diff_group_39}}'].to_numpy() @ pop_coef)
    min_c.append(one_data[f'min_{target}_dd_{{diff_group_39}}'].to_numpy() @ pop_coef)
    all_ages.append(one_data['all_ages_dd_{diff_group_39}'].to_numpy() @ pop_coef)
    no_vac.append(one_data['no_vac_dd_{diff_group_39}'].to_numpy() @ pop_coef)
plt.plot(min_c, color = 'tab:blue')
plt.plot(max_c, color = 'tab:red')
plt.plot(all_ages, color = 'k')
plt.plot(no_vac, color = 'tab:green')

fig, axes = plt.subplots(6, 7)
fig1, axes1 = plt.subplots(6, 7)
for i in range(40):
    one_data = edata['necs_from_pattern_(diff_group)'][i]['dist']
    plt.sca(axes[i // 7][i % 7])
    plt.bar(np.arange(16), one_data[f'max_{target}_dd_{{diff_group_39}}'].to_numpy() * pop_coef)
    plt.sca(axes1[i // 7][i % 7])
    plt.bar(np.arange(16), one_data[f'min_{target}_dd_{{diff_group_39}}'].to_numpy() * pop_coef, color = 'tab:orange')
'''

countries = ['United States', 'Ireland', 'Japan']
country_data = load_all_data(countries, basic_params.group_div)    
res = {}
optm_alloc = {}
worst_alloc = {}
target = 'c'
country = 'Japan'
pop_coef = country_data[country]['populations'] if target == 'c' else country_data[country]['populations'] * country_data[country]['ifrs']
for expr_name, task_params in task_list.items():
    for task_param in task_params:
        task_name = f'{expr_name}_({task_param})'
        res[task_name] = []
        optm_alloc[task_name] = []
        worst_alloc[task_name] = []
        for file_idx in range(info[expr_name][task_param]):
            res[task_name].append([])
            for param_idx in range(40):
                one_data = edata[task_name][file_idx]['dist']
                append_name = f'dd_{{{task_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
                res[task_name][-1].append(one_data[f'max_{target}_{append_name}'].to_numpy() @ pop_coef - one_data[f'min_{target}_{append_name}'].to_numpy() @ pop_coef)
                
            param_idx = 14
            one_data = edata[task_name][file_idx]['alloc']
            append_name = f'dd_{{{task_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            optm_alloc[task_name].append(one_data[f'min_{target}_{append_name}'].to_numpy() * pop_coef)
            worst_alloc[task_name].append(one_data[f'max_{target}_{append_name}'].to_numpy() * pop_coef)
                

fig, axes = plt.subplots(2, 10)
for i in range(15, 25):
    plt.sca(axes[0][i - 15])
    plt.bar(np.arange(16), optm_alloc[task_name][i], color = 'tab:red')
    plt.sca(axes[1][i-15])
    plt.bar(np.arange(16), worst_alloc[task_name][i], color = 'tab:blue')

                
from matplotlib import colormaps  

from mpl_toolkits.mplot3d.art3d import Line3DCollection             
cmap = colormaps.get_cmap('rainbow')
colors = cmap(np.linspace(0, 1, 40))

for expr_name, task_params in task_list.items():
    for task_param in task_params:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        task_name = f'{expr_name}_({task_param})' 
        x = np.arange(40) * 0.075
        y = np.arange(40) / 40
        X, Y = np.meshgrid(x, y)
        Z = np.array(res[task_name])
        surface = ax.plot_surface(X, Y, Z, cmap='rainbow')
# =============================================================================
#         for i in range(40):
#             line = np.column_stack((X[:, i], Y[:, i], Z[:, i]))
#             plt.gca().add_collection3d(Line3DCollection([line], color = colors[i]))
# =============================================================================
        plt.xlabel('coef')
        plt.xlim(0, 3)
        #plt.gca().set_zlim(0, 0.02)
        #plt.xscale("log")
        plt.ylabel(r'$\ln{R_0}$')
        #plt.zlabel('necessity')
        #plt.title({'0': 'home', '1': 'school', '2': 'work', '3': 'other locations'}[task_param])
    