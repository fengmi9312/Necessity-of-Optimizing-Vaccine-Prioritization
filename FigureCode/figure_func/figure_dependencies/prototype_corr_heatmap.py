# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting
import seaborn as sns


def draw(anal_data, expr_name, expr_param, anal_name = 'corr_from_r0_factor', **kwargs):
    data_type = kwargs.pop('data_type', 'corr')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    corr_contour = kwargs.pop('corr_contour', True)
    ####################################################
    scale_prop = 10
    if expr_param == 'delay': grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (36, 0), 'size': (2, 30)}]]
    else: grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 6}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 15
    tick_fontsize = 9
    #####################################################
    task_name = f'{expr_name}_({expr_param})'
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        if data_type == 'corr': z.append((np.arccos(anal_data[anal_name][sheet_name]['optimal_indx']) - (np.arccos(anal_data[anal_name][sheet_name]['optimal_dirx']))) / np.arccos(anal_data[anal_name][sheet_name]['effect_corrx']))
        elif data_type == 'corr_ind': z.append(1 - anal_data[anal_name][sheet_name]['optimal_indx'])
        elif data_type == 'corr_dir': z.append(1 - anal_data[anal_name][sheet_name]['optimal_dirx'])
        else: pass
    c = ax.pcolormesh(x, y, z, cmap = sns.color_palette("coolwarm", as_cmap=True))
    ax.set_xscale('log')
    if target == 'x': target_sub = 'd'
    else: target_sub = target
    if anal_name == 'corr_from_r0_fatality_by_contact': plt.title(rf'Indirect-deviation index ($\xi_{{\mathrm{{{target_sub}}}}}^{{\ast, \mathrm{{opt}}}}$)', fontsize = 15, pad=8,linespacing=1.1)
    else: plt.title(rf'Protection-orientation index ($\xi_{{\mathrm{{{target_sub}}}}}^{{\mathrm{{opt}}}}$)', fontsize = 15, pad=8,linespacing=1.1)
    if corr_contour:
        X, Y = np.meshgrid(x, y)
        ax.clabel(plt.contour(X, Y, z, levels=[0], colors='k', linestyles = 'solid', linewidths = 1), fontsize = 10, fmt = lambda x: rf'$\xi = {0 if x == 0 else np.round(x, 1)}$')
    
    
    param_list = {'delay': np.arange(40) / 2, 'vac_eff': np.arange(22, 101, 2), 'vac_avail': np.arange(12, 91, 2), 'c_perct': np.arange(215, 801, 15) / 10, 'vac_dur': np.arange(1, 41), 'time_course': np.arange(2, 42)}
    if expr_name == 'necs_from_fatality':
        y_label = r'$\gamma$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name == 'necs_from_fatality_by_contact':
        y_label = r'$\gamma^*$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name == 'necs_from_contact':
        y_label = r'$\varrho$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name in ['necs_from_param', 'necs_from_param_by_eta']: 
        y_label = {'delay': r'$\delta$ (days)', 'vac_eff': r'$\eta$ (%)', 'vac_avail': r'$B$ (%)', 'c_perct': r'$\mathcal{P}_{\mathrm{vac}}$ (%)', 'vac_dur': r'\mathcal{D}_{\mathrm{roll}}'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
    elif expr_name == 'necs_from_time_course_fixd_with_vac_avail': 
        y_label = r'$B$ (%)'
        ax.set_yticks(np.arange(40)[0::13], param_list['vac_avail'][0::13])
    elif expr_name in ['necs_from_time_course', 'necs_from_time_course_fixd']:
        y_label = r'$\mathcal{D}_{\mathrm{roll}}$'
        ax.set_yticks(np.arange(40)[0::13], param_list['time_course'][0::13])
    elif expr_name == 'necs_from_populations':
        y_label = r'Age-profile center, $o_{\rho}$'
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name  == 'necs_from_time_course_fixd_by_fatality':
        y_label = r'$\gamma$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    else: pass
    figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    if anal_name == 'corr_from_r0_fatality_by_contact': cbar.ax.set_title(rf'$\xi_{{\mathrm{{{target_sub}}}}}^{{\ast,\mathrm{{opt}}}}$', pad = 6, fontsize = 12)
    else: cbar.ax.set_title(rf'$\xi_{{\mathrm{{{target_sub}}}}}^{{\mathrm{{opt}}}}$', pad = 6, fontsize = 12)
    cbar.ax.tick_params(labelsize = 6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    if expr_param == 'delay':
        Tg = 5.05
        secay = ax.secondary_yaxis('right', functions=(lambda d: d / Tg, lambda d_star: d_star * Tg))
        secay.set_ylabel(r'$\delta^*=\delta/T_g$ (generations)', fontsize = 12)
        secay.set_yticks(np.arange(4) * 2, np.arange(4))
    
    return fig, axes


# if expr_name == 'necs_from_param' and expr_param == 'delay':
#     center_x, center_y, width, height = 0.5, 8, 1.02, 1.2
#     ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:orange', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
    # center_x, center_y, width, height = 0.5, 0, 1.02, 1.2
    # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:purple', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
    # center_x, center_y, width, height = np.exp(8 * 0.075), 0.5, np.exp((8 - 0.6) * 0.075) - np.exp((8 + 0.6) * 0.075), 1.02
    # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:red', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
    # center_x, center_y, width, height = np.exp(24 * 0.075), 0.5, np.exp((24 - 0.6) * 0.075) - np.exp((24 + 0.6) * 0.075), 1.02
    # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:blue', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
