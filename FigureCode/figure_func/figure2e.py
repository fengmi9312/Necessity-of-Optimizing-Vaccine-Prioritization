# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting



def draw(anal_data):
    scale_prop = 14
    grid_attrs = [[{'pos': (0, 0), 'size': (12, 24)}], ]
    margin_attr = {'top': 1, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    ax = axes[0][0]
    plt.sca(ax)
    cmap = plt.get_cmap('rainbow')
    x_idx_list = np.arange(4, 37, 4)[::-1]
    r0_list = [f'$R_0$ = {r0}' for r0 in np.round(np.exp(x_idx_list * 0.075), 2)]
    
    overlap = 0.5
    x, ys = [0], []
    for idx, x_idx in enumerate(x_idx_list):
        ys.append([0])
        for key, item in enumerate(1 - anal_data['dist_diff_from_r0']['dist_diff'][f'dist_diff_{x_idx}']):
            if idx == 0:
                x.append(key)
                x.append(key + 1)
            ys[-1].append(item)
            ys[-1].append(item)
        if idx == 0: x.append(key + 1)
        ys[-1].append(0)
        ys[-1] = np.array(ys[-1])
    for idx, y in enumerate(ys):
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder=len(ys) - idx + 1, color = cmap(1 - idx / len(x_idx_list)))
        plt.plot(x, y + idx * overlap, color = 'white', zorder=len(ys) - idx + 1, linewidth = 2)
        plt.plot(np.arange(-1, 18), np.ones(19) * (idx * overlap), color = cmap(1 - idx / len(x_idx_list)), zorder=len(ys) - idx + 1, linewidth = 2)
        
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.set_ylim(ymin = -0.1)
    plt.yticks(np.arange(0, len(r0_list)) * overlap, r0_list, fontsize = 6)
    for ytick, color in zip(ax.get_yticklabels(), [cmap(1 - idx / len(x_idx_list)) for idx in range(len(x_idx_list))]):
        ytick.set_color(color)
        
    ax.spines['bottom'].set_color(cmap(1.0))
    ax.spines['bottom'].set_linewidth(1.2)
    ax.set_xticks(np.arange(16) + 0.5, age_groups, rotation = 90, color = cmap(1.0), fontsize = 5)
    plt.tick_params(left = False)
    ax.tick_params('both', which='major', width = 1.2, color = cmap(1.0))
    ax.tick_params('both', which='minor', width = 1.2, color = cmap(1.0))
    plt.xlabel('Age Group', color = cmap(1.0), fontsize = 8)
    return ax