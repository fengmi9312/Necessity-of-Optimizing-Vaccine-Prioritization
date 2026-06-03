# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:09:09 2025

@author: MIFENG
"""

if __name__ != "__main__":
    raise ImportError("This module cannot be imported.")
    
import os
import sys
code_root, folder_level = os.path.dirname(os.path.abspath(__file__)), 1
for _ in range(folder_level): code_root = os.path.dirname(code_root)
sys.path.append(code_root)


import FigureCode.figure_func as ff
import AnalysisCode.analysis_func as af
from Dependencies.FrameDependencies import load_experimental_data
import importlib
import matplotlib.pyplot as plt

expr_data = {}
anal_data = {}   
task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
             'necs_line_from_param': {'delay_8': 40, 'delay_10': 40, 'delay_0': 40, 'delay_13': 40, 'delay_26': 40, 'delay_39': 40}, 
             'necs_from_example': {'delay':  9},
             'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
             'necs_from_contact': {'0': 40, '1': 40, '2': 40, '3': 40, '4': 40, '5': 40, '6': 40, '7': 40, '8': 40, '9': 40, '10': 40, '11': 40, '12': 40, '13': 40},
             'necs_from_growth_gen': {'weibull_0': 9, 'weibull_1': 9, 'weibull_2': 9, 'gamma_0': 9, 'gamma_1': 9, 'gamma_2': 9, 'lognormal_0': 9, 'lognormal_1': 9, 'lognormal_2': 9},
             'necs_line_from_fatality': {'coef_alpha_0_0': 40, 'coef_alpha_0_13': 40, 'coef_alpha_0_26': 40, 'coef_alpha_0_39': 40, 'coef_alpha_1_0': 40, 'coef_alpha_1_13': 40, 'coef_alpha_1_26': 40, 'coef_alpha_1_39': 40, 
                                         'coef_beta_0_0': 40, 'coef_beta_0_13': 40, 'coef_beta_0_26': 40, 'coef_beta_0_39': 40,'coef_beta_1_0': 40,  'coef_beta_1_13': 40, 'coef_beta_1_26': 40, 'coef_beta_1_39': 40},
             'contact_before_protect': {'param': 1}, 'necs_space': {'param': 2}, 'optm_transition': {'param': 41},
             'necs_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
             'param_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, }
additional_task_dict = {'necs_from_contact': {'0': 40, '1': 40, '2': 40, '3': 40, '4': 40, '5': 40, '6': 40, '7': 40, '8': 40, '9': 40, '10': 40, '11': 40, '12': 40, '13': 40}}
additional_task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
                        'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
                        'necs_from_contact': {'1': 40, '2': 40, '13': 40}}
additional_task_dict = {}
for task_key, task_item in additional_task_dict.items():
    expr_data.update(load_experimental_data.load_certain_edata({task_key: task_item}))

importlib.reload(af)
anal_list = ['necs_from_r0_factor', 'necs_line_from_r0', 'corr_line_from_r0', 'fraction_from_time_with_example', 'alloc_from_age_with_example', 'dist_diff_from_r0', 
             'corr_from_r0_factor', 'necs_from_growth', 'prdt_from_xycoef', 'bnf_from_example', 'fitted_fraction_from_time', 'param_from_country', 'necs_from_country']
additional_anal_list = ['necs_line_from_r0', 'corr_line_from_r0']
for anal_name in additional_anal_list:
    anal_data.update({anal_name: getattr(af, f'get_{anal_name}').analyze(expr_data)})

# ff.figure6c.draw(anal_data)
# ff.figure6d.draw(anal_data)

# import numpy as np
# grid_data_x = []
# grid_data_y = []
# grid_data_tot = []
# for i in range(40):
#     res = anal_data['corr_from_r0_factor'][f'necs_from_fatality_(coef_alpha_1)_d_{i}_us']
#     optimal_corr, worst_corr = np.array(res['optimal_corr']), np.array(res['worst_corr'])
#     grid_data_x.append(optimal_corr)
#     grid_data_y.append(worst_corr)


# grid_data = grid_data_x
# fig, ax = plt.subplots()
# # # plt.plot(grid_data[8], linestyle = '', marker = '*')

# # # for i in range(40):
# # #     plt.plot(grid_data[i])


# im = ax.imshow(grid_data)
# ax.invert_yaxis()
# plt.colorbar(im)
# cs = ax.contour(grid_data, levels=[0], colors='w', linewidths=1.5) 

# import string
# lowercase = list(string.ascii_lowercase)
# save_enabled = True
# file_type = 'pdf'
# figure_path = []
# for idx in range(7):
#     figure_path.append(os.path.join(code_root, 'FigureTmp', f'figure{idx}'))

# importlib.reload(ff)
# for idx in lowercase[:6]:
#     getattr(ff, f'figure2{idx}').draw(anal_data)
#     if save_enabled: plt.savefig(os.path.join(figure_path[2], f'figure2{idx}.{file_type}'))



# for idx in lowercase[4:6]:
#     getattr(ff, f'figure4{idx}').draw(anal_data)
#     if save_enabled: plt.savefig(os.path.join(figure_path[4], f'figure4{idx}.{file_type}'))

# ff.figure1d.draw(anal_data)
# if save_enabled: plt.savefig(os.path.join(figure_path[1], f'figure1d.{file_type}'))


# ff.figure2a.draw(anal_data)

# plt.figure()
# r0_idx = 4
# res = []
# for idx in range(40):
#     res.append(anal_data['corr_from_r0_factor'][f'necs_from_fatality_(coef_beta_1)_d_{idx}_us']['optimal'][r0_idx])
# plt.plot(res)