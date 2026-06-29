# -*- coding: utf-8 -*-
"""
Country mortality penalty across the estimated R0 range.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting


COUNTRIES = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany',
             'United States', 'Spain', 'Austria', 'Israel', 'South Korea']

COUNTRY_LABELS = {'Ireland': 'IRL', 'Japan': 'JPN', 'United Kingdom': 'UK',
                  'France': 'FRA', 'Germany': 'DEU', 'United States': 'US',
                  'Spain': 'ESP', 'Austria': 'AUT', 'Israel': 'ISR',
                  'South Korea': 'KOR'}


def _format_log_tick(value, pos):
    if value <= 0:
        return ''
    if any(np.isclose(value, tick) for tick in [2, 3, 4]):
        return fr'${int(value)} \times 10^0$'
    return ''


def _mean_ci(values):
    values = np.asarray(values, dtype=float)
    return np.mean(values), np.percentile(values, 2.5), np.percentile(values, 97.5)


def draw(anal_data, **kwargs):
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    param_idx = kwargs.pop('param_idx', 7)
    country_for_theory = kwargs.pop('country', 'United States')

    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (34, 24)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    ax = axes[0][0]
    plt.sca(ax)

    spine_linewidth = 0.8
    label_fontsize = 10
    tick_fontsize = 8

    r0_mean, r0_lower, r0_upper = [], [], []
    pnlt_mean, pnlt_lower, pnlt_upper = [], [], []
    sheet_name = f"d_{acc_type}{'_dur' if dur else ''}"
    for country in COUNTRIES:
        r0_stats = _mean_ci(anal_data['necs_from_country_35']['r0'][country])
        r0_mean.append(r0_stats[0])
        r0_lower.append(r0_stats[1])
        r0_upper.append(r0_stats[2])

        pnlt_stats = _mean_ci(
            anal_data['necs_from_country_35'][sheet_name][f'{country}_none_pnlt'] * 100
        )
        pnlt_mean.append(pnlt_stats[0])
        pnlt_lower.append(pnlt_stats[1])
        pnlt_upper.append(pnlt_stats[2])

    r0_mean = np.asarray(r0_mean)
    r0_lower = np.asarray(r0_lower)
    r0_upper = np.asarray(r0_upper)
    pnlt_mean = np.asarray(pnlt_mean)
    pnlt_lower = np.asarray(pnlt_lower)
    pnlt_upper = np.asarray(pnlt_upper)
    order = np.argsort(r0_mean)
    countries_sorted = np.asarray(COUNTRIES)[order]

    r0_mean = r0_mean[order]
    r0_lower = r0_lower[order]
    r0_upper = r0_upper[order]
    pnlt_mean = pnlt_mean[order]
    pnlt_lower = pnlt_lower[order]
    pnlt_upper = pnlt_upper[order]

    orange = '#CF5C1D'
    x_theory = np.exp(np.arange(40) * 3 / 40)
    country_abbr = basic_params.country_abbr[country_for_theory]
    prefix = (
        f"necs_from_param_(delay)-{country_abbr}_d_{acc_type}"
        f"{'_dur' if dur else ''}"
    )
    target_min = anal_data['necs_from_r0_factor'][f'{prefix}_min']
    target_anti_min = anal_data['necs_from_r0_factor'][f'{prefix}_anti_min']
    target_no_vac = anal_data['necs_from_r0_factor'][f'{prefix}_no_vac']
    theory = (
        (target_anti_min - target_min) / (target_no_vac - target_min)
    )[param_idx].to_numpy() * 100

    ax.plot(x_theory, theory, color=orange, linestyle='--',
            linewidth=1.0, alpha=0.35, zorder=1,
            label=r'Theoretical $\Phi_{\mathrm{d}}^{(\mathrm{c})}$')
    ax.errorbar(
        r0_mean,
        pnlt_mean,
        yerr=[pnlt_mean - pnlt_lower, pnlt_upper - pnlt_mean],
        fmt='none',
        ecolor='#E7A579',
        elinewidth=0.6,
        capsize=1.6,
        capthick=0.6,
        zorder=1.5,
    )
    ax.plot(
        r0_mean,
        pnlt_mean,
        color=orange,
        marker='s',
        markersize=3.6,
        linewidth=1.55,
        label=r'Country-specific $\Phi_{\mathrm{d}}^{(\mathrm{c})}$',
        zorder=3,
    )

    label_offsets = {
        'Ireland': (0.03, 0.5),
        'Japan': (-0.07, 4.2),
        'United Kingdom': (-0.06, -4.6),
        'France': (0.01, 2.5),
        'Germany': (0.02, -3.4),
        'United States': (0.04, 0),
        'Spain': (0.02, 4.2),
        'Austria': (0.06, 0),
        'Israel': (0.02, 4.0),
        'South Korea': (0.02, 4.0),
    }
    for country, x_val, y_val in zip(countries_sorted, r0_mean, pnlt_mean):
        dx, dy = label_offsets[country]
        ax.text(x_val + dx, y_val + dy, COUNTRY_LABELS[country], fontsize=5.5,
                color='0.25', ha='left', va='center', zorder=4)

    ax.set_xscale('log')
    ax.set_xlim(1.35, 4.2)
    ax.set_ylim(0, 85)
    ax.set_yticks(np.arange(0, 81, 20))
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(2, 3, 4)))
    ax.xaxis.set_major_formatter(FuncFormatter(_format_log_tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, color='0.88', linestyle=':', linewidth=0.55)
    ax.set_axisbelow(True)

    ax.set_title('Country-specific death penalty from\n''infection-minimizing allocation',
                 fontsize=11, fontweight='bold', pad=6)
    figure_setting.set_xylabel(
        ax,
        r'Estimated $R_0$',
        'Cross-objective penalty (%)',
        fontsize=label_fontsize,
        xlabel_coords=-0.11,
        ylabel_coords=-0.08,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    ax.legend(frameon=False, fontsize=7, loc='upper left',
              bbox_to_anchor=(0.01, 0.99), handlelength=2.2)

    return fig, axes
