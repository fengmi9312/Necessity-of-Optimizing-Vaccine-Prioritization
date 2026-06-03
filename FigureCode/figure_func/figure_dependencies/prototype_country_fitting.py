# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:29:49 2025

@author: fengm
"""



import numpy as np
import matplotlib.pyplot as plt
from Dependencies.CodeDependencies import basic_params
from . import figure_setting


def draw(anal_data, **kwargs):
    country = kwargs.pop('country', 'United States')
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (6, 0), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 2, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    from matplotlib.ticker import ScalarFormatter
    ax = axes[0][0]
    plt.sca(ax)
    best_left, best_right = anal_data['fitted_fraction_from_time']['fitted_period'][country]
    real_time_line = anal_data['fitted_fraction_from_time']['real_data'][f'{country}_time'][best_left:best_right]
    plt.plot(real_time_line, anal_data['fitted_fraction_from_time']['real_data'][f'{country}_data'][best_left:best_right], 'o', markerfacecolor=(1.0, 0.5, 0.5, 0.75), 
             markeredgecolor='#F08080', markeredgewidth = 1, markersize = 3, label = 'Real Data')
    best_left_x, best_right_x = best_left * basic_params.day_div, best_right * basic_params.day_div
    plt.plot(anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_time'][best_left_x:best_right_x], anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_mean'][best_left_x:best_right_x], color = "#6495ED", label = 'Fitted Curve')
    plt.fill_between(anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_time'][best_left_x:best_right_x], anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_lower'][best_left_x:best_right_x], 
                     anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_upper'][best_left_x:best_right_x], color = "#6495ED", alpha = 0.5, linewidth = 0, label = '95% CI of Fitted Curve')
    figure_setting.set_xylabel(ax, 'Date', 'Cumulative infections (%)', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.12)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    start_date = np.datetime64('2020-01-22')
    date_list = np.arange(start_date, start_date + np.timedelta64(90, 'D'))
    ax.set_xticks(real_time_line[::14], date_list[real_time_line[::14]], fontsize = tick_fontsize)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.get_offset_text().set_size(tick_fontsize)
    plt.legend(fontsize = 8)
    return fig, axes

