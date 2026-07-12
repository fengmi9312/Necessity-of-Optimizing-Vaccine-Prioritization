# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting

RED = '#D43732'
BLUE = '#2B69B7'
GREEN = '#2E8E2F'

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    delay_idx = 0
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 8)}, {'pos': (28, 0), 'size': (20, 8)}, {'pos': (56, 0), 'size': (20, 8)}], 
                  [{'pos': (0, 13), 'size': (20, 8)}, {'pos': (28, 13), 'size': (20, 8)}, {'pos': (56, 13), 'size': (20, 8)}],
                  [{'pos': (0, 26), 'size': (20, 8)}, {'pos': (28, 26), 'size': (20, 8)}, {'pos': (56, 26), 'size': (20, 8)}],]
    margin_attr = {'top': 4, 'bottom': 7, 'left': 6, 'right': 2}
    removed_labels = {'x': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], 'y': [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)], 'xtick': [], 'ytick': []}
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
    # x_upper = [[100, 40, 24]]
    # y_upper = [[100, 100, 100]]
    # sttgs = ['no_vac', f'max_{target}', f'min_{target}']
    # colors = {'no_vac': 'black', f'max_{target}': '#d43732', f'min_{target}': '#2b69b7'}
    # linestyles = {'no_vac': (0, (2, 1)), f'min_{target}': '-', f'max_{target}': (0, (8, 0.8))}
    # labels = {'no_vac': 'No vaccination', f'min_{target}': 'Optimal allocation', f'max_{target}': 'Worst allocation'}
    # for ax_idx, ax in enumerate(axes[0]):
    #     plt.sca(ax)
    #     len_limit = min([len(anal_data['fraction_from_time_with_example'][f"{delay_idx}_{ax_idx + 7}_{sttg}_{acc_type}{'_dur' if dur else ''}"]['time_line']) for sttg in sttgs])
    #     for sttg in sttgs:
    #         sheet_name = f"{delay_idx}_{ax_idx + 7}_{sttg}_{acc_type}{'_dur' if dur else ''}"
    #         plt.plot(anal_data['fraction_from_time_with_example'][sheet_name]['time_line'][:len_limit], 
    #                  anal_data['fraction_from_time_with_example'][sheet_name][f'curve_{target}'][:len_limit] * 100, linewidth = 2, color = colors[sttg], linestyle = linestyles[sttg], label = labels[sttg])
        
        
    #     figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative infections (%)', fontsize = label_fontsize, xlabel_coords = -0.24, ylabel_coords = -0.24)
    #     figure_setting.set_spine_linewidth(ax, spine_linewidth)
    #     figure_setting.set_tick_fontsize(ax, tick_fontsize)
    #     plt.ylim(-5, 100)
    #     ax.set_yticks(np.arange(0, 101, 50), np.arange(0, 101, 50))
    #     plt.xlim(0, x_upper[delay_idx][ax_idx])
    #     plt.ylim(- y_upper[delay_idx][ax_idx] / 20, y_upper[delay_idx][ax_idx] * 1.05)
    #     ax.set_xticks(np.arange(0, x_upper[delay_idx][ax_idx] + 1, x_upper[delay_idx][ax_idx] // 2), np.arange(0, x_upper[delay_idx][ax_idx] + 1, x_upper[delay_idx][ax_idx] // 2))
    #     ax.spines['left'].set_bounds(0, y_upper[delay_idx][ax_idx])
    #     ax.spines['left'].set_position(('axes', -0.03))
    #     figure_setting.remove_spines(ax, ['top', 'right'])
    #     plt.title(f'$R_0 = {[1.8, 5.5, 16][ax_idx]}$', fontsize = label_fontsize, math_fontfamily = 'cm')
    #     if ax_idx == 0: plt.legend(loc = 'upper left', fontsize = 7.5, handlelength=4.5)
    
    spine_linewidth = 1.2
    label_fontsize = 9
    tick_fontsize = 9.5
    for idx, optm_dir in enumerate(['max', 'min', 'sensitivity']):
        for ax_idx, ax in enumerate(axes[idx]):
            plt.sca(ax)
            if idx <= 1:
                ax.bar(np.arange(16), anal_data['alloc_from_age_with_example']['alloc'][f"{delay_idx}_{ax_idx + 7}_{optm_dir}_{target}"] * 100, 
                       color = RED if optm_dir == 'min' else BLUE, width = 0.7, edgecolor='black', linewidth = 0.5)
                figure_setting.set_xylabel(ax, 'Age group', ['Burden-maximizing''\n''allocation (%)', 'Optimal allocation (%)'][idx], fontsize = label_fontsize, xlabel_coords = -0.5, ylabel_coords = -0.1)
                ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
                ax.set_ylim(0, 8)
            else:
                ax.bar(np.arange(16), -anal_data['group_effect_from_r0_factor']['example'][['low', 'mid', 'high'][ax_idx]], 
                       color = GREEN, width = 0.7, edgecolor='black', linewidth = 0.5)
                figure_setting.set_xylabel(ax, 'Age group', 'Marginal vaccination''\n''benefit (relative)', fontsize = label_fontsize, xlabel_coords = -0.5, ylabel_coords = -0.1)
                ax.set_yticks(np.arange(0, 3, 1), np.arange(0, 3, 1))
                ax.set_ylim(0, 2)
            if idx == 0:
                plt.title([r'Low $R_0$ (indirect protection)''\n'r'$R_0=1.8$', r'Balanced''\n'r'$R_0=5.5$', r'High $R_0$ (direct protection)''\n'r'$R_0=16$'][ax_idx], fontsize = label_fontsize, math_fontfamily = 'cm')
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, tick_fontsize)
            plt.xticks(rotation = 90, fontsize = tick_fontsize * 0.6)
            ax.set_xlim(-1, 16)
            ax.spines['bottom'].set_bounds(0, 15)
            ax.set_xticks(np.arange(16), age_groups, rotation = 90)
            #ax.spines['left'].set_position(('outward', 1))
            ax.tick_params(axis='x', which='major', pad=1)
            figure_setting.remove_spines(ax, ['top', 'right'])
    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes