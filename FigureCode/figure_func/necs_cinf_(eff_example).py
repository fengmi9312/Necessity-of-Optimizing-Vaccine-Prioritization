# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting


def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    delay_idx = 0
    scale_prop = 10
    grid_attrs = [[{'pos': (1, 0), 'size': (14, 8)}, {'pos': (25, 0), 'size': (14, 8)}, {'pos': (49, 0), 'size': (14, 8)}],]
    margin_attr = {'top': 3, 'bottom': 7, 'left': 6, 'right': 2}
    removed_labels = {'x': [], 'y': [(0, 1), (0, 2)], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 9
    tick_fontsize = 9
    text_fontsize = 10
    ####################################################
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    spine_linewidth = 1.2
    label_fontsize = 9
    tick_fontsize = 9.5
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        ax.bar(np.arange(16), -anal_data['group_effect_from_r0_factor']['example'][['low', 'mid', 'high'][ax_idx]], 
               color = 'tab:green', width = 0.8, edgecolor='black', linewidth = 0.5)
        figure_setting.set_xylabel(ax, 'Age group', 'Sensitivity', fontsize = label_fontsize, xlabel_coords = -0.5, ylabel_coords = -0.16)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xticks(rotation = 90, fontsize = tick_fontsize * 0.6)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.set_yticks(np.arange(0, 3, 1), np.arange(0, 3, 1))
        ax.set_ylim(0, 2)
        ax.spines['left'].set_position(('outward', 1))
        ax.tick_params(axis='x', which='major', pad=1)
        figure_setting.remove_spines(ax, ['top', 'right'])
        ax.text(0.5, 1, f'$R_0 = {[1.8, 5.5, 16][ax_idx]}$', ha='center', va='bottom', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes