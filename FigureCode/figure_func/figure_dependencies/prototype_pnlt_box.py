# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 03:12:26 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import pandas as pd
import seaborn as sns
import itertools

def draw(anal_data, **kwargs):
    ####################################################
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (90, 27)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 9
    tick_fontsize = 7
    ####################################################
    ax = axes[0][0]
    ax.set_title('Country-specific cross-objective penalties', fontsize=11, fontweight='bold', pad=6)
    countries = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
    def prepare_data(data_dict):
        mean_res = {country: np.mean(data_dict['necs_from_country'][f"c_{acc_type}{'_dur' if dur else ''}"][f'{country}_none_necs']) for country in countries}
        sorted_countries = sorted(mean_res, key=mean_res.get, reverse=True)
        rows = []
        for country, target in itertools.product(sorted_countries, ['c', 'd']):
            sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
            for value in data_dict['necs_from_country'][sheet_name][ f'{country}_none_pnlt']:
                rows.append({ 'Country': country, 'Target': {'c': r'$\Phi_{\mathrm{c}}^{(\mathrm{d})}$', 'd': r'$\Phi_{\mathrm{d}}^{(\mathrm{c})}$'}[target], 'Penalty': value * 100})
        return pd.DataFrame(rows)
    
    plt.sca(ax)
    df = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    edge_width = 0.75
    sns.boxplot(data=df, y="Penalty", x="Country", hue="Target", width=.4, palette=['#55a868', '#dd8452'], flierprops={'markersize': 1.5, 'markeredgewidth': edge_width},
                boxprops={'linewidth': edge_width}, whiskerprops={'linewidth': edge_width}, capprops={'linewidth': edge_width}, medianprops={'linewidth': edge_width})

    ax.yaxis.grid(True)
    figure_setting.set_xylabel(ax, '', 'Cross-objective penalty (%)', fontsize = label_fontsize , xlabel_coords = -0.1, ylabel_coords = -0.03)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    sns.despine(trim=True, bottom=True)
    ax.legend(fontsize = 8, loc = 'center left', bbox_to_anchor=(0, 1), ncol = 2)
    return fig, axes
