# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 22:39:39 2025

@author: fengm
"""


import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
dpi = plt.rcParams['figure.dpi']

def generate_grid(grid_attrs, margin_attr, scale_prop, dpi = dpi, d_list = []):
    from itertools import chain
    grid_row, grid_col = margin_attr['left'], margin_attr['top']
    for grid_attr in list(chain.from_iterable(grid_attrs)):
        if margin_attr['left'] + grid_attr['pos'][0] + grid_attr['size'][0] > grid_row: grid_row = margin_attr['left'] + grid_attr['pos'][0] + grid_attr['size'][0]
        if margin_attr['top'] + grid_attr['pos'][1] + grid_attr['size'][1] > grid_col: grid_col = margin_attr['top'] + grid_attr['pos'][1] + grid_attr['size'][1]
    grid_row += margin_attr['right']
    grid_col += margin_attr['bottom']
    fig = plt.figure(figsize = [grid_row * scale_prop / dpi, grid_col * scale_prop / dpi])
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
