# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt

from Dependencies.CodeDependencies import basic_params
from .figure_dependencies import figure_setting


RED = '#D43732'
BLUE = '#2B69B7'


def _necs_slice(anal_data, target, d_roll_idx):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_(param)'
    sheet_name = (
        f'{task_name}-{basic_params.country_abbr[country]}_'
        f'{target}_dd_necs'
    )
    return np.asarray(anal_data['necs_from_r0_time_course'][sheet_name]).T[d_roll_idx] * 100


def _necs_slice_ref(anal_data, target, c_perct_idx):
    country = 'United States'
    task_name = 'necs_from_param_(c_perct)'
    sheet_name = (
        f'{task_name}-{basic_params.country_abbr[country]}_'
        f'{target}_dd_necs'
    )
    return np.asarray(anal_data['necs_from_r0_factor'][sheet_name]).T[c_perct_idx] * 100


def _xi_slice(anal_data, target, d_roll_idx):
    country = 'United States'
    task_name = 'necs_from_time_course_fixd_(param)'
    sheet_name = f'{task_name}_{target}_{d_roll_idx}_{basic_params.country_abbr[country]}'
    corr_data = anal_data['corr_from_r0_time_course'][sheet_name]
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


def _xi_slice_ref(anal_data, target, c_perct_idx):
    country = 'United States'
    task_name = 'necs_from_param_(c_perct)'
    sheet_name = f'{task_name}_{target}_{c_perct_idx}_{basic_params.country_abbr[country]}'
    corr_data = anal_data['corr_from_r0_factor'][sheet_name]
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


def _set_line_ylim(ax, values, target):
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


def _set_xi_ylim(ax, *xi_values):
    values = np.concatenate(xi_values)
    bound = max(0.2, np.nanmax(np.abs(values)) * 1.08)
    bound = min(1.05, np.ceil(bound * 10) / 10)
    ax.set_ylim(-bound, bound)
    ax.spines['left'].set_bounds(-bound, bound)
    ax.set_yticks(np.linspace(-bound, bound, 5))


def draw(anal_data, **kwargs):
    d_roll = kwargs.pop('d_roll', 28)
    c_perct_idx = kwargs.pop('c_perct_idx', 1)
    d_roll_idx = d_roll - 2
    if not 0 <= d_roll_idx < 40:
        raise ValueError('d_roll must be between 2 and 41')

    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (18, 12)},
                   {'pos': (24, 0), 'size': (18, 12)}],
                  [{'pos': (0, 18), 'size': (18, 12)},
                   {'pos': (24, 18), 'size': (18, 12)}]]
    margin_attr = {'top': 5, 'bottom': 5, 'left': 7, 'right': 2}
    removed_labels = {
        'x': [(0, 0), (0, 1)],
        'y': [],
        'xtick': [],
        'ytick': [],
    }
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)

    spine_linewidth = 1.5
    label_fontsize = 11
    tick_fontsize = 9
    text_fontsize = 10

    x = np.exp(np.arange(40) * 3 / 40)
    targets = ['c', 'd']
    row_labels = {
        'c': rf'Cumulative infections ($\mathcal{{D}}_{{\mathrm{{roll}}}}={d_roll}$)',
        'd': rf'Deaths ($\mathcal{{D}}_{{\mathrm{{roll}}}}={d_roll}$)',
    }
    ylabels = {
        'c': r'$\mathcal{N}_{\mathrm{c}}$ (%)',
        'd': r'$\mathcal{N}_{\mathrm{d}}$ (%)',
    }

    for row_idx, target in enumerate(targets):
        necs = _necs_slice(anal_data, target, d_roll_idx)
        necs_ref = _necs_slice_ref(anal_data, target, c_perct_idx)
        xi_opt, xi_worst = _xi_slice(anal_data, target, d_roll_idx)
        xi_opt_ref, xi_worst_ref = _xi_slice_ref(anal_data, target, c_perct_idx)

        ax = axes[row_idx][0]
        plt.sca(ax)
        ax.plot(
            x,
            necs,
            linewidth=2.5,
            color='tab:orange',
            label='Time-course',
        )
        ax.plot(
            x,
            necs_ref,
            linewidth=2.5,
            linestyle='--',
            color='tab:gray',
            alpha = 0.75,
            label='Comparable one-time',
        )
        ax.text(
            0.03,
            1.15,
            row_labels[target],
            ha='left',
            va='top',
            fontsize=text_fontsize,
            transform=ax.transAxes,
        )
        ax.set_xscale('log')
        _set_line_ylim(ax, np.concatenate([necs, necs_ref]), target)
        figure_setting.set_xylabel(
            ax,
            r'$R_0$',
            ylabels[target],
            fontsize=label_fontsize,
            xlabel_coords=-0.15 if target == 'c' else -0.18,
            ylabel_coords=-0.14 if target == 'c' else -0.18,
        )
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        if row_idx == 0:
            ax.legend(
                loc='lower center',
                fontsize=7,
                bbox_to_anchor=(0.5, 1.13),
                ncol=2,
                columnspacing=0.9,
                handletextpad=0.4,
                handlelength=3.2,
            )
       

        ax = axes[row_idx][1]
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
            alpha=0.35,
            label='Burden-maximizing',
        )
        ax.plot(
            x,
            xi_opt_ref,
            linestyle='',
            marker='x',
            markeredgecolor='tab:green',
            markersize=3.2,
            markeredgewidth=1.0,
            alpha=0.35,
            label='Comparable optimal',
            zorder = 0
        )
        ax.plot(
            x,
            xi_worst_ref,
            linestyle='',
            marker='o',
            markerfacecolor='white',
            markeredgecolor='tab:orange',
            markersize=3.2,
            markeredgewidth=1.0,
            alpha=0.25,
            label='Comparable burden-maximizing',
            zorder = 0
        )
        ax.text(
            0.03,
            1.15,
            row_labels[target],
            ha='left',
            va='top',
            fontsize=text_fontsize,
            transform=ax.transAxes,
        )
        ax.axhline(0, 0, 1, linestyle=':', color='tab:gray', linewidth=1)
        ax.set_xscale('log')
        _set_xi_ylim(ax, xi_opt, xi_worst, xi_opt_ref, xi_worst_ref)
        figure_setting.set_xylabel(
            ax,
            r'$R_0$',
            r'$\xi$',
            fontsize=label_fontsize,
            xlabel_coords=-0.2,
            ylabel_coords=-0.2,
        )
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        if row_idx == 0:
            leg = ax.legend(
                loc='lower center',
                fontsize=7,
                bbox_to_anchor=(0.45, 1.13),
                ncol=2,
                columnspacing=0.7,
                handletextpad=0.4,
            )
            for handle in leg.legend_handles:
                handle.set_markersize(5)
                handle.set_markeredgewidth(1.5)

    figure_setting.remove_labels(axes, removed_labels)
    return fig, axes
