# -*- coding: utf-8 -*-
"""
Plot cross-objective penalties and allocation correlations for contact and
population profile perturbations.
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
from itertools import combinations

from Dependencies.CodeDependencies import basic_params
from Dependencies.CodeDependencies.param_data_loader import load_all_data
from . import figure_setting


def _safe_zero_contour(ax, x, y, z, **kwargs):
    z = np.asarray(z, dtype=float)
    valid = np.isfinite(z)
    if not valid.any() or not (np.nanmin(z) <= 0 <= np.nanmax(z)):
        return None
    return ax.contour(x, y, z, levels=[0], **kwargs)


def _contour_midpoints(cs):
    segments = [seg for seg in cs.allsegs[0] if len(seg) >= 2]
    if not segments:
        return []

    def segment_length(seg):
        # Use log-x distance because these panels are shown on a log x-axis.
        dx = np.diff(np.log(seg[:, 0]))
        dy = np.diff(seg[:, 1])
        return np.sqrt(dx ** 2 + dy ** 2)

    midpoints = []
    for seg in segments:
        lengths = segment_length(seg)
        total_length = lengths.sum()
        if total_length == 0:
            midpoints.append(tuple(seg[len(seg) // 2]))
            continue

        midpoint = total_length / 2
        cumulative = np.concatenate([[0], np.cumsum(lengths)])
        idx = np.searchsorted(cumulative, midpoint, side='right') - 1
        idx = min(max(idx, 0), len(lengths) - 1)
        interval_length = cumulative[idx + 1] - cumulative[idx]
        frac = 0 if interval_length == 0 else (midpoint - cumulative[idx]) / interval_length
        point = seg[idx] + frac * (seg[idx + 1] - seg[idx])
        midpoints.append(tuple(point))
    return midpoints


def _label_contour_midpoint(ax, cs, fontsize=10):
    midpoints = _contour_midpoints(cs)
    if not midpoints:
        return
    ax.clabel(
        cs,
        fontsize=fontsize,
        fmt=lambda value: rf'$\theta = {0 if value == 0 else np.round(value, 1)}$',
        manual=midpoints,
    )


def _contact_xy(expr_param):
    country_data = load_all_data(['United States'], basic_params.group_div)
    contacts = country_data['United States']['contacts']
    populations = country_data['United States']['populations']
    contact_regions = ['home', 'school', 'work', 'other_locations']
    coef_pos_list = []
    for r in range(1, 4):
        for combo in combinations(range(len(contact_regions)), r):
            coef_pos_list.append(list(combo))

    x_base = np.exp(np.arange(40) * 3 / 40)
    y_idx = np.arange(40)
    y = y_idx / 39
    coef_pos = coef_pos_list[int(expr_param)]
    x_rows = []
    for param_val in y:
        contacts_total = np.array([contacts[region] for region in contact_regions])
        original_radius = np.max(np.linalg.eig(populations[None, :] * contacts_total.sum(axis=0))[0])
        contacts_total[coef_pos] *= param_val
        adjusted_radius = np.max(np.linalg.eig(populations[None, :] * contacts_total.sum(axis=0))[0])
        x_rows.append(x_base * adjusted_radius / original_radius)
    Y = np.array([39 - y_idx for _ in range(40)]).T
    return np.asarray(x_rows), Y


def _contact_penalty(anal_data, expr_param, target):
    anal_name = 'necs_from_r0_factor'
    country_abbr = basic_params.country_abbr['United States']
    task_name = f'necs_from_contact_({expr_param})'
    pre = f'{task_name}-{country_abbr}_{target}_dd'
    min_val = anal_data[anal_name][f'{pre}_min'].to_numpy()
    anti_min_val = anal_data[anal_name][f'{pre}_anti_min'].to_numpy()
    no_vac_val = anal_data[anal_name][f'{pre}_no_vac'].to_numpy()
    z = ((anti_min_val - min_val) / (no_vac_val - min_val)).T

    return z


def _contact_alloc_corr(anal_data, expr_param):
    anal_name = 'corr_from_r0_factor'
    country_abbr = basic_params.country_abbr['United States']
    task_name = f'necs_from_contact_({expr_param})'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{param_idx}_{country_abbr}'
        z.append(anal_data[anal_name][sheet_name]['alloc_corr'])
    return np.asarray(z, dtype=float)


def _contact_xi(anal_data, expr_param, target):
    anal_name = 'corr_from_r0_factor'
    country_abbr = basic_params.country_abbr['United States']
    task_name = f'necs_from_contact_({expr_param})'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{country_abbr}'
        corr_data = anal_data[anal_name][sheet_name]
        z.append(
            (np.arccos(corr_data['optimal_dirx']) -
             np.arccos(corr_data['optimal_indx'])) /
            np.arccos(corr_data['effect_corrx'])
        )
    return np.asarray(z, dtype=float)


def _population_penalty(anal_data, target):
    anal_name = 'necs_from_r0_populations'
    country_abbr = basic_params.country_abbr['United States']
    task_name = 'necs_from_populations_(param)'
    pre = f'{task_name}-{country_abbr}_{target}_dd'
    min_val = anal_data[anal_name][f'{pre}_min'].to_numpy()
    anti_min_val = anal_data[anal_name][f'{pre}_anti_min'].to_numpy()
    no_vac_val = anal_data[anal_name][f'{pre}_no_vac'].to_numpy()
    return ((anti_min_val - min_val) / (no_vac_val - min_val)).T


def _population_alloc_corr(anal_data):
    anal_name = 'corr_from_r0_populations'
    country_abbr = basic_params.country_abbr['United States']
    task_name = 'necs_from_populations_(param)'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{param_idx}_{country_abbr}'
        z.append(anal_data[anal_name][sheet_name]['alloc_corr'])
    return np.asarray(z, dtype=float)


def _population_xi(anal_data, target):
    anal_name = 'corr_from_r0_populations'
    country_abbr = basic_params.country_abbr['United States']
    task_name = 'necs_from_populations_(param)'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{country_abbr}'
        corr_data = anal_data[anal_name][sheet_name]
        z.append(
            (np.arccos(corr_data['optimal_dirx']) -
             np.arccos(corr_data['optimal_indx'])) /
            np.arccos(corr_data['effect_corrx'])
        )
    return np.asarray(z, dtype=float)


def _format_contact_axis(ax, label_fontsize, tick_fontsize, spine_linewidth):
    ax.set_xscale('log')
    ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    figure_setting.set_xylabel(
        ax,
        r'$R_0$',
        r'Contact-closure level, $\varrho$',
        fontsize=label_fontsize,
        xlabel_coords=-0.14,
        ylabel_coords=-0.16,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)


def _format_population_axis(ax, label_fontsize, tick_fontsize, spine_linewidth):
    ax.set_xscale('log')
    ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    figure_setting.set_xylabel(
        ax,
        r'$R_0$',
        r'Age-profile center, $o_{\rho}$',
        fontsize=label_fontsize,
        xlabel_coords=-0.14,
        ylabel_coords=-0.16,
    )
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)


def _add_cbar(fig, cax, mesh, title, spine_linewidth, tick_fontsize):
    cbar = fig.colorbar(mesh, cax=cax)
    cbar.ax.set_title(title, pad=6, fontsize=10)
    cbar.ax.tick_params(labelsize=6.4)
    figure_setting.set_cbar_spine_linewidth(cbar, spine_linewidth)
    figure_setting.set_tick_fontsize(cbar.ax, tick_fontsize)


def draw_contact_penalty(anal_data, expr_param, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', True))
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (18, 72)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 4, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9
    overlap = 0.75
    edge_width = 1
    X, Y = _contact_xy(expr_param)
    x_rows = X[::-1]
    zc = _contact_penalty(anal_data, expr_param, 'c')[::-1]
    zd = _contact_penalty(anal_data, expr_param, 'd')[::-1]
    theta = _contact_alloc_corr(anal_data, expr_param)[::-1]

    ax = axes[0][0]
    plt.sca(ax)
    deep_colors = sns.color_palette('deep')
    x_left = np.nanmin(x_rows) * 0.78
    for idx in range(zc.shape[0]):
        base = idx * overlap
        x = x_rows[idx]
        ax.fill_between(
            x,
            zc[idx] + base,
            np.ones_like(x) * base,
            zorder=zc.shape[0] - idx + 1,
            color=deep_colors[2],
            alpha=0.65,
            linewidth=0,
            label=r'$\Phi_{\mathrm{c}}^{(\mathrm{d})}$' if idx == 0 else None,
        )
        ax.plot(x, zc[idx] + base, color=deep_colors[2], zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.plot(x, np.ones_like(x) * base, color='tab:gray', zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.fill_between(
            x,
            zd[idx] + base,
            np.ones_like(x) * base,
            zorder=zc.shape[0] - idx + 1,
            color=deep_colors[1],
            alpha=0.65,
            linewidth=0,
            label=r'$\Phi_{\mathrm{d}}^{(\mathrm{c})}$' if idx == 0 else None,
        )
        ax.plot(x, zd[idx] + base, color=deep_colors[1], zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.plot(x, np.ones_like(x) * base, color='tab:gray', zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        if idx in [0, 13, 26, 39]:
            label = ['0', '1/3', '2/3', '1'][idx // 13]
            ax.text(
                x[0] * 0.92,
                base,
                rf'$\varrho = {label}$',
                fontsize=7,
                color='black',
                ha='right',
                va='bottom',
                transform=ax.transData,
                clip_on=False,
            )

    contour_y = np.array([np.ones(theta.shape[1]) * idx * overlap for idx in range(theta.shape[0])])
    _safe_zero_contour(
        ax,
        x_rows,
        contour_y,
        theta,
        colors='tab:gray',
        linestyles='--',
        linewidths=1.5,
        zorder=100,
    )
    handles, labels = ax.get_legend_handles_labels()
    handles.append(mlines.Line2D([], [], color='tab:gray', linestyle='--', linewidth=1.5))
    labels.append(r'$\theta = 0$')
    ax.set_xscale('log')
    ax.set_xlim(left=x_left)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin=-0.1)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    figure_setting.set_xylabel(ax, r'$R_0$', None, fontsize=label_fontsize, xlabel_coords=-0.03, ylabel_coords=-0.22)
    if show_legend:
        ax.legend(handles=handles, labels=labels, loc='upper center', fontsize=8, bbox_to_anchor=(0.4, 1.01), ncol=3)
    return fig, axes


def draw_contact_alloc_corr(anal_data, expr_param, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', True))
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 20)},
                   {'pos': (22, 0), 'size': (2, 20)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 4}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 14
    tick_fontsize = 9
    X, Y = _contact_xy(expr_param)
    z = _contact_alloc_corr(anal_data, expr_param)
    original_cmap = sns.color_palette('Blues', as_cmap=True)
    colors = original_cmap(np.linspace(0, 0.6, 256))

    ax = axes[0][0]
    plt.sca(ax)
    mesh = ax.pcolormesh(X[::-1], Y[::-1], z[::-1], cmap=mcolors.ListedColormap(colors), shading='auto')
    theta_cs = _safe_zero_contour(
        ax,
        X[::-1],
        Y[::-1],
        z[::-1],
        colors='black',
        linestyles='solid',
        linewidths=1.2,
        zorder=10,
    )
    if theta_cs is not None:
        _label_contour_midpoint(ax, theta_cs, fontsize=10)

    markers = {'c': 'x', 'd': 'o'}
    colors_obj = {'c': sns.color_palette('deep')[2], 'd': sns.color_palette('deep')[1]}
    for target in ['c', 'd']:
        xi_z = _contact_xi(anal_data, expr_param, target)
        xi_cs = _safe_zero_contour(
            ax,
            X[::-1],
            Y[::-1],
            xi_z[::-1],
            colors=colors_obj[target],
            linestyles='solid',
            linewidths=0,
            zorder=11,
        )
        if xi_cs is not None:
            for seg_idx, seg in enumerate(xi_cs.allsegs[0]):
                ax.plot(
                    seg[:, 0],
                    seg[:, 1],
                    linestyle='',
                    marker=markers[target],
                    markevery=3,
                    color=colors_obj[target],
                    markerfacecolor='none',
                    markeredgewidth=1.1,
                    label=rf'$\xi_{{\mathrm{{{target}}}}}=0$' if seg_idx == 0 else None,
                )

    # ax.set_title(r'Allocation correlation ($\theta$)', fontsize=14, pad=8)
    _format_contact_axis(ax, label_fontsize, tick_fontsize, spine_linewidth)
    if show_legend:
        ax.legend(loc='lower left', fontsize=8, bbox_to_anchor=(0, 1.01), ncol=2)
    _add_cbar(fig, axes[0][1], mesh, r'$\theta$', spine_linewidth, tick_fontsize)
    return fig, axes


def draw_population_penalty(anal_data, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', True))
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (18, 72)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 4, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 9
    overlap = 0.75
    edge_width = 1
    x = np.exp(np.arange(40) * 3 / 40)
    zc = _population_penalty(anal_data, 'c')
    zd = _population_penalty(anal_data, 'd')
    theta = _population_alloc_corr(anal_data)

    ax = axes[0][0]
    plt.sca(ax)
    deep_colors = sns.color_palette('deep')
    x_left = np.nanmin(x) * 0.78
    for idx in range(zc.shape[0]):
        base = idx * overlap
        ax.fill_between(
            x,
            zc[idx] + base,
            np.ones_like(x) * base,
            zorder=zc.shape[0] - idx + 1,
            color=deep_colors[2],
            alpha=0.65,
            linewidth=0,
            label=r'$\Phi_{\mathrm{c}}^{(\mathrm{d})}$' if idx == 0 else None,
        )
        ax.plot(x, zc[idx] + base, color=deep_colors[2], zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.plot(x, np.ones_like(x) * base, color='tab:gray', zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.fill_between(
            x,
            zd[idx] + base,
            np.ones_like(x) * base,
            zorder=zc.shape[0] - idx + 1,
            color=deep_colors[1],
            alpha=0.65,
            linewidth=0,
            label=r'$\Phi_{\mathrm{d}}^{(\mathrm{c})}$' if idx == 0 else None,
        )
        ax.plot(x, zd[idx] + base, color=deep_colors[1], zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        ax.plot(x, np.ones_like(x) * base, color='tab:gray', zorder=zc.shape[0] - idx + 1, linewidth=edge_width)
        if idx in [0, 13, 26, 39]:
            label = ['0', '1/3', '2/3', '1'][idx // 13]
            ax.text(
                x[0] * 0.92,
                base,
                rf'$o_{{\rho}} = {label}$',
                fontsize=7,
                color='black',
                ha='right',
                va='bottom',
                transform=ax.transData,
                clip_on=False,
            )

    X, Y = np.meshgrid(x, np.arange(theta.shape[0]) * overlap)
    _safe_zero_contour(
        ax,
        X,
        Y,
        theta,
        colors='tab:gray',
        linestyles='--',
        linewidths=1.5,
        zorder=100,
    )
    handles, labels = ax.get_legend_handles_labels()
    handles.append(mlines.Line2D([], [], color='tab:gray', linestyle='--', linewidth=1.5))
    labels.append(r'$\theta = 0$')
    ax.set_xscale('log')
    ax.set_xlim(left=x_left)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin=-0.1)
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    figure_setting.set_xylabel(ax, r'$R_0$', None, fontsize=label_fontsize, xlabel_coords=-0.03, ylabel_coords=-0.22)
    if show_legend:
        ax.legend(handles=handles, labels=labels, loc='upper center', fontsize=8, bbox_to_anchor=(0.4, 1.01), ncol=3)
    return fig, axes


def draw_population_alloc_corr(anal_data, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', True))
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 20)},
                   {'pos': (22, 0), 'size': (2, 20)}]]
    margin_attr = {'top': 3, 'bottom': 5, 'left': 7, 'right': 4}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1
    label_fontsize = 14
    tick_fontsize = 9
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    X, Y = np.meshgrid(x, y)
    z = _population_alloc_corr(anal_data)
    original_cmap = sns.color_palette('Blues', as_cmap=True)
    colors = original_cmap(np.linspace(0, 0.6, 256))

    ax = axes[0][0]
    plt.sca(ax)
    mesh = ax.pcolormesh(x, y, z, cmap=mcolors.ListedColormap(colors), shading='auto')
    theta_cs = _safe_zero_contour(
        ax,
        X,
        Y,
        z,
        colors='black',
        linestyles='solid',
        linewidths=1.2,
        zorder=10,
    )
    if theta_cs is not None:
        _label_contour_midpoint(ax, theta_cs, fontsize=10)

    markers = {'c': 'x', 'd': 'o'}
    colors_obj = {'c': sns.color_palette('deep')[2], 'd': sns.color_palette('deep')[1]}
    for target in ['c', 'd']:
        xi_z = _population_xi(anal_data, target)
        xi_cs = _safe_zero_contour(
            ax,
            X,
            Y,
            xi_z,
            colors=colors_obj[target],
            linestyles='solid',
            linewidths=0,
            zorder=11,
        )
        if xi_cs is not None:
            for seg_idx, seg in enumerate(xi_cs.allsegs[0]):
                ax.plot(
                    seg[:, 0],
                    seg[:, 1],
                    linestyle='',
                    marker=markers[target],
                    markevery=3,
                    color=colors_obj[target],
                    markerfacecolor='none',
                    markeredgewidth=1.1,
                    label=rf'$\xi_{{\mathrm{{{target}}}}}=0$' if seg_idx == 0 else None,
                )

    # ax.set_title(r'Allocation correlation ($\theta$)', fontsize=14, pad=8)
    _format_population_axis(ax, label_fontsize, tick_fontsize, spine_linewidth)
    if show_legend:
        ax.legend(loc='lower left', fontsize=8, bbox_to_anchor=(0, 1.01), ncol=2)
    _add_cbar(fig, axes[0][1], mesh, r'$\theta$', spine_linewidth, tick_fontsize)
    return fig, axes
