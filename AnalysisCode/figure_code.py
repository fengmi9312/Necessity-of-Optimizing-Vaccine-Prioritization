# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:29:35 2025

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import basic_params
from data_loader import load_all_data
import itertools
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches
from matplotlib.transforms import blended_transform_factory
import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
unit = 1
dpi = plt.rcParams['figure.dpi']
from itertools import chain
data_of_countries = load_all_data(['United States', 'United Kingdom', 'Ireland', 'France', 'Germany', 'Spain', 'Austria', 'Israel', 'Japan', 'South Korea'], basic_params.group_div)

def gererate_grid(grid_attrs, margin_attr, scale_prop, shape_prop = 1, dpi = dpi, unit = unit, d_list = []):
    grid_row, grid_col = margin_attr['left'], margin_attr['top']
    for grid_attr in list(chain.from_iterable(grid_attrs)):
        if margin_attr['left'] + grid_attr['pos'][0] + grid_attr['size'][0] > grid_row: grid_row = margin_attr['left'] + grid_attr['pos'][0] + grid_attr['size'][0]
        if margin_attr['top'] + grid_attr['pos'][1] + grid_attr['size'][1] > grid_col: grid_col = margin_attr['top'] + grid_attr['pos'][1] + grid_attr['size'][1]
    grid_row += margin_attr['right']
    grid_col += margin_attr['bottom']
    fig = plt.figure(figsize = [grid_row * scale_prop * shape_prop * unit / dpi, grid_col * scale_prop * unit / dpi])
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    for i, grid_attr_arr in enumerate(grid_attrs):
        axes.append([])
        for j, grid_attr in enumerate(grid_attr_arr):
            axes[-1].append(fig.add_subplot(gs[margin_attr['top'] + grid_attr['pos'][1]:margin_attr['top'] + grid_attr['pos'][1] + grid_attr['size'][1], 
                                               margin_attr['left'] + grid_attr['pos'][0]:margin_attr['left'] + grid_attr['pos'][0] + grid_attr['size'][0]], projection = '3d' if (i, j) in d_list else None))
    plt.subplots_adjust(top = 1, bottom = 0, left = 0, right = 1,  hspace = 0, wspace = 0) 
    return fig, axes





def set_xylabel(ax, xlabel, ylabel, fontsize, xlabel_coords = None, ylabel_coords = None):
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_ylabel(ylabel, fontsize = fontsize)
    if xlabel_coords is not None:
        ax.xaxis.set_label_coords(0.5, xlabel_coords, transform = ax.transAxes)
    if ylabel_coords is not None:
        ax.yaxis.set_label_coords(ylabel_coords, 0.5, transform = ax.transAxes)
    return ax

def set_spine_linewidth(ax, linewidth):
    ax.spines['left'].set_linewidth(linewidth)
    ax.spines['right'].set_linewidth(linewidth)
    ax.spines['bottom'].set_linewidth(linewidth)
    ax.spines['top'].set_linewidth(linewidth) 
    ax.tick_params('both', which='major', width = linewidth)
    ax.tick_params('both', which='minor', width = linewidth)
    return ax   

def set_cbar_spine_linewidth(cbar, linewidth):
    cbar.outline.set_linewidth(linewidth)
    cbar.ax.tick_params('y', width = linewidth, length = 4 * linewidth, pad = 2 * linewidth)
    return cbar 
        
def set_tick_fontsize(ax, fontsize):
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    return ax

def remove_labels(axes, idxes):
    for row_idx, ax_row in enumerate(axes):
        for col_idx, ax in enumerate(ax_row):
            if (row_idx, col_idx) in idxes['x']: ax.set_xlabel(None)
            if (row_idx, col_idx) in idxes['y']: ax.set_ylabel(None)
            if (row_idx, col_idx) in idxes['xtick']: ax.set_xticklabels([])
            if (row_idx, col_idx) in idxes['ytick']: ax.set_yticklabels([])

def remove_spines(ax, spines):
    ax.spines[spines].set_visible(False)
    if 'left' in spines: ax.set_yticks([])
    if 'bottom' in spines: ax. set_xticks([])
    return ax

def remove_all_spines(ax):
    ax.spines[['left', 'right', 'top', 'bottom']].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def cut_line(x, y):
    p_mark = 0
    x_res, y_res = [], []
    for idx in range(len(x) - 1):
        if abs((y[idx] - y[idx + 1]) / y[idx]) > 0.02:
            x_res.append(x[p_mark:idx+1])
            y_res.append(y[p_mark:idx+1])
            p_mark = idx + 1
    x_res.append(x[p_mark:])
    y_res.append(y[p_mark:])
    return x_res, y_res

####################################################################################################


def heatmap_necs_from_r0_facotr(anal_data, expr_name, expr_param, **kwargs):
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 5}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 9 * unit
    #####################################################
    task_name = f'{expr_name}_({expr_param})'
    anal_name = 'necs_from_r0_factor'
    sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
    sheet_name = f'{sheet_name_preppend}_necs'
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    c = ax.pcolormesh(x, y, anal_data[anal_name][sheet_name].T * 100, cmap = 'Blues')
    ax.set_xscale('log')
    task_name = f'{expr_name}_({expr_param})'
    anal_name = 'corr_from_r0_factor'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        z.append(anal_data[anal_name][sheet_name]['optimal'])
    X, Y = np.meshgrid(x, y)
    plt.contour(X, Y, z, levels=[0], colors='tab:gray', linestyles = 'solid', linewidths = 1 * unit)
    
    param_list = {'delay': np.arange(40) / 2, 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 
                  'c_perct': np.linspace(0.215, 0.8, 40), 'vac_dur': np.arange(1, 41)}
    if expr_name == 'necs_from_fatality':
        y_label = r'$\theta$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name == 'necs_from_param': 
        y_label = {'delay': r'$T_{\mathrm{resp}}$', 'vac_eff': r'$\eta$', 'vac_avail': r'$\rho$', 'c_perct': 'x', 'vac_dur': 'x'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
    else: pass
    set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.set_label('Necessity (%)', labelpad = 2, fontsize = 10 * unit)
    cbar.ax.tick_params(labelsize = 6.4 * unit)
    set_cbar_spine_linewidth(cbar, spine_linewidth)
    set_tick_fontsize(cbar.ax, tick_fontsize)
    
    if expr_name == 'necs_from_param' and expr_param == 'delay':
        center_x, center_y, width, height = 0.5, 10, 1.02, 1.2
        ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:orange', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = 0.5, 0, 1.02, 1.2
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:purple', facecolor='none', linestyle = '--', clip_on=False, transform = blended_transform_factory(ax.transAxes,ax.transData)))
        # center_x, center_y, width, height = np.exp(8 * 0.075), 0.5, np.exp((8 - 0.6) * 0.075) - np.exp((8 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:red', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
        # center_x, center_y, width, height = np.exp(24 * 0.075), 0.5, np.exp((24 - 0.6) * 0.075) - np.exp((24 + 0.6) * 0.075), 1.02
        # ax.add_patch(patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, edgecolor='tab:blue', facecolor='none', linestyle = ':', clip_on=False, transform = blended_transform_factory(ax.transData,ax.transAxes)))
    return ax

def heatmap_optimal_from_r0_facotr(anal_data, expr_name, expr_param, **kwargs):
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 30)}, {'pos': (32, 0), 'size': (2, 30)}]]
    margin_attr = {'top': 4, 'bottom': 5, 'left': 7, 'right': 5}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 9 * unit
    #####################################################
    task_name = f'{expr_name}_({expr_param})'
    anal_name = 'corr_from_r0_factor'
    z = []
    for param_idx in range(40):
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        z.append(anal_data[anal_name][sheet_name]['optimal'] >= 0)
    ax = axes[0][0]
    plt.sca(axes[0][0])
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40)
    c = ax.pcolormesh(x, y, np.array(z), cmap = 'Blues')
    ax.set_xscale('log')
    param_list = {'delay': np.arange(40) / 2, 'vac_eff': np.linspace(0.22, 1, 40), 'vac_avail': np.linspace(0.12, 0.9, 40), 
                  'c_perct': np.linspace(0.215, 0.8, 40), 'vac_dur': np.arange(1, 41)}
    if expr_name == 'necs_from_fatality':
        y_label = r'$\theta$' 
        ax.set_yticks(np.arange(40)[0::13], ['0', r'$1/3$', r'$2/3$', '1'])
    elif expr_name == 'necs_from_param': 
        y_label = {'delay': r'$T_{\mathrm{resp}}$', 'vac_eff': r'$\eta$', 'vac_avail': r'$\rho$', 'c_perct': 'x', 'vac_dur': 'x'}[expr_param]
        ax.set_yticks(np.arange(40)[0::13], param_list[expr_param][0::13])
    else: pass
    set_xylabel(ax, r'$R_0$', y_label, fontsize = label_fontsize, xlabel_coords = -0.09, ylabel_coords = -0.12)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize)
    cbar = fig.colorbar(c, cax=axes[0][1])
    cbar.set_label('Necessity (%)', labelpad = 2, fontsize = 10 * unit)
    cbar.ax.tick_params(labelsize = 6.4 * unit)
    set_cbar_spine_linewidth(cbar, spine_linewidth)
    set_tick_fontsize(cbar.ax, tick_fontsize)
    return ax


def plot_necs_from_growth(anal_data, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 15)}, {'pos': (0, 17), 'size': (20, 15)}]]
    margin_attr = {'top': 8, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    
    spine_linewidth = 1.5 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    markers = {'weibull_0':'o', 'weibull_1': 's', 'weibull_2': 'D', 'gamma_0': '^', 'gamma_1': '1', 'gamma_2': '+', 'lognormal_0': 'x', 'lognormal_1': '*', 'lognormal_2': 'h'}
    colors = {'weibull_0':'black', 'weibull_1': 'tab:cyan', 'weibull_2': 'tab:brown', 'gamma_0': 'tab:purple', 'gamma_1': 'tab:gray', 'gamma_2': 'tab:orange', 'lognormal_0': 'tab:green', 'lognormal_1': 'tab:red', 'lognormal_2': 'tab:blue'}
    labels = {'weibull_0': r'$\alpha = 0.7$', 'weibull_1': r'$\alpha = 1$', 'weibull_2' : r'$\alpha = 2$', 
              'gamma_0': r'$\alpha = 0.7$', 'gamma_1': r'$\alpha = 1$', 'gamma_2': r'$\alpha = 2$', 
              'lognormal_0': r'$\sigma = 0.15$', 'lognormal_1': r'$\sigma = 0.35$', 'lognormal_2': r'$\sigma = 1.45$'}
    r0_list = np.round(np.exp(np.array([8, 16, 24, 32]) * 0.075), 2)
    markeredgewidth = 1.5 * unit
    markersize = 6 * unit
    text_fontsize = 10 * unit
    anal_name = 'necs_from_growth'
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        for expr_param in expr_params:
            sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
            plt.plot(anal_data[anal_name][sheet_name][f'growth_{ax_idx * 2}'], anal_data[anal_name][sheet_name][f'necs_{ax_idx * 2}'] * 100, linestyle = '', 
                     marker = markers[expr_param], markerfacecolor='none', markeredgecolor=colors[expr_param], markeredgewidth = markeredgewidth, markersize = markersize, label = labels[expr_param])
        if ax_idx == 1: set_xylabel(ax, r'$gT_{\mathrm{resp}}$', 'Necessity (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.16, ylabel_coords = -0.16)
        else: set_xylabel(ax, None, 'Necessity (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.16, ylabel_coords = -0.16)
        set_spine_linewidth(ax, spine_linewidth)
        set_tick_fontsize(ax, tick_fontsize)
        ax.text(0.985, 0.95, f"$R_0 = {r0_list[ax_idx * 2]}$", ha='right', va='top', fontsize= text_fontsize, transform=ax.transAxes)
        ax.set_xticks(np.arange(0, 14, 6), np.arange(0, 14, 6))
        if ax_idx == 0: leg = plt.legend(ncol = 3, loc='lower center', bbox_to_anchor=(0.5, 1), fontsize = 7.5 * unit, labelspacing=0.25, columnspacing=0.75, handletextpad=0.1, frameon=False)
    
    axes[0][1].set_xlim(axes[0][0].get_xlim())
    axes[0][0].set_xticklabels([])
    bbox = leg.get_window_extent()
    bbox = bbox.transformed(plt.gcf().transFigure.inverted())
    leg_titles = ['Weibull:', 'Gamma:', 'Log-normal:']
    for i in range(3): plt.text(bbox.x0 + 0.1 + i * 0.27, bbox.y1 + 0.0025, leg_titles[i], transform=plt.gcf().transFigure, fontsize=7.5 * unit, ha='center')
    return fig, axes



def plot_necs_from_growth_s(anal_data, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 15)}, {'pos': (0, 17), 'size': (20, 15)}]]
    margin_attr = {'top': 8, 'bottom': 5, 'left': 5, 'right': 2}
    fig, axes = plt.subplots(3,4)
    
    ######################################################
    
    spine_linewidth = 1.5 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    markers = {'weibull_0':'o', 'weibull_1': 's', 'weibull_2': 'D', 'gamma_0': '^', 'gamma_1': '1', 'gamma_2': '+', 'lognormal_0': 'x', 'lognormal_1': '*', 'lognormal_2': 'h'}
    colors = {'weibull_0':'black', 'weibull_1': 'tab:cyan', 'weibull_2': 'tab:brown', 'gamma_0': 'tab:purple', 'gamma_1': 'tab:gray', 'gamma_2': 'tab:orange', 'lognormal_0': 'tab:green', 'lognormal_1': 'tab:red', 'lognormal_2': 'tab:blue'}
    
    r0_list = np.round(np.exp(np.arange(40) * 0.075), 2)
    markeredgewidth = 1.5 * unit
    markersize = 6 * unit
    text_fontsize = 10 * unit
    anal_name = 'necs_from_growth_s'
    for i, j in itertools.product(range(3), range(4)):
        ax = axes[i][j]
        plt.sca(ax)
        for expr_param in expr_params[:6]:
            sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}_{i * 4 + j}"
            plt.plot(anal_data[anal_name][sheet_name][f'r0'], anal_data[anal_name][sheet_name][f'necs'] * 100, linestyle = '', 
                     marker = markers[expr_param], markerfacecolor='none', markeredgecolor=colors[expr_param], markeredgewidth = markeredgewidth, markersize = markersize)
        plt.xscale('log')
        plt.xlim(-1, 20)
    plt.xlabel('r0')
    plt.ylabel('growth')
    return fig, ax


