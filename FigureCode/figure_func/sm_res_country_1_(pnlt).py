# -*- coding: utf-8 -*-
"""
Country cross-objective penalties across the estimated R0 range.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting


COUNTRIES = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany',
             'United States', 'Spain', 'Austria', 'Israel', 'South Korea']

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
    param_idx = kwargs.pop('param_idx', 28)
    country_for_theory = kwargs.pop('country', 'United States')

    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (34, 24)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    ax = axes[0][0]
    plt.sca(ax)

    spine_linewidth = 0.8
    label_fontsize = 10
    tick_fontsize = 8

    r0_mean, r0_lower, r0_upper = [], [], []
    c_pnlt, c_lower, c_upper = [], [], []
    d_pnlt, d_lower, d_upper = [], [], []
    for country in COUNTRIES:
        r0_stats = _mean_ci(anal_data['necs_from_country_140']['r0'][country])
        r0_mean.append(r0_stats[0])
        r0_lower.append(r0_stats[1])
        r0_upper.append(r0_stats[2])

        c_sheet = f"c_{acc_type}{'_dur' if dur else ''}"
        d_sheet = f"d_{acc_type}{'_dur' if dur else ''}"
        c_stats = _mean_ci(anal_data['necs_from_country_140'][c_sheet][f'{country}_none_pnlt'] * 100)
        d_stats = _mean_ci(anal_data['necs_from_country_140'][d_sheet][f'{country}_none_pnlt'] * 100)
        c_pnlt.append(c_stats[0])
        c_lower.append(c_stats[1])
        c_upper.append(c_stats[2])
        d_pnlt.append(d_stats[0])
        d_lower.append(d_stats[1])
        d_upper.append(d_stats[2])

    r0_mean = np.asarray(r0_mean)
    r0_lower = np.asarray(r0_lower)
    r0_upper = np.asarray(r0_upper)
    c_pnlt = np.asarray(c_pnlt)
    c_lower = np.asarray(c_lower)
    c_upper = np.asarray(c_upper)
    d_pnlt = np.asarray(d_pnlt)
    d_lower = np.asarray(d_lower)
    d_upper = np.asarray(d_upper)
    order = np.argsort(r0_mean)

    r0_mean = r0_mean[order]
    r0_lower = r0_lower[order]
    r0_upper = r0_upper[order]
    c_pnlt = c_pnlt[order]
    c_lower = c_lower[order]
    c_upper = c_upper[order]
    d_pnlt = d_pnlt[order]
    d_lower = d_lower[order]
    d_upper = d_upper[order]

    green = '#2E8B57'
    orange = '#CF5C1D'
    x_theory = np.exp(np.arange(40) * 3 / 40)
    country_abbr = basic_params.country_abbr[country_for_theory]
    theory = {}
    for target in ['c', 'd']:
        prefix = (
            f"necs_from_param_(delay)-{country_abbr}_{target}_{acc_type}"
            f"{'_dur' if dur else ''}"
        )
        target_min = anal_data['necs_from_r0_factor'][f'{prefix}_min']
        target_anti_min = anal_data['necs_from_r0_factor'][f'{prefix}_anti_min']
        target_no_vac = anal_data['necs_from_r0_factor'][f'{prefix}_no_vac']
        theory[target] = (
            (target_anti_min - target_min) / (target_no_vac - target_min)
        )[param_idx].to_numpy() * 100

    ax.plot(x_theory, theory['c'], color=green, linestyle='--',
            linewidth=0.9, alpha=0.28, zorder=1)
    ax.plot(x_theory, theory['d'], color=orange, linestyle='--',
            linewidth=0.9, alpha=0.28, zorder=1)

    # ax.errorbar(
    #     r0_mean,
    #     (c_pnlt + d_pnlt) / 2,
    #     xerr=[r0_mean - r0_lower, r0_upper - r0_mean],
    #     fmt='none',
    #     ecolor='0.72',
    #     elinewidth=0.45,
    #     capsize=0,
    #     alpha=0.5,
    #     zorder=1,
    # )
    ax.errorbar(
        r0_mean,
        c_pnlt,
        yerr=[c_pnlt - c_lower, c_upper - c_pnlt],
        fmt='none',
        ecolor='#8BC2A3',
        elinewidth=0.55,
        capsize=0,
        alpha=0.45,
        zorder=1.5,
    )
    ax.errorbar(
        r0_mean,
        d_pnlt,
        yerr=[d_pnlt - d_lower, d_upper - d_pnlt],
        fmt='none',
        ecolor='#E7A579',
        elinewidth=0.55,
        capsize=0,
        alpha=0.45,
        zorder=1.5,
    )
    ax.plot(
        r0_mean,
        c_pnlt,
        color=green,
        marker='o',
        markersize=3.8,
        linewidth=1.55,
        label=r'$\Phi_{\mathrm{c}}^{(\mathrm{d})}$',
        zorder=3,
    )
    ax.plot(
        r0_mean,
        d_pnlt,
        color=orange,
        marker='s',
        markersize=3.6,
        linewidth=1.55,
        label=r'$\Phi_{\mathrm{d}}^{(\mathrm{c})}$',
        zorder=3,
    )

    ax.set_xscale('log')
    ax.set_xlim(1.35, 4.2)
    ax.set_ylim(0, 75)
    ax.set_yticks(np.arange(0, 71, 10))
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(2, 3, 4)))
    ax.xaxis.set_major_formatter(FuncFormatter(_format_log_tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, color='0.88', linestyle=':', linewidth=0.55)
    ax.set_axisbelow(True)

    ax.set_title('Country-specific cross-objective penalties',
                 fontsize=12, fontweight='bold', pad=6)
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
    ax.legend(frameon=False, fontsize=8, loc='upper right',
              bbox_to_anchor=(1, 1.04), handlelength=2.2, ncol = 2)

    return fig, axes
