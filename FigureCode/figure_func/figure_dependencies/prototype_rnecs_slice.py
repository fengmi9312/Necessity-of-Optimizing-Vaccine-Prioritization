# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:28:51 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting
import matplotlib.pyplot as plt

RED = '#D43732'
BLUE = '#2B69B7'
GREEN = '#2E8E2F'

def draw(anal_data, expr_name, expr_param, **kwargs):
    ####################################################
    param_idx = kwargs.pop('param_idx', 0)
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    scale_prop = kwargs.pop('scale_prop', 12)
    ####################################################
    grid_attrs = [[{'pos': (0, 0), 'size': (18, 12)}, {'pos': (24, 0), 'size': (18, 12)}], [{'pos': (0, 15), 'size': (18, 12)}, {'pos': (24, 15), 'size': (18, 12)}]]
    margin_attr = {'top': 6, 'bottom': 4, 'left': 6, 'right': 3}
    removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 1), (1, 1)], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    text_fontsize = 12
        ####################################################
    for i in range(2):
        ax = axes[0][i]
        plt.sca(ax)
        task_name = f'{expr_name}_({expr_param})'
        anal_name = 'necs_from_r0_factor'
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        data_line_max = anal_data[anal_name][f'{sheet_name_preppend}_max'][[8, 13][i]] * 100
        data_line_min = anal_data[anal_name][f'{sheet_name_preppend}_min'][[8, 13][i]] * 100
        data_line_no_vac = anal_data[anal_name][f'{sheet_name_preppend}_no_vac'][[8, 13][i]] * 100
        x_line = np.exp(np.arange(40) * 0.075)
        plt.plot(x_line, data_line_no_vac, linewidth = 2.5, color = 'black', linestyle = (0, (2, 1)), label = 'No vaccination')
        plt.plot(x_line, data_line_max, linewidth = 2.5, color = BLUE, linestyle = (0, (8, 0.8)), label = 'Burden-maximizing')
        plt.plot(x_line, data_line_min, linewidth = 2.5, color = RED, label = 'Optimal')
        plt.ylim(-5, 105)
        plt.yticks([0, 50, 100], [0, 50, 100])
        #ax.text(0.06, 0.97, f"$\\delta = {text}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        plt.xscale('log')
        figure_setting.set_xylabel(ax, r'$R_0$', 'Final cumulative''\n''infections (%)', fontsize = label_fontsize, xlabel_coords = -0.16 if target == 'c' else -0.24, ylabel_coords = -0.12 if target == 'c' else -0.21)
        # figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.title(f"$\\delta = {[4, 6.5][i]}$ days", ha='center', va='bottom', fontsize= text_fontsize, transform=ax.transAxes)
        if i == 0: 
            plt.legend(loc = 'lower left', fontsize = 9, ncol = 3, handlelength=4.5, bbox_to_anchor=(0, 1.15))
            # for x_point in [1.8, 5.5, 16]: plt.axvline(x_point, linestyle = '--', color = 'tab:gray', linewidth = 0.8, zorder = 0)
        
        # ax = axes[1][i]
        # plt.sca(ax)
        # plt.plot(x_line, (data_line_max - data_line_min) / (data_line_no_vac - data_line_min) * 100, linewidth = 1.5, color = 'tab:orange', marker = '^', linestyle = 'none', mfc='none', markersize = 6, label = 'Relative loss')
        # plt.ylim(-5, 105)
        # plt.yticks([0, 50, 100], [0, 50, 100])
        # plt.xscale('log')
        # figure_setting.set_xylabel(ax, r'$R_0$', 'Relative loss (%)', fontsize = label_fontsize, xlabel_coords = -0.16 if target == 'c' else -0.24, ylabel_coords = -0.18 if target == 'c' else -0.21)
        # figure_setting.set_tick_fontsize(ax, tick_fontsize)
        # figure_setting.set_spine_linewidth(ax, spine_linewidth)
        # if i == 0: 
        #     # plt.legend(loc = 'upper left', fontsize = 9, bbox_to_anchor=(0.01, 0.99))
        #     for x_point in [1.8, 5.5, 16]: plt.axvline(x_point, linestyle = '--', color = 'tab:gray', linewidth = 0.8, zorder = 0)
            
        ax = axes[1][i]
        plt.sca(ax)
        task_name = 'group_effect_(delay)'
        anal_name = 'group_effect_from_r0_factor'
        x_line = np.exp(np.arange(40) * 0.075)
        param_idx = [8, 13][i]
        res = [anal_data[anal_name][f"{task_name}-us_c"][str(r0_idx)][param_idx] for r0_idx in range(40)]
        plt.plot(x_line, res, linewidth = 2.5, label = 'Heterogeneity of''\n''marginal benefits (Gini)', color = GREEN, marker = '+', linestyle = 'none', mfc='none', markersize = 6)
        plt.xscale('log')
        figure_setting.set_xylabel(ax, r'$R_0$', 'Heterogeneity of''\n''marginal benefits (Gini)', fontsize = label_fontsize, xlabel_coords = -0.16, ylabel_coords = -0.12)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        #ax.text(0.01, 0.97, f"$\\delta = {[4, 6.5][i]}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        if i == 0: 
            for x_point in [1.8, 5.5, 16]: plt.axvline(x_point, linestyle = '--', color = 'tab:gray', linewidth = 0.8, zorder = 0)
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes
