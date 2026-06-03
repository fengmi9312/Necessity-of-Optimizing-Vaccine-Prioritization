# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:57:03 2025

@author: fengm
"""

import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import pandas as pd
import seaborn as sns
import itertools
from Dependencies.CodeDependencies import  basic_params, param_data_loader

def draw(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 9
    grid_attrs = [[{'pos': (0, 0), 'size': (45, 27)}]]
    margin_attr = {'top': 2, 'bottom': 10, 'left': 5, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 9
    tick_fontsize = 7
    ####################################################
    ax = axes[0][0]
    sorted_countries = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
    targets = {'c': 'Cumulative Infections', 'd': 'Deaths'}
    def prepare_data(data_dict):
        sheet_name = f"c_{acc_type}{'_dur' if dur else ''}"
        # mean_res = {country: np.mean(data_dict['necs_from_country'][sheet_name][f'{country}_none_necs']) for country in countries}
        # sorted_countries = sorted(mean_res, key=mean_res.get, reverse=True)
        country_data = param_data_loader.load_all_data(basic_params.country_abbr.keys(), basic_params.group_div)
        rows = []
        tot_ifrs = []
        r0_list = []
        for country in sorted_countries:
            sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
            tot_ifrs.append(country_data[country]['populations'] @ country_data[country]['ifrs'])
            param_data = data_dict['param_from_country']['r0'][country]
            for value in data_dict['necs_from_country'][sheet_name][ f'{country}_none_necs']:
                rows.append({ 'Country': country, 'Objective': targets[target], 'Necessity': value * 100})
            r0_list.append([np.mean(param_data), np.percentile(param_data, 2.5), np.percentile(param_data, 97.5)])
        return sorted_countries, pd.DataFrame(rows), tot_ifrs, np.array(r0_list)
    
    edge_width = 0.75
    plt.sca(ax)
    countries, df, tot_ifrs, r0_array = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    sns.boxplot(data=df, y="Necessity", x="Country", hue="Objective", width=.6, palette= ['#509FD1'] if target == 'c' else ['#DF7384'], flierprops={'markersize': 1.5, 'markeredgewidth': edge_width},
                boxprops={'linewidth': edge_width}, whiskerprops={'linewidth': edge_width}, capprops={'linewidth': edge_width}, medianprops={'linewidth': edge_width})
   
    main_ylims = ax.get_ylim()
    ax.set_ylim(bottom = - main_ylims[-1] / 100)
    ax.spines['left'].set_bounds(0, main_ylims[-1])
    ax.yaxis.grid(True)
    sns.despine(trim=True, bottom=True)
    figure_setting.set_xylabel(ax, '', fr'$\mathcal{{N}}_{{\mathrm{{{target}}}}}$ (%)', fontsize = label_fontsize , xlabel_coords = -0.1, ylabel_coords = -0.06)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    plt.xticks(rotation=-60)
    
    if target == 'c': 
        ax.legend(fontsize = 8, loc = 'upper right')
    #     ax_twin = ax.twinx()
    #     plt.sca(ax_twin)
    #     mean_res = r0_array[:, 0]
    #     lower_res = r0_array[:, 1]
    #     upper_res = r0_array[:, 2]
    #     print(r0_array)
    #     ax_twin.errorbar(np.arange(len(mean_res)), mean_res, yerr=[mean_res - lower_res, upper_res - mean_res], markersize = 6, linewidth = 1.5, capthick = 0,
    #                      fmt='D', linestyle = '-', color = 'black', capsize = 6, markeredgewidth = 1, markeredgecolor = 'white', label = r'Basic Reproduction Number ($R_0$)')
    #     ax_twin.spines['top'].set_visible(False)
    #     ax_twin.spines['bottom'].set_visible(False)
    #     ax_twin.spines['left'].set_visible(False)
    #     ax_twin.set_yticks(np.arange(1, 6), np.arange(1, 6))
    #     twin_bounds = (1, 5)
    #     plt.ylabel(r'$R_0$', fontsize = label_fontsize)
    #     plt.legend(loc = 'lower right', fontsize = 8)
    elif target == 'd':
        ax.legend(fontsize = 8, loc = 'upper left', bbox_to_anchor=(0.5, 1))
        ax_twin = ax.twinx()
        plt.sca(ax_twin)
        plt.plot(np.arange(len(tot_ifrs)), tot_ifrs, marker = 'X', color = 'tab:gray', markersize = 12, linewidth = 2, 
                 linestyle = '-', markeredgewidth = 1, markeredgecolor = 'white', zorder = 1, label = 'Overall IFR')
        ax_twin.spines['top'].set_visible(False)
        ax_twin.spines['bottom'].set_visible(False)
        ax_twin.spines['left'].set_visible(False)
        ax_twin.set_yticks(np.arange(7) / 100, np.arange(7))
        twin_bounds = (0, 0.06)
        plt.ylabel('Overall IFR (%)', fontsize = label_fontsize)
        plt.legend(loc = 'upper left', fontsize = 8, bbox_to_anchor=(0.72, 1))
        main_ylims = ax.get_ylim()
        main_bounds = ax.spines['left'].get_bounds()
        lower_ylim = twin_bounds[0] + (main_ylims[0] - main_bounds[0]) * (twin_bounds[1] - twin_bounds[0]) / (main_bounds[1] - main_bounds[0])
        upper_ylim = twin_bounds[1] + (main_ylims[1] - main_bounds[1]) * (twin_bounds[1] - twin_bounds[0]) / (main_bounds[1] - main_bounds[0])
        ax_twin.set_ylim(lower_ylim, upper_ylim)
        ax_twin.spines['right'].set_bounds(twin_bounds[0], twin_bounds[1])

    return fig, axes
