# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:52:24 2025

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import load_experimental_data


edata = {}
task_list = {'necs_from_param': ['delay', 'vac_eff', 'vac_avail', 'c_perct', 'vac_dur'],
            'necs_from_contact': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
            'necs_from_population': ['peak', 'equity'],
            'necs_from_fatality': ['coef_alpha_0', 'coef_alpha_1','coef_beta_0', 'coef_beta_1'],
            'necs_line_from_fatality': ['coef_alpha_0_0', 'coef_alpha_0_13', 'coef_alpha_0_26', 'coef_alpha_0_39', 'coef_alpha_1_0', 'coef_alpha_1_13', 'coef_alpha_1_26', 'coef_alpha_1_39', 
                                        'coef_beta_0_0', 'coef_beta_0_13', 'coef_beta_0_26', 'coef_beta_0_39', 'coef_beta_1_0', 'coef_beta_1_13', 'coef_beta_1_26', 'coef_beta_1_39'],
            'necs_line_from_param': ['delay_10', 'delay_0', 'delay_13', 'delay_26', 'delay_39'],
            'necs_from_growth_gen': ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2'],
            'necs_from_country': ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea'], 
            'param_from_country': ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea'], 
            'necs_from_example': ['delay'],
            'necs_space': ['param'], 'optm_transition': ['param'], 'contact_before_protect': ['param']}
for task_key, task_item in task_list.items():
    edata.update(load_experimental_data.load_certain_edata({task_key: task_item}))






import analysis_code as ac
anal_types = ['necs_from_r0_factor', 'necs_line_from_r0', 'corr_from_r0_factor', 'corr_line_from_r0', 'alloc_from_r0_factor', 'necs_from_growth', 'fraction_from_time_with_example', 'alloc_from_age_with_example', 'prdt_from_corr', 'prdt_from_xycoef', 'necs_from_country', 'bnf_from_example', 'dist_diff_from_r0']
anal_data = {}
for anal_type in anal_types:
    anal_data[anal_type] = getattr(ac, f'get_{anal_type}')(edata)
    print(f'{anal_type} completed')

import figure_code as fc
import matplotlib.pyplot as plt
import numpy as np
xxx
save_enabled = True
file_type = 'pdf'
subfig2_path = os.path.join(code_root, 'FigureTmp', 'figure2')

fig, ax = plt.subplots(1, 1, figsize=(4.8, 4))
fc.heatmap_necs_from_r0_param(ax, anal_data['necs_from_r0_param'], expr_param = 'delay')
if save_enabled: plt.savefig(os.path.join(subfig2_path, f'heatmap_necs_from_r0_delay.{file_type}'))

fc.plot_necs_from_growth(anal_data)      
if save_enabled: plt.savefig(os.path.join(subfig2_path, f'plot_necs_from_growth.{file_type}'))


fc.curve_necs_line_from_r0(anal_data, expr_name = 'necs_line_from_r0_with_param')
if save_enabled: plt.savefig(os.path.join(subfig2_path, f'curve_necs_line_from_r0_with_param.{file_type}'))

for delay_idx in range(2):
    fc.curve_example(anal_data, delay_idx = delay_idx)
    if save_enabled: plt.savefig(os.path.join(subfig2_path, f'curve_example_{delay_idx}.{file_type}'))
    

fc.curve_necs_line_from_r0(anal_data, expr_name = 'necs_line_from_r0_with_param', target = 'c', data_type = 'corr')
if save_enabled: plt.savefig(os.path.join(subfig2_path, f'plot_corr_line_from_r0_with_param_c.{file_type}'))


subfig3_path = os.path.join(code_root, 'FigureTmp', 'figure3')
fc.curve_necs_line_from_r0(anal_data, expr_name = 'necs_line_from_r0_with_param', target = 'd')
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_line_from_r0_with_param_d.{file_type}'))

fc.curve_necs_line_from_r0(anal_data, expr_name = 'necs_line_from_r0_with_fatality', target = 'd')
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_line_from_r0_with_fatality_d.{file_type}'))
    
