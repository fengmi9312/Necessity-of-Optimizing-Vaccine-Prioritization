# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:31:46 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
from Dependencies.CodeDependencies import basic_params
from Dependencies.CodeDependencies.param_data_loader import load_all_data

def draw(anal_data):
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (20, 0), 'size': (15, 10)}, {'pos': (40, 0), 'size': (15, 10)}, {'pos': (60, 0), 'size': (15, 10)}],]
    margin_attr = {'top': 3, 'bottom': 8, 'left': 6, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 10
    tick_fontsize = 8
    text_fontsize = 9
    ####################################################
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    for ax_idx in range(4):
        ax = axes[0][ax_idx]
        plt.sca(ax)
        plt.bar(np.arange(16), anal_data['direct_effects']['delay_14_c'][str(ax_idx * 8)], color = 'tab:green', width = 0.8, edgecolor='k', linewidth = 1)
        ax.set_ylim(0, 1)
        ax.spines['left'].set_bounds(0, 1)
        ax.set_yticks(np.arange(0, 3, 1) / 2)
        figure_setting.set_xylabel(ax, 'Age group', 'Direct effect', fontsize = label_fontsize, xlabel_coords = -0.3, ylabel_coords = -0.15)
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xticks(rotation = 90, fontsize = label_fontsize * 0.6)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.tick_params(axis='x', which='major', pad=1)
        ax.text(0.03, 1, rf"$\ln R_0 = {[0, 0.6, 1.2, 1.8][ax_idx]}$", ha='left', va='bottom', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
    
    return fig, axes