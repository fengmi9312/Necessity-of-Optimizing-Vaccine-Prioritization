# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:53:12 2025

@author: MIFENG
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params, func
from .figure_dependencies import figure_setting
import matplotlib.patches as patches
from matplotlib.transforms import blended_transform_factory
from scipy.ndimage import minimum_filter


def draw(anal_data, expr_name = 'necs_from_param', expr_param = 'vac_dur', anal_name = 'necs_from_r0_factor', **kwargs):
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
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 15
    tick_fontsize = 9
    #####################################################
    task_name = f'{expr_name}_({expr_param})'
    sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    sheet_name = f'{sheet_name_preppend}_{data_type}'
    res = anal_data[anal_name][sheet_name][14] * 100
    c = ax.plot(x, res, color = 'tab:blue')
    task_name = f'necs_from_time_course_(param)'
    sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}"
    sheet_name = f'{sheet_name_preppend}_{data_type}'
    anal_name = 'necs_from_r0_time_course'
    res = anal_data[anal_name][sheet_name].to_numpy()[0,:] * 100
    c = ax.plot(x, res, color = 'tab:red')
    
    ax.set_xscale('log')
   
    
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