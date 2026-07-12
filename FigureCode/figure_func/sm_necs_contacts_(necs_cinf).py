# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params, func
from .figure_dependencies import figure_setting
import matplotlib.patches as patches
from matplotlib.transforms import blended_transform_factory
from scipy.ndimage import minimum_filter
from copy import deepcopy
from itertools import combinations
from Dependencies.CodeDependencies.param_data_loader import load_all_data

def draw(anal_data, **kwargs):
    corr_contour = kwargs.pop('corr_contour', True)
    anal_name = 'necs_from_r0_factor'
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (50, 0), 'size': (30, 30)}], 
                  [{'pos': (32, 0), 'size': (2, 30)}, {'pos': (82, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 6, 'bottom': 5, 'left': 7, 'right': 4}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 15
    tick_fontsize = 9
    #####################################################
    target = 'c'
    acc_type = 'dd'
    country = 'United States'
    
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    coef_pos_list = []
    for r in range(1, 4):
        for combo in combinations([0, 1, 2, 3], r):
            coef_pos_list.append(list(combo))
    
    for ax_idx, expr_param in enumerate(['1', '13']):
        task_name = f'necs_from_contact_({expr_param})'
        corr_anal_name = f"corr_{anal_name.partition('_')[2]}"
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}"
        ax = axes[0][ax_idx]
        plt.sca(ax)
        x = np.exp(np.arange(40) * 3 / 40)
        y = np.arange(41) / 40
        X = []
        corr_z = []
        coef_pos = coef_pos_list[int(expr_param)]
        for param_idx, param_val in enumerate(y):
            corr_sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            contacts_total = np.array([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']])
            xxx = np.max(np.linalg.eig(country_data['United States']['populations'][None, :] * contacts_total.sum(axis = 0))[0])
            contacts_total[coef_pos] *= param_val
            yyy = np.max(np.linalg.eig(country_data['United States']['populations'][None, :] * contacts_total.sum(axis = 0))[0])
            X.append(x * yyy / xxx)
            if param_idx < 40: corr_z.append((np.arccos(anal_data[corr_anal_name][corr_sheet_name]['optimal_dirx']) - np.arccos(anal_data[corr_anal_name][corr_sheet_name]['optimal_indx'])) / np.arccos(anal_data[corr_anal_name][corr_sheet_name]['effect_corrx']))
        Y = np.array([y for i in range(40)]).T
        sheet_name = f'{sheet_name_preppend}_necs'
        res = anal_data[anal_name][sheet_name].to_numpy().T * 100
        res = np.vstack((res, anal_data[anal_name][f'necs_from_param_(delay)-{basic_params.country_abbr[country]}_{target}_{acc_type}_necs'].to_numpy().T[14] * 100))
        corr_add = anal_data[corr_anal_name][f'necs_from_param_(delay)_{target}_14_{basic_params.country_abbr[country]}']
        corr_z = np.vstack((corr_z, (np.arccos(corr_add['optimal_dirx']) - np.arccos(corr_add['optimal_indx'])) / np.arccos(corr_add['effect_corrx'])))
        c = ax.pcolormesh(X[::-1], 1 - Y[::-1], res[::-1], cmap = 'Blues')
        if corr_contour:
            ax.clabel(plt.contour(X[::-1], 1 - Y[::-1], corr_z[::-1], levels=[0], colors='k', linestyles = 'solid', linewidths = 1), fontsize = 10, fmt = lambda x: rf'$\xi = {0 if x == 0 else np.round(x, 1)}$')
     
        
        ax.set_xscale('log')
        
        y_label = r'Contact-closure level, $\varrho$' 
        ax.set_yticks(np.arange(40)[0::13] / 39, ['0', r'$1/3$', r'$2/3$', '1'])
        target_name = {'c': 'cumulative infections', 'd': 'deaths'}[target]
        if target == 'c': title = f'Epidemiological necessity for\n'fr'{target_name} ($\mathcal{{N}}_{{\mathrm{{{target}}}}}$)'
        else: title = f'Epidemiological necessity\n'fr'for {target_name} ($\mathcal{{N}}_{{\mathrm{{{target}}}}}$)'
        plt.title(title, fontsize = 15, pad=8,linespacing=1.15)
        
        figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        cbar = fig.colorbar(c, cax=axes[1][ax_idx])
        cbar.ax.set_title(r'$\mathcal{N}_{\mathrm{c}}$ (%)', pad = 6, fontsize = 10)
        cbar.ax.tick_params(labelsize = 6.4)
        figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
        figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    
    return fig, axes




    # if expr_name == 'necs_from_param' and expr_param == 'delay' and target == 'c':
    #     center_x, center_y, width, height = 0.5, 10, 1.02, 1.2
    #     ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:orange', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = 0.5, 0, 1.02, 1.2
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:purple', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = np.exp(8 * 0.075), 0.5, np.exp((8 - 0.6) * 0.075) - np.exp((8 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:red', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
        # center_x, center_y, width, height = np.exp(24 * 0.075), 0.5, np.exp((24 - 0.6) * 0.075) - np.exp((24 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:blue', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
