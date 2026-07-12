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
    expr_name_type = expr_name.split('_')[-1]
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    mark = kwargs.pop('mark', True)
    data_type = kwargs.pop('data_type', 'necs')
    text = kwargs.pop('text', '0')
    scale_prop = kwargs.pop('scale_prop', 12)
    ####################################################
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (20, 0), 'size': (15, 10)}],
                  [{'pos': (0, 17), 'size': (15, 10)}, {'pos': (20, 17), 'size': (15, 10)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [(0, 1), (1, 1)], 'xtick': [], 'ytick': []}
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
        sheet_name = f"{expr_name}_(delay_{[8, 13][i]})-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}_necs"
        data_line = anal_data['necs_line_from_r0'][sheet_name]['res'] * 100
        diff_necs = np.diff(data_line, prepend = 0)
        xvlines = np.exp(np.where(diff_necs[:-1] * diff_necs[1:] < 0)[0] * 0.075)
        plt.plot(np.exp(np.arange(1600) * 0.075 / 40), data_line, linewidth = 2.5, color = 'tab:orange')
        plt.title(f"$\\delta = {[4, 6.5][i]}$ days", ha='center', va='bottom', fontsize= text_fontsize, transform=ax.transAxes)
        plt.xscale('log')
        # if expr_name.split('_')[-1] == 'param':
        if target == 'c': 
            ax.set_ylim(0, 40)
            ax.set_yticks(np.arange(0, 41, 10))
        elif target == 'd': 
            ax.set_ylim(0, 2.7)
            ax.set_yticks(np.arange(0, 28, 9) / 10)
        else: pass
        # elif expr_name.split('_')[-1] == 'fatality':
        #     if target == 'c': plt.ylim(0, 35)
        #     elif target == 'd': plt.ylim(0, 1.5)
        #     else: pass
        # else: pass
        figure_setting.set_xylabel(ax, r'$R_0$', r'$\mathcal{N}_\mathrm{c}$ (%)', fontsize = label_fontsize, xlabel_coords = -0.2 if target == 'c' else -0.24, ylabel_coords = -0.15 if target == 'c' else -0.21)
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        
        
        ####################################################
        spine_linewidth = 1.5
        label_fontsize = 12
        tick_fontsize = 9
        ####################################################
        ax = axes[1][i]
        plt.sca(ax)
        sheet_name = f"{expr_name}_(delay_{[8, 13][i]})_{target}_{basic_params.country_abbr[country]}"
        x = np.exp(np.arange(1600) * 0.075 / 40)
        
        plt.plot(x[::5], (anal_data['corr_line_from_r0'][sheet_name]['optimal_dir'] - anal_data['corr_line_from_r0'][sheet_name]['optimal_ind'])[::5], 
                 linestyle = '', marker = 'x', markerfacecolor = 'white', markeredgecolor = RED, markersize = 3.5, markeredgewidth = 0.6, label = 'Optimal')
        plt.plot(x[::5], (anal_data['corr_line_from_r0'][sheet_name]['worst_dir'] - anal_data['corr_line_from_r0'][sheet_name]['worst_ind'])[::5], 
                 linestyle = '', marker = 'o', markerfacecolor = 'white', markeredgecolor = BLUE, markersize = 3.5, markeredgewidth = 0.6, label = 'Burden-maximizing')
        # plt.plot(x[::5], (anal_data['corr_line_from_r0'][sheet_name]['optimal_dir'] - anal_data['corr_line_from_r0'][sheet_name]['optimal_ind'])[::5], 
        #          linestyle = '', marker = 'x', markerfacecolor = 'white', markeredgecolor = RED, markersize = 3.5, markeredgewidth = 0.6, label = 'Optimal')
        # plt.plot(x[::5], (anal_data['corr_line_from_r0'][sheet_name]['worst_dir'] - anal_data['corr_line_from_r0'][sheet_name]['worst_ind'])[::5], 
        #          linestyle = '', marker = 'o', markerfacecolor = 'white', markeredgecolor = BLUE, markersize = 3.5, markeredgewidth = 0.6, label = 'Worst')
        # plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['alloc_corr'], linestyle = '--', linewidth = 0.5, color = 'black')
        # plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['optimal_1'], linestyle = '', marker = 'o', markerfacecolor = 'tab:orange', markeredgecolor = 'white', markersize = 1.5, markeredgewidth = 0)
        # plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['worst_1'], linestyle = '', marker = 'o', markerfacecolor = 'tab:green', markeredgecolor = 'white', markersize = 1.5, markeredgewidth = 0)
        plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
        # for x_val in vline_xs:
        #     plt.axvline(x_val, linestyle = '--', color = 'tab:gray')
        figure_setting.set_xylabel(ax, r'$R_0$', r'$\xi$', fontsize = label_fontsize, xlabel_coords = -0.25 if target == 'c' else -0.2, ylabel_coords = -0.15 if target == 'c' else -0.24)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xscale('log')
        if i == 0: leg = plt.legend(loc = 'lower left', fontsize = 9, bbox_to_anchor=(0, 1.01), ncol = 2)
        for h in leg.legend_handles: 
            h.set_markersize(5)
            h.set_markeredgewidth(1.5)
        
        # ax_twin = ax.twinx()
        # plt.sca(ax_twin)
        # plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['alloc_corr'], color = 'k')
        # figure_setting.remove_labels(axes, removed_labels)
        # if mark and expr_name == 'necs_line_from_param' and (expr_param == 'delay_8') and target == 'c':
        if i == 0:
            ax = axes[1][0]
            plt.sca(ax)
            for x_point in [1.8, 5.5, 16]:
                plt.axvline(x_point, linestyle = '--', color = 'tab:gray', linewidth = 0.8, zorder = 0)
    figure_setting.remove_labels(axes, removed_labels)
    fig.suptitle('Slices at two response delays',fontsize=15, y=0.97)
    return fig, axes
