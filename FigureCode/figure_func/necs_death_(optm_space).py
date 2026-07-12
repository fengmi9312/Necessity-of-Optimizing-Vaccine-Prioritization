# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 00:51:58 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
import seaborn as sns
from AnalysisCode.analysis_func.analysis_dependencies import required_generated_data as rgd
from Dependencies.CodeDependencies import basic_params
from copy import deepcopy
data_of_countries = rgd.data_of_countries

def draw(anal_data):
    x_coords, y_coords, z_values = [], [], []
    alloc_coef_idxes = []
    for idx in range(2):
        x_coords.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['x_coef'].to_numpy())
        y_coords.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['y_coef'].to_numpy())
        z_values.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['prdt'].to_numpy() * 100)
        alloc_coef_idxes.append(np.array([x_coords[-1], y_coords[-1]]).T)
        
    
    ####################################################
    # scale_prop = 0.3
    # grid_attrs = [[{'pos': (0, 0), 'size': (max(x_coords[0]) - min(x_coords[0]), max(y_coords[0]) - min(y_coords[0]))}, 
    #                {'pos': (max(x_coords[0]) - min(x_coords[0]) + 100, 0), 'size': (max(x_coords[1]) - min(x_coords[1]), max(y_coords[1]) - min(y_coords[1]))}], ]
    # margin_attr = {'top': 100, 'bottom': 100, 'left': 100, 'right': 100}
    # removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 0), (0, 1)], 'xtick': [(0, 0), (0, 1)], 'ytick': [(0, 0), (0, 1)]}
    # fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    
    scale_prop = 6
    grid_attrs = [[{'pos': (0, 4), 'size': (40, 40)}, {'pos': (64, 4), 'size': (40, 40)}], 
                  [{'pos': (4, 0), 'size': (36, 2)}, {'pos': (68, 0), 'size': (36, 2)}], 
                  [{'pos': (4, 44), 'size': (22, 16)}, {'pos': (36, 44), 'size': (22, 16)}, {'pos': (68, 44), 'size': (22, 16)}, {'pos': (100, 44), 'size': (22, 16)}]]
    margin_attr = {'top': 5, 'bottom': 10, 'left': 5, 'right': 5}
    removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 0), (0, 1)], 'xtick': [(0, 0), (0, 1)], 'ytick': [(0, 0), (0, 1)]}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    
    deep_colors = sns.color_palette('deep')
    ####################################################
    spine_linewidth = 1
    label_fontsize = 9
    tick_fontsize = 8
    ####################################################
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        x_min, x_max = min(x_coords[ax_idx]), max(x_coords[ax_idx])
        y_min, y_max = min(y_coords[ax_idx]), max(y_coords[ax_idx])
        grid = np.full((x_max - x_min + 1, y_max - y_min + 1), np.nan)
        
        # Map x, y positions to grid
        for (x, y), z in zip(alloc_coef_idxes[ax_idx], z_values[ax_idx]):
            grid[x - x_min, y - y_min] = z
                
        pm = plt.pcolormesh(np.arange(x_max - x_min + 1), np.arange(y_max - y_min + 1), grid.T, cmap=sns.color_palette("viridis", as_cmap=True), rasterized=True)
        
        plt.plot([0, x_max - x_min], [0 - y_min, 0 - y_min], color = 'black', linestyle = ':', linewidth = 1)
        plt.plot([0], [0 - y_min], marker = 'x', color = deep_colors[1], markersize = 8 , markeredgewidth = 2 )
        plt.plot([x_max - x_min], [0 - y_min], marker = '+', color = deep_colors[2], markersize = 8 , markeredgewidth = 2)
        plt.xlim(- 0.1 * (x_max - x_min), 1.1 * (x_max - x_min))
        plt.ylim(- 0.1 * (y_max - y_min), 1.1 * (y_max - y_min))
        #set_xylabel(ax, 'Dimension 1', 'Dimension 2', fontsize = label_fontsize * unit, xlabel_coords = -0.05, ylabel_coords = -0.05)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        cbar = fig.colorbar(pm, cax=axes[1][ax_idx], orientation='horizontal')
        cbar.set_label('Deaths (%)', labelpad=2, fontsize = 7.2)
        cbar.ax.tick_params(labelsize= 6.4)
        figure_setting.remove_all_spines(ax)
        ax.text(0.2, 0.8, f'$R_0 = {[1.70, 1.74][ax_idx]}$', fontsize = 9, ha = 'center', va = 'center', transform=ax.transAxes, math_fontfamily = 'cm')
        ax.annotate('Direct protection', xy=(x_max - x_min, 0 - y_min), xytext=(x_max - x_min - 350, 0 - y_min + 270), ha='center', va='top',
            arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7), fontsize = 8, math_fontfamily = 'cm')
        ax.annotate('Balanced Protection', xy=(0, 0 - y_min), xytext=(- 350, 0 - y_min + 270), ha='center', va='top', arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7), fontsize = 8, math_fontfamily = 'cm')
        ax.invert_xaxis()
        ax.invert_yaxis()
        #cbar_ax.yaxis.set_ticks_position('right')
        # divider = make_axes_locatable(ax)
        # cbar_ax = divider.append_axes("right", size="5%", pad=0.2)
        # cbar = fig.colorbar(pm, cax=cbar_ax)
        #cbar.set_label("Fraction (%)", rotation=270, labelpad=15)
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    from scipy.stats import pearsonr
    contact_arr = np.sum([data_of_countries['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    calc_params = deepcopy(basic_params.calc_params)
    for ax_idx, ax in enumerate(axes[2]):
        plt.sca(ax)
        alloc = anal_data['prdt_from_xycoef']['alloc_res'][f"alloc_{ax_idx // 2}_{['n', 'p'][ax_idx % 2]}"]
        ax.bar(np.arange(16), alloc * 100, color = [deep_colors[2], deep_colors[1]][ax_idx % 2], width = 0.8, edgecolor='black', linewidth = 0.5)
        figure_setting.set_xylabel(ax, 'Age group', 'Allocation (%)', fontsize = label_fontsize, xlabel_coords = -0.38, ylabel_coords = -0.14)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize * 0.7)
        plt.xticks(rotation = 90)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90, fontsize = 5.5)
        ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4), fontsize = 7)
        ax.set_ylim(0, 8)
        #ax.spines['left'].set_position(('outward', 1))
        ax.tick_params(axis='x', which='major', pad=1)
        figure_setting.remove_spines(ax, ['top', 'right'])
        indirect_corr = anal_data['prdt_from_xycoef']['angles'][f"corr_{ax_idx // 2}_{['n', 'p'][ax_idx % 2]}_ind"][0]
        direct_corr = anal_data['prdt_from_xycoef']['angles'][f"corr_{ax_idx // 2}_{['n', 'p'][ax_idx % 2]}_dir"][0]
        tot_corr = anal_data['prdt_from_xycoef']['angles'][f"corr_{ax_idx // 2}_{['n', 'p'][ax_idx % 2]}_tot"][0]
        ax.text(0.05, 0.9, rf"$\xi = {np.round((indirect_corr - direct_corr) / tot_corr, 3)}$", fontsize = 8, ha = 'left', va = 'top', transform=ax.transAxes, math_fontfamily = 'cm')
        
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes

