fc.prdt_in_alloc_space(anal_data)
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'prdt_in_alloc_space.{file_type}'))
    

fc.minimimum_transition(anal_data)
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'minimimum_transition.{file_type}'))


subfig4_path = os.path.join(code_root, 'FigureTmp', 'figure4')
for target in ['c', 'd']:
    fc.necs_from_contact(anal_data, target = target)
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'necs_from_contact_{target}.{file_type}'))


fc.fitting_countries(anal_data)
if save_enabled: plt.savefig(os.path.join(subfig4_path, f'fitting_countries.{file_type}'))


fc.table_necs(anal_data)
if save_enabled: plt.savefig(os.path.join(subfig4_path, f'table_necs.{file_type}'))

for target in ['c', 'd']:
    fc.neces_from_country(anal_data, target = target)
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'neces_from_country_{target}.{file_type}'))



subfig5_path = os.path.join(code_root, 'FigureTmp', 'figure5')

for idx in range(2):
    fc.sacr_from_example(anal_data, idx = idx)
    if save_enabled: plt.savefig(os.path.join(subfig5_path, f'sacr_from_example_{idx}.{file_type}'))

fc.sacr_comparison_from_r0(anal_data, 'param', 'delay')
if save_enabled: plt.savefig(os.path.join(subfig5_path, f'sacr_comparison_from_r0_param_delay.{file_type}'))

fc.sacr_comparison_from_r0(anal_data, 'fatality', 'coef_beta_1')
if save_enabled: plt.savefig(os.path.join(subfig5_path, f'sacr_comparison_from_r0_fatality_coef_beta_1.{file_type}'))

fc.sacrs_from_country(anal_data)
if save_enabled: plt.savefig(os.path.join(subfig5_path, f'sacrs_from_country.{file_type}'))

fc.corr_from_r0_factors(anal_data, 'necs_from_param', 'vac_eff')
























fig, axes = plt.subplots(5, 8)
for i, ax_arr in enumerate(axes):
    for j, ax in enumerate(ax_arr):
        plt.sca(axes[i][j])
        fc.plot_corr_from_r0(ax, anal_data['corr_from_r0'], expr_name = 'necs_from_param', expr_param='delay', param_idx = i * 8 + j, target = 'd')



















    
# for param_idx in [0, 10]:
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.curve_necs_from_r0(ax, anal_data['necs_from_r0_param'], expr_name = 'necs_from_param', expr_param = 'delay', param_idx = param_idx)
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig2_path, f'curve_necs_from_r0_{param_idx}.{file_type}'))
    

for delay_idx in range(2):
    for r0_idx in range(3):
        fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.35)
        fc.curve_fraction_from_time_with_example(ax, anal_data['fraction_from_time_with_example'], r0_idx = r0_idx, delay_idx = delay_idx)
        plt.subplots_adjust(top = 0.88, bottom = 0.22, left = 0.22, right = 0.9,  hspace = 1, wspace = 1) 
        if save_enabled: plt.savefig(os.path.join(subfig2_path, f'curve_fraction_from_time_with_example_{delay_idx}_{r0_idx}.{file_type}'))
    
for delay_idx in range(2):
    for r0_idx in range(3):
        fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.25)
        fc.bar_alloc_from_age_with_example(ax, anal_data['alloc_from_age_with_example'], r0_idx = r0_idx, delay_idx = delay_idx, optm_dir = 'min')
        plt.subplots_adjust(top = 0.88, bottom = 0.23, left = 0.20, right = 0.9,  hspace = 1, wspace = 1) 
        if save_enabled: plt.savefig(os.path.join(subfig2_path, f'bar_optimal_alloc_from_age_with_example_{delay_idx}_{r0_idx}.{file_type}'))
        fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.25)
        fc.bar_alloc_from_age_with_example(ax, anal_data['alloc_from_age_with_example'], r0_idx = r0_idx, delay_idx = delay_idx, optm_dir = 'max')
        plt.subplots_adjust(top = 0.88, bottom = 0.23, left = 0.20, right = 0.9,  hspace = 1, wspace = 1) 
        if save_enabled: plt.savefig(os.path.join(subfig2_path, f'bar_worst_alloc_from_age_with_example_{delay_idx}_{r0_idx}.{file_type}'))

