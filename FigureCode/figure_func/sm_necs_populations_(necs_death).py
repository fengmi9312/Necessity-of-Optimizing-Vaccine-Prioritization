# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 2026

@author: fengm
"""


import numpy as np

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import prototype_necs_heatmap


def _population_corr_z(anal_data, corr_data_type):
    task_name = 'necs_from_populations_(param)'
    country_abbr = basic_params.country_abbr['United States']
    rows = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_d_{param_idx}_{country_abbr}'
        corr_data = anal_data['corr_from_r0_populations'][sheet_name]
        if corr_data_type == 'corr':
            rows.append(
                (np.arccos(corr_data['optimal_indx']) -
                 np.arccos(corr_data['optimal_dirx'])) /
                np.arccos(corr_data['effect_corrx'])
            )
        elif corr_data_type == 'corr_ind':
            rows.append(corr_data['optimal_ind'])
        elif corr_data_type == 'corr_dir':
            rows.append(corr_data['optimal_dir'])
    return np.asarray(rows, dtype=float)


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


def _add_corr_contour_with_interior_label(ax, anal_data, corr_data_type='corr', label_margin=3):
    z = _population_corr_z(anal_data, corr_data_type)
    valid = np.isfinite(z)
    if not valid.any() or not (np.nanmin(z) <= 0 <= np.nanmax(z)):
        return

    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    X, Y = np.meshgrid(x, y)
    cs = ax.contour(
        X,
        Y,
        z,
        levels=[0],
        colors='k',
        linestyles='solid',
        linewidths=1,
    )
    manual_positions = _interior_label_positions(cs, x, y, label_margin=label_margin)
    if manual_positions:
        ax.clabel(
            cs,
            fontsize=10,
            fmt=lambda value: rf'$\xi = {0 if value == 0 else np.round(value, 1)}$',
            manual=manual_positions,
        )


def draw(anal_data, **kwargs):
    corr_contour = kwargs.pop('corr_contour', True)
    corr_data_type = kwargs.pop('corr_data_type', 'corr')
    contour_label_margin = kwargs.pop(
        'contour_label_margin',
        kwargs.pop('contour_edge_margin', 3),
    )

    fig, axes = prototype_necs_heatmap.draw(
        anal_data,
        'necs_from_populations',
        'param',
        anal_name='necs_from_r0_populations',
        target='d',
        corr_contour=False,
    )
    if corr_contour:
        _add_corr_contour_with_interior_label(
            axes[0][0],
            anal_data,
            corr_data_type=corr_data_type,
            label_margin=contour_label_margin,
        )
    return fig, axes
