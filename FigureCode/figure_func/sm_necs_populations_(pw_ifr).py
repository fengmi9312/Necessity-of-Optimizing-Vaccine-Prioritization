# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt

from Dependencies.CodeDependencies import basic_params, param_data_loader
from .figure_dependencies import figure_setting


def make_age_dist(idx, n, n_group, sigma_rel=0.75):
    if not 0 <= idx < n:
        raise ValueError('idx must be in range(n)')
    if n <= 1:
        raise ValueError('n must be greater than 1')
    if n_group <= 1:
        raise ValueError('n_group must be greater than 1')
    if sigma_rel <= 0:
        raise ValueError('sigma_rel must be positive')

    age_pos = np.linspace(0, 1, n_group)
    center = idx / (n - 1)
    weights = np.exp(-0.5 * ((age_pos - center) / sigma_rel) ** 2)
    return weights / weights.sum()


def draw(anal_data):
    country = 'United States'

    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (28, 20)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9

    country_data = param_data_loader.load_all_data(
        basic_params.country_abbr.keys(),
        basic_params.group_div,
    )
    ifrs = country_data[country]['ifrs']
    center_vals = np.arange(40) / 39
    pw_ifr = np.array([
        make_age_dist(idx, 40, len(ifrs), 0.75) @ ifrs
        for idx in range(40)
    ]) * 100

    ax = axes[0][0]
    plt.sca(ax)
    ax.plot(center_vals, pw_ifr, color='tab:red', marker='o',
            markersize=3, linewidth=1.2)
    ax.set_title(r'Population-weighted overall IFR ($\varepsilon$)', fontsize=13, pad=6)
    ax.set_xticks(
        [0, 1 / 3, 2 / 3, 1],
        ['0', r'$1/3$', r'$2/3$', '1'],
    )
    ax.grid(True, color='0.9', linestyle=':', linewidth=0.6)
    figure_setting.set_xylabel(
        ax,
        r'Age-profile center, $o_{\rho}$',
        r'$\varepsilon$ (%)',
        fontsize=label_fontsize,
        xlabel_coords=-0.13,
        ylabel_coords=-0.12,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)

    return fig, axes