for idx in [0, 13, 26, 39]:  
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.plot_corr_line_from_r0(ax, anal_data['corr_line_from_r0'], expr_name = 'necs_line_from_param', expr_param=f'delay_{idx}')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.21, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig2_path, f'plot_corr_line_from_r0_delay_{idx}.{file_type}'))
    
# for delay_idx in [0, 10]:  
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.plot_corr_from_r0(ax, anal_data['corr_from_r0'], expr_name = 'necs_from_param', expr_param='delay', param_idx = delay_idx)
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig2_path, f'plot_corr_from_r0_{delay_idx}.{file_type}'))

    

# for delay_idx in [0, 13, 26, 39]:  
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.plot_corr_from_r0(ax, anal_data['corr_from_r0'], expr_name = 'necs_from_param', expr_param='delay', param_idx = delay_idx)
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 


# for delay_idx in [0, 13, 26, 39]:  
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.plot_corr_from_r0(ax, anal_data['corr_from_r0'], expr_name = 'necs_from_param', expr_param='delay', param_idx = delay_idx, target = 'd')
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 

fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
fc.plot_dist_diff_from_r0(ax,anal_data['dist_diff_from_r0'] )
plt.subplots_adjust(top = 0.95, bottom = 0.05, left = 0.28, right = 0.99,  hspace = 1, wspace = 1) 
if save_enabled: plt.savefig(os.path.join(subfig2_path, f'plot_dist_diff_from_r0.{file_type}'))




subfig3_path = os.path.join(code_root, 'FigureTmp', 'figure3')

fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.8)
fc.heatmap_necs_from_r0_param(ax, anal_data['necs_from_r0_param'], expr_param = 'delay', target = 'd')
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'heatmap_necs_from_r0_delay.{file_type}'))


for idx in [0, 13, 26, 39]:
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.curve_necs_line_from_r0(ax, anal_data['necs_line_from_r0_with_param'], expr_name = 'necs_line_from_r0_with_param', expr_param = f'delay_{idx}', target = 'd')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_line_from_r0_delay_{idx}.{file_type}'))


for idx in [0, 13, 26, 39]:  
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.plot_corr_line_from_r0(ax, anal_data['corr_line_from_r0'], expr_name = 'necs_line_from_param', expr_param=f'delay_{idx}', target = 'd')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.21, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'plot_corr_line_from_r0_delay_{idx}.{file_type}'))

# for param_idx in [0, 13, 26, 39]:
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.curve_necs_from_r0(ax, anal_data['necs_from_r0_param'], expr_name = 'necs_from_param', expr_param = 'delay', param_idx = param_idx, target = 'd', mark = False)
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_from_r0_{param_idx}_d.{file_type}'))


# for param_idx in [0, 13, 26, 39]:
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.curve_necs_from_r0(ax, anal_data['necs_from_r0_fatality'], expr_name = 'necs_from_r0_fatality', expr_param = 'coef_beta_1', param_idx = param_idx, target = 'd', mark = False)
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_from_r0_fatality_{param_idx}_d.{file_type}'))
    
# for param_idx in [0, 13, 26, 39]:  
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
#     fc.plot_corr_from_r0(ax, anal_data['corr_from_r0'], expr_name = 'necs_from_fatality', expr_param='coef_beta_1', param_idx = param_idx, target = 'd')
#     plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig3_path, f'corr_from_r0_{param_idx}_d.{file_type}'))

fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.8)
fc.heatmap_necs_from_r0_param(ax, anal_data['necs_from_r0_fatality'], expr_param = 'coef_beta_1', target = 'd')
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'heatmap_necs_from_r0_fatality.{file_type}'))