def plot_necs_from_growth_xxx(anal_data, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 15)}, {'pos': (0, 17), 'size': (20, 15)}]]
    margin_attr = {'top': 8, 'bottom': 5, 'left': 5, 'right': 2}
    fig = plt.figure()

    # Add a 3D subplot
    ax = fig.add_subplot(111, projection='3d')
    
    ######################################################
    
    spine_linewidth = 1.5 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    markers = {'weibull_0':'o', 'weibull_1': 's', 'weibull_2': 'D', 'gamma_0': '^', 'gamma_1': '1', 'gamma_2': '+', 'lognormal_0': 'x', 'lognormal_1': '*', 'lognormal_2': 'h'}
    colors = {'weibull_0':'black', 'weibull_1': 'tab:cyan', 'weibull_2': 'tab:brown', 'gamma_0': 'tab:purple', 'gamma_1': 'tab:gray', 'gamma_2': 'tab:orange', 'lognormal_0': 'tab:green', 'lognormal_1': 'tab:red', 'lognormal_2': 'tab:blue'}
    
    r0_list = np.round(np.exp(np.arange(40) * 0.075), 2)
    markeredgewidth = 1.5 * unit
    markersize = 6 * unit
    text_fontsize = 10 * unit
    anal_name = 'necs_from_growth_s'
    plt.sca(ax)
    for i in range(40):
        for expr_param in expr_params:
            sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
            ax.scatter(i, anal_data[anal_name][sheet_name][f'growth_{i}'], anal_data[anal_name][sheet_name][f'necs_{i}'] * 100, linestyle = '', 
                     marker = markers[expr_param], color=colors[expr_param], s = 0.2)
    plt.ylim(-1, 12)
    plt.xlabel('r0')
    plt.ylabel('growth')
    return fig, ax


def curve_necs_line_from_r0(anal_data, expr_name, **kwargs):
    expr_name_type = expr_name.split('_')[-1]
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    mark = kwargs.pop('mark', True)
    data_type = kwargs.pop('data_type', 'necs')
    ####################################################
    scale_prop = 10
    if expr_name_type == 'param' and target == 'c':
        if data_type == 'necs':
            grid_attrs = [[{'pos': (0, 0), 'size': (20, 15)}, {'pos': (24, 0), 'size': (20, 15)},
                           {'pos': (0, 20), 'size': (20, 15)}, {'pos': (24, 20), 'size': (20, 15)}]]
            margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
            removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 1), (0, 3)], 'xtick': [], 'ytick': []}
        elif data_type == 'corr':
            grid_attrs = [[{'pos': (0, 0), 'size': (18, 12)}, {'pos': (22, 0), 'size': (18, 12)}, {'pos': (44, 0), 'size': (18, 12)}, {'pos': (66, 0), 'size': (18, 12)}]]
            margin_attr = {'top': 2, 'bottom': 5, 'left': 7, 'right': 2}
            removed_labels = {'x': [], 'y': [(0, 1), (0, 2), (0, 3)], 'xtick': [], 'ytick': []}
    elif expr_name_type == 'fatality' or (expr_name_type == 'param' and target == 'd'):
        grid_attrs = [[{'pos': (0, 0), 'size': (15, 10)}, {'pos': (21, 0), 'size': (15, 10)}, {'pos': (42, 0), 'size': (15, 10)}, {'pos': (63, 0), 'size': (15, 10)}],
                      [{'pos': (0, 15), 'size': (15, 10)}, {'pos': (21, 15), 'size': (15, 10)}, {'pos': (42, 15), 'size': (15, 10)}, {'pos': (63, 15), 'size': (15, 10)}]]
        margin_attr = {'top': 2, 'bottom': 5, 'left': 7, 'right': 2}
        removed_labels = {'x': [], 'y': [(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3)], 'xtick': [], 'ytick': []}
    else: pass
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    if not (expr_name_type == 'param' and target == 'c' and data_type == 'corr'): 
        ####################################################
        spine_linewidth = 1.5 * unit
        label_fontsize = 10 * unit
        tick_fontsize = 9 * unit
        text_fontsize = 9 * unit
        ####################################################
        for ax_idx, ax in enumerate(axes[0]):
            plt.sca(ax)
            if expr_name_type == 'param': expr_param = f'delay_{ax_idx * 13}'
            elif expr_name_type == 'fatality': expr_param = f'coef_beta_1_{ax_idx * 13}'
            else: pass
            data_line = anal_data[expr_name][f"necs_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"]['res'] * 100
            plt.plot(np.exp(np.arange(1600) * 0.075 / 40)[::10], data_line[::10], linewidth = 2.5 * unit, color = 'tab:orange')
            if expr_name_type == 'param': ax.text(0.03, 0.97, f"$T_{{\\mathrm{{resp}}}} = {ax_idx * 6.5}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes)
            elif expr_name_type == 'fatality': ax.text(0.03, 0.97, f"$\\mu = {ax_idx} / 3$" if ax_idx != 0 and ax_idx != 3 else f"$\\mu = {int(ax_idx / 3)}$", ha='left', va='top', fontsize= text_fontsize, transform=ax.transAxes)
            plt.xscale('log')
            if expr_name.split('_')[-1] == 'param':
                if target == 'c': 
                    ax.set_ylim(0, 40)
                    ax.set_yticks(np.arange(0, 41, 10))
                elif target == 'd': 
                    ax.set_ylim(0, 2.7)
                    ax.set_yticks(np.arange(0, 28, 9) / 10)
                else: pass
            elif expr_name.split('_')[-1] == 'fatality':
                if target == 'c': plt.ylim(0, 35)
                elif target == 'd': plt.ylim(0, 1.5)
                else: pass
            else: pass
            set_xylabel(ax, r'$R_0$', 'Necessity (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.15 if target == 'c' else -0.24, ylabel_coords = -0.14 if target == 'c' else -0.21)
            remove_spines(ax, ['top', 'right'])
            set_spine_linewidth(ax, spine_linewidth)
            set_tick_fontsize(ax, tick_fontsize)
            if mark and expr_name == 'necs_line_from_r0_with_param' and (expr_param == 'delay_0' or expr_param == 'delay_13') and target == 'c':
                plt.plot(np.exp(np.array([286, 779, 1141]) * 0.075 / 40), data_line[[286, 779, 1141]], linestyle = '', marker = 'x', markersize = 10 * unit, color = 'tab:green', markeredgewidth = 2 * unit)
    if not (expr_name_type == 'param' and target == 'c' and data_type == 'necs'):
        import itertools
        ####################################################
        spine_linewidth = 1.5 * unit
        label_fontsize = 10 * unit
        tick_fontsize = 9 * unit
        text_fontsize = 9 * unit
        ####################################################
        for ax_idx, ax in enumerate(axes[0] if expr_name_type == 'param' and target == 'c' and data_type == 'corr' else axes[1]):
            if expr_name_type == 'param': expr_param = f'delay_{ax_idx * 13}'
            elif expr_name_type == 'fatality': expr_param = f'coef_beta_1_{ax_idx * 13}'
            else: pass
            plt.sca(ax)
            sheet_name = f'{expr_param}_{target}_{basic_params.country_abbr[country]}'
            x = np.array([np.exp((r0_head + r0_tail / 40) * 0.075) for r0_head, r0_tail in itertools.product(range(40), range(40))])
            plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['optimal'], linestyle = '', marker = 'o', markerfacecolor = '#C54E53', markeredgecolor = 'white', markersize = 1.5 * unit, markeredgewidth = 0 * unit)
            plt.plot(x, anal_data['corr_line_from_r0'][sheet_name]['worst'], linestyle = '', marker = 'o', markerfacecolor = '#4C72B1', markeredgecolor = 'white', markersize = 1.5 * unit, markeredgewidth = 0 * unit)
            plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
            set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.22 if target == 'c' else -0.2, ylabel_coords = -0.205 if target == 'c' else -0.24)
            set_spine_linewidth(ax, spine_linewidth * unit)
            set_tick_fontsize(ax, tick_fontsize * unit)
            plt.xscale('log')
        
    remove_labels(axes, removed_labels)
    return fig, axes


