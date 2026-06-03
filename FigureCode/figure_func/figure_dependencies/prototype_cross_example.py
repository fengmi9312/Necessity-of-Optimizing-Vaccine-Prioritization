# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 15:26:53 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns

def draw(anal_data, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    data_idx = kwargs.pop('data_idx', 0)
    ####################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (16, 12)}, {'pos': (0, 17), 'size': (16, 12)}, ],
                  [{'pos': (25, 7), 'size': (24, 20)}]]
    margin_attr = {'top': 2, 'bottom': 6, 'left': 5, 'right': 8}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    
    deep_colors = sns.color_palette('deep')
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    for ax_idx, ax in enumerate(axes[0]):
        optm_target = ['c', 'd'][ax_idx]
        plt.sca(ax)
        acc_type = 'dd'
        alloc_colors = {'c': deep_colors[2], 'd': deep_colors[1]}
        titles = {'c': r'$\boldsymbol{\vartheta}_\mathrm{c}^{\mathrm{opt}}$', 'd': r'$\boldsymbol{\vartheta}_\mathrm{d}^{\mathrm{opt}}$'}
        sheet_name = 'example_alloc'
        data_tmp = anal_data['bnf_from_example'][sheet_name]
        ax.bar(np.arange(16), data_tmp[f'min_{optm_target}_{data_idx}_{acc_type}'] * 100, color = alloc_colors[optm_target], width = 0.75, edgecolor='black', linewidth = 0.5)
        figure_setting.set_xylabel(ax, 'Age group', 'Allocation (%)', fontsize = label_fontsize * 0.75, xlabel_coords = -0.3, ylabel_coords = -0.1)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize * 0.6)
        plt.xticks(rotation = 90)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
        ax.set_ylim(0, 8)
        #ax.spines['left'].set_position(('outward', 1))
        ax.tick_params(axis='x', which='major', pad=1)
        figure_setting.remove_spines(ax, ['top', 'right'])
        ax.text(0.05, 0.9, [r'$\boldsymbol{\vartheta}_{\mathrm{c}}^{\mathrm{opt}}$', r'$\boldsymbol{\vartheta}_{\mathrm{d}}^{\mathrm{opt}}$'][ax_idx], fontsize = 12, ha = 'left', va = 'center', transform=ax.transAxes)
        if ax_idx == 0: ax.set_xlabel(None)
    
    for ax_idx, ax in enumerate(axes[1]):
        plt.sca(ax)
        acc_type = 'dd'
        alloc_colors = ['black', deep_colors[2], deep_colors[1]]
        titles = [r'$\vartheta_\mathrm{best, c}$', r'$\vartheta_\mathrm{best, d}$']
        sheet_name = 'example_res'
        data_tmp = anal_data['bnf_from_example'][sheet_name]
        ax.bar([-0.5, 0.5, 1.5], [data_tmp[f'no_vac_res_c_{data_idx}_{acc_type}'][0], data_tmp[f'min_c_res_c_{data_idx}_{acc_type}'][0], data_tmp[f'min_d_res_c_{data_idx}_{acc_type}'][0]], 
                 width = 0.9, color = 'none', edgecolor = alloc_colors, linewidth = 1.5, hatch='///', 
                 label = [r'$\tilde{\chi}_\mathrm{c}(\boldsymbol{0})$', r'$\tilde{\chi}_\mathrm{c}(\boldsymbol{\vartheta}_\mathrm{c}^{\mathrm{opt}})$', r'$\tilde{\chi}_\mathrm{c}(\boldsymbol{\vartheta}_\mathrm{d}^{\mathrm{opt}})$'])
        ax.set_ylabel('Final cumulative infections (%)', fontsize = label_fontsize * 0.8)
        ax_d =  ax.twinx()
        ax_d.bar([4.5, 5.5, 6.5], [data_tmp[f'no_vac_res_d_{data_idx}_{acc_type}'][0], data_tmp[f'min_c_res_d_{data_idx}_{acc_type}'][0], data_tmp[f'min_d_res_d_{data_idx}_{acc_type}'][0]], 
                 width = 0.9, color = 'none', edgecolor = alloc_colors, linewidth = 1.5, hatch='...', 
                 label = [r'$\tilde{\chi}_\mathrm{d}(\boldsymbol{0})$', r'$\tilde{\chi}_\mathrm{d}(\boldsymbol{\vartheta}_\mathrm{c}^{\mathrm{opt}})$', r'$\tilde{\chi}_\mathrm{d}(\boldsymbol{\vartheta}_\mathrm{d}^{\mathrm{opt}})$'])
        ax_d.set_ylabel('Final deaths (%)', fontsize = label_fontsize * 0.8)
        if data_idx == 0: 
            ax.set_ylim(0, 0.6)
            ax_d.set_ylim(0, 0.009)
            ax.set_yticks(np.arange(0, 0.61, 0.2), np.arange(0, 61, 20), fontsize = tick_fontsize)
            ax_d.set_yticks(np.arange(0, 0.01, 0.003), np.arange(0, 100, 30) / 100, fontsize = tick_fontsize)
            leg = ax.legend(loc = 'lower right', fontsize = 10, bbox_to_anchor = (0.45, 1.01), labelspacing=0.1, frameon = False)
            for txt in leg.get_texts(): txt.set_math_fontfamily('cm')
            leg = ax_d.legend(loc = 'lower left', fontsize = 10, bbox_to_anchor = (0.55, 1.01), labelspacing=0.1, frameon = False)
            for txt in leg.get_texts(): txt.set_math_fontfamily('cm')
        else: 
            ax.set_ylim(0, 1)
            ax_d.set_ylim(0, 0.03)
            ax.set_yticks(np.arange(0, 1.1, 0.25), np.arange(0, 110, 25), fontsize = tick_fontsize)
            ax_d.set_yticks(np.arange(0, 0.031, 0.01), np.arange(0, 4), fontsize = tick_fontsize)
        ax.set_xticks([0.5, 5.5], ['Cumulative infections', 'Deaths'], fontsize = label_fontsize * 0.8)
    return fig, axes