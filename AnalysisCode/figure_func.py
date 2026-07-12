# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 13:37:33 2024

@author: fengmi9312
"""
import sys
sys.path.append('../Dependencies/CodeDependencies')
sys.path.append('../ExperimentalCode')
import matplotlib.pyplot as plt
import cmocean
import seaborn as sns
from matplotlib.gridspec import GridSpec
#from mpl_toolkits.axes_grid.inset_locator import inset_axes
import matplotlib.patches as patches
import string
import numpy as np
import basic_params
import func
import tasks
import tkinter as tk
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

unit = 0.65

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
    ax.tick_params('both', width = linewidth, length = 4 * linewidth, pad = 2 * linewidth)
    return ax   

def set_cbar_spine_linewidth(cbar, linewidth):
    cbar.outline.set_linewidth(linewidth)
    cbar.ax.tick_params('y', width = linewidth, length = 4 * linewidth, pad = 2 * linewidth)
    return cbar 
        
def set_tick_fontsize(ax, fontsize):
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    return ax

def set_ax_index(axes, fontsize, offset = [-0.04, 1], lowercase = True):
    idx = 0
    lettercase_func = string.ascii_lowercase if lowercase else string.ascii_uppercase
    for ax_list in axes:
        for ax in ax_list:
            ax.text(offset[0], offset[1], lettercase_func[idx], fontsize = fontsize, 
                    fontweight = 'bold', horizontalalignment='right', verticalalignment='bottom', 
                    transform= ax.transAxes)
            idx += 1
    return axes

def removal_all_spine(ax):
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

def generate_fig2(anal_data, target = 'c', other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 7, 19
    scale_prop, shape_prop = 120, 1
    fig_width = grid_row * scale_prop * shape_prop * unit / dpi
    fig_height = grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:7, 0:7]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:7, 8:15]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:3, 16:19]))
    axes[-1].append(fig.add_subplot(gs[4:7, 16:19]))
    
    ax = axes[0][0]
    plt.sca(ax)
    linewidth = 3 * unit
    markeredgewidth = 2 * unit
    markersize = 15 * unit
    colors = {'curve_'+target: 'tab:orange', 'curve_s': 'tab:green', 
              'prdt_'+target: 'tab:purple', 'prdt_non_'+target: 'tab:purple'}
    labels = {'curve_'+target: r'$\chi_\mathrm{c}(t)$', 'curve_s': r'$\chi_\mathrm{s}(t)$', 
              'prdt_'+target: 'Prediction', 
              'prdt_non_'+target: 'Prediction'}
    sheet_name = 'prdt_' + target
    output_lines = ['curve_'+target, 'curve_s'] if target == 'c' \
                   else ['curve_'+target, 'prdt_'+target]
    time_line = anal_data[sheet_name]['time_line_no_vac']
    for line_name in output_lines:
        plt.plot(time_line, anal_data[sheet_name][line_name + '_no_vac'],
                 linewidth = linewidth, color = colors[line_name], 
                 label = labels[line_name] + ' without vaccine', linestyle = '--')
    plt.plot(time_line, anal_data[sheet_name]['prdt_' + target + '_no_vac'], 
             marker = 'x', linewidth = linewidth, 
             markersize = markersize, markeredgewidth = markeredgewidth,
             linestyle = 'none', markevery = 500,
             color = colors['prdt_'+target], 
             label = labels['prdt_'+target] + ' without vaccine')
    time_line = anal_data[sheet_name]['time_line_all_ages']
    plt.plot(time_line, anal_data[sheet_name]['curve_' + target + '_all_ages'],
             linewidth = linewidth, color = colors['curve_' + target], 
             label = labels['curve_' + target] + ' with vaccine')
    if target == 'c':
        time_lines, curve_s = cut_line(anal_data[sheet_name]['time_line_all_ages'], 
                                       anal_data[sheet_name]['curve_s_all_ages'])
        for idx in range(len(time_lines)):
            plt.plot(time_lines[idx], curve_s[idx], '-', linewidth = linewidth, 
                     color = colors['curve_s'], 
                     label = labels['curve_s'] + ' with vaccine' if idx == 0 else None)
        plt.axvline(time_lines[0][-1], linestyle = ':', linewidth = linewidth / 2, 
                    color = 'tab:gray', alpha = 0.5)
        plt.plot([time_lines[0][-1], time_lines[0][-1]], [curve_s[0][-1], curve_s[1][0]], 
                 linestyle = ':', linewidth = linewidth, color = colors['curve_s'])
    time_lines, prdts = cut_line(anal_data[sheet_name]['time_line_all_ages'], 
                                 anal_data[sheet_name]['prdt_' + target + '_all_ages'])
    for idx in range(len(time_lines)):
        plt.plot(time_lines[idx], prdts[idx], marker = 'o', linewidth = linewidth, 
                 linestyle = 'none', color = colors['prdt_'+target], 
                 markersize = markersize, markeredgewidth = markeredgewidth,
                 label = labels['prdt_'+target] + ' with vaccine' if idx == 0 else None,
                 markerfacecolor='none', markevery = 500)
    
    set_spine_linewidth(ax, 2 * unit)
    set_tick_fontsize(ax, 20 * unit)
    set_xylabel(ax, 'Time (d)', 'Fraction (%)', 25 * unit, xlabel_coords=-0.08, ylabel_coords=-0.08)
    plt.legend(fontsize = 15 * unit)
        
    ax = axes[1][0]
    plt.sca(ax)
    sheet_name = 'compr_' + target
    colors = {'under_20': 'tab:purple', '20-49': 'tab:green', '20+':'tab:brown', 
              '60+': 'tab:gray', 'all_ages': 'tab:orange', 
              'min_'+target: 'tab:red', 'max_'+target: 'tab:blue',
              'no_vac': 'black'}
    labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
              '60+': '60+', 'all_ages': 'All Ages', 'min_'+target: 'Optimal', 'max_'+target: 'Worst',
              'no_vac': 'No Vaccine'}
    for sttg in ['no_vac'] + list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target]:
        plt.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+sttg + '_gd'],
                 label = labels[sttg], color = colors[sttg], linewidth = linewidth)
# =============================================================================
#     colors = {'min_'+target: 'darkred', 'max_'+target: 'darkblue'}
#     markers = {'min_'+target: 'o', 'max_'+target: 'D'}
#     for sttg in ['min_'+target, 'max_'+target]:
#         plt.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+sttg + '_gd'],
#                  label = 'Approximate ' + labels[sttg], color = colors[sttg], linestyle = 'none',
#                  marker = markers[sttg], markersize = 8, markerfacecolor='none', markevery = 200, 
#                  markeredgewidth = 2)
# =============================================================================
    set_spine_linewidth(ax, 2 * unit)
    set_xylabel(ax, 'Time (d)', 'Fraction (%)', 25 * unit, xlabel_coords=-0.08, ylabel_coords=-0.08)
    set_tick_fontsize(ax, 20 * unit)
    plt.legend(loc = 'upper left', fontsize = 15 * unit)
# =============================================================================
#     
#     upper_end, lower_end, x_end = anal_data[sheet_name]['curve_no_vac_gg'][-1], anal_data[sheet_name]['curve_min_' + target + '_gg'][-1], anal_data[sheet_name]['time_line'][-1]
#     plt.xlim(- x_end / 10, x_end * 1.2)
#     ax.annotate('', 
#                 xy=(x_end * 1.075, upper_end), 
#                 xytext=(x_end * 1.075, lower_end),
#                 arrowprops=dict(arrowstyle='<->', lw=2))
#     plt.hlines(upper_end, x_end * 1.05, x_end * 1.1, color = 'k', lw = 2)
#     plt.hlines(lower_end, x_end * 1.05, x_end * 1.1, color = 'k', lw = 2)
#     plt.text(x_end * 1.085, (upper_end + lower_end) / 2, 
#              r'$\sigma^\mathrm{acc}_\mathrm{c, min}$', ha='left', va = 'center')
#     
#     sttg = 'min_'+target
#     y_lower, y_upper = anal_data[sheet_name]['curve_'+ sttg + '_gg'][-3], \
#                        anal_data[sheet_name]['curve_'+ sttg + '_gd'][-1]
#     y_gap = y_upper - y_lower
#     y_lower -= y_gap / 2
#     y_upper += y_gap / 2
#     axin = ax.inset_axes(
#     [0.5, 0.05, 0.4, 0.32],
#     xlim=(anal_data[sheet_name]['time_line'][-5] - 0.005, anal_data[sheet_name]['time_line'][-1] + 0.035), 
#     ylim=(y_lower, y_upper), xticklabels=[], yticklabels=[])
#     axin.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+ sttg + '_gd'],
#              label = 'Approximate ' + labels[sttg], color = colors[sttg], linestyle = 'none',
#              marker = markers[sttg], markersize = 8, markerfacecolor='none', 
#              markeredgewidth = 2)
#     axin.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+ sttg + '_gg'],
#              label = labels[sttg] if sttg[:3] != 'min' and sttg[:3] != 'max' else 'Accurate ' + labels[sttg], 
#              color = colors[sttg], linewidth = linewidth)
#     upper_end, lower_end, x_end = anal_data[sheet_name]['curve_min_' + target + '_gd'][-1], \
#                                   anal_data[sheet_name]['curve_min_' + target + '_gg'][-1], \
#                                   anal_data[sheet_name]['time_line'][-1]
#     axin.annotate('', xy=(x_end + 0.0125, upper_end), 
#                   xytext=(x_end + 0.0125, lower_end),
#                   arrowprops=dict(arrowstyle='<->', lw=2))
#     axin.hlines(upper_end, x_end + 0.0075, x_end + 0.0175, color = 'k', lw = 2)
#     axin.hlines(lower_end, x_end + 0.0075, x_end + 0.0175, color = 'k', lw = 2)
#     axin.text(x_end + 0.0145, (upper_end + lower_end) / 2, 
#              r'$\varepsilon_\mathrm{c, min}$', ha='left', va = 'center')
#     ax.indicate_inset_zoom(axin, edgecolor="black")
#     set_spine_linewidth(axin, 1.5)
#     axin.tick_params(axis='both', which='both', bottom=False, left=False)
# =============================================================================
        
    sheet_name = 'compr_alloc_' + target
    colors = {'max': 'tab:blue', 'min': 'tab:red'}
    titles = {'max': r'Worst Allocation $\vartheta_\mathrm{worst, c}$', 
              'min': r'Best Allocation $\vartheta_\mathrm{best, c}$'}
    for idx, optm_dir in enumerate(['max', 'min']):
        optm_type = 'gd'
        ax = axes[2][idx]
        plt.sca(ax)
        group_amount = 8
        ax.bar(np.arange(group_amount) * 10 + 5, 
               anal_data[sheet_name]['alloc_' + optm_dir + '_' + optm_type], 
               color = colors[optm_dir], width = 9)
        ax.set_ylim(0, 0.5)
        ax.set_yticks(np.linspace(0, 0.45, 4), 
                      list(map("{:.0f}".format, np.linspace(0, 0.45, 4) * 100)))
        ax.set_xticks(np.arange(0, 81, 10), np.arange(0, 81, 10))
        ax.set_title(titles[optm_dir], fontsize = 15 * unit)
        
        set_spine_linewidth(ax, 2 * unit)
        set_tick_fontsize(ax, 12 * unit)
        set_xylabel(ax, 'Age', 'Proportion (%)', 15 * unit, xlabel_coords=-0.15, ylabel_coords=-0.15)
            
    plt.subplots_adjust(top = 0.9, bottom = 0.12, left = 0.05, right = 0.985, 
                        hspace = 1, wspace = 1)       
    set_ax_index(axes, 25 * unit)

    if other_screen:    
        mngr = plt.get_current_fig_manager()
        geom = mngr.window.geometry()
        x,y,dx,dy = geom.getRect()
        mngr.window.setGeometry(2000, 100, dx,dy)  
    if savefig is not None:
        plt.savefig(savefig + '/figure_2_'+target+'.png')
        
# =============================================================================
#     test_fig = plt.figure()
#     x0 = anal_data[sheet_name]['alloc_min_' + optm_type]
#     x1 = anal_data[sheet_name]['alloc_max_' + optm_type]
#     dx = x1 - x0
#     ratio = np.linspace(0,1, 100)
#     equity = [func.calc_equity(x0 + i * dx) for i in ratio]
#     plt.plot(equity)
# =============================================================================
    
    return fig, axes

def generate_sfigx(anal_data, target = 'c', other_screen = False, savefig = None):
    acc_param_list = {'var': np.linspace(1.5 / 21, 0.5, 20),
                      'mean': np.arange(3, 23),
                      'domain': np.arange(0, 20)}
    
    fig_width, fig_height = 28, 16
    scale_prop, shape_prop = 0.8, 0.8
    fig = plt.figure(figsize = [fig_width * scale_prop, fig_height * scale_prop * shape_prop])
    axes = []
    gs = GridSpec(fig_height, fig_width, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:6, 0:8]))
    axes[-1].append(fig.add_subplot(gs[8:16, 0:8]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:6, 10:18]))
    axes[-1].append(fig.add_subplot(gs[8:16, 10:18]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:6, 20:28]))
    axes[-1].append(fig.add_subplot(gs[8:16, 20:28]))
    axes.append([])
    
    linewidth = 3
    colors = {'curve_'+target: 'tab:orange', 'curve_s': 'tab:blue', 
              'prdt_'+target: 'tab:purple', 'prdt_non_'+target: 'tab:purple'}
    labels = {'curve_'+target: 'Cumulative Infected', 'curve_s': 'Susceptible', 
              'prdt_'+target: 'Prediction', 
              'prdt_non_'+target: 'Prediction'}
    
    val_select = {'var':[acc_param_list['var'][0], acc_param_list['var'][10], acc_param_list['var'][-1]],
                  'mean':[3, 13, 22],
                  'domain':[5, 10, 15],}
    axins = []
    for idx, x_type in enumerate(['var', 'mean', 'domain']):
        ax = axes[idx][0]
        removal_all_spine(ax)
        colors = ['tab:blue', 'tab:green', 'tab:orange']
        axins.append([])
        for i in range(3):
            axins[-1].append(ax.inset_axes([0, (2 - i) / 3, 1, 0.6], zorder=3-i))
            axin = axins[-1][-1]
            axin.spines['top'].set_visible(False)
            axin.spines['right'].set_visible(False)
            axin.spines['left'].set_visible(False)
            axin.yaxis.set_ticks([])
            axin.set_yticklabels([])
            if i == 2: 
                axin.tick_params(axis='x', which='major', labelsize=15)
                axin.tick_params('both', width = 1.5)
                axin.spines['bottom'].set_linewidth(1.5)
                axin.set_xlabel(r'$\tau$', fontsize = 16)
            else:
                axin.xaxis.set_ticks([])
                axin.spines['bottom'].set_visible(False)
                axin.set_xticklabels([])
            val = val_select[x_type][i]
            if idx == 0:
                delay_day = 7
                alphabeta = 0.25 * 3 / val - 0.5
                srv_imm = func.srv_beta(alphabeta, alphabeta, 3 * 200 + 1, 0.01, shift = (delay_day - 3) * 100)
                tau = np.arange(0, 14 * 100) * 0.01
                psi = np.append(func.get_dist_from_srv(srv_imm) * 100, np.zeros(400))
                axin.fill_between(tau, psi, color=colors[i], alpha=0.5, linewidth = 2)
                if i == 0: val_str = "{:.2e}".format(val)
                elif i == 1: val_str = "{:.2e}".format(val)
                else: val_str = str(val)
                axin.text(0, 0.5 if i == 0 else 0.3, 'Variance = ' + val_str, color = colors[i], fontsize = 12)
                axin.set_ylim(0, 1.2)
                axin.set_xlim(0, 14)
            elif idx == 1:
                srv_imm = func.srv_beta(3, 3, 3 * 200 + 1, 0.01, shift = (val - 3) * 100)
                tau = np.arange(25 * 100) * 0.01
                psi = np.append(func.get_dist_from_srv(srv_imm) * 100, np.zeros((22 - val) * 100))
                axin.fill_between(tau, psi, np.zeros(25 * 100), color=colors[i], alpha=0.5, linewidth = 2)
                axin.text(6 if i == 0 else 0, 0.15, 'Mean = ' + str(val), color = colors[i], fontsize = 12)
                axin.set_ylim(0, 0.6)
                axin.set_xlim(0, 25)
            elif idx == 2:
                srv_imm = func.srv_beta(3, 3, val * 100 + 1, 0.01) if val != 0 else np.array([1, 0])
                tau = np.arange(19 * 100) * 0.01
                psi = np.append(func.get_dist_from_srv(srv_imm) * 100, np.zeros((19 - val) * 100))
                axin.fill_between(tau, psi, np.zeros(19 * 100), color=colors[i], alpha=0.5, linewidth = 2)
                axin.text(10, 0.15, 'Domain = ' + str(val), color = colors[i], fontsize = 12)
                axin.set_ylim(0, 0.6)
                axin.set_xlim(0, 15)
                if i == 2: axin.set_xticks(np.linspace(0, 15, 6))
                
    linestyles = [':', '-.', '--']
    axin_set = []
    sheet_name = 'acc_compr_' + target
    xlabels = {'var': 'Variance', 'mean': 'Mean', 'domain': 'Domain Length'}
    for idx, x_type in enumerate(['var', 'mean', 'domain']):
        ax = axes[idx][1]
        plt.sca(ax)
        plt.plot(anal_data[sheet_name][x_type], 
                 anal_data[sheet_name][x_type + '_varepsilon'], 
                 marker = 'x', markersize = 12, color = 'tab:red',
                 linestyle = 'none', markeredgewidth = 2, markerfacecolor = 'none',
                 label = r'$\tilde{\chi}^\mathrm{approx}_\mathrm{c, min} - \tilde{\chi}^\mathrm{acc}_\mathrm{c, min}$')
        plt.plot(anal_data[sheet_name][x_type], 
                 anal_data[sheet_name][x_type + '_sigma'],
                 marker = 'o',  markersize = 12, color = 'black',
                 linestyle = 'none', markeredgewidth = 2, markerfacecolor = 'none',
                 label = r'$\tilde{\chi}_\mathrm{c, 0} - \tilde{\chi}^\mathrm{acc}_\mathrm{c, min}$')
        set_spine_linewidth(ax, 1.5)
        set_tick_fontsize(ax, 15)
        set_xylabel(ax, xlabels[x_type], 'Fraction (%)', 15)
        
        if idx == 0: 
            ax.set_yticks(np.arange(0, 0.05, 0.01), np.arange(0, 5, 1))
            axin = ax.inset_axes([0.6, 0.25, 0.32, 0.4])
            axin.set_yticks(np.arange(0, 0.016, 0.004), np.arange(0, 16, 4) / 10)
        elif idx == 1: 
            ax.set_yticks(np.arange(0, 0.25, 0.05), np.arange(0, 25, 5))
            axin = ax.inset_axes([0.63, 0.55, 0.32, 0.4])
            axin.set_yticks(np.arange(0, 0.008, 0.002), np.arange(0, 8, 2)/10)
        else: 
            ax.set_yticks(np.arange(0, 0.6, 0.1), np.arange(0, 60, 10))
            axin = ax.inset_axes([0.65, 0.55, 0.32, 0.4])
            axin.set_yticks(np.arange(0, 0.08, 0.02), np.arange(0, 8, 2))
        
        axin_set.append(axin)
        axin.plot(anal_data[sheet_name][x_type], anal_data[sheet_name][x_type + '_ratio'], '.')
        if idx == 0: plt.legend(fontsize = 15, loc = 2)
        for i in range(3):
            plt.axvline(val_select[x_type][i], linestyle = linestyles[i], 
                        color = colors[i], linewidth = 3)
        set_spine_linewidth(axin, 1)
        set_tick_fontsize(axin, 9)
        set_xylabel(axin, xlabels[x_type], 'Fraction (%)', 12)
        axin.set_xticks(ax.get_xticks())
        axin.set_xlim(ax.get_xlim())
    set_ax_index(axes, 20)
    if savefig is not None:
        plt.savefig(savefig + '/sfigure_x_'+target+'.png')
    return fig, axes

def generate_fig3(anal_data, target = 'c', other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 11, 15
    scale_prop, shape_prop = 100, 1
    fig_width, fig_height = grid_row * scale_prop * shape_prop * unit / dpi, grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:11, 0:11]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:3, 12:15]))
    axes[-1].append(fig.add_subplot(gs[4:7, 12:15]))
    axes[-1].append(fig.add_subplot(gs[8:11, 12:15]))
    
    markers = ['^', '+', 'x']
    colors = ['tab:orange', 'tab:blue', 'tab:red']
    labels = [r'$T_{\mathrm{inf}} = 1.5$, $T_{\mathrm{rem}} = 3.5$', 
              r'$T_{\mathrm{inf}} = 2$, $T_{\mathrm{rem}} = 3$', 
              r'$T_{\mathrm{inf}} = 2.5$, $T_{\mathrm{rem}} = 2.5$']
    dist_labels = {'weibull': 'Weibull', 'gamma': 'Gamma', 'lognormal': 'Log-normal'}
    sheet_name = 'ratio_' + target
    colors = {'weibull': ['tab:cyan', 'tab:blue', 'tab:red'], 
              'gamma': ['tab:pink', 'tab:purple', 'tab:brown'],
              'lognormal': ['tab:gray', 'tab:green', 'tab:orange']}
    ax = axes[0][0]
    plt.sca(ax)
    for expt_type in ['weibull', 'gamma', 'lognormal']:
        for idx in range(3):
            plt.plot(anal_data[sheet_name]['ratio_'+expt_type+'_' + str(idx) + '_g_tvac' ], 
                     anal_data[sheet_name]['ratio_'+expt_type+'_' + str(idx) + '_necs'], 
                     markers[idx], color = colors[expt_type][idx], 
                     fillstyle='none', label = dist_labels[expt_type] + ': ' + labels[idx], 
                     markersize = 15 * unit, markeredgewidth = 2 * unit, markerfacecolor = 'none')
    set_spine_linewidth(ax, 2.5 * unit)
    set_xylabel(ax, r'$gT_\mathrm{resp}$', r'$\nu_{\mathrm{c}}$', 30 * unit, -0.075, -0.12)
    set_tick_fontsize(ax, 20 * unit)
    plt.legend(fontsize = 16 * unit)
    
    linewidth = 3 * unit
    for i in range(3):
        ax = axes[1][i]
        plt.sca(ax)
        sheet_name = 'illu_' + str(i) + '_'+ target
        colors = {'under_20': 'tab:purple', '20-49': 'tab:green', '20+':'tab:brown', 
                  '60+': 'tab:gray', 'all_ages': 'tab:orange', 
                  'min_'+target: 'tab:red', 'max_'+target: 'tab:blue',
                  'no_vac': 'black'}
        labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
                  '60+': '60+', 'all_ages': 'All Ages', 'min_'+target: 'Optimal', 'max_'+target: 'Worst',
                  'no_vac': 'No Vaccine'}
        for sttg in ['no_vac'] + list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target]:
            plt.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+sttg + '_gd'],
                     label = labels[sttg], color = colors[sttg], linewidth = linewidth)
    
    
    set_ax_index(axes, fontsize = 32 * unit)
    plt.subplots_adjust(top = 0.9, bottom = 0.12, left = 0.075, right = 0.985, 
                        hspace = 1, wspace = 1)       
    if savefig is not None:
        plt.savefig(savefig + '/figure_3_'+target+'.png')
    return fig, axes
    

def generate_fig4(anal_data, target = 'c', other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 9, 19
    scale_prop, shape_prop = 100, 1.1
    fig_width, fig_height = grid_row * scale_prop * shape_prop * unit / dpi, grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:9, 0:9]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:4, 10:14, ]))
    axes[-1].append(fig.add_subplot(gs[0:4, 15:19]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[5:9, 10:18]))
    
    
    ax = axes[0][0]
    plt.sca(ax)
    colors = ['tab:orange', 'tab:green', 'black']
    labels = [r'$gT_\mathrm{resp} = 0$', r'$gT_\mathrm{resp} = 1.8$', r'$gT_\mathrm{resp} = 3.6$']
    
    sheet_name = 'proc_' + target
    for idx in range(3):
        plt.plot(anal_data[sheet_name]['coe_' + str(idx)], 
                 anal_data[sheet_name]['res_' + str(idx)], 
                 label = labels[idx], color = colors[idx], 
                 linewidth = 2.5 * unit)
    ax.set_yticks(np.arange(0, 0.4, 0.1), np.arange(0, 40, 10))
    ax.set_xticks(np.arange(0, 1.2, 0.2), np.arange(0, 120, 20))
    
    plt.legend(fontsize = 20 * unit)
    set_spine_linewidth(ax, 2 * unit)
    set_xylabel(ax, r'$\varepsilon$ (%)', r'$\Delta_\mathrm{min}\tilde{\chi}_\mathrm{c}$ (%)', 
                25 * unit, -0.075, -0.06)
    set_tick_fontsize(ax, 20 * unit)
    
    
    group_amount = 8
    sheet_name = 'proc_alloc'
    colors = ['tab:blue', 'tab:red']
    titles = [r'Worst Allocation $\vartheta_\mathrm{worst, c}$', 
              r'Best Allocation $\vartheta_\mathrm{best, c}$']
    for idx, optm_dir in enumerate(['max', 'min']):
        ax = axes[1][idx]
        plt.sca(ax)
        ax.bar(np.arange(group_amount) * 10 + 5, 
               anal_data[sheet_name]['0_' + target + '_' + optm_dir], 
               color = colors[idx], width = 9)
        ax.set_ylim(0, 0.5)
        ax.set_yticks(np.arange(0, 0.60, 0.15), np.arange(0, 60, 15))
        ax.set_xticks(np.arange(0, 81, 10), np.arange(0, 81, 10))
        set_spine_linewidth(ax, 2 * unit)
        set_xylabel(ax, 'Age', 'Proportion (%)', 20 * unit, -0.125, -0.125)
        set_tick_fontsize(ax, 12.5 * unit)
        ax.set_title(titles[idx], fontsize = 16 * unit)
        
    ax = axes[2][0]
    plt.sca(ax)
    colors = {'under_20': 'tab:purple', '20-49': 'tab:green', '20+':'tab:brown', 
              '60+': 'tab:gray', 'all_ages': 'tab:orange', 
              'min': 'tab:red', 'max': 'tab:blue'}
    labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
              '60+': '60+', 'all_ages': 'All Ages', 'min': 'Best', 'max': 'Worst'}
    sheet_name = 'proc_sttg_' + target
    x_range = np.array([0, 10, 20])
    for idx, sttg in enumerate(list(basic_params.empirical_groups.keys()) + ['min', 'max']):
        plt.bar(x_range + idx - 3, anal_data[sheet_name][sttg], color = colors[sttg], width = 0.9, 
                label = labels[sttg])
    ax.set_xticks(x_range, np.array([0, 36 / 20, 36 / 10]))
    ax.set_yticks(np.arange(0, 0.8, 0.2), np.arange(0, 80, 20))
    
    plt.legend(fontsize = 12.5 * unit, bbox_to_anchor=(1, 1))
    set_spine_linewidth(ax, 2 * unit)
    set_xylabel(ax, r'$gT_\mathrm{resp}$', r'$\tilde{\chi}_\mathrm{c}$ (%)', 20 * unit, -0.15, -0.06)
    set_tick_fontsize(ax, 15 * unit)
    
    set_ax_index(axes, 30 * unit)
    plt.subplots_adjust(top = 0.9, bottom = 0.12, left = 0.075, right = 0.97, 
                        hspace = 1, wspace = 1)       
    if savefig is not None:
        plt.savefig(savefig + '/figure_4_'+target+'.png')
    return fig, axes
    



def generate_fig3x(anal_data, target = 'c', other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_width, grid_height = 19, 19
    scale_prop, shape_prop = 80, 1.2
    fig_width, fig_height = grid_width * scale_prop * shape_prop * unit / dpi, grid_height * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    axes = []
    gs = GridSpec(grid_height, grid_width, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:9, 0:9]))
    axes[-1].append(fig.add_subplot(gs[1:8, 10:19]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[10:19, 0:9]))
    axes[-1].append(fig.add_subplot(gs[10:14, 12:17]))
    axes[-1].append(fig.add_subplot(gs[15:19, 12:17]))
    
    ax = axes[0][0]
    plt.sca(ax)
    markers = ['^', '+', 'x']
    colors = ['tab:orange', 'tab:blue', 'tab:red']
    labels = [r'$T_{\mathrm{inf}} = 1.5$, $T_{\mathrm{rem}} = 3.5$', 
              r'$T_{\mathrm{inf}} = 2$, $T_{\mathrm{rem}} = 3$', 
              r'$T_{\mathrm{inf}} = 2.5$, $T_{\mathrm{rem}} = 2.5$']
    dist_labels = {'weibull': 'Weibull', 'gamma': 'Gamma', 'lognormal': 'Log-normal'}
    sheet_name = 'ratio_' + target
    colors = {'weibull': ['tab:cyan', 'tab:blue', 'tab:red'], 
              'gamma': ['tab:pink', 'tab:purple', 'tab:brown'],
              'lognormal': ['tab:gray', 'tab:green', 'tab:orange']}
    for expt_type in ['weibull', 'gamma', 'lognormal']:
        for idx in range(3):
            plt.plot(anal_data[sheet_name]['ratio_'+expt_type+'_' + str(idx) + '_g_tvac'], 
                     anal_data[sheet_name]['ratio_'+expt_type+'_' + str(idx) + '_necs'], 
                     markers[idx], color = colors[expt_type][idx], 
                     fillstyle='none', label = dist_labels[expt_type] + ': ' + labels[idx], 
                     markersize = 12 * unit, markeredgewidth = 2 * unit, markerfacecolor = 'none')
    
    plt.legend(fontsize = 12 * unit)
    set_spine_linewidth(ax, 2 * unit)
    set_xylabel(ax, r'$gT_\mathrm{resp}$', r'$\nu_{\mathrm{c}}$', 30 * unit, -0.08, -0.12)
    set_tick_fontsize(ax, 20 * unit)
    
    ax = axes[0][1]
    plt.sca(ax)
    colors = {'under_20': 'tab:purple', '20-49': 'tab:green', '20+':'tab:brown', 
              '60+': 'tab:gray', 'all_ages': 'tab:orange', 
              'min': 'tab:red', 'max': 'tab:blue'}
    labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
              '60+': '60+', 'all_ages': 'All Ages', 'min': 'Best', 'max': 'Worst'}
    sheet_name = 'ratio_prdt_' + target
    x_range = np.array([0, 10, 20])
    for idx, sttg in enumerate(list(basic_params.empirical_groups.keys()) + ['min', 'max']):
        plt.bar(x_range + idx - 3, anal_data[sheet_name][sttg], color = colors[sttg], width = 0.9, 
                label = labels[sttg])
    ax.set_xticks(x_range, anal_data[sheet_name]['g_tvac'])
    plt.legend(fontsize = 12 * unit, bbox_to_anchor=(1, 1))
    set_spine_linewidth(ax, 1.5 * unit)
    set_xylabel(ax, r'$gT_\mathrm{resp}$', r'$\tilde{\chi}_{\mathrm{c}}$', 20 * unit)
    set_tick_fontsize(ax, 15 * unit)
    
    ax = axes[1][0]
    plt.sca(ax)
    colors = ['tab:orange', 'tab:green', 'black']
    labels = [r'$gT_\mathrm{resp} = 0.36$', r'$gT_\mathrm{resp} = 1.81$', r'$gT_\mathrm{resp} = 3.62$']
    
    sheet_name = 'proc_' + target
    for idx in range(3):
        plt.plot(anal_data[sheet_name]['coe_' + str(idx)], 
                 anal_data[sheet_name]['res_' + str(idx)], 
                 label = labels[idx], color = colors[idx], linewidth = 2.5 * unit)
    plt.legend(fontsize = 15 * unit)
    set_spine_linewidth(ax, 1.5 * unit)
    set_xylabel(ax, r'$\varsigma$', r'$\Delta_\mathrm{min}\tilde{\chi}_\mathrm{c}$', 20 * unit, -0.08, -0.12)
    set_tick_fontsize(ax, 15 * unit)
    
    
    group_amount = 8
    sheet_name = 'proc_alloc'
    colors = ['tab:blue', 'tab:red']
    titles = ['Worst Allocation', 'Best Allocation']
    for idx, optm_dir in enumerate(['max', 'min']):
        ax = axes[1][idx + 1]
        plt.sca(ax)
        ax.bar(np.arange(group_amount) * 10 + 5, 
               anal_data[sheet_name]['0_' + target + '_' + optm_dir], 
               color = colors[idx], width = 9)
        ax.set_yticks(np.arange(0, 0.60, 0.15), np.arange(0, 60, 15))
        ax.set_xticks(np.arange(0, 81, 10), np.arange(0, 81, 10))
        set_spine_linewidth(ax, 1.5 * unit)
        set_xylabel(ax, 'Age', 'Fraction (%)', 12 * unit)
        set_tick_fontsize(ax, 10 * unit)
        ax.set_title(titles[idx], fontsize = 12 * unit)
    
# =============================================================================
#     mean_inf, mean_rem = 2, 3
#     alpha_inf, alpha_rem = 1.5, 3
#     beta_inf = basic_params.beta_funcs['Weibull'](alpha_inf, mean_inf)
#     beta_rem = basic_params.beta_funcs['Weibull'](alpha_rem, mean_rem)
#     g_val = func.find_g(func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, basic_params.step), 
#                         func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, basic_params.step), 
#                         2, basic_params.step)
#     g_data = {'covid_19': 14 * func.find_g_from_gen(func.srv_weibull(2.826, 5.665, 16000, 0.01), 2, 0.01),
#               'covid_delta': 14 * 0.14,
#               'covid_omicron': 14 * 0.137, 
#               'h1n1': 14 * 0.106}
#     r0_data = {'covid_19': 2, 'covid_delta': 1.44, 'covid_omicron': 1.90, 'h1n1': 1.36}
#     markers = ['o', 'D', '+', 'x']
#     legends = {'covid_19': 'COVID-19 (ancestral)', 'covid_delta': 'COVID-19 (Delta)', 
#                'covid_omicron': 'COVID-19 (Omicron)', 'h1n1': 'H1N1'}
#     eff_data = {'Pfizer/BioNTech': {'Acestral': 0.95, 'Delta': 0.83, 'Omicron': 0.88},
#                 'Sinopharm': {'Acestral': 0.69, 'Delta': 0.67}, 
#                 'Moderna': {'Acestral': 0.97, 'Delta': 0.91},
#                 'Novavax': {'Acestral': 0.83, 'Delta': 0.51}}
# =============================================================================
    
    set_ax_index(axes, 20 * unit)
    plt.subplots_adjust(top = 0.93, bottom = 0.125, left = 0.1, right = 0.9, 
                        hspace = 1, wspace = 1)  
    if savefig is not None:
        plt.savefig(savefig + '/figure_s3x_'+target+'.png')     
    return fig, axes


def generate_fig5(anal_data, ext = False, other_screen = False, savefig = None):
    param_name = 'r0_ext' if ext else 'r0'
    
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 26, 27
    scale_prop, shape_prop = 50, 1.2
    fig_width = grid_row * scale_prop * shape_prop * unit / dpi
    fig_height = grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:12, 0:12]))
    axes[-1].append(fig.add_subplot(gs[0:12, 15:27]))
    
    
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[13:16, 0:3]))
    axes[-1].append(fig.add_subplot(gs[13:16, 4:7]))
    axes[-1].append(fig.add_subplot(gs[13:16, 8:11]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[13:16, 15:18]))
    axes[-1].append(fig.add_subplot(gs[13:16, 19:22]))
    axes[-1].append(fig.add_subplot(gs[13:16, 23:26]))
    
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[17:21, 0:4]))
    axes[-1].append(fig.add_subplot(gs[22:26, 0:4]))
    axes[-1].append(fig.add_subplot(gs[17:26, 5:12]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[17:21, 15:19]))
    axes[-1].append(fig.add_subplot(gs[22:26, 15:19]))
    axes[-1].append(fig.add_subplot(gs[17:26, 20:27]))
    
    titles = ['Cumulative Infections', 'Deaths']
    for idx, target in enumerate(['c', 'd']):
        sheet_name = 'necs_with_' + param_name + '_' + target
        ax = axes[0][idx]
        plt.sca(ax)
        res = [anal_data[sheet_name][str(i)] for i in range(tasks.task_info['necs_with_r0'][1])]
        im = plt.imshow(res)
        cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
        ax.invert_yaxis()
        ax.set_xticks(np.arange(0, 40, 6), (np.arange(0, 40, 6) + 11) / 10)
        ax.set_yticks(np.arange(0, 3.6, 0.7) * 4 / 0.36, np.arange(0, 36, 7) / 10)
        set_spine_linewidth(ax, 2 * unit)
        set_xylabel(ax, r'$R_0$', r'$gT_\mathrm{resp}$', 20 * unit, 
                    xlabel_coords=-0.06, ylabel_coords=-0.08)
        set_tick_fontsize(ax, 15 * unit)
        set_spine_linewidth(ax, 2 * unit)
        set_tick_fontsize(cbar.ax, 15 * unit)
        set_cbar_spine_linewidth(cbar, 2 * unit)
        plt.title(titles[idx], fontsize = 25 * unit)
    
    
    linewidth = 3 * unit
    for idx, target in enumerate(['c', 'd']):
        for i in range(3):
            ax = axes[idx + 1][i]
            plt.sca(ax)
            sheet_name = 'r0examples_' + str(i) + '_'+ target
            colors = {'under_20': 'tab:purple', '20-49': 'tab:green', '20+':'tab:brown', 
                      '60+': 'tab:gray', 'all_ages': 'tab:orange', 
                      'min_'+target: 'tab:red', 'max_'+target: 'tab:blue',
                      'no_vac': 'black'}
            labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
                      '60+': '60+', 'all_ages': 'All Ages', 'min_'+target: 'Optimal', 'max_'+target: 'Worst',
                      'no_vac': 'No Vaccine'}
            for sttg in ['no_vac'] + list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target]:
                plt.plot(anal_data[sheet_name]['time_line'], anal_data[sheet_name]['curve_'+sttg + '_gd'],
                         label = labels[sttg], color = colors[sttg], linewidth = linewidth)
            plt.ylim(0, [1, 0.025][idx])
    
    
    alloc_colors = ['tab:red', 'black']
    titles = [r'$\vartheta_\mathrm{best, c}$', r'$\vartheta_\mathrm{best, d}$']
    for idx, r0_idx in enumerate(['9', '39']):
        sheet_name = 'alloc_with_' + param_name
        data_tmp = anal_data[sheet_name]
        for i, meth_target in enumerate(['c', 'd']):
            ax = axes[idx + 3][i]
            plt.sca(ax)
            plt.bar(np.arange(basic_params.group_amount) * 10 + 5, 
                    data_tmp['min_' + meth_target + '_' + r0_idx],
                    color = alloc_colors[i], width = 9)
            ax.set_xticks(np.arange(0, 81, 10), np.arange(0, 81, 10))
            ax.set_yticks(np.arange(0, 0.6, 0.15), np.arange(0, 60, 15))
            ax.set_ylim(0, 0.5)
            ax.text(0.02, 0.98, titles[i], fontsize = 15 * unit, color = alloc_colors[i],
                    horizontalalignment='left', verticalalignment='top', 
                    transform= ax.transAxes)
            set_spine_linewidth(ax, 1.5 * unit)
            set_tick_fontsize(ax, 10 * unit)
            set_xylabel(ax, 'Age', 'Fraction (%)', 15 * unit, 
                        xlabel_coords=-0.175, ylabel_coords=-0.15)
        sheet_name = 'prdt_with_' + param_name
        data_tmp = anal_data[sheet_name]
        ax_c = axes[idx + 3][2]
        ax_c.bar([-0.5, 0.5], [data_tmp['min_c_c_'+r0_idx], data_tmp['min_d_c_'+r0_idx]], 
                 width = 0.92, color = 'none', edgecolor = alloc_colors, linewidth = 2 * unit, hatch='///', 
                 label = [r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, c}$', 
                          r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, d}$'])
        
        ax_d =  ax_c.twinx()
        ax_d.bar([3.5, 4.5], [data_tmp['min_c_d_'+r0_idx], data_tmp['min_d_d_'+r0_idx]], 
                 width = 0.92, color = 'none', edgecolor = alloc_colors, linewidth = 2 * unit, hatch='...', 
                 label = [r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, c}$', 
                          r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, d}$'])
        if idx == 0: 
            ax_c.set_ylim(0, 0.65)
            ax_d.set_ylim(0, 0.0045)
            ax_c.set_yticks(np.arange(0, 0.8, 0.2), np.arange(0, 80, 20))
            ax_d.set_yticks(np.arange(0, 0.0045, 0.0005), np.arange(0, 45, 5) / 100)
            ax_c.legend(loc = 'upper left', fontsize = 12.5 * unit)
            ax_d.legend(loc = 'upper right', fontsize = 12.5 * unit)
        else: 
            ax_c.set_ylim(0, 0.85)
            ax_d.set_ylim(0, 0.0175)
            ax_c.set_yticks(np.arange(0, 1, 0.2), np.arange(0, 100, 20))
            ax_d.set_yticks(np.arange(0, 0.02, 0.004), np.arange(0, 20, 4) / 10)
        ax_c.set_xticks([0, 4], ['Cumulative Infections', 'Deaths'], fontsize = 20 * unit)
        set_xylabel(ax_c, None, 'Fraction (%)', 15 * unit, xlabel_coords=-0.075, ylabel_coords=-0.1)
        set_xylabel(ax_d, None, 'Fraction (%)', 15 * unit, xlabel_coords=-0.075, ylabel_coords=1.15)
        set_spine_linewidth(ax_c, 1.5 * unit)
        set_tick_fontsize(ax_c, 15 * unit)
        set_spine_linewidth(ax_d, 1.5 * unit)
        set_tick_fontsize(ax_d, 15 * unit)
        
    set_ax_index(axes, 20 * unit)
    plt.subplots_adjust(top = 0.97, bottom = 0.05, left = 0.035, right = 0.95, 
                        hspace = 1, wspace = 1)    
    if savefig is not None:
        plt.savefig(savefig + '/figure_5.png')     
    return fig, axes


def generate_fig6(anal_data, target = 'c', other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 13, 13
    scale_prop, shape_prop = 100, 1.2
    fig_width = grid_row * scale_prop * shape_prop * unit / dpi
    fig_height = grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:6, 0:6]))
    axes[-1].append(fig.add_subplot(gs[0:6, 7:13]))
    axes[-1].append(fig.add_subplot(gs[7:13, 0:6]))
    axes[-1].append(fig.add_subplot(gs[7:13, 7:13]))
    
    mean_inf, mean_rem = 2, 3
    alpha_inf, alpha_rem = 1.5, 3
    beta_inf = basic_params.beta_funcs['Weibull'](alpha_inf, mean_inf)
    beta_rem = basic_params.beta_funcs['Weibull'](alpha_rem, mean_rem)
    g_val = func.find_g(func.srv_weibull(alpha_inf, beta_inf, basic_params.srv_length, basic_params.step), 
                        func.srv_weibull(alpha_rem, beta_rem, basic_params.srv_length, basic_params.step), 
                        2, basic_params.step)
    xlabels = ['Vaccine Efficacy', 'Vaccine Availability', 'Percentile', 'Duration']
    for idx, param in enumerate(['vac_eff', 'vac_avail', 'c_perct', 'vac_dur']):
        sheet_name = 'necs_with_' + param + '_' + target
        ax = axes[0][idx]
        plt.sca(ax)
        res = [anal_data[sheet_name][str(i)] for i in range(tasks.task_info['necs_with_' + param][1])]
        im = plt.imshow(res)
        cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
        ax.invert_yaxis()
        if idx == 0: ax.set_xticks(np.arange(0, 40, 13), np.arange(22, 102, 26) / 100)
        elif idx == 1: ax.set_xticks(np.arange(0, 40, 13), np.arange(12, 92, 26) / 100)
        elif idx == 2: ax.set_xticks(np.arange(0, 40, 13), np.arange(215, 815, 15 * 13) / 10)
        elif idx == 3: ax.set_xticks(np.arange(0, 40, 13), np.arange(1, 41, 13))
        else: pass
        ax.set_yticks(np.arange(0, 3.6, 0.7) * 4 / g_val, np.arange(0, 36, 7) / 10)
        set_xylabel(ax, xlabels[idx], r'$gT_\mathrm{resp}$', 20 * unit)
        set_tick_fontsize(ax, 15 * unit)
        set_spine_linewidth(ax, 2 * unit)
        set_tick_fontsize(cbar.ax, 15 * unit)
        set_cbar_spine_linewidth(cbar, 2 * unit)
        set_tick_fontsize(cbar.ax, 20 * unit)
        
    set_ax_index(axes, 25 * unit)
    plt.subplots_adjust(top = 0.96, bottom = 0.12, left = 0, right = 0.95, 
                        hspace = 1, wspace = 0)    
    if savefig is not None:
        plt.savefig(savefig + '/figure_6_'+target+'.png')
    return fig, axes

def generate_fig_countries(anal_data, other_screen = False, savefig = None):
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 13, 13
    scale_prop, shape_prop = 100, 1.2
    fig_width = grid_row * scale_prop * shape_prop * unit / dpi
    fig_height = grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:6, 0:6]))
    axes[-1].append(fig.add_subplot(gs[0:6, 7:13]))
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[7:13, 0:6]))
    axes[-1].append(fig.add_subplot(gs[7:13, 7:13]))
    
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland']
    
    for idx, target in enumerate(['c', 'd']):
        plt.sca(axes[idx][1])
        plt.boxplot([anal_data[f'necs_countries_{target}'][country] for country in countries], vert=True, patch_artist=True, labels=countries)
        plt.xticks(rotation=45)
    return fig, axes
    


def generate_fig_equity(anal_data, ext = False, other_screen = False, savefig = None):
    param_name = 'r0'
    
    dpi = plt.rcParams['figure.dpi']
    grid_col, grid_row = 12, 27
    scale_prop, shape_prop = 60, 1.2
    fig_width = grid_row * scale_prop * shape_prop * unit / dpi
    fig_height = grid_col * scale_prop * unit / dpi
    fig = plt.figure(figsize = [fig_width, fig_height])
    
    axes = []
    gs = GridSpec(grid_col, grid_row, figure = fig)
    axes.append([])
    axes[-1].append(fig.add_subplot(gs[0:12, 0:12]))
    axes[-1].append(fig.add_subplot(gs[0:12, 15:27]))
    
    titles = ['Cumulative Infections', 'Deaths']
    for idx, target in enumerate(['c', 'd']):
        sheet_name = 'equity_with_' + param_name + '_' + target
        ax = axes[0][idx]
        plt.sca(ax)
        res = [anal_data[sheet_name][str(i)] for i in range(tasks.task_info['necs_with_r0'][1])]
        im = plt.imshow(res)
        cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
        ax.invert_yaxis()
        ax.set_xticks(np.arange(0, 40, 6), (np.arange(0, 40, 6) + 11) / 10)
        ax.set_yticks(np.arange(0, 3.6, 0.7) * 4 / 0.36, np.arange(0, 36, 7) / 10)
        set_spine_linewidth(ax, 2 * unit)
        set_xylabel(ax, r'$R_0$', r'$gT_\mathrm{resp}$', 20 * unit, 
                    xlabel_coords=-0.06, ylabel_coords=-0.08)
        set_tick_fontsize(ax, 15 * unit)
        set_spine_linewidth(ax, 2 * unit)
        set_tick_fontsize(cbar.ax, 15 * unit)
        set_cbar_spine_linewidth(cbar, 2 * unit)
        plt.title(titles[idx], fontsize = 25 * unit)














