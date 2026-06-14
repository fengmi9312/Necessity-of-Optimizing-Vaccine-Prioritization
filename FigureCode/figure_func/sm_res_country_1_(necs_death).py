# -*- coding: utf-8 -*-
"""
Country death necessity against demographic fatality risk.
"""

import numpy as np
import matplotlib.pyplot as plt

from Dependencies.CodeDependencies import basic_params, param_data_loader
from .figure_dependencies import figure_setting


COUNTRIES = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany',
             'United States', 'Spain', 'Austria', 'Israel', 'South Korea']

COUNTRY_LABELS = {'Ireland': 'IRL', 'Japan': 'JPN', 'United Kingdom': 'UK',
                  'France': 'FRA', 'Germany': 'DEU', 'United States': 'US',
                  'Spain': 'ESP', 'Austria': 'AUT', 'Israel': 'ISR',
                  'South Korea': 'KOR'}


def _mean_ci(values):
    values = np.asarray(values, dtype=float)
    return np.mean(values), np.percentile(values, 2.5), np.percentile(values, 97.5)


def draw(anal_data, **kwargs):
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)

    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (34, 24)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    ax = axes[0][0]
    plt.sca(ax)

    spine_linewidth = 0.8
    label_fontsize = 10
    tick_fontsize = 8

    country_data = param_data_loader.load_all_data(
        basic_params.country_abbr.keys(),
        basic_params.group_div,
    )

    ifr_mean = []
    necs_mean, necs_lower, necs_upper = [], [], []
    sheet_name = f"d_{acc_type}{'_dur' if dur else ''}"

    for country in COUNTRIES:
        ifr_mean.append(country_data[country]['populations'] @ country_data[country]['ifrs'] * 100)

        necs_key = f'{country}_none_necs'
        necs_stats = _mean_ci(anal_data['necs_from_country_70'][sheet_name][necs_key] * 100)
        necs_mean.append(necs_stats[0])
        necs_lower.append(necs_stats[1])
        necs_upper.append(necs_stats[2])

    ifr_mean = np.asarray(ifr_mean)
    necs_mean = np.asarray(necs_mean)
    necs_lower = np.asarray(necs_lower)
    necs_upper = np.asarray(necs_upper)

    red = '#FF9A9A'
    error_red = '#F4A3A3'
    ax.errorbar(
        ifr_mean,
        necs_mean,
        yerr=[necs_mean - necs_lower, necs_upper - necs_mean],
        fmt='o',
        color=red,
        ecolor=error_red,
        elinewidth=0.8,
        capsize=2,
        capthick=0.8,
        markersize=4,
        markeredgewidth=0.4,
        markeredgecolor=red,
        markerfacecolor=red,
        zorder=3,
    )

    coef = np.polyfit(ifr_mean, necs_mean, 1)
    x_line = np.linspace(1.7, 5.35, 100)
    ax.plot(x_line, np.polyval(coef, x_line), color='0.55',
            linestyle='--', linewidth=1.1, zorder=1)

    label_offsets = {
        'Israel': (0.03, 0.03),
        'South Korea': (0.04, -0.04),
        'Ireland': (-0.16, 0.03),
        'United States': (-0.16, -0.06),
        'United Kingdom': (-0.16, -0.02),
        'France': (0.05, -0.06),
        'Germany': (0.03, -0.05),
        'Spain': (0.04, 0.04),
        'Austria': (-0.18, 0.02),
        'Japan': (0.03, 0.03),
    }
    for country, x_val, y_val in zip(COUNTRIES, ifr_mean, necs_mean):
        dx, dy = label_offsets[country]
        ax.text(x_val + dx, y_val + dy, COUNTRY_LABELS[country], fontsize=6,
                color='0.25', ha='left', va='center', zorder=4)

    # ax.text(0.03, 0.93, 'Older demographic profiles shift countries upward',
    #         transform=ax.transAxes, fontsize=7, color='0.25', ha='left')

    ax.set_xlim(1.7, 5.35)
    ax.set_ylim(0, 1.45)
    ax.set_yticks(np.arange(0, 1.41, 0.2))
    ax.grid(True, color='0.88', linestyle=':', linewidth=0.55)
    ax.set_axisbelow(True)

    ax.set_title('Country-specific death necessity\n''across population-weighted IFR',
                 fontsize=12, fontweight='bold', pad=6)
    figure_setting.set_xylabel(
        ax,
        'Population-weighted overall IFR (%)',
        r'$\mathcal{N}_{\mathrm{d}}$ (%)',
        fontsize=label_fontsize,
        xlabel_coords=-0.11,
        ylabel_coords=-0.08,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)

    return fig, axes
