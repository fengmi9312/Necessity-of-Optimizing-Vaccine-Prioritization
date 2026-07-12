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
    grid_attrs = [[{'pos': (0, 0), 'size': (24, 24)}],[{'pos': (25, 0), 'size': (1, 24)}]]
    margin_attr = {'top': 3, 'bottom': 7, 'left': 7, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    ####################################################
    
    country = 'Israel'
    countries = [country]
    country_data = load_all_data(countries, basic_params.group_div)
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    contacts = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    ax = axes[0][0]
    plt.sca(ax)
    im = plt.imshow(contacts, origin = 'lower', cmap = 'Reds')
    plt.xticks(np.arange(len(age_groups)), age_groups, rotation = -90, fontsize = tick_fontsize)
    plt.yticks(np.arange(len(age_groups)), age_groups, fontsize = tick_fontsize)
    figure_setting.set_xylabel(ax, 'Age group', 'Age group', fontsize = label_fontsize, xlabel_coords = -0.2, ylabel_coords = -0.2)
    plt.title(country, fontsize = 15)
    cbar = fig.colorbar(im, cax=axes[1][0])
    cbar.set_label('Contact intensity', fontsize = 10)
    
    return fig, axes