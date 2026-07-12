# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt

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
    scale_prop = 10
    grid_attrs = [[
        {'pos': (0, 0), 'size': (24, 21)},
        {'pos': (36, 0), 'size': (24, 21)},
        {'pos': (72, 0), 'size': (24, 21)},
        {'pos': (108, 0), 'size': (24, 21)},
    ]]
    margin_attr = {'top': 4, 'bottom': 7, 'left': 6, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1.5
    label_fontsize = 15
    tick_fontsize = 12

    idx_list = [0, 13, 26, 39]
    center_labels = ['0', r'1/3', r'2/3', '1']
    age_groups = [f'{idx * 5}-{idx * 5 + 4}' for idx in range(16)]

    for ax, pop_idx, center_label in zip(axes[0], idx_list, center_labels):
        plt.sca(ax)
        population = make_age_dist(pop_idx, 40, 16, 0.75) * 100
        ax.bar(
            np.arange(16),
            population,
            color='tab:orange',
            width=0.8,
            edgecolor='tab:gray',
            linewidth=1,
        )
        ax.set_title(rf'$o_{{\rho}} = {center_label}$', fontsize=16, pad=5)
        ax.set_ylim(0, 10)
        ax.spines['left'].set_bounds(0, 10)
        ax.set_yticks(np.arange(0, 11, 5))
        figure_setting.set_xylabel(
            ax,
            'Age group',
            'Population share (%)',
            fontsize=label_fontsize,
            xlabel_coords=-0.2,
            ylabel_coords=-0.12,
        )
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xticks(rotation=90, fontsize=label_fontsize * 0.6)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation=90)
        ax.tick_params(axis='x', which='major', pad=1)

    return fig, axes
