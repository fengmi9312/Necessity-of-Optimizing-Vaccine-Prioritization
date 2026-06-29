# -*- coding: utf-8 -*-
"""
Country infection necessity against the fitted R0 landscape.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter

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


def _format_log_tick(value, pos):
    if value <= 0:
        return ''
    if np.isclose(value, 1):
        return r'$10^0$'
    if any(np.isclose(value, tick) for tick in [2, 4, 6]):
        return fr'${int(value)} \times 10^0$'
    return ''


def draw(anal_data, **kwargs):
    target = kwargs.pop('target', 'd')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    param_idx = kwargs.pop('param_idx', 28)
    country_for_landscape = kwargs.pop('country', 'United States')
    country_data = param_data_loader.load_all_data(
        basic_params.country_abbr.keys(),
        basic_params.group_div,
    )
    
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (34, 24)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    ax = axes[0][0]
    plt.sca(ax)

    spine_linewidth = 0.8
    label_fontsize = 10
    tick_fontsize = 8

    r0_mean, r0_lower, r0_upper = [], [], []
    necs_mean, necs_lower, necs_upper = [], [], []
    sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"

    for country in COUNTRIES:
        ifr_mean = country_data[country]['populations'] @ country_data[country]['ifrs']
        r0_stats = _mean_ci(anal_data['necs_from_country_140']['r0'][country])
        r0_mean.append(r0_stats[0])
        r0_lower.append(r0_stats[1])
        r0_upper.append(r0_stats[2])

        necs_key = f'{country}_none_necs'
        necs_stats = _mean_ci(anal_data['necs_from_country_140'][sheet_name][necs_key] * 100)
        necs_mean.append(necs_stats[0] / ifr_mean)
        necs_lower.append(necs_stats[1] / ifr_mean)
        necs_upper.append(necs_stats[2] / ifr_mean)

    r0_mean = np.asarray(r0_mean)
    r0_lower = np.asarray(r0_lower)
    r0_upper = np.asarray(r0_upper)
    necs_mean = np.asarray(necs_mean)
    necs_lower = np.asarray(necs_lower)
    necs_upper = np.asarray(necs_upper)

    x = np.exp(np.arange(40) * 3 / 40)
    country_abbr = basic_params.country_abbr[country_for_landscape]
    landscape_key = (
        f"necs_from_param_(delay)-{country_abbr}_{target}_{acc_type}"
        f"{'_dur' if dur else ''}_necs"
    )
    landscape = anal_data['necs_from_r0_factor'][landscape_key][param_idx] * 100 / (country_data['United States']['populations'] @ country_data['United States']['ifrs'])
    ax.plot(x, landscape, color='0.55', linewidth=1.15, label='Theoretical landscape',
            zorder=1)

    blue = '#2F80ED'
    ax.errorbar(
        r0_mean,
        necs_mean,
        xerr=[r0_mean - r0_lower, r0_upper - r0_mean],
        yerr=[necs_mean - necs_lower, necs_upper - necs_mean],
        fmt='o',
        color=blue,
        ecolor='#8AB8FF',
        elinewidth=0.8,
        capsize=2,
        capthick=0.8,
        markersize=3.6,
        markeredgewidth=0.4,
        markeredgecolor=blue,
        markerfacecolor=blue,
        zorder=3,
    )

    main_label_offsets = {
        'Ireland': (0.02, 1.0),
        'United States': (-0.15, -1.0),
        'Spain': (-0.18, 0.7),
        'Austria': (0.06, 0.4),
        'Israel': (-0.27, -0.9),
        'South Korea': (0.04, 0.9),
    }
    for country, x_val, y_val in zip(COUNTRIES, r0_mean, necs_mean):
        if country not in main_label_offsets:
            continue
        dx, dy = main_label_offsets[country]
        label_x = x_val + dx
        label_y = y_val + dy
        ax.text(label_x, label_y, COUNTRY_LABELS[country], fontsize=6,
                color='0.25', ha='left', va='center', zorder=4)

    cluster_countries = {'Japan', 'United Kingdom', 'France', 'Germany'}
    axins = ax.inset_axes([0.60, 0.54, 0.30, 0.27])
    axins.errorbar(
        r0_mean,
        necs_mean,
        xerr=[r0_mean - r0_lower, r0_upper - r0_mean],
        yerr=[necs_mean - necs_lower, necs_upper - necs_mean],
        fmt='o',
        color=blue,
        ecolor='#8AB8FF',
        elinewidth=0.65,
        capsize=1.6,
        capthick=0.65,
        markersize=2.8,
        markeredgewidth=0.35,
        markeredgecolor=blue,
        markerfacecolor=blue,
        zorder=3,
    )
    zoom_x0, zoom_x1 = 1.55, 2.15
    zoom_y0, zoom_y1 = 12.2, 17.25
    axins.set_xlim(zoom_x0, zoom_x1)
    axins.set_ylim(zoom_y0, zoom_y1)
    axins.grid(True, color='0.9', linestyle=':', linewidth=0.45)
    axins.tick_params(axis='both', which='major', labelsize=5, length=2, width=0.5, pad=1)
    for spine in axins.spines.values():
        spine.set_linewidth(0.6)
        spine.set_color('0.35')
    cluster_label_offsets = {
        'Japan': (-0.12, -0.75),
        'United Kingdom': (-0.06, 0.95),
        'France': (0.05, 0.45),
        'Germany': (0.04, -0.65),
    }
    for country, x_val, y_val in zip(COUNTRIES, r0_mean, necs_mean):
        if country not in cluster_countries:
            continue
        dx, dy = cluster_label_offsets[country]
        axins.text(x_val + dx, y_val + dy, COUNTRY_LABELS[country], fontsize=5.4,
                   color='0.25', ha='left', va='center',
                   bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 0.2,
                         'alpha': 0.85},
                   zorder=4)

    
    ax.add_patch(Rectangle(
        (zoom_x0, zoom_y0),
        zoom_x1 - zoom_x0,
        zoom_y1 - zoom_y0,
        fill=False,
        linestyle=':',
        linewidth=0.5,
        edgecolor='k',
        alpha=0.65,
        zorder=2,
    ))
    fig.add_artist(ConnectionPatch(
        xyA=(zoom_x1, zoom_y1),
        coordsA=ax.transData,
        xyB=(0, 1),
        coordsB=axins.transAxes,
        color='k',
        linestyle=':',
        linewidth=0.5,
        alpha=0.6,
        zorder=2,
    ))
    fig.add_artist(ConnectionPatch(
        xyA=(zoom_x1, zoom_y0),
        coordsA=ax.transData,
        xyB=(0, 0),
        coordsB=axins.transAxes,
        color='k',
        linestyle=':',
        linewidth=0.5,
        alpha=0.6,
        zorder=2,
    ))

    # ax.annotate(
    #     'country estimates mainly\noccupy the descending branch',
    #     xy=(2.55, 10.3),
    #     xytext=(3.0, 15.5),
    #     fontsize=6,
    #     color='0.25',
    #     arrowprops={'arrowstyle': '->', 'linewidth': 0.7, 'color': '0.25',
    #                 'shrinkA': 0, 'shrinkB': 2},
    #     ha='left',
    #     va='center',
    # )

    ax.set_xscale('log')
    ax.set_xlim(1, 6.3)
    ax.set_ylim(0, 25)
    ax.set_yticks(np.arange(0, 26, 5))
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1, 2, 3, 4, 5, 6)))
    ax.xaxis.set_major_formatter(FuncFormatter(_format_log_tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, color='0.88', linestyle=':', linewidth=0.55)
    ax.set_axisbelow(True)

    ax.set_title('Country-specific necessity for minimizing\n'r'cumulative infections on $R_0$ landscape',
                 fontsize=12, fontweight='bold', pad=6)
    figure_setting.set_xylabel(
        ax,
        r'Estimated $R_0$',
        r'$\mathcal{N}_{\mathrm{d}} / \tilde{\chi}_{\mathrm{d}}^{\mathrm{all}}$ (%)',
        fontsize=label_fontsize,
        xlabel_coords=-0.11,
        ylabel_coords=-0.08,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    ax.legend(frameon=False, fontsize=8, loc='upper right', handlelength=2.2)

    return fig, axes
