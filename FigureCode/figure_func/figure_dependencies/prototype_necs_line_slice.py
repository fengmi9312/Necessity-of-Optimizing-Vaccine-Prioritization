# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:28:51 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting


def draw(anal_data, expr_name, **kwargs):
    expr_name_type = expr_name.split('_')[-1]
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (0, 14), 'size': (15, 10)}, {'pos': (0, 28), 'size': (15, 10)}, {'pos': (0, 42), 'size': (15, 10)}],
                  [{'pos': (22, 0), 'size': (15, 10)}, {'pos': (22, 14), 'size': (15, 10)}, {'pos': (22, 28), 'size': (15, 10)}, {'pos': (22, 42), 'size': (15, 10)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 2}
    removed_labels = {'x': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    text_fontsize = 9
    ####################################################
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        if expr_name_type == 'param': expr_param = 'delay'
        elif expr_name_type == 'fatality': expr_param = 'coef_beta_1'
        else: pass
        sheet_name = f"{expr_name}_({expr_param}_{ax_idx * 13})-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}_necs"
        data_line = anal_data['necs_line_from_r0'][sheet_name]['res'] * 100
        plt.plot(np.exp(np.arange(1600) * 0.075 / 40), data_line, linewidth = 2.5, color = 'tab:orange')
        if expr_name_type == 'param': ax.text(0.03, 0.97, f"$T_{{\\mathrm{{resp}}}} = {ax_idx * 6.5}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        elif expr_name_type == 'fatality': ax.text(0.03, 0.97, f"$\\gamma = {ax_idx} / 3$" if ax_idx != 0 and ax_idx != 3 else f"$\\gamma = {int(ax_idx / 3)}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        plt.xscale('log')
        if expr_name.split('_')[-1] == 'param':
            if target == 'c': 
                ax.set_ylim(0, 40)
                ax.set_yticks(np.arange(0, 41, 10))
            elif target == 'd': 
                ax.set_ylim(0, 2.7)
                ax.set_yticks(np.arange(0, 28, 9) / 10)
            else: pass
        elif expr_name.split('_')[-1] == 'fatality':
            if target == 'c': plt.ylim(0, 35)
            elif target == 'd': plt.ylim(0, 1.5)
            else: pass
        else: pass
        figure_setting.set_xylabel(ax, r'$R_0$', fr'$\mathcal{{N}}_{{\mathrm{{{target}}}}}$', fontsize = label_fontsize, xlabel_coords = -0.15 if target == 'c' else -0.24, ylabel_coords = -0.14 if target == 'c' else -0.14)
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        
       
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    text_fontsize = 9
    ####################################################
    for ax_idx, ax in enumerate(axes[1]):
        if expr_name_type == 'param': expr_param = 'delay'
        elif expr_name_type == 'fatality': expr_param = 'coef_beta_1'
        else: pass
        plt.sca(ax)
        sheet_name = f"{expr_name}_({expr_param}_{ax_idx * 13})_{target}_{basic_params.country_abbr[country]}"
        x = np.exp(np.arange(1600) * 0.075 / 40)
        plt.plot(x, (np.arccos(anal_data['corr_line_from_r0'][sheet_name]['optimal_indx']) - np.arccos(anal_data['corr_line_from_r0'][sheet_name]['optimal_dirx'])) / np.arccos(anal_data['corr_line_from_r0'][sheet_name]['effect_corrx']), 
                 linestyle = '', marker = 'x', markerfacecolor = 'white', markeredgecolor = '#C54E53', markersize = 4, markeredgewidth = 1.2, label = 'Optimal')
        plt.plot(x, (np.arccos(anal_data['corr_line_from_r0'][sheet_name]['worst_indx']) - np.arccos(anal_data['corr_line_from_r0'][sheet_name]['worst_dirx'])) / np.arccos(anal_data['corr_line_from_r0'][sheet_name]['effect_corrx']), 
                 linestyle = '', marker = 'o', markerfacecolor = 'white', markeredgecolor = '#4C72B1', markersize = 4, markeredgewidth = 1.2, alpha = 0.3, label = 'Burden-maximizing')
        
        plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
        figure_setting.set_xylabel(ax, r'$R_0$', r'$\xi$', fontsize = label_fontsize, xlabel_coords = -0.22 if target == 'c' else -0.2, ylabel_coords = -0.21 if target == 'c' else -0.21)
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