def curve_example(anal_data, delay_idx, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    mark = kwargs.pop('mark', True)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (16, 12)}, {'pos': (21, 0), 'size': (16, 12)}, {'pos': (42, 0), 'size': (16, 12)}], 
                  [{'pos': (1, 19), 'size': (14, 10)}, {'pos': (22, 19), 'size': (14, 10)}, {'pos': (43, 19), 'size': (14, 10)}], 
                  [{'pos': (1, 34), 'size': (14, 10)}, {'pos': (22, 34), 'size': (14, 10)}, {'pos': (43, 34), 'size': (14, 10)}], ]
    margin_attr = {'top': 3, 'bottom': 7, 'left': 6, 'right': 2}
    removed_labels = {'x': [(1, 0), (1, 1), (1,2)], 'y': [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    spine_linewidth = 1.5 * unit
    label_fontsize = 10 * unit
    tick_fontsize = 9 * unit
    text_fontsize = 10 * unit
    ####################################################
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    x_upper = [[120, 50, 30], [120, 50, 30]]
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        sttgs = ['no_vac', f'max_{target}', f'min_{target}']
        colors = {'no_vac': 'black', f'max_{target}': '#4C72B1', f'min_{target}': '#C54E53'}
        len_limit = min([len(anal_data['fraction_from_time_with_example'][f"{delay_idx}_{ax_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"]['time_line']) for sttg in sttgs])
        for sttg in sttgs:
            sheet_name = f"{delay_idx}_{ax_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"
            plt.plot(anal_data['fraction_from_time_with_example'][sheet_name]['time_line'][:len_limit], 
                     anal_data['fraction_from_time_with_example'][sheet_name][f'curve_{target}'][:len_limit] * 100, linewidth = 2 * unit, color = colors[sttg])
        
        set_xylabel(ax, 'Time (d)', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.24, ylabel_coords = -0.24)
        set_spine_linewidth(ax, spine_linewidth)
        set_tick_fontsize(ax, tick_fontsize)
        plt.ylim(-5, 100)
        ax.set_yticks(np.arange(0, 101, 50), np.arange(0, 101, 50))
        plt.xlim(0, x_upper[delay_idx][ax_idx])
        ax.set_xticks(np.arange(0, x_upper[delay_idx][ax_idx] + 1, x_upper[delay_idx][ax_idx] // 2), np.arange(0, x_upper[delay_idx][ax_idx] + 1, x_upper[delay_idx][ax_idx] // 2))
        ax.spines['left'].set_bounds(0, 100)
        ax.spines['left'].set_position(('axes', -0.03))
        remove_spines(ax, ['top', 'right'])
        plt.title(f'$R_0 = {np.round(np.exp([286, 779, 1141][ax_idx] * 0.075 / 40), 2)}$', fontsize = label_fontsize)
    
    spine_linewidth = 1.2 * unit
    label_fontsize = 10 * unit
    tick_fontsize = 10 * unit
    text_fontsize = 10 * unit
    for idx, optm_dir in enumerate(['min', 'max']):
        for ax_idx, ax in enumerate(axes[idx + 1]):
            plt.sca(ax)
            ax.bar(np.arange(16), anal_data['alloc_from_age_with_example']['alloc'][f"{delay_idx}_{ax_idx}_{optm_dir}_{target}"] * 100, 
                   color = '#C54E53' if optm_dir == 'min' else '#4C72B1', width = 0.8, edgecolor='black', linewidth = 0.5)
            set_xylabel(ax, 'Age', 'Fraction (%)', fontsize = label_fontsize, xlabel_coords = -0.4, ylabel_coords = -0.14)
            set_spine_linewidth(ax, spine_linewidth)
            set_tick_fontsize(ax, tick_fontsize)
            plt.xticks(rotation = 90, fontsize = label_fontsize * 0.6)
            ax.set_xlim(-1, 16)
            ax.spines['bottom'].set_bounds(0, 15)
            ax.set_xticks(np.arange(16), age_groups, rotation = 90)
            ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
            ax.set_ylim(0, 8)
            #ax.spines['left'].set_position(('outward', 1))
            ax.tick_params(axis='x', which='major', pad=1)
            remove_spines(ax, ['top', 'right'])
    remove_labels(axes, removed_labels)
    return fig, axes



def prdt_in_alloc_space(anal_data):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    x_coords, y_coords, z_values = [], [], []
    alloc_coef_idxes = []
    for idx in range(2):
        x_coords.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['x_coef'].to_numpy())
        y_coords.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['y_coef'].to_numpy())
        z_values.append(anal_data['prdt_from_xycoef'][f'res_{idx}']['prdt'].to_numpy() * 100)
        alloc_coef_idxes.append(np.array([x_coords[-1], y_coords[-1]]).T)
        
    
    ####################################################
    # scale_prop = 0.3
    # grid_attrs = [[{'pos': (0, 0), 'size': (max(x_coords[0]) - min(x_coords[0]), max(y_coords[0]) - min(y_coords[0]))}, 
    #                {'pos': (max(x_coords[0]) - min(x_coords[0]) + 100, 0), 'size': (max(x_coords[1]) - min(x_coords[1]), max(y_coords[1]) - min(y_coords[1]))}], ]
    # margin_attr = {'top': 100, 'bottom': 100, 'left': 100, 'right': 100}
    # removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 0), (0, 1)], 'xtick': [(0, 0), (0, 1)], 'ytick': [(0, 0), (0, 1)]}
    # fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ####################################################
    
    scale_prop = 5
    grid_attrs = [[{'pos': (0, 4), 'size': (40, 40)}, {'pos': (64, 4), 'size': (40, 40)}], 
                  [{'pos': (4, 0), 'size': (36, 2)}, {'pos': (68, 0), 'size': (36, 2)}], 
                  [{'pos': (4, 44), 'size': (22, 16)}, {'pos': (36, 44), 'size': (22, 16)}, {'pos': (68, 44), 'size': (22, 16)}, {'pos': (100, 44), 'size': (22, 16)}]]
    margin_attr = {'top': 5, 'bottom': 10, 'left': 5, 'right': 5}
    removed_labels = {'x': [(0, 0), (0, 1)], 'y': [(0, 0), (0, 1)], 'xtick': [(0, 0), (0, 1)], 'ytick': [(0, 0), (0, 1)]}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    
    
    deep_colors = sns.color_palette('deep')
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 9 * unit
    tick_fontsize = 8 * unit
    ####################################################
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        x_min, x_max = min(x_coords[ax_idx]), max(x_coords[ax_idx])
        y_min, y_max = min(y_coords[ax_idx]), max(y_coords[ax_idx])
        grid = np.full((x_max - x_min + 1, y_max - y_min + 1), np.nan)
        
        # Map x, y positions to grid
        for (x, y), z in zip(alloc_coef_idxes[ax_idx], z_values[ax_idx]):
            grid[x - x_min, y - y_min] = z
                
        pm = plt.pcolormesh(np.arange(x_max - x_min + 1), np.arange(y_max - y_min + 1), grid.T, cmap=sns.color_palette("viridis", as_cmap=True))
        
        plt.plot([0, x_max - x_min], [0 - y_min, 0 - y_min], color = 'black', linestyle = ':', linewidth = 1 * unit)
        plt.plot([0], [0 - y_min], marker = 'x', color = deep_colors[1], markersize = 8 * unit, markeredgewidth = 2 * unit)
        plt.plot([x_max - x_min], [0 - y_min], marker = '+', color = deep_colors[2], markersize = 8 * unit, markeredgewidth = 2 * unit)
        plt.xlim(- 0.1 * (x_max - x_min), 1.1 * (x_max - x_min))
        plt.ylim(- 0.1 * (y_max - y_min), 1.1 * (y_max - y_min))
        #set_xylabel(ax, 'Dimension 1', 'Dimension 2', fontsize = label_fontsize * unit, xlabel_coords = -0.05, ylabel_coords = -0.05)
        set_spine_linewidth(ax, spine_linewidth)
        cbar = fig.colorbar(pm, cax=axes[1][ax_idx], orientation='horizontal')
        cbar.set_label('Fraction (%)', labelpad=2, fontsize = 7.2 * unit)
        cbar.ax.tick_params(labelsize= 6.4 * unit)
        remove_all_spines(ax)
        ax.text(0.2, 0.8, f'$R_0 = {[1.70, 1.74][ax_idx]}$', fontsize = 9 * unit, ha = 'center', va = 'center', transform=ax.transAxes)
        ax.annotate('Local Min (-)', xy=(x_max - x_min, 0 - y_min), xytext=(x_max - x_min - 350, 0 - y_min + 240), ha='center', va='top',
            arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7), fontsize = 8 * unit)
        ax.annotate('Local Min (+)', xy=(0, 0 - y_min), xytext=(- 350, 0 - y_min + 240), ha='center', va='top', arrowprops=dict(facecolor='black', arrowstyle='->', shrinkB=7), fontsize = 8 * unit)
        ax.invert_xaxis()
        ax.invert_yaxis()
        #cbar_ax.yaxis.set_ticks_position('right')
        # divider = make_axes_locatable(ax)
        # cbar_ax = divider.append_axes("right", size="5%", pad=0.2)
        # cbar = fig.colorbar(pm, cax=cbar_ax)
        #cbar.set_label("Fraction (%)", rotation=270, labelpad=15)
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    from scipy.stats import pearsonr
    contact_arr = np.sum([data_of_countries['United States']['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    for ax_idx, ax in enumerate(axes[2]):
        plt.sca(ax)
        alloc = anal_data['prdt_from_xycoef']['alloc_res'][f"alloc_{ax_idx // 2}_{['n', 'p'][ax_idx % 2]}"]
        ax.bar(np.arange(16), alloc * 100, color = [deep_colors[2], deep_colors[1]][ax_idx % 2], width = 0.8, edgecolor='black', linewidth = 0.5)
        set_xylabel(ax, 'Age', 'Fraction (%)', fontsize = label_fontsize * 0.6, xlabel_coords = -0.35, ylabel_coords = -0.14)
        set_spine_linewidth(ax, spine_linewidth)
        set_tick_fontsize(ax, tick_fontsize * 0.6)
        plt.xticks(rotation = 90)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
        ax.set_ylim(0, 8)
        #ax.spines['left'].set_position(('outward', 1))
        ax.tick_params(axis='x', which='major', pad=1)
        remove_spines(ax, ['top', 'right'])
        ax.text(0.05, 0.9, f'$Corr = {np.round(pearsonr(alloc, contact_arr)[0], 3)}$', fontsize = 6 * unit, ha = 'left', va = 'top', transform=ax.transAxes)
        
    remove_labels(axes, removed_labels)
    return fig, axes





def minimimum_transition(anal_data, **kwargs):
    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    import matplotlib.patches as patches
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 16)}, {'pos': (21, 0), 'size': (1, 16)}, {'pos': (32, 0), 'size': (20, 16)}]]
    margin_attr = {'top': 4, 'bottom': 6, 'left': 6, 'right': 4}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    
    ax = axes[0][0]
    plt.sca(ax)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 10 * unit
    tick_fontsize = 8 * unit
    ####################################################
    
    sheet_name = 'res'
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    deep_colors = sns.color_palette('deep')
    cnorm = mcolors.Normalize(vmin=1.70, vmax=1.74)
    plt.axvline(0, linewidth = 1 * unit, linestyle = ':', color = 'black')
    for file_idx in np.arange(41)[1:-1]:
        plt.plot(anal_data['prdt_from_corr'][sheet_name][f'corr_{file_idx}'], np.array(anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40), linewidth = 0.5 * unit, linestyle = '-')
    for file_idx in [0, 40]:
        plt.plot(anal_data['prdt_from_corr'][sheet_name][f'corr_{file_idx}'], np.array(anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40), linewidth = 1.2 * unit, linestyle = '-')
    set_spine_linewidth(ax, spine_linewidth)
    set_tick_fontsize(ax, tick_fontsize)
    set_xylabel(ax, 'Pearson Correlation', 'Fraction (%)', fontsize = label_fontsize, xlabel_coords = -0.15, ylabel_coords = -0.18)
    x_pos, y_pos = anal_data['prdt_from_corr'][sheet_name]['corr_0'][350], np.array(anal_data['prdt_from_corr'][sheet_name]['prdt_0'])[350] * 100
    ax.annotate(r'$R_0 = 1.70$', xy=(x_pos, y_pos), xytext=(x_pos - 0.12, y_pos - 0.0075), ha='center', va='top', arrowprops=dict(arrowstyle='->', color = cmap(0)), color = cmap(0), fontsize = 7.5 * unit)
    x_pos, y_pos = anal_data['prdt_from_corr'][sheet_name]['corr_40'][150], np.array(anal_data['prdt_from_corr'][sheet_name]['prdt_40'])[150] * 100
    ax.annotate(r'$R_0 = 1.74$', xy=(x_pos, y_pos), xytext=(x_pos + 0.06, y_pos + 0.009), ha='center', va='top', arrowprops=dict(arrowstyle='->', color = cmap(1.0)), color = cmap(1.0), fontsize = 7.5 * unit)
    ax.add_patch(patches.Rectangle((-0.825, 0.23), 0.04, 0.015, linewidth= 1.2 * unit, edgecolor=deep_colors[2], facecolor='none', linestyle = '--', zorder = 3))
    ax.add_patch(patches.Rectangle((0.26, 0.2265), 0.05, 0.023, linewidth=1.2 * unit, edgecolor=deep_colors[1], facecolor='none', linestyle = '--', zorder = 3))
    plt.ylim(0.223, 0.262)
    ax.text(0.02, 0.12, 'Local Min (-)', color = deep_colors[2], fontsize = 6 * unit, ha = 'left', va = 'bottom', transform=ax.transAxes)
    ax.text(0.99, 0.02, 'Local Min (+)', color = deep_colors[1], fontsize = 6 * unit, ha = 'right', va = 'bottom', transform=ax.transAxes)
    sm = cm.ScalarMappable(cmap=cmap, norm=cnorm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=axes[0][1])
    cbar.set_label(r'$R_0$', fontsize = label_fontsize * 0.8)
    cbar.ax.tick_params(labelsize=tick_fontsize * 0.8)
    cbar.set_ticks(np.arange(5) / 100 + 1.7)
    
    from matplotlib.ticker import ScalarFormatter
    ax = axes[0][2]
    plt.sca(ax)
    ax.plot(1.7 + (np.arange(0, 41, 4) / 1000), [anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}'][0] * 100 - anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}'][-1] * 100 for file_idx in np.arange(0, 41, 4)], color = 'tab:orange', linewidth = 1.5 * unit)
    #plt.axvline(0)
    plt.axhline(0, linewidth = 1 * unit, linestyle = ':', color = 'black')
    set_spine_linewidth(ax, spine_linewidth)
    set_tick_fontsize(ax, tick_fontsize)
    set_xylabel(ax, r'$R_0$', 'Difference (%)', fontsize = label_fontsize, xlabel_coords = -0.15, ylabel_coords = -0.1)
    ax.set_xticks(np.arange(1.70, 1.741, 0.02), np.arange(1.70, 1.741, 0.02))
    ax.set_yticks(np.arange(-4, 5, 4) / 1000, np.arange(-4, 5, 4) / 1000)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.get_offset_text().set_size(tick_fontsize)
    return fig, axes



def necs_from_contact(anal_data, **kwargs):
    ####################################################
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 8
    grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (30, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [(0, 1), (0, 2), (0, 3)], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1 * unit
    label_fontsize = 8 * unit
    tick_fontsize = 7 * unit
    ####################################################
    expr_params = ['1', '2', '3', '13']
    titles = ['School Closure', 'Remote Work', 'Travel Restriction', 'Full Lockdown']
    for ax_idx, ax in enumerate(axes[0]):
        plt.sca(ax)
        expr_param = expr_params[ax_idx]
        r0_ls = np.exp(np.arange(40) * 3 / 40)
        data_tmp = anal_data['necs_from_r0_contact'][f"{data_type}_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"] * 100
        plt.quiver(r0_ls, data_tmp[:, -1], np.zeros(len(r0_ls)), data_tmp[:, 0] - data_tmp[:, -1], color = 'tab:gray',angles='xy',scale_units='xy', scale = 1)
        ax.plot(r0_ls, data_tmp[:, -1], linestyle='', marker = 'o', color = 'lightcoral', markersize = 3 * unit, label = 'No Intervetion')
        ax.plot(r0_ls, data_tmp[:, 0], linestyle='', marker = 'o', color = 'skyblue', markersize = 3 * unit, label = 'Post Intervetion')
        set_xylabel(ax, r'$R_0$', 'Necessity (%)', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.12)
        set_spine_linewidth(ax, spine_linewidth)
        set_tick_fontsize(ax, tick_fontsize)
        if target == 'c':
            plt.ylim(-1, 31)
            ax.set_yticks(np.arange(0, 31, 10))
        elif target == 'd':
            plt.ylim(-1 / 20, 31 / 20)
            ax.set_yticks(np.arange(0, 31, 10) / 20)
        plt.xscale('log')
        ax.text(0.04, 0.96, titles[ax_idx], fontsize = 7.5 * unit, color = 'black', horizontalalignment='left', verticalalignment='top', transform= ax.transAxes)
        if ax_idx == 0: plt.legend(fontsize = 7 * unit, loc = 'upper right' if target == 'c' else 'lower right', handletextpad=0.1)
    remove_labels(axes, removed_labels)
    return ax

def fitting_countries(anal_data, **kwargs):
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (6, 0), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 2, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    from matplotlib.ticker import ScalarFormatter
    ax = axes[0][0]
    plt.sca(ax)
    country = 'United States'
    best_left, best_right = anal_data['fitted_fraction_from_time']['fitted_period'][country]
    real_time_line = anal_data['fitted_fraction_from_time']['real_data'][f'{country}_time'][best_left:best_right]
    plt.plot(real_time_line, anal_data['fitted_fraction_from_time']['real_data'][f'{country}_data'][best_left:best_right], 'o', markerfacecolor=(1.0, 0.5, 0.5, 0.75), 
             markeredgecolor='#F08080', markeredgewidth = 1 * unit, markersize = 3 * unit, label = 'Real Data')
    best_left_x, best_right_x = best_left * basic_params.day_div, best_right * basic_params.day_div
    plt.plot(anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_time'][best_left_x:best_right_x], anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_mean'][best_left_x:best_right_x], color = "#6495ED", label = 'Fitted Curve')
    plt.fill_between(anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_time'][best_left_x:best_right_x], anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_lower'][best_left_x:best_right_x], 
                     anal_data['fitted_fraction_from_time']['fitted_data'][f'{country}_upper'][best_left_x:best_right_x], color = "#6495ED", alpha = 0.5, linewidth = 0, label = '95% CI of Fitted Curve')
    set_xylabel(ax, 'Date', 'Fraction (%)', fontsize = label_fontsize, xlabel_coords = -0.12, ylabel_coords = -0.12)
    set_spine_linewidth(ax, spine_linewidth)
    set_tick_fontsize(ax, tick_fontsize)
    start_date = np.datetime64('2020-01-22')
    date_list = np.arange(start_date, start_date + np.timedelta64(90, 'D'))
    ax.set_xticks(real_time_line[::14], date_list[real_time_line[::14]], fontsize = tick_fontsize)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.get_offset_text().set_size(tick_fontsize)
    plt.legend(fontsize = 8 * unit)
    return fig, axes



def table_necs(anal_data, **kwargs):
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (45, 54)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [(0, 1), (0, 2), (0, 3)], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    
    from plottable import ColumnDefinition, Table
    from plottable.plots import circled_image
    
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    res = {}
    col_names = {'flag': 'Flag', 'growth_rate': 'Growth Rate (95% CI)', 'r0': r'$R_0$ (95% CI)'}
    round_num = {'growth_rate': 3, 'r0': 3}
    for col_type in ['flag', 'growth_rate','r0']:
        res[col_names[col_type]] = []
        for country in countries:
            if col_type == 'flag':
                res[col_names[col_type]].append(os.path.join(code_root, 'Dependencies', 'CountryFlags', f'{country}.png'))
            else:
                data_tmp = anal_data['param_from_country'][col_type][country]
                res[col_names[col_type]].append(f"{np.round(np.mean(data_tmp), round_num[col_type])} ({np.round(np.percentile(data_tmp, 2.5), round_num[col_type])} – {np.round(np.percentile(data_tmp, 97.5), round_num[col_type])})")
    df = pd.DataFrame(res, index = countries)
    df = df.rename_axis('Country')
    ax = axes[0][0]
    plt.sca(ax)
    col_defs = ([ColumnDefinition(name="Flag", title="", textprops={"ha": "center"}, width=0.25, plot_fn=circled_image,),
                 ColumnDefinition(name="Country", textprops={"ha": "left", "weight": "bold"}, width=0.75,),
                 ColumnDefinition( name='Growth Rate (95% CI)', textprops={"ha": "center"}, width=0.75,),
                 ColumnDefinition(name=r'$R_0$ (95% CI)', textprops={"ha": "center"}, width=0.75,),])
     
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    plt.rcParams["savefig.bbox"] = "tight"
    
    Table(df, column_definitions=col_defs, row_dividers=True, footer_divider=True, ax=ax, textprops={"fontsize": 6}, 
          row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))}, col_label_divider_kw={"linewidth": 1, "linestyle": "-"}, 
          column_border_kw={"linewidth": 1, "linestyle": "-"}).autoset_fontcolors(colnames=[])
    return fig, axes


def neces_from_country(anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (81, 27)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 9 * unit
    tick_fontsize = 7 * unit
    ####################################################
    ax = axes[0][0]
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    restrictions = {'none': 'No Intervention', 's': 'School Closure', 'w': 'Remote Work', 'o': 'Travel Restriction', 'swo': 'Full Lockdown'}
    def prepare_data(data_dict):
        import itertools
        rows = []
        sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
        for country, contact_type in itertools.product(countries, ['none', 's', 'w', 'o', 'swo']):
            for value in data_dict['necs_from_country'][sheet_name][f'{country}_{contact_type}']:
                rows.append({ 'Country': country, 'Restriction Type': restrictions[contact_type], 'Necessity': value * 100})
        return pd.DataFrame(rows)
    
    plt.sca(ax)
    df = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    edge_width = 0.75 * unit
    sns.boxplot(data=df, y="Necessity", x="Country", hue="Restriction Type", width=.6, palette="vlag", flierprops={'markersize': 1.5, 'markeredgewidth': edge_width},
                boxprops={'linewidth': edge_width}, whiskerprops={'linewidth': edge_width}, capprops={'linewidth': edge_width}, medianprops={'linewidth': edge_width})

    ax.yaxis.grid(True)
    set_xylabel(ax, '', 'Necessity (%)', fontsize = label_fontsize , xlabel_coords = -0.1, ylabel_coords = -0.03 if target == 'c' else -0.04)
    set_tick_fontsize(ax, tick_fontsize)
    sns.despine(trim=True, bottom=True)
    if target == 'c': ax.legend(fontsize = 8 * unit, loc = 'upper center', bbox_to_anchor=(0.7, 0.97))
    elif target == 'd': ax.legend(fontsize = 8 * unit, loc = 'upper right')
    else: pass
    return fig, axes





def scar_comparision_line_from_r0(anal_data, expr_name, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (30, 60)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 8, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    expr_params = {'necs_line_from_param': ['delay_0', 'delay_13', 'delay_26', 'delay_39'], 'necs_line_from_fatality': ['coef_beta_1_0', 'coef_beta_1_13', 'coef_beta_1_26', 'coef_beta_1_39']}
    x = np.exp(np.arange(1600) * 3 / 1600)
    ax = axes[0][0]
    plt.sca(ax)
    overlap = 3
    param_lens = len(expr_params[expr_name])
    
    deep_colors = sns.color_palette('deep')
    for idx, expr_param in enumerate(expr_params[expr_name]):
        task_name = f'{expr_name}_({expr_param})'
        sheet_name = f'{task_name}_{basic_params.country_abbr[country]}'
        sacr_c = anal_data['sacr_line_from_r0'][sheet_name]['sacr_c']
        sacr_d = anal_data['sacr_line_from_r0'][sheet_name]['sacr_d']
        ax.fill_between(x, sacr_c + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = param_lens - idx + 1, color = deep_colors[2], alpha = 0.5)
        plt.plot(x, sacr_c + idx * overlap, color = deep_colors[2], zorder = param_lens - idx + 1, linewidth = 1 * unit, )
        plt.plot(x, np.ones(1600) * (idx * overlap), color = deep_colors[2], zorder = param_lens - idx + 1, linewidth = 1 * unit)
        ax.fill_between(x, sacr_d + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = param_lens - idx + 1, color = deep_colors[1], alpha = 0.5)
        plt.plot(x, sacr_d + idx * overlap, color = deep_colors[1], zorder = param_lens - idx + 1, linewidth = 1 * unit)
        plt.plot(x, np.ones(1600) * (idx * overlap), color = deep_colors[1], zorder = param_lens - idx + 1, linewidth = 1 * unit)
        ax.text(0.9, idx * overlap, f'$T_{{\\mathrm{{resp}}}} = {(39 - idx * 3) / 2}$', fontsize = 8 * unit, color = 'black', horizontalalignment='right', verticalalignment='bottom', transform= ax.transData)

    plt.xscale('log')   
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin = -0.1)
    set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    
    
    
    # for ax_idx, ax in enumerate(axes[0]):
    #     plt.sca(ax)
    #     plt.plot(x, zc[ax_idx * 13], color = 'tab:green')
    #     plt.fill_between(x, 0, zc[ax_idx * 13], color = 'tab:green', alpha = 0.5)
    #     plt.plot(x, zd[ax_idx * 13], color = 'tab:orange')
    #     plt.fill_between(x, 0, zd[ax_idx * 13], color = 'tab:orange', alpha = 0.5)
    #     ax.set_xscale('log')
    #     set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    #     set_spine_linewidth(ax, spine_linewidth * unit)
    #     set_tick_fontsize(ax, tick_fontsize * unit)
    return fig, axes



def sacr_from_example(anal_data, idx, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (16, 12)}, {'pos': (20, 0), 'size': (16, 12)}, ],
                  [{'pos': (3, 18), 'size': (30, 25)}]]
    margin_attr = {'top': 2, 'bottom': 8, 'left': 8, 'right': 8}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    
    deep_colors = sns.color_palette('deep')
    age_groups = []
    for i in range(16):
        if i != 15: age_groups.append(f'{i * 5}–{(i + 1) * 5 - 1}')
        else:age_groups.append('75+')
    
    for ax_idx, ax in enumerate(axes[0]):
        optm_target = ['c', 'd'][ax_idx]
        plt.sca(ax)
        acc_type = 'dd'
        alloc_colors = {'c': deep_colors[2], 'd': deep_colors[1]}
        titles = {'c': r'$\vartheta_\mathrm{best, c}$', 'd': r'$\vartheta_\mathrm{best, d}$'}
        sheet_name = 'example_alloc'
        data_tmp = anal_data['sacr_from_example'][sheet_name]
        ax.bar(np.arange(16), data_tmp[f'min_{optm_target}_{idx}_{acc_type}'] * 100, color = alloc_colors[optm_target], width = 0.8, edgecolor='black', linewidth = 0.5)
        set_xylabel(ax, 'Age', 'Fraction (%)', fontsize = label_fontsize * 0.6, xlabel_coords = -0.3, ylabel_coords = -0.1)
        set_spine_linewidth(ax, spine_linewidth)
        set_tick_fontsize(ax, tick_fontsize * 0.6)
        plt.xticks(rotation = 90)
        ax.set_xlim(-1, 16)
        ax.spines['bottom'].set_bounds(0, 15)
        ax.set_xticks(np.arange(16), age_groups, rotation = 90)
        ax.set_yticks(np.arange(0, 9, 4), np.arange(0, 9, 4))
        ax.set_ylim(0, 8)
        #ax.spines['left'].set_position(('outward', 1))
        ax.tick_params(axis='x', which='major', pad=1)
        remove_spines(ax, ['top', 'right'])
        if ax_idx == 1: ax.set_ylabel(None)
    
    for ax_idx, ax in enumerate(axes[1]):
        plt.sca(ax)
        acc_type = 'dd'
        alloc_colors = ['black', deep_colors[2], deep_colors[1]]
        titles = [r'$\vartheta_\mathrm{best, c}$', r'$\vartheta_\mathrm{best, d}$']
        sheet_name = 'example_res'
        data_tmp = anal_data['sacr_from_example'][sheet_name]
        ax.bar([-0.5, 0.5, 1.5], [data_tmp[f'no_vac_res_c_{idx}_{acc_type}'][0], data_tmp[f'min_c_res_c_{idx}_{acc_type}'][0], data_tmp[f'min_d_res_c_{idx}_{acc_type}'][0]], 
                 width = 0.9 * unit, color = 'none', edgecolor = alloc_colors, linewidth = 1.5 * unit, hatch='///', 
                 label = [r'$\tilde{\chi}_\mathrm{c}$ without vaccination', r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, c}$', r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, d}$'])
        ax.set_ylabel('Fraction (%)', fontsize = label_fontsize * unit)
        ax_d =  ax.twinx()
        ax_d.bar([4.5, 5.5, 6.5], [data_tmp[f'no_vac_res_d_{idx}_{acc_type}'][0], data_tmp[f'min_c_res_d_{idx}_{acc_type}'][0], data_tmp[f'min_d_res_d_{idx}_{acc_type}'][0]], 
                 width = 0.9 * unit, color = 'none', edgecolor = alloc_colors, linewidth = 1.5 * unit, hatch='...', 
                 label = [r'$\tilde{\chi}_\mathrm{d}$ without vaccination', r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, c}$', r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, d}$'])
        ax_d.set_ylabel('Fraction (%)', fontsize = label_fontsize * unit)
        if idx == 0: 
            ax.set_ylim(0, 0.8)
            ax_d.set_ylim(0, 0.02)
            ax.set_yticks(np.arange(0, 0.81, 0.2), np.arange(0, 81, 20), fontsize = tick_fontsize * unit)
            ax_d.set_yticks(np.arange(0, 0.021, 0.005), np.arange(0, 210, 50) / 100, fontsize = tick_fontsize * unit)
            ax.legend(loc = 'upper left', fontsize = 6 * unit, bbox_to_anchor = (0.01, 1.01))
            ax_d.legend(loc = 'upper right', fontsize = 6 * unit, bbox_to_anchor = (0.99, 1.01))
        else: 
            ax.set_ylim(0, 1)
            ax_d.set_ylim(0, 0.03)
            ax.set_yticks(np.arange(0, 1.1, 0.25), np.arange(0, 110, 25), fontsize = tick_fontsize * unit)
            ax_d.set_yticks(np.arange(0, 0.031, 0.006), np.arange(0, 31, 6) / 10, fontsize = tick_fontsize * unit)
        ax.set_xticks([0.5, 5.5], ['Cumulative Infections', 'Deaths'], fontsize = label_fontsize * unit)
    return fig, axes







def sacr_comparison_from_r0(anal_data, expr_name_end, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 8 * unit
    tick_fontsize = 7 * unit
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (15, 70)}], 
                  [{'pos': (20, 2), 'size': (15, 12)}, {'pos': (20, 20), 'size': (15, 12)}, {'pos': (20, 38), 'size': (15, 12)}, {'pos': (20, 56), 'size': (15, 12)}]]
    margin_attr = {'top': 1, 'bottom': 5, 'left': 8, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    x = np.exp(np.arange(40) * 3 / 40)
    if expr_name_end == 'param':
        dc = anal_data['sacr_from_r0_param'][f"anti_min_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        cc = anal_data['sacr_from_r0_param'][f"min_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        no_vac_c = anal_data['sacr_from_r0_param'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        cd = anal_data['sacr_from_r0_param'][f"anti_min_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
        dd = anal_data['sacr_from_r0_param'][f"min_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
        no_vac_d = anal_data['sacr_from_r0_param'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    elif expr_name_end == 'fatality':
        dc = anal_data['sacr_from_r0_fatality'][f"min_d_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        cc = anal_data['sacr_from_r0_fatality'][f"min_c_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        no_vac_c = anal_data['sacr_from_r0_fatality'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
        cd = anal_data['sacr_from_r0_fatality'][f"min_c_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
        dd = anal_data['sacr_from_r0_fatality'][f"min_d_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
        no_vac_d = anal_data['sacr_from_r0_fatality'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    else:  pass
    zc = (dc - cc) / (no_vac_c - dc)
    zd = (cd - dd) / (no_vac_d - cd)
    ax = axes[0][0]
    plt.sca(ax)
    overlap = 2
    deep_colors = sns.color_palette('deep')
    for idx in range(40):
        y = zc[39 - idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = deep_colors[2], alpha = 0.75)
        plt.plot(x, y + idx * overlap, color = 'white', zorder = 40 - idx + 1, linewidth = 1.5 * unit, )
        plt.plot(x, np.ones(40) * (idx * overlap), color = deep_colors[2], zorder = 40 - idx + 1, linewidth = 1 * unit)
        y = zd[39 - idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = deep_colors[1], alpha = 0.75)
        plt.plot(x, y + idx * overlap, color = 'white', zorder = 40 - idx + 1, linewidth = 1.5 * unit)
        plt.plot(x, np.ones(40) * (idx * overlap), color = deep_colors[1], zorder = 40 - idx + 1, linewidth = 1 * unit)
        ax.text(0.9, idx * overlap, f'$T_{{\\mathrm{{resp}}}} = {(39 - idx) / 2}$' if expr_name_end == 'param' else f'$\\mu = {39 - idx} / 39$', fontsize = 4.5 * unit, color = 'black', horizontalalignment='right', verticalalignment='bottom', transform= ax.transData)
    
    plt.xscale('log')   
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin = -0.1)
    set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    set_xylabel(ax, r'$R_0$', None, fontsize = label_fontsize * unit, xlabel_coords = -0.03 , ylabel_coords = -0.22)
    
    
    expr_params = {'param': ['delay_0', 'delay_13', 'delay_26', 'delay_39'], 'fatality': ['coef_beta_1_0', 'coef_beta_1_13', 'coef_beta_1_26', 'coef_beta_1_39']}
    x = np.array([np.exp((r0_head + r0_tail / 40) * 0.075) for  r0_head, r0_tail in itertools.product(range(40), range(40))])
    for ax_idx, ax in enumerate(axes[1]):
        plt.sca(ax)
        task_name = f'necs_line_from_{expr_name_end}_({expr_params[expr_name_end][ax_idx]})'
        sheet_name = f'{task_name}_{basic_params.country_abbr[country]}'
        plt.plot(x, anal_data['sacr_line_from_r0'][sheet_name]['alloc_corr'], linestyle = '', marker = 'o', markerfacecolor = deep_colors[-1], markeredgecolor = 'white', markersize = 1.5 * unit, markeredgewidth = 0 * unit)
        plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
        set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.22)
        set_spine_linewidth(ax, spine_linewidth * unit)
        set_tick_fontsize(ax, tick_fontsize * unit)
        plt.xscale('log')
    
    
    
    
    
    # for ax_idx, ax in enumerate(axes[0]):
    #     plt.sca(ax)
    #     plt.plot(x, zc[ax_idx * 13], color = 'tab:green')
    #     plt.fill_between(x, 0, zc[ax_idx * 13], color = 'tab:green', alpha = 0.5)
    #     plt.plot(x, zd[ax_idx * 13], color = 'tab:orange')
    #     plt.fill_between(x, 0, zd[ax_idx * 13], color = 'tab:orange', alpha = 0.5)
    #     ax.set_xscale('log')
    #     set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    #     set_spine_linewidth(ax, spine_linewidth * unit)
    #     set_tick_fontsize(ax, tick_fontsize * unit)
    return fig, axes


def sacr_comparison_from_r0_fatality(anal_data, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 90)}], 
                  [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (30, 25), 'size': (25, 20)}, {'pos': (30, 50), 'size': (25, 20)}, {'pos': (30, 75), 'size': (25, 20)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 8, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    x = np.exp(np.arange(40) * 3 / 40)
    dc = anal_data['sacr_from_r0_fatality'][f"min_d_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    cc = anal_data['sacr_from_r0_fatality'][f"min_c_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    no_vac_c = anal_data['sacr_from_r0_fatality'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    cd = anal_data['sacr_from_r0_fatality'][f"min_c_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    dd = anal_data['sacr_from_r0_fatality'][f"min_d_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    no_vac_d = anal_data['sacr_from_r0_fatality'][f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    zc = (dc - cc) / (no_vac_c - dc)
    zd = (cd - dd) / (no_vac_d - cd)
    ax = axes[0][0]
    plt.sca(ax)
    overlap = 1.5
    
    for idx in range(40):
        y = zc[39 - idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = 'tab:green', alpha = 0.75)
        plt.plot(x, y + idx * overlap, color = 'white', zorder = 40 - idx + 1, linewidth = 1.5 * unit, )
        plt.plot(x, np.ones(40) * (idx * overlap), color = 'tab:green', zorder = 40 - idx + 1, linewidth = 1 * unit)
        y = zd[39 - idx]
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder = 40 - idx + 1, color = 'tab:orange', alpha = 0.75)
        plt.plot(x, y + idx * overlap, color = 'white', zorder = 40 - idx + 1, linewidth = 1.5 * unit)
        plt.plot(x, np.ones(40) * (idx * overlap), color = 'tab:orange', zorder = 40 - idx + 1, linewidth = 1 * unit)
        ax.text(0.9, idx * overlap, f'$\\mu = {39 - idx} / 39$', fontsize = 6 * unit, color = 'black', horizontalalignment='right', verticalalignment='bottom', transform= ax.transData)
    
    
    
    plt.xscale('log')   
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.set_ylim(ymin = -0.1)
    set_spine_linewidth(ax, spine_linewidth)
    ax.set_yticklabels([])
    
    
    
    # for ax_idx, ax in enumerate(axes[0]):
    #     plt.sca(ax)
    #     plt.plot(x, zc[ax_idx * 13], color = 'tab:green')
    #     plt.fill_between(x, 0, zc[ax_idx * 13], color = 'tab:green', alpha = 0.5)
    #     plt.plot(x, zd[ax_idx * 13], color = 'tab:orange')
    #     plt.fill_between(x, 0, zd[ax_idx * 13], color = 'tab:orange', alpha = 0.5)
    #     ax.set_xscale('log')
    #     set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    #     set_spine_linewidth(ax, spine_linewidth * unit)
    #     set_tick_fontsize(ax, tick_fontsize * unit)
    return fig, axes


def sacrs_from_country(anal_data, **kwargs):
    ####################################################
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (87, 29)}]]
    margin_attr = {'top': 2, 'bottom': 5, 'left': 5, 'right': 2}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    label_fontsize = 9 * unit
    tick_fontsize = 7.5 * unit
    ####################################################
    ax = axes[0][0]
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    targets = {'c': 'Cumulative Infections', 'd': 'Deaths'}
    def prepare_data(data_dict):
        import itertools
        rows = []
        sheet_name = f"{acc_type}{'_dur' if dur else ''}"
        for country, target in itertools.product(countries, ['c', 'd']):
            for value in data_dict['sacr_from_country'][sheet_name][f'{country}_{target}']:
                rows.append({ 'Country': country, 'Target': targets[target], 'Sacrifice': value * 100})
        return pd.DataFrame(rows)
    deep_colors = sns.color_palette('deep')
    plt.sca(ax)
    df = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    edge_width = 0.75 * unit
    sns.boxplot(data=df, y="Sacrifice", x="Country", hue="Target", width=.3, palette= deep_colors[2:0:-1], flierprops={'markersize': 1.5, 'markeredgewidth': edge_width},
                boxprops={'linewidth': edge_width}, whiskerprops={'linewidth': edge_width}, capprops={'linewidth': edge_width}, medianprops={'linewidth': edge_width})

    ax.yaxis.grid(True)
    set_xylabel(ax, '', 'Sacrifice (%)', fontsize = label_fontsize , xlabel_coords = -0.1, ylabel_coords = -0.03)
    set_tick_fontsize(ax, tick_fontsize)
    sns.despine(trim=True, bottom=True)
    ax.legend(fontsize = 8 * unit, loc = 'upper right', bbox_to_anchor=(0.8, 0.97))
    return fig, axes







def corr_from_r0_factors(anal_data, expr_name, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = 1 * unit
    label_fontsize = 12 * unit
    tick_fontsize = 10 * unit
    ####################################################
    scale_prop = 10
    # grid_attrs = [[{'pos': (0, 0), 'size': (25, 20)}, {'pos': (60, 0), 'size': (25, 20)}, {'pos': (0, 30), 'size': (25, 20)}, {'pos': (60, 30), 'size': (25, 20)}],
    #               [{'pos': (30, 0), 'size': (25, 20)}, {'pos': (90, 0), 'size': (25, 20)}, {'pos': (30, 30), 'size': (25, 20)}, {'pos': (90, 30), 'size': (25, 20)}]]
    grid_attrs = [[{'pos': (0, 0), 'size': (20, 20)}]]
    margin_attr = {'top': 2, 'bottom': 8, 'left': 8, 'right': 8}
    removed_labels = {'x': [], 'y': [], 'xtick': [], 'ytick': []}
    fig, axes = gererate_grid(grid_attrs, margin_attr, scale_prop, d_list = [(0, 0)])
    ######################################################
    task_name = f'{expr_name}_({expr_param})'
    ax = axes[0][0]
    plt.sca(ax)
    for param_idx in range(40):
        ax.scatter(np.arange(40), param_idx, anal_data['corr_from_r0'][f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}']['optimal'], color = 'tab:red', marker='o')
    plt.xlabel(r'$R_0$')
    return fig, axes



















def curve_necs_from_r0(ax, anal_data, expr_name, expr_param, param_idx, **kwargs):
    
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    mark = kwargs.pop('mark', True)
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    data_line = anal_data[f"necs_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"][:, param_idx] * 100
    plt.plot(np.exp(np.arange(40) * 0.075), data_line, linewidth = 2 * unit, color = 'tab:blue')
    plt.xscale('log')
    set_xylabel(ax, r'$R_0$', 'Necessity (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.14, ylabel_coords = -0.13)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    if mark and expr_name == 'necs_from_param' and expr_param == 'delay':
        if param_idx == 18: plt.plot(np.exp(np.array([7, 18, 24]) * 0.075), data_line[[7, 18, 24]], linestyle = '', marker = 'x', markersize = 10 * unit, color = 'tab:red', markeredgewidth = 2 * unit)
        else: plt.plot(np.exp(np.array([8, 22, 33]) * 0.075), data_line[[8, 22, 33]], linestyle = '', marker = 'x', markersize = 10 * unit, color = 'tab:red', markeredgewidth = 2 * unit)
    return ax



def curve_fraction_from_time_with_example(ax, anal_data, r0_idx, delay_idx, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    sttgs = ['no_vac', f'max_{target}', f'min_{target}']
    colors = {'no_vac': 'black', f'max_{target}': 'tab:blue', f'min_{target}': 'tab:red'}
    len_limit = min([len(anal_data[f"{delay_idx}_{r0_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"]['time_line']) for sttg in sttgs])
    for sttg in sttgs:
        sheet_name = f"{delay_idx}_{r0_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"
        plt.plot(anal_data[sheet_name]['time_line'][:len_limit], anal_data[sheet_name][f'curve_{target}'][:len_limit] * 100, linewidth = 2 * unit, color = colors[sttg])
    plt.ylim(0, 100)
    set_xylabel(ax, 'Time (d)', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.18)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    ax.set_yticks(np.arange(0, 101, 50), np.arange(0, 101, 50))
    return ax


def bar_alloc_from_age_with_example(ax, anal_data, r0_idx, delay_idx, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    optm_dir = kwargs.pop('optm_dir', 'min')
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 9)
    tick_fontsize = kwargs.pop('tick_fontsize', 7.5)
    ####################################################
    plt.sca(ax)
    ax.bar(np.arange(16) * 5 + 2.5, anal_data['alloc'][f"{delay_idx}_{r0_idx}_{optm_dir}_{target}"] * 100, 
           color = 'tab:red' if optm_dir == 'min' else 'tab:blue', width = 4)
    set_xylabel(ax, 'Age', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.14)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
    ax.set_yticks(np.arange(0, 7, 3), np.arange(0, 7, 3))
    ax.set_ylim(0, 7)
    return ax
    

def plot_corr_from_r0(ax, anal_data, expr_name, expr_param, param_idx, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 9)
    tick_fontsize = kwargs.pop('tick_fontsize', 7.5)
    ####################################################
    plt.sca(ax)
    sheet_name = f'{expr_name}_({expr_param})_{target}_{param_idx}_{basic_params.country_abbr[country]}'
    plt.plot(np.exp(np.arange(40) * 0.075), anal_data[sheet_name]['optimal'], linestyle = '', marker = 'x', color = 'tab:red', markersize = 5 * unit, markeredgewidth = 1 * unit)
    plt.plot(np.exp(np.arange(40) * 0.075), anal_data[sheet_name]['worst'], linestyle = '', marker = '+', color = 'tab:blue', markersize = 5 * unit, markeredgewidth = 1 * unit)
    set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.18)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    plt.xscale('log')
    return ax


# def curve_necs_line_from_r0(ax, anal_data, expr_param, **kwargs):
#     ####################################################
#     country = kwargs.pop('country', 'United States')
#     target = kwargs.pop('target', 'd')
#     acc_type = kwargs.pop('acc_type', 'dd')
#     dur = kwargs.pop('dur', False)
#     ####################################################
#     spine_linewidth = kwargs.pop('spine_linewidth', 1)
#     label_fontsize = kwargs.pop('label_fontsize', 12)
#     tick_fontsize = kwargs.pop('tick_fontsize', 10)
#     ####################################################
#     import itertools
#     plt.sca(ax)
#     linewidth = 2
#     x = np.array([np.exp((r0_head + r0_tail / 40) * 0.075) for r0_head, r0_tail in itertools.product(range(40), range(40))])
    
#     ax.plot(x, anal_data[f"necs_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"]['res'] * 100, linewidth = linewidth * unit, color = 'tab:green')
#     ax.set_xscale('log')
#     # axin_max = ax.inset_axes([1.1, 0.6, 0.4, 0.4])
#     # axin_max.plot(x, anal_data[f"max_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"]['res'] * 100, linewidth = linewidth * unit, color = 'tab:blue')
#     # axin_max.set_xscale('log')
#     # axin_min = ax.inset_axes([1.1, 0.1, 0.4, 0.4])
#     # axin_min.plot(x, anal_data[f"min_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"]['res'] * 100, linewidth = linewidth * unit, color = 'tab:red')
#     # axin_min.set_xscale('log')
#     set_xylabel(ax, r'$R_0$', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.12, ylabel_coords = -0.12)
#     set_spine_linewidth(ax, spine_linewidth * unit)
#     set_tick_fontsize(ax, tick_fontsize * unit)
#     return ax

def plot_corr_line_from_r0(ax, anal_data, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    import itertools
    plt.sca(ax)
    sheet_name = f'{expr_param}_{target}_{basic_params.country_abbr[country]}'
    x = np.array([np.exp((r0_head + r0_tail / 40) * 0.075) for r0_head, r0_tail in itertools.product(range(40), range(40))])
    plt.plot(x, anal_data[sheet_name]['optimal'], linestyle = '', marker = 'o', markerfacecolor = '#C54E53', markeredgecolor = 'white', markersize = 1.5 * unit, markeredgewidth = 0 * unit)
    plt.plot(x, anal_data[sheet_name]['worst'], linestyle = '', marker = 'o', markerfacecolor = '#4C72B1', markeredgecolor = 'white', markersize = 1.5 * unit, markeredgewidth = 0 * unit)
    plt.axhline(0, 0, 1, linestyle = ':', color = 'tab:gray')
    set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.12, ylabel_coords = -0.2)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    plt.xscale('log')
    return ax
    

def heatmap_prdt_from_xycoef(ax, anal_data, sheet_idx, **kwargs):
    from matplotlib.ticker import MultipleLocator
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    
    plt.sca(ax)
    x_coords = anal_data[f'res_{sheet_idx}']['x_coef'].to_numpy()
    y_coords = anal_data[f'res_{sheet_idx}']['y_coef'].to_numpy()
    z_values = anal_data[f'res_{sheet_idx}']['prdt'].to_numpy() * 100
    alloc_coef_idxes = np.array([x_coords, y_coords]).T
    
    # Step 2: Determine the grid size, handling floats
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    # Step 3: Create a 2D grid and populate it with NaN
    grid = np.full((x_max - x_min + 1, y_max - y_min + 1), np.nan)
    
    # Map x, y positions to grid
    for (x, y), z in zip(alloc_coef_idxes, z_values):
        grid[x - x_min, y - y_min] = z
            
    plt.imshow(grid.T, origin="lower", cmap="viridis", extent=(x_min, x_max, y_min, y_max), interpolation="nearest", aspect="auto")
    
    # Add color bar and labels
    cbar = plt.colorbar(label="Fraction (%)")
    plt.plot([0], [0], marker = '.', color = 'tab:red', markersize = 15 * unit)
    plt.plot([max(x_coords)], [0], marker = '.', color = 'tab:orange', markersize = 15 * unit)
    set_xylabel(ax, 'Dimension 1', 'Dimension 2', fontsize = label_fontsize * unit, xlabel_coords = -0.05, ylabel_coords = -0.05)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    return ax


def curve_prdt_from_corr(ax, anal_data, **kwargs):
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    from matplotlib.ticker import ScalarFormatter
    plt.sca(ax)
    sheet_name = 'res'
    cmap = plt.get_cmap('coolwarm')
    for file_idx in np.arange(41)[1:-1]:
        plt.plot(anal_data[sheet_name][f'corr_{file_idx}'], np.array(anal_data[sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40), linewidth = 0.8 * unit, linestyle = '-')
    for file_idx in [0, 40]:
        plt.plot(anal_data[sheet_name][f'corr_{file_idx}'], np.array(anal_data[sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40), linewidth = 2 * unit, linestyle = '-')
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    set_xylabel(ax, 'Pearson Correlation', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.15, ylabel_coords = -0.15)
    inset_position = [0.225, 0.15, 0.3, 0.25]
    # axin = ax.inset_axes(inset_position)
    # axin.plot(1.7 + (np.arange(0, 41, 4) / 1000), [anal_data[sheet_name][f'prdt_{file_idx}'][-1] * 100 - anal_data[sheet_name][f'prdt_{file_idx}'][0] * 100 for file_idx in np.arange(0, 41, 4)])
    # set_spine_linewidth(axin, spine_linewidth * unit)
    # set_tick_fontsize(axin, tick_fontsize * unit / 1.5)
    # set_xylabel(axin, r'$R_0$', 'Fraction (%)', fontsize = label_fontsize * unit / 2, xlabel_coords = -0.3, ylabel_coords = -0.28)
    # axin.set_xticks(np.arange(1.70, 1.741, 0.02), np.arange(1.70, 1.741, 0.02))
    # axin.set_yticks(np.arange(-4, 5, 4) / 1000, np.arange(-4, 5, 4) / 1000)
    # axin.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    # axin.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    # axin.yaxis.get_offset_text().set_size(tick_fontsize * unit / 1.5)
    return ax

def curve_prdt_diff_from_r0(ax, anal_data, **kwargs):
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    from matplotlib.ticker import ScalarFormatter
    plt.sca(ax)
    sheet_name = 'res'
    plt.plot(1.7 + (np.arange(0, 41, 4) / 1000), [anal_data[sheet_name][f'prdt_{file_idx}'][-1] * 100 - anal_data[sheet_name][f'prdt_{file_idx}'][0] * 100 for file_idx in np.arange(0, 41, 4)])
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    set_xylabel(ax, r'$R_0$', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.1, ylabel_coords = -0.1)
    ax.set_xticks(np.arange(1.70, 1.741, 0.02), np.arange(1.70, 1.741, 0.02))
    ax.set_yticks(np.arange(-4, 5, 4) / 1000, np.arange(-4, 5, 4) / 1000)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.get_offset_text().set_size(tick_fontsize * unit)
    return ax
    
    

def boxplot_neces_from_country(ax, anal_data, **kwargs):
    ####################################################
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    restrictions = {'none': 'No Intervention', 's': 'School Closure', 'w': 'Remote Work', 'o': 'Travel Restriction', 'swo': 'Full Lockdown'}
    def prepare_data(data_dict):
        import itertools
        rows = []
        sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
        for country, contact_type in itertools.product(countries, ['none', 's', 'w', 'o', 'swo']):
            for value in data_dict[sheet_name][f'{country}_{contact_type}']:
                rows.append({ 'Country': country, 'Restriction Type': restrictions[contact_type], 'Necessity': value * 100})
        return pd.DataFrame(rows)
    
    plt.sca(ax)
    df = prepare_data(anal_data)
    sns.despine(bottom=True, left=True)
    sns.boxplot(data=df, y="Necessity", x="Country", hue="Restriction Type", width=.6, palette="vlag", flierprops={'markersize': 3})

    ax.yaxis.grid(True)
    set_xylabel(ax, '', 'Necessity (%)', fontsize = label_fontsize * unit , xlabel_coords = -0.1, ylabel_coords = -0.032)
    set_tick_fontsize(ax, tick_fontsize * unit)
    sns.despine(trim=True, bottom=True)
    return ax

def change_necs_from_contact(ax, anal_data, expr_param, **kwargs):
    ####################################################
    data_type = kwargs.pop('data_type', 'necs')
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    x = np.exp(np.arange(40) * 3 / 40)
    data_tmp = anal_data[f"{data_type}_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"] * 100
    y = data_tmp[:, 0] - data_tmp[:, -1]
    # for r0_idx, r0 in enumerate(r0_ls):
    #     data_tmp = anal_data[f"{data_type}_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"][r0_idx] * 100
    #     plt.quiver(r0, data_tmp[-1], 0, data_tmp[0] - data_tmp[-1], angles='xy', scale_units='xy', scale = 1, 
    #                headlength=3.5 * unit, headwidth=4 * unit, headaxislength=1.5 * unit, width=0.01 * unit,
    #                color = 'tab:gray')
    # ax.plot(r0_ls, anal_data[f"{data_type}_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"][:, 0] * 100, linestyle='', marker = 'o', color = 'skyblue', markersize = 4 * unit)
    # ax.plot(r0_ls, anal_data[f"{data_type}_{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"][:, -1] * 100, linestyle='', marker = 'o', color = 'lightgreen', markersize = 4 * unit)
    #colors = np.where(y >= 0, 'orange', 'skyblue')
    #plt.vlines(x = x, ymin = 0, ymax = y, color = colors, alpha=0.7, linewidth = 2 * unit)
    #plt.plot(x, y, color = colors, s = 4 * unit, alpha = 1, marker = 'o')
    for i in range(len(x)):
        plt.plot([x[i], x[i]], [0, y[i]], color = 'orange' if y[i]>=0 else 'skyblue', alpha=0.7,linewidth = 1 * unit)
        plt.plot([x[i],], [y[i],], color = 'orange' if y[i]>=0 else 'skyblue', alpha=1, marker = 'o', markersize = 2 * unit)
    set_xylabel(ax, r'$R_0$', 'Necessity (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.12, ylabel_coords = -0.18)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    
    plt.xscale('log')
    return ax

def heatmap_sacr_from_r0_param(ax, anal_data, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40) / 2
    dc = anal_data[f"anti_min_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    cc = anal_data[f"min_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    no_vac_c = anal_data[f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    cd = anal_data[f"anti_min_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    dd = anal_data[f"min_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    no_vac_d = anal_data[f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    if target == 'c': z = (dc - cc) / (no_vac_c - dc)
    elif target == 'd': z = (cd - dd) / (no_vac_d - cd)
    c = ax.pcolormesh(x, y, z, cmap = 'Reds')
    ax.set_xscale('log')
    set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    cbar = plt.colorbar(c, pad=0.05)
    set_cbar_spine_linewidth(cbar, spine_linewidth * unit)
    cbar.set_label('Sacrifice', fontsize = label_fontsize * unit)
    set_tick_fontsize(cbar.ax, tick_fontsize * unit)
    return ax



def heatmap_sacr_from_r0_fatality(ax, anal_data, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    target = kwargs.pop('target', 'c')
    acc_type = kwargs.pop('acc_type', 'dd')
    dur = kwargs.pop('dur', False)
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    x = np.exp(np.arange(40) * 3 / 40)
    y = np.arange(40) / 2
    no_vac_c =  anal_data[f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    dc = anal_data[f"min_d_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    cc = anal_data[f"min_c_{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}{'_dur' if dur else ''}"].T
    no_vac_d =  anal_data[f"no_vac_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    cd = anal_data[f"min_c_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    dd = anal_data[f"min_d_{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}{'_dur' if dur else ''}"].T
    if target == 'c': z = (dc - cc) / (no_vac_c - dc)
    elif target == 'd': z = (cd - dd) / (no_vac_d - cd)
    c = ax.pcolormesh(x, y, z, cmap = 'Reds')
    ax.set_xscale('log')
    set_xylabel(ax, r'$R_0$', r'$T_{\mathrm{resp}}$', fontsize = label_fontsize * unit, xlabel_coords = -0.075, ylabel_coords = -0.12)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    cbar = plt.colorbar(c, pad=0.05)
    set_cbar_spine_linewidth(cbar, spine_linewidth * unit)
    cbar.set_label('Sacrifice', fontsize = label_fontsize * unit)
    set_tick_fontsize(cbar.ax, tick_fontsize * unit)
    return ax

def bar_sacr_from_example(ax, anal_data, idx, **kwargs):
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 12)
    tick_fontsize = kwargs.pop('tick_fontsize', 10)
    ####################################################
    plt.sca(ax)
    acc_type = 'dd'
    alloc_colors = ['black', 'tab:green', 'tab:orange']
    titles = [r'$\vartheta_\mathrm{best, c}$', r'$\vartheta_\mathrm{best, d}$']
    sheet_name = 'example_res'
    data_tmp = anal_data[sheet_name]
    ax.bar([-0.5, 0.5, 1.5], [data_tmp[f'no_vac_res_c_{idx}_{acc_type}'][0], data_tmp[f'min_c_res_c_{idx}_{acc_type}'][0], data_tmp[f'min_d_res_c_{idx}_{acc_type}'][0]], 
             width = 0.9 * unit, color = 'none', edgecolor = alloc_colors, linewidth = 1.5 * unit, hatch='///', 
             label = [r'$\tilde{\chi}_\mathrm{c}$ without vaccination', r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, c}$', r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, d}$'])
    ax.set_ylabel('Fraction (%)', fontsize = label_fontsize * unit)
    ax_d =  ax.twinx()
    ax_d.bar([4.5, 5.5, 6.5], [data_tmp[f'no_vac_res_d_{idx}_{acc_type}'][0], data_tmp[f'min_c_res_d_{idx}_{acc_type}'][0], data_tmp[f'min_d_res_d_{idx}_{acc_type}'][0]], 
             width = 0.9 * unit, color = 'none', edgecolor = alloc_colors, linewidth = 1.5 * unit, hatch='...', 
             label = [r'$\tilde{\chi}_\mathrm{d}$ without vaccination', r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, c}$', r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, d}$'])
    ax_d.set_ylabel('Fraction (%)', fontsize = label_fontsize * unit)
    if idx == 0: 
        ax.set_ylim(0, 1)
        ax_d.set_ylim(0, 0.015)
        ax.set_yticks(np.arange(0, 0.8, 0.2), np.arange(0, 80, 20), fontsize = tick_fontsize * unit)
        ax_d.set_yticks(np.arange(0, 0.0045, 0.0005), np.arange(0, 45, 5) / 100, fontsize = tick_fontsize * unit)
        ax.legend(loc = 'upper left', fontsize = 7 * unit)
        ax_d.legend(loc = 'upper right', fontsize = 7 * unit)
    else: 
        ax.set_ylim(0, 1)
        ax_d.set_ylim(0, 0.03)
        ax.set_yticks(np.arange(0, 1, 0.2), np.arange(0, 100, 20), fontsize = tick_fontsize * unit)
        ax_d.set_yticks(np.arange(0, 0.02, 0.004), np.arange(0, 20, 4) / 10, fontsize = tick_fontsize * unit)
    ax.set_xticks([0, 4], ['Cumulative Infections', 'Deaths'], fontsize = label_fontsize * unit)
    return ax

def bar_alloc_from_sacr_example(ax, anal_data, idx, optm_target, **kwargs):
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 9)
    tick_fontsize = kwargs.pop('tick_fontsize', 7)
    ####################################################
    plt.sca(ax)
    acc_type = 'dd'
    alloc_colors = {'c': 'tab:red', 'd': 'black'}
    titles = {'c': r'$\vartheta_\mathrm{best, c}$', 'd': r'$\vartheta_\mathrm{best, d}$'}
    sheet_name = 'example_alloc'
    data_tmp = anal_data[sheet_name]
    plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, 
            data_tmp[f'min_{optm_target}_{idx}_{acc_type}'],
            color = alloc_colors[optm_target], width = 4)
    ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
    ax.set_yticks(np.arange(0, 0.11, 0.05), np.arange(0, 11, 5))
    ax.set_ylim(0, 0.1)
    ax.text(0.02, 0.98, titles[optm_target], fontsize = 15 * unit, color = alloc_colors[optm_target],
            horizontalalignment='left', verticalalignment='top', 
            transform= ax.transAxes)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    set_xylabel(ax, 'Age', 'Fraction (%)', fontsize = label_fontsize * unit, xlabel_coords = -0.12, ylabel_coords = -0.08)
    return ax


def plot_alloc_corr_line_from_r0(ax, anal_data, expr_name, expr_param, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 9)
    tick_fontsize = kwargs.pop('tick_fontsize', 7.5)
    ####################################################
    plt.sca(ax)
    sheet_name = f'{expr_name}_({expr_param})_{basic_params.country_abbr[country]}'
    plt.plot(np.exp(np.arange(1600) * 0.075 / 40), anal_data[sheet_name]['alloc_corr'], linestyle = '', marker = 'x', color = 'tab:red', markersize = 2 * unit, markeredgewidth = 0.5 * unit)
    set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.18)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    plt.xscale('log')
    return ax    


def plot_alloc_corr_from_r0(ax, anal_data, expr_name, expr_param, param_idx, **kwargs):
    ####################################################
    country = kwargs.pop('country', 'United States')
    ####################################################
    spine_linewidth = kwargs.pop('spine_linewidth', 1)
    label_fontsize = kwargs.pop('label_fontsize', 9)
    tick_fontsize = kwargs.pop('tick_fontsize', 7.5)
    ####################################################
    plt.sca(ax)
    sheet_name = f'{expr_name}_({expr_param})_{param_idx}_{basic_params.country_abbr[country]}'
    plt.plot(np.exp(np.arange(40) * 0.075), anal_data[sheet_name]['alloc_corr'], linestyle = '', marker = 'x', color = 'tab:red', markersize = 5 * unit, markeredgewidth = 1 * unit)
    set_xylabel(ax, r'$R_0$', 'Pearson Correlation', fontsize = label_fontsize * unit, xlabel_coords = -0.18, ylabel_coords = -0.18)
    set_spine_linewidth(ax, spine_linewidth * unit)
    set_tick_fontsize(ax, tick_fontsize * unit)
    plt.xscale('log')
    return ax    

def plot_dist_diff_from_r0(ax, anal_data):
    
    plt.sca(ax)
    cmap = plt.get_cmap('rainbow')
    x_idx_list = np.array([4, 12, 20, 28, 36])
    r0_list = [f'$R_0$ = {r0}' for r0 in np.round(np.exp(x_idx_list * 0.075), 2)]
    
    overlap = 0.5
    x, ys = [0], []
    for idx, x_idx in enumerate(x_idx_list):
        ys.append([0])
        for key, item in enumerate(anal_data['dist_diff'][f'dist_diff_{x_idx}']):
            if idx == 0:
                x.append(key)
                x.append(key + 1)
            ys[-1].append(item)
            ys[-1].append(item)
        if idx == 0: x.append(key + 1)
        ys[-1].append(0)
        ys[-1] = np.array(ys[-1])
    for idx, y in enumerate(ys):
        ax.fill_between(x, y + idx * overlap, np.ones(len(x)) * (idx * overlap), zorder=len(ys) - idx + 1, color = cmap(1 - idx / len(x_idx_list)))
        plt.plot(x, y + idx * overlap, color = 'white', zorder=len(ys) - idx + 1, linewidth = 2.5 * unit)
        plt.plot(np.arange(-1, 18), np.ones(19) * (idx * overlap), color = cmap(1 - idx / len(x_idx_list)), zorder=len(ys) - idx + 1, linewidth = 2.5 * unit)
        
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([], [])
    ax.set_ylim(ymin = -0.1)
    plt.yticks(np.arange(0, len(r0_list)) * overlap, r0_list, fontsize = 8 * unit)
    for xtick, color in zip(ax.get_yticklabels(), [cmap(1 - idx / len(x_idx_list)) for idx in range(8)]):
        xtick.set_color(color)
    plt.tick_params(bottom=False, left = False)
    return ax


def curve_fitted_fraction_from_time(ax, anal_data):
    plt.sca(ax)
    country = 'United States'
    plt.plot(anal_data['real_data'][f'{country}_time'], anal_data['real_data'][f'{country}_data'], 'o', markerfacecolor=(1.0, 0.5, 0.5, 0.75), 
             markeredgecolor='#F08080', markeredgewidth = 1 * unit, markersize = 3 * unit)
    plt.plot(anal_data['fitted_data'][f'{country}_time'], anal_data['fitted_data'][f'{country}_mean'], color = "#6495ED")
    plt.fill_between(anal_data['fitted_data'][f'{country}_time'], anal_data['fitted_data'][f'{country}_lower'], 
                     anal_data['fitted_data'][f'{country}_upper'], color = "#6495ED", alpha = 0.5, linewidth = 0)
    return ax

def table_param_from_country(ax, anal_data):
    from plottable import ColumnDefinition, Table
    from plottable.plots import circled_image
    
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    res = {}
    col_names = {'flag': 'Flag', 'r0': r'$R_0$ (95% CI)', 'growth_rate': 'Growth Rate (95% CI)'}
    round_num = {'r0': 3, 'growth_rate': 3}
    for col_type in ['flag' ,'r0', 'growth_rate']:
        res[col_names[col_type]] = []
        for country in countries:
            if col_type == 'flag':
                res[col_names[col_type]].append(os.path.join(code_root, 'Dependencies', 'CountryFlags', f'{country}.png'))
            else:
                #mean, confience_interval = calculate_confidence_interval(anal_data[col_type][country][::25])
                res[col_names[col_type]].append(f'{np.round(np.mean(anal_data[col_type][country]), round_num[col_type])} ({np.round(np.percentile(anal_data[col_type][country], 2.5), round_num[col_type])} - {np.round(np.percentile(anal_data[col_type][country], 97.5), round_num[col_type])})')
    df = pd.DataFrame(res, index = countries)
    df = df.rename_axis('Country')
    
    plt.sca(ax)
    col_defs = ([ColumnDefinition(name="Flag", title="", textprops={"ha": "center"}, width=0.25, plot_fn=circled_image,),
                 ColumnDefinition(name="Country", textprops={"ha": "left", "weight": "bold"}, width=0.75,),
                 ColumnDefinition(name=r'$R_0$ (95% CI)', textprops={"ha": "center"}, width=0.75,),
                 ColumnDefinition( name='Growth Rate (95% CI)', textprops={"ha": "center"}, width=0.75,),])
     
    plt.rcParams["font.family"] = ["DejaVu Sans"]
    plt.rcParams["savefig.bbox"] = "tight"
    
    table = Table(
        df,
        column_definitions=col_defs,
        row_dividers=True,
        footer_divider=True,
        ax=ax,
        textprops={"fontsize": 6},
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
        column_border_kw={"linewidth": 1, "linestyle": "-"},
    ).autoset_fontcolors(colnames=[])
    return ax



# def plot_contact_pearsonr(axes, anal_data):
#     for delay_idx, delay_type in enumerate(['no_delay', 'plus_delay']):
#         ax = axes[delay_idx]
#         plt.sca(ax)
#         for optm_dir_idx, optm_dir in enumerate(['worst', 'optm']):
#             plt.plot(anal_data['alloc_diff']['ln_r0'], anal_data['alloc_diff'][f'{optm_dir}_with_{delay_type}'], '.', color = ['tab:blue', 'tab:red'][optm_dir_idx])
#             plt.xlabel(r'$\ln{R_0}$')
#             plt.ylabel('Pearson Correlation')

# def plot_fig2(anal_data):
#     dpi = plt.rcParams['figure.dpi']
#     grid_col, grid_row = 69, 98
#     scale_prop, shape_prop = 25, 1
#     fig_width = grid_row * scale_prop * shape_prop * unit / dpi
#     fig_height = grid_col * scale_prop * unit / dpi
#     fig = plt.figure(figsize = [fig_width, fig_height])
#     axes = []
#     gs = GridSpec(grid_col, grid_row, figure = fig)
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:29, 12:39]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[10:28, 47:65]))
#     axes[-1].append(fig.add_subplot(gs[10:28, 71:89]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[37:46, 3:13]))
#     axes[-1].append(fig.add_subplot(gs[37:46, 28:38]))
#     axes[-1].append(fig.add_subplot(gs[37:46, 53:63]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[55:64, 3:13]))
#     axes[-1].append(fig.add_subplot(gs[55:64, 28:38]))
#     axes[-1].append(fig.add_subplot(gs[55:64, 53:63]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[35:40, 16:23]))
#     axes[-1].append(fig.add_subplot(gs[35:40, 41:48]))
#     axes[-1].append(fig.add_subplot(gs[35:40, 66:73]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[43:48, 16:23]))
#     axes[-1].append(fig.add_subplot(gs[43:48, 41:48]))
#     axes[-1].append(fig.add_subplot(gs[43:48, 66:73]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[53:58, 16:23]))
#     axes[-1].append(fig.add_subplot(gs[53:58, 41:48]))
#     axes[-1].append(fig.add_subplot(gs[53:58, 66:73]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[61:66, 16:23]))
#     axes[-1].append(fig.add_subplot(gs[61:66, 41:48]))
#     axes[-1].append(fig.add_subplot(gs[61:66, 66:73]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[34:49, 79:95]))
#     axes[-1].append(fig.add_subplot(gs[52:67, 79:95]))
    
#     ax = axes[0][0]
#     plt.sca(ax)
#     plt.imshow(anal_data['necs_grid'].T)
#     plt.colorbar(orientation='horizontal', location='top')
#     plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#     plt.xlabel(r'$\ln{R_0}$')
#     ax.set_yticks(np.arange(40)[5::10], np.arange(0, 2000, 50)[5::10] * basic_params.step)
#     plt.ylabel(r'$T_{\mathrm{resp}}$')
    
#     for idx, r0_idx in enumerate([0, 2]):
#         ax = axes[1][idx]
#         plt.sca(ax)
#         for expr_param in ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']:
#             plt.plot(anal_data['growth_res'][r0_idx][f'{expr_param}_growth'],  anal_data['growth_res'][r0_idx][f'{expr_param}_necs'], '.')
#         plt.xlabel(r'$gT_{\mathrm{resp}}$')
#         plt.ylabel('Necessity')
#         plt.xlim(-0.2, 10.2)
        
#     for delay_idx, delay_type in enumerate(['no_delay', 'plus_delay']):
#         for r0_idx in range(3):
#             ax = axes[delay_idx + 2][r0_idx]
#             plt.sca(ax)
#             plt.plot(anal_data['example_res'][f'time_line_{r0_idx}_{delay_type}'], anal_data['example_res'][f'curve_no_vac_{r0_idx}_{delay_type}'], color = 'black')
#             plt.plot(anal_data['example_res'][f'time_line_{r0_idx}_{delay_type}'], anal_data['example_res'][f'curve_min_{r0_idx}_{delay_type}'], color = 'tab:red')
#             plt.plot(anal_data['example_res'][f'time_line_{r0_idx}_{delay_type}'], anal_data['example_res'][f'curve_max_{r0_idx}_{delay_type}'], color = 'tab:blue')
#             plt.xlabel('Time (d)')
#             plt.ylabel('Fraction (%)')
#             ax.set_yticks(np.arange(0, 101, 50) / 100, np.arange(0, 101, 50))
            
    
#     for delay_idx, delay_type in enumerate(['no_delay', 'plus_delay']):
#         for r0_idx in range(3):
#             for optm_dir_idx, optm_dir in enumerate(['worst', 'optm']):
#                 ax = axes[delay_idx * 2 + optm_dir_idx + 4][r0_idx]
#                 plt.sca(ax)
#                 plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, anal_data['alloc'][f'{optm_dir}_{r0_idx}_{delay_type}'], color = ['tab:blue', 'tab:red'][optm_dir_idx], width = 4)
#                 ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
#                 ax.set_yticks(np.arange(0, 9, 4) / 100, np.arange(0, 9, 4))
#                 plt.xlabel('Age', fontsize = 10 * unit)
#                 plt.ylabel('Fraction (%)', fontsize = 10 * unit)
   
#     for delay_idx, delay_type in enumerate(['no_delay', 'plus_delay']):
#         ax = axes[8][delay_idx]
#         plt.sca(ax)
#         for optm_dir_idx, optm_dir in enumerate(['worst', 'optm']):
#             plt.plot(anal_data['alloc_diff']['ln_r0'], anal_data['alloc_diff'][f'{optm_dir}_with_{delay_type}'], '.', color = ['tab:blue', 'tab:red'][optm_dir_idx])
#             plt.xlabel(r'$\ln{R_0}$')
#             plt.ylabel('Pearson Correlation')

#     return fig, axes