# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 01:24:48 2025

@author: fengm
"""


import numpy as np
import matplotlib.pyplot as plt
from .figure_dependencies import figure_setting
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.patches as patches

def draw(anal_data, **kwargs):
    scale_prop = 14
    grid_attrs = [[{'pos': (0, 0), 'size': (27, 16)}, {'pos': (28, 0), 'size': (1, 16)}]]
    margin_attr = {'top': 2, 'bottom': 4, 'left': 7, 'right': 4}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    
    ax = axes[0][0]
    plt.sca(ax)
    ax.yaxis.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.4, zorder = 0)
    ax.set_axisbelow(True)
    ####################################################
    spine_linewidth = 1
    label_fontsize = 12
    tick_fontsize = 10
    ####################################################
    
    sheet_name = 'res'
    cmap = sns.color_palette("coolwarm", as_cmap=True)
    deep_colors = sns.color_palette('deep')
    cnorm = mcolors.Normalize(vmin=1.70, vmax=1.74)
    plt.axvline(0, linewidth = 1, linestyle = ':', color = 'black')
    trans_idx = np.argmin([abs(anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}'].to_numpy()[0] - anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}'].to_numpy()[-1]) for file_idx in range(41)])
    for file_idx in np.arange(41)[1:-1]:
        plt.plot(anal_data['prdt_from_corr'][sheet_name][f'corr_{file_idx}'], np.array(anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40) if file_idx != trans_idx else 'black', linewidth = 0.5 if file_idx != trans_idx else 1, linestyle = '-')
    for file_idx in [0, 40]:
        plt.plot(anal_data['prdt_from_corr'][sheet_name][f'corr_{file_idx}'], np.array(anal_data['prdt_from_corr'][sheet_name][f'prdt_{file_idx}']) * 100, color = cmap(file_idx / 40), linewidth = 1.2, linestyle = '-')
    figure_setting.set_spine_linewidth(ax, spine_linewidth)
    figure_setting.set_tick_fontsize(ax, tick_fontsize)
    figure_setting.set_xylabel(ax, r'$\xi$', r'$\tilde{\chi}_{\mathrm{d}}$ (%)', fontsize = label_fontsize, xlabel_coords = -0.15, ylabel_coords = -0.12)
    x_pos, y_pos = anal_data['prdt_from_corr'][sheet_name]['corr_0'][350], np.array(anal_data['prdt_from_corr'][sheet_name]['prdt_0'])[350] * 100
    ax.annotate(r'$R_0 = 1.70$', xy=(x_pos, y_pos), xytext=(x_pos - 0.08, y_pos - 0.0075), ha='center', va='top', arrowprops=dict(arrowstyle='->', color = cmap(0)), color = cmap(0), fontsize = 8)
    x_pos, y_pos = anal_data['prdt_from_corr'][sheet_name]['corr_40'][125], np.array(anal_data['prdt_from_corr'][sheet_name]['prdt_40'])[125] * 100
    ax.annotate(r'$R_0 = 1.74$', xy=(x_pos, y_pos), xytext=(x_pos + 0.06, y_pos + 0.009), ha='center', va='top', arrowprops=dict(arrowstyle='->', color = cmap(1.0)), color = cmap(1.0), fontsize = 8)
    x_pos, y_pos = anal_data['prdt_from_corr'][sheet_name][f'corr_{trans_idx}'][450], np.array(anal_data['prdt_from_corr'][sheet_name][f'prdt_{trans_idx}'])[450] * 100
    ax.annotate(rf'Critical $R_0 \approx {np.round(1.7 + trans_idx * 0.001, 3)}$', xy=(x_pos, y_pos), xytext=(x_pos - 0.08, y_pos - 0.01), ha='center', va='top', arrowprops=dict(arrowstyle='->', color = 'black'), color = 'black', fontsize = 8)
    ax.add_patch(patches.Rectangle((-0.475, 0.23), 0.02, 0.015, linewidth= 1.2, edgecolor=deep_colors[2], facecolor='none', linestyle = '--', zorder = 3))
    ax.add_patch(patches.Rectangle((0.095, 0.2265), 0.02, 0.023, linewidth=1.2, edgecolor=deep_colors[1], facecolor='none', linestyle = '--', zorder = 3))
    plt.ylim(0.223, 0.262)
    ax.text(0.02, 0.12, 'Direct protection', color = deep_colors[2], fontsize = 8, ha = 'left', va = 'bottom', transform=ax.transAxes)
    ax.text(0.99, 0.02, 'Balanced protection', color = deep_colors[1], fontsize = 8, ha = 'right', va = 'bottom', transform=ax.transAxes)
    sm = cm.ScalarMappable(cmap=cmap, norm=cnorm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=axes[0][1])
    cbar.ax.set_title(r'$R_0$', fontsize = label_fontsize * 0.8, pad = 6)
    cbar.ax.tick_params(labelsize=tick_fontsize * 0.8)
    cbar.set_ticks(np.arange(5) / 100 + 1.7)
    
    return fig, axes
