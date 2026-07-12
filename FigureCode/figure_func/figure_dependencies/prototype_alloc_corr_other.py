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

def draw(anal_data, expr_name, expr_param, **kwargs):
    country = kwargs.pop('country', 'United States')
    ####################################################
    scale_prop = 8
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    if expr_param == 'delay': margin_attr = {'top': 4, 'bottom': 6, 'left': 7, 'right': 12}
    else: margin_attr = {'top': 4, 'bottom': 6, 'left': 7, 'right': 3}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9
    #####################################################
    
    deep_colors = sns.color_palette('deep')
    obj_marker = {'c':'x', 'd': 'o'}
    obj_color = {'c': deep_colors[2], 'd': deep_colors[1]}
    
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    task_name = f'{expr_name}_({expr_param})'
    anal_name = 'corr_from_r0_factor'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
        z.append(anal_data[anal_name][sheet_name]['alloc_corr'])
    original_cmap = sns.color_palette("Blues", as_cmap=True)
    color_start, color_end = 0, 0.6
    colors = original_cmap(np.linspace(color_start, color_end, 256))
    c = ax.pcolormesh(x, y, np.array(z) , cmap = mcolors.ListedColormap(colors))
    ax.set_xscale('log')
    
    for target in ['c', 'd']:
        xx = np.exp(np.arange(40) * 3 / 40)
        yy = np.arange(40)
        task_name = f'{expr_name}_({expr_param})'
        anal_name = 'corr_from_r0_factor'
        zz = []
        for param_idx in range(40):
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            zz.append((np.arccos(anal_data[anal_name][sheet_name]['optimal_dir']) - np.arccos(anal_data[anal_name][sheet_name]['optimal_ind'])) / np.arccos(anal_data[anal_name][sheet_name]['effect_corr']))
        cg = contour_generator(xx, yy, zz)
        cs_data = cg.lines(level = 0)
        for cs_idx, cs_item in enumerate(cs_data): 
            cs_keep = cs_item[cs_item[:, 0] >= 1.05]
            plt.plot(cs_keep[:, 0], cs_keep[:, 1], marker = obj_marker[target], linestyle = '', markevery = 2, color = obj_color[target], markerfacecolor = 'none',  markeredgewidth = 1.2, label = rf'$\xi_{{\mathrm{{{target}}}}} = 0$' if cs_idx == 0 else None)
            
    X, Y = np.meshgrid(x, y)
    cs = plt.contour(X, Y, z, levels=[0], colors='black', linestyles = 'solid', linewidths = 1.5, zorder = 10)
    clabel = ax.clabel(cs, fontsize = 12, fmt = lambda x: rf'$\mu = {0 if x == 0 else np.round(x, 1)}$')
    for t in clabel: 
        t.set_zorder(20)
    if expr_param == 'delay':
        plt.legend(loc = 'lower left', fontsize = 8, bbox_to_anchor=(0, 1.01), ncol = 2)
    param_list = {'delay': np.arange(40) / 2, 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 
                  'c_perct': np.linspace(0.215, 0.8, 40), 'vac_dur': np.arange(1, 41)}
    if expr_name == 'necs_from_fatality':
        y_label = r'$\gamma$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name == 'necs_from_param': 
        y_label = {'delay': r'$\delta$  (days)', 'vac_eff': r'$\eta$', 'vac_avail': r'$\Theta$', 'c_perct': r'$\chi_{\mathrm{c,vac}}$', 'vac_dur': r'$\mathcal{D}$'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
    else: pass
    figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.set_label(r'Similarity, $\mu$', labelpad = 1, fontsize = 12)
    cbar.ax.tick_params(labelsize = 6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    
    return fig, axes