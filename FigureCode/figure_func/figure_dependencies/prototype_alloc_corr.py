# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:47:14 2025

@author: MIFENG
"""

import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting
import seaborn as sns
import matplotlib.colors as mcolors
from contourpy import contour_generator

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

def draw(anal_data, expr_name, expr_param, anal_name = 'corr_from_r0_factor', **kwargs):
    country = kwargs.pop('country', 'United States')
    ####################################################
    scale_prop = 8
    if anal_name == 'corr_from_r0_factor':
        if expr_param == 'delay':
            grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (36, 0), 'size': (2, 30)}], [{'pos': (52, 0), 'size': (18, 12)}, {'pos': (52, 18), 'size': (18, 12)}]]
        else:
            grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}], [{'pos': (48, 0), 'size': (18, 12)}, {'pos': (48, 18), 'size': (18, 12)}]]
    else:
        if expr_param == 'delay':
            grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (36, 0), 'size': (2, 30)}]]
        else: 
            grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    if expr_param == 'delay' and anal_name == 'corr_from_r0_factor': margin_attr = {'top': 4, 'bottom': 6, 'left': 7, 'right': 15}
    else: margin_attr = {'top': 4, 'bottom': 6, 'left': 7, 'right': 4}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9
    #####################################################
    
    deep_colors = sns.color_palette('deep')
    obj_marker = {'c':'x', 'd': 'o'}
    obj_color = {'c': deep_colors[2], 'd': deep_colors[1]}
    param_idx_list = [30, 15] 
    
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    task_name = f'{expr_name}_({expr_param})'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
        z.append(anal_data[anal_name][sheet_name]['alloc_corr'])
    original_cmap = sns.color_palette("Blues", as_cmap=True)
    color_start, color_end = 0, 0.6
    colors = original_cmap(np.linspace(color_start, color_end, 256))
    c = ax.pcolormesh(x, y, np.array(z) , cmap = mcolors.ListedColormap(colors))
    ax.set_xscale('log')
    
    zero_crossing_poi = {}
    targets = ['c', 'd'] if anal_name != 'corr_from_r0_fatality_by_contact' else  ['w', 'x']
    target_text = {'c': 'c', 'd': 'd', 'w': 'c', 'x': 'd'}
    if anal_name != 'corr_from_r0_fatality_by_contact':
        for target in targets:
            xx = np.exp(np.arange(40) * 3 / 40)
            yy = np.arange(40)
            task_name = f'{expr_name}_({expr_param})'
            corr_anal_name = f"corr_{anal_name.partition('_')[2]}"
            zz = []
            for param_idx in range(40):
                sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
                zz.append((np.arccos(anal_data[corr_anal_name][sheet_name]['optimal_dirx']) - np.arccos(anal_data[corr_anal_name][sheet_name]['optimal_indx'])) / np.arccos(anal_data[corr_anal_name][sheet_name]['effect_corrx']))
            cg = contour_generator(xx, yy, zz)
            cs_data = cg.lines(level = 0)
            for cs_idx, cs_item in enumerate(cs_data): 
                cs_keep = cs_item[cs_item[:, 0] >= 1.05]
                plt.plot(cs_keep[:, 0], cs_keep[:, 1], marker = obj_marker[target_text[target]], linestyle = '', markevery = 2, color = obj_color[target_text[target]], markerfacecolor = 'none',  
                         markeredgewidth = 1.2, label = rf'$\xi_{{\mathrm{{{target_text[target]}}}}} = 0$' if cs_idx == 0 else None)
                
            XX, YY = np.meshgrid(xx, yy)
            
            if anal_name == 'corr_from_r0_factor':
                zero_crossing_poi[target] = np.array([crossings_on_row(XX, YY, zz, param_idx) for param_idx in param_idx_list])
                for i in range(len(zero_crossing_poi[target])): zero_crossing_poi[target][i] = zero_crossing_poi[target][i][zero_crossing_poi[target][i] > 1.05]
    
    X, Y = np.meshgrid(x, y)
    cs = plt.contour(X, Y, z, levels=[0], colors='black', linestyles = 'solid', linewidths = 1.5, zorder = 10)
    clabel = ax.clabel(cs, fontsize = 12, fmt = lambda x: rf'$\theta = {0 if x == 0 else np.round(x, 1)}$')
    for t in clabel: 
        t.set_zorder(20)
    if expr_param == 'delay':
        plt.legend(loc = 'lower left', fontsize = 8, bbox_to_anchor=(0, 1.01), ncol = 2)
    param_list = {'delay': np.arange(40) / 2, 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 
                  'c_perct': np.linspace(0.215, 0.8, 40), 'vac_dur': np.arange(1, 41)}
    if expr_param in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']:
        if expr_name == 'necs_from_fatality_by_contact': y_label = r'$\gamma^*$' 
        else:  y_label = r'$\gamma$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    else: 
        y_label = {'delay': r'$\delta$  (days)', 'vac_eff': r'$\eta$', 'vac_avail': r'$\Theta$', 'c_perct': r'$\chi_{\mathrm{c,vac}}$', 'vac_dur': r'$\mathcal{D}$'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
    figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.14)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.ax.set_title(r'$\theta$', pad = 6, fontsize = 12)
    cbar.ax.tick_params(labelsize = 6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    if expr_param == 'delay':
        Tg = 5.05
        secay = ax.secondary_yaxis('right', functions=(lambda d: d / Tg, lambda d_star: d_star * Tg))
        secay.set_ylabel(r'$\delta^*=\delta/T_g$ (generations)', fontsize = 12)
        secay.set_yticks(np.arange(4) * 2, np.arange(4))
    
    
    if anal_name == 'corr_from_r0_factor':
        zero_crossing = [crossings_on_row(X, Y, z, param_idx) for param_idx in param_idx_list]
        print(zero_crossing)
        for i in range(2):
            ax = axes[1][i]
            plt.sca(ax)
            task_name = f'{expr_name}_({expr_param})'
            if anal_name != 'corr_from_r0_fatality_by_contact': 
                sheet_name_c = f"{task_name}_c_{param_idx_list[i]}_{basic_params.country_abbr[country]}"
                sheet_name_d = f"{task_name}_d_{param_idx_list[i]}_{basic_params.country_abbr[country]}"
            else: 
                sheet_name_c = f"{task_name}_w_{param_idx_list[i]}_{basic_params.country_abbr[country]}"
                sheet_name_d = f"{task_name}_x_{param_idx_list[i]}_{basic_params.country_abbr[country]}"
            x_line = np.exp(np.arange(40) * 0.075)
            plt.plot(x_line, (np.arccos(anal_data[anal_name][sheet_name_c]['optimal_dirx']) - np.arccos(anal_data[anal_name][sheet_name_c]['optimal_indx'])) / np.arccos(anal_data[anal_name][sheet_name_c]['effect_corrx']), 
                     linestyle = '', marker = obj_marker['c'], markerfacecolor = 'white', markeredgecolor = obj_color['c'], markersize = 3.5, markeredgewidth = 0.8, label = r'$\xi_{\mathrm{c}}$')
            plt.plot(x_line, (np.arccos(anal_data[anal_name][sheet_name_d]['optimal_dirx']) - np.arccos(anal_data[anal_name][sheet_name_d]['optimal_indx'])) / np.arccos(anal_data[anal_name][sheet_name_d]['effect_corrx']), 
                     linestyle = '', marker = obj_marker['d'], markerfacecolor = 'white', markeredgecolor = obj_color['d'], markersize = 3.5, markeredgewidth = 0.8, label = r'$\xi_{\mathrm{d}}$')
            plt.axvline(zero_crossing_poi['c'][i][0], color = obj_color['c'], linestyle = '--', label = r'$R_0^\ast:\ \xi_{\mathrm{c}}=0$')
            plt.axvline(zero_crossing_poi['d'][i][0], color = obj_color['d'], linestyle = '-.', label = r'$R_0^\ast:\ \xi_{\mathrm{d}}=0$')
            plt.axvspan(zero_crossing[i][0], zero_crossing[i][1], color='tab:gray', alpha=0.3, linewidth = 0, label = r'$\theta \leq 0$')
            plt.xscale('log')
            figure_setting.set_xylabel(ax, r'$R_0$', r'$\xi$', fontsize = label_fontsize, xlabel_coords = -0.25, ylabel_coords = -0.21)
            if i == 0 and expr_param == 'delay':
                ax.legend(loc = 'upper left', fontsize = 8, bbox_to_anchor=(1.01, 1), ncol = 1, handlelength=3)
            if expr_param == 'delay': ax.text(0.99, 0.97, f"$\\delta = {[15, 7.5][i]}$", ha='right', va='top', fontsize= 10, transform=ax.transAxes)
            elif expr_param == 'coef_beta_1': ax.text(0.99, 0.97, f"$\\gamma = {['10/13', '5/13'][i]}$", ha='right', va='top', fontsize= 10, transform=ax.transAxes)
            else: pass
            # figure_setting.remove_spines(ax, ['top', 'right'])
            figure_setting.set_spine_linewidth(ax, spine_linewidth)
            figure_setting.set_tick_fontsize(ax, 8)
    
    return fig, axes