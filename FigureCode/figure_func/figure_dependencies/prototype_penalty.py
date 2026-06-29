# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:07:06 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import seaborn as sns
from Dependencies.CodeDependencies import basic_params
import itertools
import matplotlib.lines as mlines



def crossings_on_row(X, Y, Z, y0, level=0.0):
    x = X[0]
    j = np.argmin(np.abs(Y[:,0]-y0))
    j2 = min(j+1, Y.shape[0]-1)
    y1, y2 = Y[j,0], Y[j2,0]
    if y1 == y2:
        zrow = Z[j]
    else:
        w = (y0 - y1)/(y2 - y1)
        zrow = (1-w)*Z[j] + w*Z[j2]
    # 一维线性插值过零
    s = zrow - level
    xs = []
    for k in range(len(x)-1):
        if s[k]*s[k+1] < 0:
            t = s[k]/(s[k]-s[k+1])
            xs.append(x[k] + t*(x[k+1]-x[k]))
    return np.array(xs)




def draw(anal_data, expr_name, expr_param, anal_name = 'necs_from_r0_factor', **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1
    label_fontsize = 8
    tick_fontsize = 7
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 70)}], ]
                  # [{'pos': (20, 2), 'size': (15, 12)}, {'pos': (20, 20), 'size': (15, 12)}, {'pos': (20, 38), 'size': (15, 12)}, {'pos': (20, 56), 'size': (15, 12)}]]
    margin_attr = {'top': 1, 'bottom': 5, 'left': 8, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    x = np.exp(np.arange(40) * 3 / 40)
    task_name = f'{expr_name}_({expr_param})'
    if anal_name != 'necs_from_r0_fatality_by_contact':
        pre_sheet_name = f"{task_name}-{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"
        zc_min, zc_anti_min, zc_no_vac = anal_data[anal_name][f'{pre_sheet_name}_min'], anal_data[anal_name][f'{pre_sheet_name}_anti_min'], anal_data[anal_name][f'{pre_sheet_name}_no_vac']
        zc = (zc_anti_min - zc_min) / (zc_no_vac - zc_min)
        pre_sheet_name = f"{task_name}-{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"
        zd_min, zd_anti_min, zd_no_vac = anal_data[anal_name][f'{pre_sheet_name}_min'], anal_data[anal_name][f'{pre_sheet_name}_anti_min'], anal_data[anal_name][f'{pre_sheet_name}_no_vac']
        zd = (zd_anti_min - zd_min) / (zd_no_vac - zd_min)
    else:
        pre_sheet_name = f"{task_name}-{basic_params.country_abbr[country]}_w_{acc_type}{'_dur' if dur else ''}"
        zc_min, zc_anti_min, zc_no_vac = anal_data[anal_name][f'{pre_sheet_name}_min'], anal_data[anal_name][f'{pre_sheet_name}_anti_min'], anal_data[anal_name][f'{pre_sheet_name}_no_vac']
        zc = (zc_anti_min - zc_min) / (zc_no_vac - zc_min)
        pre_sheet_name = f"{task_name}-{basic_params.country_abbr[country]}_x_{acc_type}{'_dur' if dur else ''}"
        zd_min, zd_anti_min, zd_no_vac = anal_data[anal_name][f'{pre_sheet_name}_min'], anal_data[anal_name][f'{pre_sheet_name}_anti_min'], anal_data[anal_name][f'{pre_sheet_name}_no_vac']
        zd = (zd_anti_min - zd_min) / (zd_no_vac - zd_min)
    ax = axes[0][0]
    plt.sca(ax)
    overlap = 0.75
    deep_colors = sns.color_palette('deep')
    edge_width = 1
    for idx in range(40):
        y = zc[idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = deep_colors[2], alpha = 0.65, linewidth = 0, label = r'$\Phi_{\mathrm{c}}^{(\mathrm{d})}$' if idx == 0 else None)
        plt.plot(x, y + idx * overlap, color = deep_colors[2], zorder = 40 - idx + 1, linewidth = edge_width)
        plt.plot(x, np.ones(40) * (idx * overlap), color = 'tab:gray', zorder = 40 - idx + 1, linewidth = edge_width)
        y = zd[idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = deep_colors[1], alpha = 0.65, linewidth = 0, label = r'$\Phi_{\mathrm{d}}^{(\mathrm{c})}$' if idx==0 else None)
        plt.plot(x, y + idx * overlap, color = deep_colors[1], zorder = 40 - idx + 1, linewidth = edge_width)
        plt.plot(x, np.ones(40) * (idx * overlap), color = 'tab:gray', zorder = 40 - idx + 1, linewidth = edge_width)
        
        if expr_param == 'delay':
            param_text = f'$\\delta = {idx / 2}$'
        elif expr_name in ['necs_from_time_course', 'necs_from_time_course_fixd']:
            param_text = f'$\\mathcal{{D}}_{{\\mathrm{{roll}}}} = {idx + 2}$'
        else:
            param_text = f'$\\gamma = {idx} / 39$'
        ax.text(0.9, idx * overlap, param_text, fontsize = 7, color = 'black', horizontalalignment='right', verticalalignment='bottom', transform= ax.transData)
    
    z = []
    corr_anal_name = f"corr_{anal_name.partition('_')[2]}"
    for param_idx in range(40):
        sheet_name = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
        z.append(anal_data[corr_anal_name][sheet_name]['alloc_corr'])
    X, Y = np.meshgrid(x, np.arange(40) * overlap)
    
    plt.contour(X, Y, z, levels=[0], colors='tab:gray', linestyles = '--', linewidths = 1.5, zorder = 100)
    contour_proxy = mlines.Line2D([], [],color='tab:gray',linestyle='--',linewidth=1.5,label=r'$\theta = 0$')
    handles, labels = ax.get_legend_handles_labels()
    handles.append(contour_proxy)
    labels.append(r'$\theta = 0$')
    plt.xscale('log')   
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin = -0.1)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    figure_setting.set_xylabel(ax, r'$R_0$', None, fontsize = 12, xlabel_coords = -0.03 , ylabel_coords = -0.22)
    if expr_param == 'delay' and anal_name != 'necs_from_r0_factor_by_eta':
        ax.legend(handles=handles,labels=labels,loc='upper center',fontsize=8,bbox_to_anchor=(0.4, 1.01),ncol=3)
    elif anal_name == 'necs_from_r0_fatality_by_contact':
        ax.legend(loc='upper center',fontsize=8,bbox_to_anchor=(0.4, 1.01),ncol=2)
    else: pass
    
    # expr_params = {'param': ['delay_0', 'delay_13', 'delay_26', 'delay_39'], 'fatality': ['coef_beta_1_0', 'coef_beta_1_13', 'coef_beta_1_26', 'coef_beta_1_39']}
    # x = np.array([np.exp((r0_head + r0_tail / 40) * 0.075) for  r0_head, r0_tail in itertools.product(range(40), range(40))])
    # for ax_idx, ax in enumerate(axes[1]):
    #     plt.sca(ax)
    #     task_name = f'necs_line_from_{expr_name_end}_({expr_params[expr_name_end][ax_idx]})'
    #     sheet_name = f'{task_name}_{basic_params.country_abbr[country]}'
    #     plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['alloc_corr'], linestyle = '', marker = 'o', markerfacecolor = deep_colors[1], markeredgecolor = 'white', markersize = 1.5, markeredgewidth = 0)
    #     plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
    #     figure_setting.set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize, xlabel_coords = -0.18, ylabel_coords = -0.22)
    #     figure_setting.set_spine_linewidth(ax, spine_linewidth)
    #     figure_setting.set_tick_fontsize(ax, tick_fontsize)
    #     plt.xscale('log')
    
    
    
    
    
    # for ax_idx, ax in enumerate(axes[0]):
    #     plt.sca(ax)
    #     plt.plot(x, zc[ax_idx * 13], color = 'tab:green')
    #     plt.fill_between(x, 0, zc[ax_idx * 13], color = 'tab:green', alpha = 0.5)
    #     plt.plot(x, zd[ax_idx * 13], color = 'tab:orange')
    #     plt.fill_between(x, 0, zd[ax_idx * 13], color = 'tab:orange', alpha = 0.5)
    #     ax.set_xscale('log')
    #     set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    #     set_spine_linewidth(ax, spine_linewidth * unit)
    #     set_tick_fontsize(ax, tick_fontsize * unit)
    return fig, axes
