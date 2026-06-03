# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from matplotlib.lines import Line2D

def draw(anal_data, necs_type = 'high', **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 8
    # grid_attrs = [[{'pos': (0, 0), 'size': (36, 30)}, {'pos': (46, 0), 'size': (36, 30)}, {'pos': (90, 0), 'size': (16, 12)}, {'pos': (90, 18), 'size': (16, 12)}, ]]
    grid_attrs = [[{'pos': (0, 0), 'size': (45, 30)}], [{'pos': (0, 40), 'size': (18, 9)}, {'pos': (27, 40), 'size': (18, 9)}]] # , {'pos': (0, 36), 'size': (16, 12)}, {'pos': (20, 36), 'size': (16, 12)}, 
    if necs_type == 'high': margin_attr = {'top': 3, 'bottom': 8, 'left': 8, 'right': 3}
    elif necs_type == 'low': margin_attr = {'top': 3, 'bottom': 8, 'left': 8, 'right': 3}
    else: pass
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 2
    label_fontsize = 12
    tick_fontsize = 10
    text_fontsize = 12
    ####################################################
    if necs_type == 'high': delay_idx, r0_idx = 0, 5
    elif necs_type == 'low':  delay_idx, r0_idx =0, 11
    else: pass
    time_len = min([len(anal_data['fraction_from_time_with_example'][f'{delay_idx}_{r0_idx}_{sttg}_dd']['time_line']) for sttg in ['no_vac', f'max_{target}', f'min_{target}', 'under_20', '20-49', '20+', '60+', 'all_ages']])
    deep_colors = sns.color_palette('deep')
    # ax = axes[0][0]
    # plt.sca(ax)
    
    # data_tmp = anal_data['fraction_from_time_with_example'][f'{delay_idx}_{r0_idx}_all_ages_dd']
    # mean_prdt = np.mean(data_tmp[f'prdt_{target}'])
    # break_idx = next((i for i, value in enumerate(data_tmp[f'prdt_{target}']) if value < mean_prdt), -1)
    
    
    # data_tmp = anal_data['fraction_from_time_with_example'][f'{delay_idx}_{r0_idx}_no_vac_dd']
    # plt.plot(data_tmp['time_line'][:time_len], data_tmp[f'curve_{target}'][:time_len], color = 'tab:orange', linewidth = 2, label = r'No Vaccination: $\chi_{\mathrm{c}}(t)$')  
    # plt.plot(data_tmp['time_line'][:time_len], data_tmp['curve_s'][:time_len], color = 'tab:green', linewidth = 2, label = r'No Vaccination: $\chi_{\mathrm{s}}(t)$')  
    # plt.plot(data_tmp['time_line'][:break_idx:1000], data_tmp[f'prdt_{target}'][:break_idx:1000], color = 'tab:blue', linestyle = '', marker = 'x', markersize = 8, markeredgewidth = 1.5, label = 'No Vaccination: Predictions') 
    # plt.axhline(data_tmp['curve_c'].to_numpy()[-1], linestyle = ':', color = 'tab:gray', linewidth = 1)
    
    # data_tmp = anal_data['fraction_from_time_with_example'][f'{delay_idx}_{r0_idx}_all_ages_dd']
    # plt.plot(data_tmp['time_line'][:time_len], data_tmp[f'curve_{target}'][:time_len], color = 'tab:orange', linewidth = 2, linestyle = '--', label = r'Vaccination: $\chi_{\mathrm{c}}(t)$')  
    # plt.plot(data_tmp['time_line'][:break_idx], data_tmp['curve_s'][:break_idx], color = 'tab:green', linewidth = 2, linestyle = '--')  
    
    
    # plt.axvline(data_tmp['time_line'].to_numpy()[break_idx], color = 'tab:gray', linestyle = ':', linewidth = 1)
    # plt.plot([data_tmp['time_line'].to_numpy()[break_idx]] * 2, [data_tmp['curve_s'].to_numpy()[break_idx - 1], data_tmp['curve_s'].to_numpy()[break_idx]], color = 'tab:green', linewidth = 2, linestyle = ':')  
    # plt.plot(data_tmp['time_line'][break_idx:time_len], data_tmp['curve_s'][break_idx:time_len], color = 'tab:green', linewidth = 2, linestyle = '--', label = r'Vaccination: $\chi_{\mathrm{s}}(t)$') 
    
    # plt.plot(data_tmp['time_line'][break_idx:time_len:1000], data_tmp[f'prdt_{target}'][break_idx:time_len:1000], color = 'tab:red', linestyle = '', marker = 'x', markersize = 8, markeredgewidth = 1.5, label = 'Vaccination: Predictions') 
    # plt.axhline(data_tmp['curve_c'].to_numpy()[-1], linestyle = '-.', color = 'tab:gray', linewidth = 1)
    # figure_setting.set_xylabel(ax, 'Time (d)', 'Fraction (%)', fontsize = label_fontsize * 1.2, xlabel_coords = -0.08, ylabel_coords = -0.08 if target == 'c' else -0.15)
    # figure_setting.remove_spines(ax, ['top', 'right'])
    # figure_setting.set_spine_linewidth(ax, spine_linewidth)
    # figure_setting.set_tick_fontsize(ax, tick_fontsize)
    # ax.spines['bottom'].set_bounds(0, 120)
    # ax.spines['left'].set_bounds(0, 1)
    # ax.set_yticks(np.arange(0, 1.01, 0.25), np.arange(0, 101, 25))
    # plt.legend(fontsize = 8.5)
    
    
    ax = axes[0][0]
    plt.sca(ax)
    
    colors = {'no_vac': 'black', f'min_{target}': '#d43732', f'max_{target}': '#2b69b7', 'under_20': deep_colors[1], '20-49': deep_colors[2], '20+': deep_colors[4], '60+': deep_colors[6], 'all_ages': deep_colors[7]}
    linestyles = {'no_vac': (0, (2, 1)), f'min_{target}': '-', f'max_{target}': (0, (8, 0.8)), 'under_20': (0, (1, 1)), '20-49': (0, (3, 1)), '20+': (0, (3, 1, 1, 1)), '60+': (0, (5, 1, 2.5, 1)), 'all_ages': (0, (5, 1, 1, 1))}
    labels = {'no_vac': 'No vaccination', f'min_{target}': 'Optimal allocation', f'max_{target}': 'Burden-maximizing allocation', 'under_20': 'Under 20', '20-49': '20–49', '20+': '20+', '60+': '60+', 'all_ages': 'All Ages'}
    handles = []
    for idx, sttg in enumerate(['no_vac', f'min_{target}', f'max_{target}', 'under_20', '20-49', '20+', '60+', 'all_ages']):
        # if idx == 3:
        #     handles.append(Line2D([], [], linestyle='none', label='Heuristic rules'))
        data_tmp = anal_data['fraction_from_time_with_example'][f'{delay_idx}_{r0_idx}_{sttg}_dd']
        handles.append(ax.plot(data_tmp['time_line'][:time_len], data_tmp[f'curve_{target}'][:time_len], color = colors[sttg], linestyle = linestyles[sttg], label = labels[sttg], linewidth = 1.5)[0])
    
    figure_setting.set_xylabel(ax, 'Time (d)', 'Cumulative infections (%)', fontsize = label_fontsize, xlabel_coords = -0.11, ylabel_coords = -0.11)
    figure_setting.remove_spines(ax, ['top', 'right'])
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    if necs_type == 'high': 
        plt.xlim(0, 100)
        ax.spines['bottom'].set_bounds(0, 100)
        ax.spines['left'].set_bounds(0, 1)
        ax.set_yticks(np.arange(0, 1.01, 0.25), np.arange(0, 101, 25))
        ax.text(0.5, 1, 'High necessity', ha='center', va='bottom', fontsize= text_fontsize, transform=ax.transAxes)
    elif necs_type == 'low': 
        plt.xlim(0, 40)
        ax.spines['bottom'].set_bounds(0, 40)
        ax.spines['left'].set_bounds(0, 1)
        ax.set_yticks(np.arange(0, 1.01, 0.25), np.arange(0, 101, 25))
        leg1 = ax.legend(handles = handles[:3], loc = 'upper left', fontsize = 7, handlelength=3.45, bbox_to_anchor=(0.01, 1), frameon=False, ncol = 1)
        ax.add_artist(leg1)
        ax.legend(handles = handles[3:], loc = 'upper left', fontsize = 7, handlelength=3.45, bbox_to_anchor=(0.01, 0.8), frameon=False, ncol = 1, title='Heuristic rules', title_fontsize=8)
        ax.text(0.5, 1, 'Low necessity', ha='center', va='bottom', fontsize= text_fontsize, transform=ax.transAxes)
    else: pass
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')

    # if necs_type == 'high': ax_inset = ax.inset_axes([0.11, 0.67, 0.4, 0.3])
    # elif necs_type == 'low': ax_inset = ax.inset_axes([0.11, 0.67, 0.4, 0.3])
    # else: pass
    
    sttg_names = ['Burden-maximizing', 'Optimal']
    for i, sttg in enumerate(['max', 'min']):
        ax_inset = axes[1][i]
        ax_inset.bar(np.arange(16), anal_data['alloc_from_age_with_example']['alloc'][f"{delay_idx}_{r0_idx}_{sttg}_{target}"] * 100, 
                color = ['#2b69b7', '#d43732'][i], width = 0.7, edgecolor='black', linewidth = 0.5)
        figure_setting.set_xylabel(ax_inset, 'Age group', 'Allocation (%)', fontsize = label_fontsize * 0.75, xlabel_coords = -0.5, ylabel_coords = -0.11)
        figure_setting.set_spine_linewidth(ax_inset, spine_linewidth * 0.5)
        figure_setting.set_tick_fontsize(ax_inset, tick_fontsize * 0.65)
        ax_inset.tick_params(axis='x', rotation = 90, labelsize = label_fontsize * 0.4)
        ax_inset.set_xlim(-1, 16)
        ax_inset.spines['bottom'].set_bounds(0, 15)
        ax_inset.set_xticks(np.arange(16), age_groups, rotation = 90, fontsize = 5)
        ax_inset.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4), fontsize = 5)
        ax_inset.set_ylim(0, 8)
        ax_inset.tick_params(axis='x', which='major', pad=1)
        ax_inset.text(0.02, 0.99, f'{sttg_names[i]} allocation', fontsize = 7, ha = 'left', va = 'top', transform=ax_inset.transAxes, color = ['#2b69b7', '#d43732'][i])
        figure_setting.remove_spines(ax_inset, ['top', 'right'])
    
    
    
    # spine_linewidth = 1.2
    # label_fontsize = 10
    # tick_fontsize = 10
    # for idx, optm_dir in enumerate(['min', 'max']):
    #     ax = axes[0][1 + idx]
    #     plt.sca(ax)
    #     ax.bar(np.arange(16), anal_data['alloc_from_age_with_example']['alloc'][f"{delay_idx}_{r0_idx}_{optm_dir}_{target}"] * 100, 
    #             color = '#C54E53' if optm_dir == 'min' else '#4C72B1', width = 0.8, edgecolor='black', linewidth = 0.5)
    #     figure_setting.set_xylabel(ax, 'Age group', '' if idx != 0 else 'Allocation (%)', fontsize = label_fontsize, xlabel_coords = -0.27, ylabel_coords = -0.1)
    #     figure_setting.set_spine_linewidth(ax, spine_linewidth)
    #     figure_setting.set_tick_fontsize(ax, tick_fontsize)
    #     plt.xticks(rotation = 90, fontsize = label_fontsize * 0.6)
    #     ax.set_xlim(-1, 16)
    #     ax.spines['bottom'].set_bounds(0, 15)
    #     ax.set_xticks(np.arange(16), age_groups, rotation = 90)
    #     ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
    #     ax.set_ylim(0, 8)
    #     ax.tick_params(axis='x', which='major', pad=1)
    #     ax.text(0.02, 0.99, 'Most effective allocation' if optm_dir == 'min' else 'Least effective allocation', fontsize = 10, ha = 'left', va = 'top', transform=ax.transAxes, color = '#C54E53' if optm_dir == 'min' else '#4C72B1')
    #     figure_setting.remove_spines(ax, ['top', 'right'])
    return fig, axes