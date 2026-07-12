# -*- coding: utf-8 -*-
"""
Extended fatality-profile slice for time-course necessity.
"""


import numpy as np
import matplotlib.pyplot as plt

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting


RED = '#C54E53'
BLUE = '#4C72B1'
EXT_GAMMA = 1.05


def _necs_slice(anal_data, target):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_by_fatality_ext_(param)'
    sheet_name = (
        f'{task_name}-{basic_params.country_abbr[country]}_'
        f'{target}_dd_necs'
    )
    return np.asarray(
        anal_data['necs_from_r0_time_course_by_fatality_ext'][sheet_name]
    ).T[0] * 100


def _xi_slice(anal_data, target):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_by_fatality_ext_(param)'
    sheet_name = f'{task_name}_{target}_ext_{basic_params.country_abbr[country]}'
    corr_data = anal_data['corr_from_r0_time_course_by_fatality_ext'][sheet_name]
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
    gamma = kwargs.pop('gamma', EXT_GAMMA)

    scale_prop = 12
    grid_attrs = [[
        {'pos': (0, 0), 'size': (15, 10)},
        {'pos': (22, 0), 'size': (15, 10)},
    ]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1.5
    label_fontsize = 12
    tick_fontsize = 9
    text_fontsize = 9

    x = np.exp(np.arange(40) * 3 / 40)
    necs = _necs_slice(anal_data, target)
    xi_opt, xi_worst = _xi_slice(anal_data, target)

    ax = axes[0][0]
    plt.sca(ax)
    ax.plot(x, necs, linewidth=2.5, color='tab:orange')
    ax.text(
        0.03,
        0.97,
        rf'$\gamma = {gamma:g}$',
        ha='left',
        va='top',
        fontsize=text_fontsize,
        transform=ax.transAxes,
        math_fontfamily='cm',
    )
    ax.set_xscale('log')
    _set_necs_ylim(ax, necs, target)
    figure_setting.set_xylabel(
        ax,
        r'$R_0$',
        fr'$\mathcal{{N}}_{{\mathrm{{{target}}}}}$',
        fontsize=label_fontsize,
        xlabel_coords=-0.24 if target == 'd' else -0.15,
        ylabel_coords=-0.18,
    )
    figure_setting.remove_spines(ax, ['top', 'right'])
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)

    ax = axes[0][1]
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