for idx in [0, 13, 26, 39]:
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.curve_necs_line_from_r0(ax, anal_data['necs_line_from_r0_with_fatality'], expr_name = 'necs_line_from_r0_with_fatality', expr_param = f'coef_beta_1_{idx}', target = 'd')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_line_from_r0_fatality_{idx}.{file_type}'))


for idx in [0, 13, 26, 39]:  
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.plot_corr_line_from_r0(ax, anal_data['corr_line_from_r0'], expr_name = 'necs_line_from_r0_with_fatality', expr_param=f'coef_beta_1_{idx}', target = 'd')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.21, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'plot_corr_line_from_r0_fatality_{idx}.{file_type}'))

# for param_idx in [0, 39]:
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 8]) * 0.6)
#     fc.curve_necs_line_from_r0(ax, anal_data['necs_line_from_r0'], expr_param=f'coef_beta_1_{param_idx}')
#     plt.subplots_adjust(top = 0.88, bottom = 0.15, left = 0.15, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig3_path, f'curve_necs_line_from_r0_{param_idx}.{file_type}'))

# for param_idx in [0, 10, 34, 39]:
#     fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.6)
#     fc.plot_corr_line_from_r0(ax, anal_data['corr_line_from_r0'], expr_param=f'coef_beta_1_{param_idx}')
#     plt.subplots_adjust(top = 0.88, bottom = 0.15, left = 0.2, right = 0.9,  hspace = 1, wspace = 1) 
#     if save_enabled: plt.savefig(os.path.join(subfig3_path, f'corr_line_from_r0_{param_idx}.{file_type}'))
    
for sheet_idx in range(2):
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.6)
    fc.heatmap_prdt_from_xycoef(ax, anal_data['prdt_from_xycoef'], sheet_idx = sheet_idx)
    plt.subplots_adjust(top = 0.88, bottom = 0.11, left = 0.125, right = 0.88,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'prdt_from_xycoef_{sheet_idx}.{file_type}'))
    
fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.6)
fc.curve_prdt_from_corr(ax, anal_data['prdt_from_corr'])
plt.subplots_adjust(top = 0.88, bottom = 0.18, left = 0.17, right = 0.9,  hspace = 1, wspace = 1) 
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'prdt_from_corr.{file_type}'))

fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.6)
fc.curve_prdt_diff_from_r0(ax, anal_data['prdt_from_corr'])
plt.subplots_adjust(top = 0.88, bottom = 0.135, left = 0.135, right = 0.9,  hspace = 1, wspace = 1)
if save_enabled: plt.savefig(os.path.join(subfig3_path, f'prdt_diff_from_r0.{file_type}'))









subfig4_path = os.path.join(code_root, 'FigureTmp', 'figure4')

for idx in range(2):
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.6)
    fc.bar_sacr_from_example(ax, anal_data['sacr_from_example'], idx)
    plt.subplots_adjust(top = 0.88, bottom = 0.11, left = 0.145, right = 0.825,  hspace = 1, wspace = 1)
    if save_enabled: plt.savefig(os.path.join(subfig3_path, f'sacr_from_example_{idx}.{file_type}'))
    
for idx in range(2):
    for target in ['c', 'd']:
        fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.35)
        fc.bar_alloc_from_sacr_example(ax, anal_data['sacr_from_example'], idx, target)
        plt.subplots_adjust(top = 0.88, bottom = 0.16, left = 0.14, right = 0.9,  hspace = 1, wspace = 1) 
        if save_enabled: plt.savefig(os.path.join(subfig3_path, f'alloc_from_sacr_example_{idx}_{target}.{file_type}'))

for idx, target in enumerate(['c', 'd']):
    fig, ax = plt.subplots(1, 1, figsize=np.array([6, 5]) * 0.6)
    fc.heatmap_sacr_from_r0_param(ax, anal_data['sacr_from_r0_param'], 'delay', target = target)
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'heatmap_sacr_from_r0_param_{target}.{file_type}'))
    
