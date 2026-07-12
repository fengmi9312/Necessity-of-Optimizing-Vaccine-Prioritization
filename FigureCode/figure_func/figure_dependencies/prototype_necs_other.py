# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 01:13:03 2025

@author: fengm
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting
from matplotlib.colors import Normalize

def draw(anal_data, **kwargs):
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 7
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (45, 0), 'size': (30, 30)}, {'pos': (90, 0), 'size': (30, 30)}, {'pos': (135, 0), 'size': (30, 30)}, {'pos': (170, 0), 'size': (2, 30)},]]
    margin_attr = {'top': 4, 'bottom': 7, 'left': 10, 'right': 10}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9
    #####################################################
    expr_name = 'necs_from_param'
    norm = Normalize(vmin=0, vmax=max([np.max(anal_data['necs_from_r0_factor'][f"{expr_name}_({expr_param})-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur or expr_param == 'vac_dur' else ''}_{data_type}"].T * 100) for expr_param in ['vac_avail', 'vac_eff', 'c_perct', 'vac_dur']]))
    for ax_idx, expr_param in enumerate(['vac_avail', 'vac_eff', 'c_perct', 'vac_dur']):
        task_name = f'{expr_name}_({expr_param})'
        anal_name = 'necs_from_r0_factor'
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur or expr_param == 'vac_dur' else ''}"
        sheet_name = f'{sheet_name_preppend}_{data_type}'
        ax = axes[0][ax_idx]
        plt.sca(ax)
        x = np.exp(np.arange(40) * 3 / 40)
        y = np.arange(40)
        c = ax.pcolormesh(x, y, anal_data[anal_name][sheet_name].T * 100, cmap = 'Blues', norm = norm)
        ax.set_xscale('log')
        param_list = {'vac_avail': np.arange(12, 91, 2) / 100, 'vac_eff': np.arange(22, 101, 2) / 100,
                      'c_perct': np.arange(215, 801, 15) / 1000, 'vac_dur': np.arange(1, 41)}
        y_label = {'vac_avail': r'$\rho$', 'vac_eff': r'$\eta$', 'c_perct': r'$\chi_{\mathrm{c, vac}}$', 'vac_dur': r'$\mathcal{D}$'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
        ylabel_coords = {'vac_avail': -0.21, 'vac_eff': -0.21, 'c_perct': - 0.25, 'vac_dur': -0.15}[expr_param]
        figure_setting.set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = ylabel_coords)
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][-1])
    cbar.set_label('Necessity (%)', labelpad = 2, fontsize = 10)
    cbar.ax.tick_params(labelsize = 6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)
    
    return fig, axes