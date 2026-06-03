# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 00:26:26 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting


def draw(anal_data):
    scale_prop = 12
    ####################################################
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (20, 0), 'size': (15, 10)}]]
    margin_attr = {'top': 4, 'bottom': 4, 'left': 6, 'right': 3}
    removed_labels = {'x': [], 'y': [(0, 1)], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 7.5
    text_fontsize = 12
        ####################################################
    for i in range(2):
        ax = axes[0][i]
        plt.sca(ax)
        task_name = 'group_effect_(delay)'
        anal_name = 'group_effect_from_r0_factor'
        x_line = np.exp(np.arange(40) * 0.075)
        param_idx = [8, 13][i]
        res = [anal_data[anal_name][f"{task_name}-us_c"][str(r0_idx)][param_idx] for r0_idx in range(40)]
        plt.plot(x_line, res, linewidth = 2.5, label = 'Gini coefficient', color = 'tab:green')
        plt.xscale('log')
        figure_setting.set_xylabel(ax, r'$R_0$', 'Gini coefficient', fontsize = label_fontsize, xlabel_coords = -0.2, ylabel_coords = -0.18, math_fontfamily = 'cm')
        ax.text(0.01, 0.97, f"$\\delta = {[4, 6.5][i]}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
        if i == 0: 
            for x_point in [1.8, 5.5, 16]: plt.axvline(x_point, linestyle = '--', color = 'tab:gray', linewidth = 0.8, zorder = 0)
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes
