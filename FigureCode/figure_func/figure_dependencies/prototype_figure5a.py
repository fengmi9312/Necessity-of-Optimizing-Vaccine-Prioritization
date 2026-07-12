# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:58:06 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting

def draw(anal_data, **kwargs):
    ####################################################
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 7
    grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (30, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [(0, 1), (0, 2), (0, 3)], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 8
    tick_fontsize = 7
    ####################################################
    expr_params = ['1', '2', '13']
    titles = ['School Closure', 'Remote Work', 'Full Lockdown']
    anal_name = 'necs_from_r0_factor'
    
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        task_name = f'necs_from_contact_({expr_params[ax_idx]})'
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        sheet_name = f'{sheet_name_preppend}_{data_type}'
        r0_ls = np.exp(np.arange(40) * 3 / 40)
        data_tmp = anal_data[anal_name][sheet_name] * 100
        plt.quiver(r0_ls, data_tmp[:, -1], np.zeros(len(r0_ls)), data_tmp[:, 0] - data_tmp[:, -1], color = 'tab:gray',angles='xy',scale_units='xy', scale = 1)
        ax.plot(r0_ls, data_tmp[:, -1], linestyle='', marker = 'o', color = 'lightcoral', markersize = 3, label = 'No Intervetion')
        ax.plot(r0_ls, data_tmp[:, 0], linestyle='', marker = 'o', color = 'skyblue', markersize = 3, label = 'Post Intervetion')
        figure_setting.set_xylabel(ax, r'$R_0$', 'Necessity (%)', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.12)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        if target == 'c' and data_type == 'necs':
            plt.ylim(-1, 31)
            ax.set_yticks(np.arange(0, 31, 10))
        elif target == 'd' and data_type == 'necs':
            plt.ylim(-1 / 20, 31 / 20)
            ax.set_yticks(np.arange(0, 31, 10) / 20)
        plt.xscale('log')
        ax.text(0.04, 0.96, titles[ax_idx], fontsize = 7.5, color = 'black', horizontalalignment='left', verticalalignment='top', transform= ax.transAxes)
        if ax_idx == 0: 
            if target == 'c': plt.legend(fontsize = 7, loc = 'center right', bbox_to_anchor=(0.995, 0.75), handletextpad=0.1)
            else: plt.legend(fontsize = 7, loc = 'lower right', handletextpad=0.1)
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes