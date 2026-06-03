# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 16:05:45 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
from Dependencies.CodeDependencies import basic_params



def draw(anal_data, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 15)}, {'pos': (25, 0), 'size': (20, 15)}, {'pos': (0, 18), 'size': (20, 15)}, {'pos': (25, 18), 'size': (20, 15)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 15}
    removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 1), (0, 3)], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    markers = {'weibull_0':'o', 'weibull_1': 's', 'weibull_2': 'D', 'gamma_0': '^', 'gamma_1': '1', 'gamma_2': '+', 'lognormal_0': 'x', 'lognormal_1': '*', 'lognormal_2': 'h'}
    colors = {'weibull_0':'black', 'weibull_1': 'tab:cyan', 'weibull_2': 'tab:brown', 'gamma_0': 'tab:purple', 'gamma_1': 'tab:gray', 'gamma_2': 'tab:orange', 'lognormal_0': 'tab:green', 'lognormal_1': 'tab:red', 'lognormal_2': 'tab:blue'}
    labels = {'weibull_0': r'Weibull, $\alpha = 0.7$', 'weibull_1': r'Weibull, $\alpha = 1$', 'weibull_2' : r'Weibull, $\alpha = 2$', 
              'gamma_0': r'Gamma, $\alpha = 0.7$', 'gamma_1': r'Gamma, $\alpha = 1$', 'gamma_2': r'Gamma, $\alpha = 2$', 
              'lognormal_0': r'Lognormal, $\sigma = 0.15$', 'lognormal_1': r'Lognormal, $\sigma = 0.35$', 'lognormal_2': r'Lognormal, $\sigma = 1.45$'}
    r0_list = np.round(np.exp(np.array([8, 16, 24, 32]) * 0.075), 2)
    markeredgewidth = 1.5
    markersize = 6
    text_fontsize = 10
    anal_name = 'necs_from_growth'
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        for expr_param in expr_params:
            sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
            plt.plot(anal_data[anal_name][sheet_name][f'growth_{ax_idx}'], anal_data[anal_name][sheet_name][f'necs_{ax_idx}'] * 100, linestyle = '', 
                     marker = markers[expr_param], markerfacecolor='none', markeredgecolor=colors[expr_param], markeredgewidth = markeredgewidth, markersize = markersize, label = labels[expr_param])
        figure_setting.set_xylabel(ax, r'$gT_{\mathrm{resp}}$', 'Necessity (%)', fontsize = label_fontsize, xlabel_coords = -0.16, ylabel_coords = -0.16)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        ax.text(0.985, 0.95, f"$R_0 = {r0_list[ax_idx]}$", ha='right', va='top', fontsize= text_fontsize, transform=ax.transAxes)
        ax.set_xticks(np.arange(0, 14, 6), np.arange(0, 14, 6))
        if ax_idx == 1: plt.legend(ncol = 1, loc='center left', bbox_to_anchor=(1, -0.1), fontsize = 7.5, labelspacing=0.75, columnspacing=0.75, handletextpad=0.1, frameon=False)
    
    for i in range(1, 4):
        axes[0][i].set_xlim(axes[0][0].get_xlim())
    # bbox = leg.get_window_extent()
    # bbox = bbox.transformed(plt.gcf().transFigure.inverted())
    # leg_titles = ['Weibull:', 'Gamma:', 'Log-normal:']
    # for i in range(3): plt.text(bbox.x0 + 0.1 + i * 0.27, bbox.y1 + 0.0025, leg_titles[i], transform=plt.gcf().transFigure, fontsize=7.5, ha='center')
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes