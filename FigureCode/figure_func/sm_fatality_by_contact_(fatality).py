# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:31:46 2026

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
from Dependencies.CodeDependencies import basic_params
from Dependencies.CodeDependencies.param_data_loader import load_all_data

def assign_by_rank(a, b, b_ascending=True, stable=True):
    a = np.asarray(a)
    b = np.asarray(b)
    if a.shape != b.shape:
        raise ValueError("a 和 b 的形状必须相同且为一维。")

    # b 的排序索引
    kind = "stable" if stable else "quicksort"
    idx = np.argsort(b, kind=kind)
    if not b_ascending:
        idx = idx[::-1]

    # a 的有序值（这里用升序；如果你想让 a 与 b 同步降升，可以改成条件翻转）
    a_sorted = np.sort(a)

    # 把 a_sorted 依次放入 b 的排序位置上
    c = np.empty_like(a_sorted)
    c[idx] = a_sorted
    return c


def draw(anal_data):
    ####################################################
    scale_prop = 12
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (20, 0), 'size': (15, 10)}, {'pos': (40, 0), 'size': (15, 10)}, {'pos': (60, 0), 'size': (15, 10)}],]
    margin_attr = {'top': 3, 'bottom': 8, 'left': 6, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ####################################################
    spine_linewidth = 1.5
    label_fontsize = 10
    tick_fontsize = 8
    text_fontsize = 9
    ####################################################
    
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    contacts = np.sum([country_data['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    prdt_weights = assign_by_rank(country_data['United States']['ifrs'], contacts.sum(axis = 1))
    equal_weights = np.ones(basic_params.group_amount) * prdt_weights.sum() / basic_params.group_amount
    diff_weights = prdt_weights - equal_weights
    
    for ax_idx in range(4):
        weights_arr = equal_weights + ax_idx * diff_weights / 3
        ax = axes[0][ax_idx]
        plt.sca(ax)
        plt.bar(np.arange(16), weights_arr * 100, color = 'tab:gray', width = 0.8, edgecolor='k', linewidth = 1)
        ax.set_ylim(0, 25)
        ax.spines['left'].set_bounds(0, 25)
        ax.set_yticks(np.arange(0, 26, 5))
        figure_setting.set_xylabel(ax, 'Age group', 'IFR (%)', fontsize = label_fontsize, xlabel_coords = -0.3, ylabel_coords = -0.15)
        figure_setting.remove_spines(ax, ['top', 'right'])
        figure_setting.set_spine_linewidth(ax, spine_linewidth)
        figure_setting.set_tick_fontsize(ax, tick_fontsize)
        plt.xticks(rotation = 90, fontsize = label_fontsize * 0.6)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.tick_params(axis='x', which='major', pad=1)
        ax.text(0.03, 0.97, f"$\\gamma^* = {ax_idx} / 3$" if ax_idx != 0 and ax_idx != 3 else f"$\\gamma^* = {int(ax_idx / 3)}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes, math_fontfamily = 'cm')
    
    return fig, axes