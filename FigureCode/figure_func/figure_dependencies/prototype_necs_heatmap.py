# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params, func
from . import figure_setting
import matplotlib.patches as patches
from matplotlib.transforms import blended_transform_factory
from scipy.ndimage import minimum_filter


def draw(anal_data, expr_name, expr_param, anal_name = 'necs_from_r0_factor', **kwargs):
    data_type = kwargs.pop('data_type', 'necs')
    corr_data_type = kwargs.pop('corr_data_type', 'corr')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    corr_contour = kwargs.pop('corr_contour', True)
    ####################################################
    scale_prop = 10
    if expr_param == 'delay': grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (36, 0), 'size': (2, 30)}]]
    else: grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 6, 'bottom': 5, 'left': 7, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 15
    tick_fontsize = 9
    #####################################################
    task_name = f'{expr_name}_({expr_param})'
    sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
    if target == 'x': target_sub = 'd'
    else: target_sub = target
    target_name = {'c': 'cumulative infections', 'd': 'deaths'}[target_sub]
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    if data_type == 'rnecs':
        res = ((anal_data[anal_name][f'{sheet_name_preppend}_max'] - anal_data[anal_name][f'{sheet_name_preppend}_min']) / (anal_data[anal_name][f'{sheet_name_preppend}_no_vac'] - anal_data[anal_name][f'{sheet_name_preppend}_min'])).T
    elif data_type == 'vac_opt_necs':
        res = (anal_data[anal_name][f'{sheet_name_preppend}_no_vac'] - anal_data[anal_name][f'{sheet_name_preppend}_min']).T * 100
        if target == 'c': title = f'Vaccination necessity for\n'fr'{target_name} ($\mathcal{{M}}^{{\mathrm{{opt}}}}_{{\mathrm{{{target_sub}}}}}$)'
        else: title = f'Vaccination necessity\n'fr'for {target_name} ($\mathcal{{M}}^{{\mathrm{{opt}}}}_{{\mathrm{{{target_sub}}}}}$)'
        zlabel = fr'$\mathcal{{M}}^{{\mathrm{{opt}}}}_{{\mathrm{{{target_sub}}}}}$ (%)'
        cmap_color = 'Reds'
    elif data_type == 'vac_max_necs':
        res = (anal_data[anal_name][f'{sheet_name_preppend}_no_vac'] - anal_data[anal_name][f'{sheet_name_preppend}_max']).T * 100
        if target == 'c': title = f'Vaccination necessity for\n'fr'{target_name} ($\mathcal{{M}}^{{\mathrm{{max}}}}_{{\mathrm{{{target_sub}}}}}$)'
        else: title = f'Vaccination necessity\n'fr'for {target_name} ($\mathcal{{M}}^{{\mathrm{{max}}}}_{{\mathrm{{{target_sub}}}}}$)'
        zlabel = fr'$\mathcal{{M}}^{{\mathrm{{max}}}}_{{\mathrm{{{target_sub}}}}}$ (%)'
        cmap_color = 'Blues'
    elif data_type == 'vac_pop_necs':
        res = (anal_data[anal_name][f'{sheet_name_preppend}_no_vac'] - anal_data[anal_name][f'{sheet_name_preppend}_rand']).T * 100
        if target == 'c': title = f'Vaccination necessity for\n'fr'{target_name} ($\mathcal{{M}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$)'
        else: title = f'Vaccination necessity\n'fr'for {target_name} ($\mathcal{{M}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$)'
        zlabel = fr'$\mathcal{{M}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$ (%)'
        cmap_color = 'Oranges'
    elif data_type == 'pop_necs':
        res = (anal_data[anal_name][f'{sheet_name_preppend}_rand'] - anal_data[anal_name][f'{sheet_name_preppend}_min']).T * 100
        if target == 'c': title = f'Epidemiological necessity for\n'fr'{target_name} ($\mathcal{{N}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$)'
        else: title = f'Epidemiological necessity\n'fr'for{target_name} ($\mathcal{{N}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$)'
        zlabel = fr'$\mathcal{{N}}^{{\mathrm{{pop}}}}_{{\mathrm{{{target_sub}}}}}$ (%)'
        cmap_color = 'Oranges'
    else:
        sheet_name = f'{sheet_name_preppend}_{data_type}'
        res = anal_data[anal_name][sheet_name].T * 100
        if target == 'c': title = f'Epidemiological necessity for\n'fr'{target_name} ($\mathcal{{N}}_{{\mathrm{{{target_sub}}}}}$)'
        else: title = f'Epidemiological necessity\n'fr'for {target_name} ($\mathcal{{N}}_{{\mathrm{{{target_sub}}}}}$)'
        zlabel = fr'$\mathcal{{N}}_{{\mathrm{{{target_sub}}}}}$ (%)'
        cmap_color = 'Blues'
        if dur: 
            if target == 'c': title = f'Rollout stress-test gap for\n'fr'{target_name} ($\mathcal{{G}}_{{\mathrm{{{target_sub}}}}}$)'
            else: title = f'Rollout stress-test gap\n'fr'for {target_name} ($\mathcal{{G}}_{{\mathrm{{{target_sub}}}}}$)'
            zlabel = fr'$\mathcal{{G}}_{{\mathrm{{{target_sub}}}}}$ (%)'
            cmap_color = 'Reds'
    c = ax.pcolormesh(x, y, res, cmap = cmap_color)
 
    ax.set_xscale('log')
    if corr_contour:
        task_name = f'{expr_name}_({expr_param})'
        corr_anal_name = f"corr_{anal_name.partition('_')[2]}"
        corr_z = []
        for param_idx in range(40):
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            if corr_data_type == 'corr': corr_z.append((np.arccos(anal_data[corr_anal_name][sheet_name]['optimal_indx']) - (np.arccos(anal_data[corr_anal_name][sheet_name]['optimal_dirx']))) / np.arccos(anal_data[corr_anal_name][sheet_name]['effect_corrx']))  
            elif corr_data_type == 'corr_ind': corr_z.append(anal_data[corr_anal_name][sheet_name]['optimal_ind'])
            elif corr_data_type == 'corr_dir': corr_z.append(anal_data[corr_anal_name][sheet_name]['optimal_dir'])
            else: pass
        X, Y = np.meshgrid(x, y)
        ax.clabel(plt.contour(X, Y, corr_z, levels=[0], colors='k', linestyles = 'solid', linewidths = 1), fontsize = 10, fmt = lambda x: rf'$\xi = {0 if x == 0 else np.round(x, 1)}$')
    
    
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
        y_label = {'delay': r'$\delta$ (days)', 'vac_eff': r'$\eta$ (%)', 'vac_avail': r'$B$ (%)', 'c_perct': r'$\mathcal{P}_{\mathrm{vac}}$ (%)', 'vac_dur': r'$\mathcal{D}_{\mathrm{roll}}$'}[expr_param]
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
    plt.title(title, fontsize = 15, pad=8,linespacing=1.15)
    figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.ax.set_title(zlabel, pad = 6, fontsize = 12)
    cbar.ax.tick_params(labelsize = 6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    if expr_param == 'delay':
        Tg = 5.05
        secay = ax.secondary_yaxis('right', functions=(lambda d: d / Tg, lambda d_star: d_star * Tg))
        secay.set_ylabel(r'$\delta^*=\delta/T_g$ (generations)', fontsize = 12)
        secay.set_yticks(np.arange(4) * 2, np.arange(4))
    return fig, axes




    # if expr_name == 'necs_from_param' and expr_param == 'delay' and target == 'c':
    #     center_x, center_y, width, height = 0.5, 10, 1.02, 1.2
    #     ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:orange', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = 0.5, 0, 1.02, 1.2
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:purple', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = np.exp(8 * 0.075), 0.5, np.exp((8 - 0.6) * 0.075) - np.exp((8 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:red', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
        # center_x, center_y, width, height = np.exp(24 * 0.075), 0.5, np.exp((24 - 0.6) * 0.075) - np.exp((24 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:blue', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