for idx, target in enumerate(['c', 'd']):
    fig, ax = plt.subplots(1, 1, figsize=np.array([6, 5]) * 0.6)
    fc.heatmap_sacr_from_r0_fatality(ax, anal_data['sacr_from_r0_fatality'], 'coef_beta_1', target = target)
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'heatmap_sacr_from_r0_fatality_{target}.{file_type}'))



for idx in [0, 13, 26, 39]:  
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.plot_alloc_corr_line_from_r0(ax, anal_data['alloc_corr_line_from_r0'], expr_name = 'necs_line_from_param', expr_param=f'delay_{idx}')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'plot_alloc_corr_line_from_r0_with_delay_{idx}.{file_type}'))
    

for idx in [0, 13, 26, 39]:  
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.45)
    fc.plot_alloc_corr_line_from_r0(ax, anal_data['alloc_corr_line_from_r0'], expr_name = 'necs_line_from_fatality', expr_param=f'coef_beta_1_{idx}')
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig4_path, f'plot_alloc_corr_line_from_r0_with_fatality_{idx}.{file_type}'))



subfig5_path = os.path.join(code_root, 'FigureTmp', 'figure5')
for idx in ['1', '2', '3', '13']:
    fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.5)
    fc.change_necs_from_contact(ax, anal_data['necs_from_r0_contact'], str(idx))
    plt.subplots_adjust(top = 0.88, bottom = 0.19, left = 0.19, right = 0.9,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig5_path, f'change_necs_from_contact_{idx}.{file_type}'))

for target in ['c', 'd']:
    fig, ax = plt.subplots(1, 1, figsize = np.array([15, 5]))
    fc.boxplot_neces_from_country(ax, anal_data['necs_from_country'], target = target)
    plt.subplots_adjust(top = 1, bottom = 0.1, left = 0.06, right = 0.99,  hspace = 1, wspace = 1) 
    if save_enabled: plt.savefig(os.path.join(subfig5_path, f'boxplot_neces_from_country_{target}.{file_type}'))




fig, ax = plt.subplots(1, 1, figsize = np.array([5, 6]))
fc.table_param_from_country(ax, anal_data['param_from_country'])
if save_enabled: plt.savefig(os.path.join(subfig5_path, f'table_param_from_country.{file_type}'))

fig, ax = plt.subplots(1, 1, figsize = np.array([6, 5]) * 0.75)
fc.curve_fitted_fraction_from_time(ax, anal_data['fitted_fraction_from_time'])












fig, ax = plt.subplots(1, 1)
fc.heatmap_necs_from_r0_param(ax, anal_data['necs_from_r0_param'], expr_param = 'c_perct', target = 'c')
if save_enabled: plt.savefig(os.path.join(subfig5_path, f'heatmap_necs_from_xycoef_{sheet_idx}.{file_type}'))


# import matplotlib.pyplot as plt
# import numpy as np

# import matplotlib.animation as animation

# fig, ax = plt.subplots()

# expr_param = 'coef_beta_1_34'
# task_name = 'necs_line_from_fatality_(coef_beta_1_34)'
# artists = []
# colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple']
# for file_idx in range(40):
#     for param_idx in range(40):
#         append_name = f"dd_{{{expr_param}_us_{param_idx}}}"
#         container = ax.bar(np.arange(16), edata[task_name][file_idx]['alloc'][f'max_d_{append_name}']  * ac.data_of_countries['United States']['populations'], color = 'tab:red')
#         ax.set_ylim(0, 0.2)
#         print(f'{file_idx}_{param_idx}')
#         artists.append(container)


# ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1)
# plt.show()





# fig, ax = plt.subplots(5, 8)
# for i in range(5):
#     for j in range(8):
#         plt.sca(ax[i, j])
#         fc.plot_contact_spearman_from_r0(ax[i, j], anal_data['pearson_from_r0'], expr_name = 'necs_from_fatality', expr_param = 'coef_beta_1', param_idx = i * 8 + j, target = 'd')















