# -*- coding: utf-8 -*-
"""
Slices of death necessity under fatality-profile variation.
"""


import numpy as np
import matplotlib.pyplot as plt

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting


RED = '#C54E53'
BLUE = '#4C72B1'


def _slice_data(anal_data, target):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_by_fatality_(param)'
    sheet_name = (
        f'{task_name}-{basic_params.country_abbr[country]}_'
        f'{target}_dd_necs'
    )
    return np.asarray(anal_data['necs_from_r0_time_course_by_fatality'][sheet_name]).T * 100


def _xi_slice(anal_data, target, param_idx):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_by_fatality_(param)'
    sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
    corr_data = anal_data['corr_from_r0_time_course_by_fatality'][sheet_name]
    denom = np.arccos(corr_data['effect_corrx'])
    xi_opt = (
        np.arccos(corr_data['optimal_indx']) -
        np.arccos(corr_data['optimal_dirx'])
    ) / denom
    xi_worst = (
        np.arccos(corr_data['worst_indx']) -
        np.arccos(corr_data['worst_dirx'])
    ) / denom
    return np.asarray(xi_opt), np.asarray(xi_worst)


def _set_necs_ylim(ax, values, target):
    upper = np.nanmax(values)
    if target == 'c':
        upper = max(5, np.ceil(upper / 5) * 5)
        step = max(5, upper / 2)
    else:
        upper = max(0.2, np.ceil(upper * 10) / 10)
        step = max(0.1, upper / 3)
    ax.set_ylim(0, upper)
    ax.spines['left'].set_bounds(0, upper)
    ax.set_yticks(np.arange(0, upper + step * 0.5, step))


def _set_xi_ylim(ax, xi_opt, xi_worst):
    values = np.concatenate([xi_opt, xi_worst, np.array([0])])
    ymin = np.nanmin(values)
    ymax = np.nanmax(values)
    pad = max(0.08, (ymax - ymin) * 0.08)
    ymin = max(-1.05, ymin - pad)
    ymax = min(1.05, ymax + pad)
    ax.set_ylim(ymin, ymax)
    ax.spines['left'].set_bounds(ymin, ymax)


def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'd')
    slice_idxes = kwargs.pop('slice_idxes', [0, 13, 26, 39])

    scale_prop = 12
    grid_attrs = [
        [
            {'pos': (0, row_idx * 14), 'size': (15, 10)}
            for row_idx in range(len(slice_idxes))
        ],
        [
            {'pos': (22, row_idx * 14), 'size': (15, 10)}
            for row_idx in range(len(slice_idxes))
        ],
    ]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 2}
    removed_labels = {
        'x': [
            (col_idx, row_idx)
            for col_idx in range(2)
            for row_idx in range(len(slice_idxes) - 1)
        ],
        'y': [],
        'xtick': [],
        'ytick': [],
    }
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    text_fontsize = 9

    x = np.exp(np.arange(40) * 3 / 40)
    necs = _slice_data(anal_data, target)
    xi_pairs = [_xi_slice(anal_data, target, param_idx) for param_idx in slice_idxes]

    y_label = fr'$\mathcal{{N}}_{{\mathrm{{{target}}}}}$'
    gamma_labels = {
        0: '0',
        13: r'1/3',
        26: r'2/3',
        39: '1',
    }

    for ax_idx, param_idx in enumerate(slice_idxes):
        ax = axes[0][ax_idx]
        plt.sca(ax)
        ax.plot(x, necs[param_idx], linewidth=2.5, color='tab:orange')
        ax.text(
            0.03,
            0.97,
            rf'$\gamma = {gamma_labels.get(param_idx, f"{param_idx}/39")}$',
            ha='left',
            va='top',
            fontsize=text_fontsize,
            transform=ax.transAxes,
            math_fontfamily='cm',
        )
        ax.set_xscale('log')
        _set_necs_ylim(ax, necs[slice_idxes], target)
        figure_setting.set_xylabel(
            ax,
            r'$R_0$',
            y_label,
            fontsize=label_fontsize,
            xlabel_coords=-0.15 if target == 'c' else -0.24,
            ylabel_coords=-0.18,
        )
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)

        xi_opt, xi_worst = xi_pairs[ax_idx]
        ax = axes[1][ax_idx]
        plt.sca(ax)
        ax.plot(
            x,
            xi_opt,
            linestyle='',
            marker='x',
            markerfacecolor='white',
            markeredgecolor=RED,
            markersize=4,
            markeredgewidth=1.2,
            label='Optimal',
        )
        ax.plot(
            x,
            xi_worst,
            linestyle='',
            marker='o',
            markerfacecolor='white',
            markeredgecolor=BLUE,
            markersize=4,
            markeredgewidth=1.2,
            alpha=0.3,
            label='Burden-maximizing',
        )
        ax.axhline(0, 0, 1, linestyle=':', color='tab:gray')
        ax.set_xscale('log')
        _set_xi_ylim(ax, xi_opt, xi_worst)
        figure_setting.set_xylabel(
            ax,
            r'$R_0$',
            r'$\xi$',
            fontsize=label_fontsize,
            xlabel_coords=-0.2,
            ylabel_coords=-0.2,
        )
        # figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        if ax_idx == 0:
            leg = ax.legend(
                loc='lower center',
                fontsize=8,
                bbox_to_anchor=(0.5, 1.01),
                ncol=2,
            )
            for handle in leg.legend_handles:
                handle.set_markersize(5)
                handle.set_markeredgewidth(1.5)

    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes
