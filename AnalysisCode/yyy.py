# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:27:44 2024

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import load_experimental_data
import re
from scipy.stats import norm
import numpy as np
import func
from scipy.optimize import fsolve
from data_loader import load_all_data

task_list = ['necs_from_param_(delay)', 'necs_from_param_(vac_eff)', 'necs_from_param_(vac_avail)', 'necs_from_param_(c_perct)', 'necs_from_param_(vac_dur)']

edata = load_experimental_data.load_certain_edata(task_list)

country_data = load_all_data(['United States'],[1,] * 16)['United States']
target = 'y'
res = {}
if target == 'c': pop_coef = country_data['populations']  
elif target == 'd': country_data['populations'] * country_data['ifrs']
elif target == 'y': country_data['populations'] * country_data['ifrs'] * country_data['ylls']
else: pass
for task_name in task_list:
    res[task_name] = []
    for file_idx in range(task_info[task_name]):
        one_data = edata[task_name][file_idx]['dist']
        res[task_name].append([])
        for param_idx in range(40):
            if task_name != 'necs_from_param_(vac_dur)': res[task_name][-1].append(one_data[f'max_{target}_gd_{{us_{param_idx}}}'].to_numpy() @ pop_coef - one_data[f'min_{target}_gd_{{us_{param_idx}}}'].to_numpy() @ pop_coef)
            else: res[task_name][-1].append(one_data[f'max_{target}_gd_dur_{{us_{param_idx}}}'].to_numpy() @ pop_coef - one_data[f'min_{target}_gd_dur_{{us_{param_idx}}}'].to_numpy() @ pop_coef)
            
    res[task_name] = np.array(res[task_name]).T
            
            
import matplotlib.pyplot as plt

for task_name in task_list:
    plt.figure()
    plt.imshow(res[task_name])
    plt.gca().invert_yaxis()
    plt.xlabel(r'$R_0$')
    plt.ylabel(re.search(r'\((.*?)\)', task_name).group(1))