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


def _interior_label_positions(cs, x, y, label_margin=3, max_labels=1):
    xmin = x[label_margin]
    xmax = x[-label_margin - 1]
    ymin = y[label_margin]
    ymax = y[-label_margin - 1]
    xcenter = np.exp((np.log(xmin) + np.log(xmax)) / 2)
    ycenter = (ymin + ymax) / 2
    positions = []
    for seg in cs.allsegs[0]:
        interior = (
            (seg[:, 0] >= xmin) &
            (seg[:, 0] <= xmax) &
            (seg[:, 1] >= ymin) &
            (seg[:, 1] <= ymax)
        )
        candidates = seg[interior]
        if len(candidates) == 0:
            continue
        distance = (
            ((np.log(candidates[:, 0]) - np.log(xcenter)) /
             (np.log(xmax) - np.log(xmin))) ** 2 +
            ((candidates[:, 1] - ycenter) / (ymax - ymin)) ** 2
        )
        positions.append((distance.min(), tuple(candidates[distance.argmin()])))
    positions.sort(key=lambda item: item[0])
    return [position for _, position in positions[:max_labels]]


def draw(anal_data, **kwargs):
    corr_contour = kwargs.pop('corr_contour', True)
    corr_data_type = kwargs.pop('corr_data_type', 'corr')
    contour_label_margin = kwargs.pop(
        'contour_label_margin',
        kwargs.pop('contour_edge_margin', 3),
    )

    country = 'United States'
    expr_name = 'necs_from_populations'
    expr_param = 'param'
    anal_name = 'necs_from_r0_populations'
    acc_type = 'dd'
    target = 'd'

    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)},
                   {'pos': (32, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 6, 'bottom': 5, 'left': 7, 'right': 5}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 15
    tick_fontsize = 9

    country_data = param_data_loader.load_all_data(
        basic_params.country_abbr.keys(),
        basic_params.group_div,
    )
    ifrs = country_data[country]['ifrs']
    ifr_by_pop = np.array([
        make_age_dist(idx, 40, len(ifrs), 0.75) @ ifrs
        for idx in range(40)
    ])

    task_name = f'{expr_name}_({expr_param})'
    country_abbr = basic_params.country_abbr[country]
    sheet_name = f'{task_name}-{country_abbr}_{target}_{acc_type}_necs'
    res = anal_data[anal_name][sheet_name].T * 100 / ifr_by_pop[:, None]

    ax = axes[0][0]
    plt.sca(ax)
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    c = ax.pcolormesh(x, y, res, cmap='Blues')

    ax.set_xscale('log')
    if corr_contour:
        corr_anal_name = 'corr_from_r0_populations'
        corr_z = []
        for param_idx in range(40):
            corr_sheet_name = f'{task_name}_{target}_{param_idx}_{country_abbr}'
            corr_data = anal_data[corr_anal_name][corr_sheet_name]
            if corr_data_type == 'corr':
                corr_z.append(
                    (np.arccos(corr_data['optimal_indx']) -
                     np.arccos(corr_data['optimal_dirx'])) /
                    np.arccos(corr_data['effect_corrx'])
                )
            elif corr_data_type == 'corr_ind':
                corr_z.append(corr_data['optimal_ind'])
            elif corr_data_type == 'corr_dir':
                corr_z.append(corr_data['optimal_dir'])

        if corr_z:
            corr_z = np.asarray(corr_z, dtype=float)
            valid = np.isfinite(corr_z)
            if not valid.any() or not (np.nanmin(corr_z) <= 0 <= np.nanmax(corr_z)):
                corr_z = None
        else:
            corr_z = None

        if corr_z is not None:
            X, Y = np.meshgrid(x, y)
            cs = ax.contour(
                X,
                Y,
                corr_z,
                levels=[0],
                colors='k',
                linestyles='solid',
                linewidths=1,
            )
            manual_positions = _interior_label_positions(
                cs,
                x,
                y,
                label_margin=contour_label_margin,
            )
            if manual_positions:
                ax.clabel(
                    cs,
                    fontsize=10,
                    fmt=lambda value: rf'$\xi = {0 if value == 0 else np.round(value, 1)}$',
                    manual=manual_positions,
                )

    ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    ax.set_title(
        'IFR-adjusted epidemiological necessity\n'
        r'for deaths ($\mathcal{N}_{\mathrm{d}} / \varepsilon$)',
        fontsize=15,
        pad=8,
        linespacing=1.15,
    )
    figure_setting.set_xylabel(
        ax,
        r'$R_0$',
        r'Age-profile center, $o_{\rho}$',
        fontsize=label_fontsize,
        xlabel_coords=-0.09,
        ylabel_coords=-0.12,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)

    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.ax.set_title(
        r'$\mathcal{N}_{\mathrm{d}} / \varepsilon$ (%)',
        pad=6,
        fontsize=12,
    )
    cbar.ax.tick_params(labelsize=6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)

    return fig, axes
