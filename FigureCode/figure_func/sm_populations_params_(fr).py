# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
from Dependencies.CodeDependencies import basic_params
from Dependencies.CodeDependencies.param_data_loader import load_all_data


def draw(anal_data):
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (24, 16)}],]
    margin_attr = {'top': 3, 'bottom': 8, 'left': 6, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 15
    tick_fontsize = 12
    ####################################################
    
    country = 'France'
    countries = [country]
    country_data = load_all_data(countries, basic_params.group_div)
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    ax = axes[0][0]
    plt.sca(ax)
    plt.bar(np.arange(16), country_data[country]['populations'] * 100, color = 'tab:orange', width = 0.8, edgecolor='tab:gray', linewidth = 1)
    ax.set_ylim(0, 10)
    ax.spines['left'].set_bounds(0, 10)
    ax.set_yticks(np.arange(0, 11, 5))
    figure_setting.set_xylabel(ax, 'Age group', 'Population fraction (%)', fontsize = label_fontsize, xlabel_coords = -0.25, ylabel_coords = -0.12)
    figure_setting.remove_spines(ax, ['top', 'right'])
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    plt.xticks(rotation = 90, fontsize = label_fontsize * 0.6)
    plt.title(country, fontsize = 15)
    ax.set_xlim(-1, 16)
    ax.spines['bottom'].set_bounds(0, 15)
    ax.set_xticks(np.arange(16), age_groups, rotation = 90)
    ax.tick_params(axis='x', which='major', pad=1)
    
    return fig, axes