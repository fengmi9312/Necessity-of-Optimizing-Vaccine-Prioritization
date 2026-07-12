# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:28:51 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting

RED = '#D43732'
BLUE = '#2B69B7'
GREEN = '#2E8E2F'

def draw(anal_data):
    ####################################################
    data_type = 'necs'
    country = 'United States'
    target = 'c'
    acc_type = 'dd'
    dur = False
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (0, 14), 'size': (15, 10)}, {'pos': (0, 28), 'size': (15, 10)}, {'pos': (0, 42), 'size': (15, 10)}],
                  [{'pos': (22, 0), 'size': (15, 10)}, {'pos': (22, 14), 'size': (15, 10)}, {'pos': (22, 28), 'size': (15, 10)}, {'pos': (22, 42), 'size': (15, 10)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 2}
    removed_labels = {'x': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 10
    tick_fontsize = 9
    text_fontsize = 9
    ####################################################
    
    slice_idxes = [0, 13, 26, 39]
    
    task_name = 'necs_from_param_by_eta_(delay)'
    anal_name = 'necs_from_r0_factor_by_eta'
    sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
    sheet_name = f'{sheet_name_preppend}_{data_type}'
    necs = np.array(anal_data[anal_name][sheet_name].T * 100)
    
    anal_name = 'corr_from_r0_factor_by_eta'
    corr_opt, corr_wor = [], []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        corr_opt.append((np.arccos(anal_data[anal_name][sheet_name]['optimal_dirx']) - np.arccos(anal_data[anal_name][sheet_name]['optimal_ind']))/ np.arccos(anal_data[anal_name][sheet_name]['effect_corrx']))
        corr_wor.append((np.arccos(anal_data[anal_name][sheet_name]['worst_dirx']) - np.arccos(anal_data[anal_name][sheet_name]['worst_indx'])) / np.arccos(anal_data[anal_name][sheet_name]['effect_corrx']))
    corr_opt, corr_wor = np.array(corr_opt), np.array(corr_wor)
    x = np.exp(np.arange(40) * 0.075)
    for ax_idx in range(4):
        ax = axes[0][ax_idx]
        plt.sca(ax)
        plt.plot(x, necs[slice_idxes[ax_idx]], linewidth = 2.5, color = 'tab:orange')
        ax.text(0.03, 0.97, f"$\\gamma^* = {ax_idx} / 3$" if ax_idx != 0 and ax_idx != 3 else f"$\\gamma^* = {int(ax_idx / 3)}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        plt.xscale('log')
        ax.set_ylim(0, 40)
        ax.spines['left'].set_bounds(0, 40)
        ax.set_yticks(np.arange(0, 41, 10))
        figure_setting.set_xylabel(ax, r'$R_0$', r'$\mathcal{N}_{\mathrm{c}}$ (%)', fontsize = label_fontsize, xlabel_coords = -0.15, ylabel_coords = -0.14)
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        
        ax = axes[1][ax_idx]
        plt.sca(ax)
        plt.plot(x, corr_opt[slice_idxes[ax_idx]], 
                 linestyle = '', marker = 'x', markerfacecolor = 'white', markeredgecolor = RED, markersize = 4, markeredgewidth = 1.2, label = 'Optimal')
        plt.plot(x, corr_wor[slice_idxes[ax_idx]], 
                 linestyle = '', marker = 'o', markerfacecolor = 'white', markeredgecolor = BLUE, markersize = 4, markeredgewidth = 1.2, alpha = 0.3, label = 'Burden-maximizing')
        
        figure_setting.set_xylabel(ax, r'$R_0$', r'$\xi$', fontsize = label_fontsize, xlabel_coords = -0.2, ylabel_coords = -0.2)
        plt.xlabel(r'$R_0$', fontsize = label_fontsize)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xscale('log')
        if ax_idx == 0: leg = plt.legend(loc = 'lower center', fontsize = 8, bbox_to_anchor=(0.5, 1.01), ncol = 2)
        for h in leg.legend_handles: 
            h.set_markersize(5)
            h.set_markeredgewidth(1.5)
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes
