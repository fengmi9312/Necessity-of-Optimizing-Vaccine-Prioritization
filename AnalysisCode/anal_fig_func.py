# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:05:51 2024

@author: fengm
"""

import matplotlib.pyplot as plt
import numpy as np

def generate_no_vac_prdt_fig(ax, anal_data, time_sttg = 'one_time', target = 'c',
                              inf_pow = 4, rem_pow = 8, delay_day = 4):
    colors = {'curve_'+target: 'tab:red', 'curve_s': 'tab:blue', 'curve_s_eff':'tab:orange', 
              'prdt_'+target: 'tab:purple', 'prdt_non_'+target: 'tab:purple'}
    labels = {'curve_'+target: 'Cumulative Infected', 'curve_s': 'Susceptible', 
              'curve_s_eff':'Effective Susceptible', 
              'prdt_'+target: 'Prediction with Memory', 
              'prdt_non_'+target: 'Prediction without Memory'}
    plt.sca(ax)
    fig_data = anal_data['no_vac_prdt_' + str(inf_pow) + '_' + str(rem_pow) + '_' + time_sttg + '_' + target]
    for line_name in ['time_line', 'curve_'+target, 'prdt_'+target, 'prdt_non_'+target]:
        plt.plot(fig_data['time_line'], fig_data[line_name], color = colors[line_name], label = labels[line_name])
    return ax

def generate_rand_vac_prdt_fig(ax, anal_data, time_sttg = 'one_time', target = 'c',
                               inf_pow = 4, rem_pow = 8, delay_day = 4):
    colors = {'curve_'+target: 'tab:red', 'curve_s': 'tab:blue', 'curve_s_eff':'tab:orange', 
              'prdt_'+target: 'tab:purple', 'prdt_non_'+target: 'tab:purple'}
    labels = {'curve_'+target: 'Cumulative Infected', 'curve_s': 'Susceptible', 
              'curve_s_eff':'Effective Susceptible', 
              'prdt_'+target: 'Prediction with Memory', 
              'prdt_non_'+target: 'Prediction without Memory'}
    plt.sca(ax)
    fig_data = anal_data['rand_vac_prdt_' + str(inf_pow) + '_' + str(rem_pow) + '_' + time_sttg + '_' + target]
    output_lines = ['time_line', 'curve_'+target, 'prdt_'+target, 'curve_s', 'curve_s_eff'] if target == 'c' \
                  else ['time_line', 'curve_'+target, 'prdt_'+target]
    for line_name in output_lines:
        plt.plot(fig_data['time_line'], fig_data[line_name], color = colors[line_name], label = labels[line_name])
    return ax

def generate_sttg_compr_fig(ax, anal_data, time_sttg = 'one_time', target = 'c',
                            inf_pow = 4, rem_pow = 8, delay_day = 4):
    colors = {'under_20': 'tab:blue', '20-49': 'tab:green', '20+':'tab:brown', 
              '60+': 'tab:gray', 'all_ages': 'tab:orange', 'min_'+target: 'tab:red',
              'no_vac': 'black'}
    labels = {'under_20': 'Under 20', '20-49': '20-49', '20+':'20+', 
              '60+': '60+', 'all_ages': 'All Ages', 'min_'+target: 'Optimal',
              'no_vac': 'No Vaccine'}
    plt.sca(ax)
    linewidth = 1.5
    vac_group_keys = ['under_20', '20-49', '20+', '60+', 'all_ages']
    fig_data = anal_data['sttg_compr_' + str(inf_pow) + '_' + str(rem_pow) + '_' + time_sttg + '_' + target]
    for sttg in vac_group_keys + ['min_'+target, 'no_vac']:
        plt.plot(fig_data['time_line'], fig_data['curve_'+sttg], label = labels[sttg], color = colors[sttg], linewidth = linewidth)
    return ax

def generate_sttg_compr_alloc_data(ax, anal_data, time_sttg = 'one_time', target = 'c',
                                   inf_pow = 4, rem_pow = 8, delay_day = 4):
    fig_data = anal_data['sttg_compr_alloc_' + str(inf_pow) + '_' + str(rem_pow) + '_' + time_sttg + '_' + target]
    age_groups = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
    ax.bar(np.arange(len(age_groups)), fig_data['vac_alloc'], color = 'tab:red')
    ax.set_xticks(range(len(age_groups)), age_groups, rotation=45, fontsize = 8)
    ax.set_yticks(np.linspace(0, 0.15, 4), list(map("{:.0f}".format, np.linspace(0, 0.15, 4) * 100)), fontsize = 8)
    ax.set_xlabel('age group', fontsize = 8)
    ax.set_ylabel('allocation (%)', fontsize = 8)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['top'].set_linewidth(1.5)
    ax.tick_params('both', width = 1.5)
    return ax

def generate_vc_data(expt_data, expt_type, time_sttg = 'one_time', target = 'c',
                     func_type = 'Weibull', mean_inf = 2, mean_rem = 3,
                     inf_pow = 4, rem_pow = 8, delay_day = 4):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow) + '_' + str(delay_day)
    anal_data[expt_type] =  expt_data[expt_type][param_type][expt_type + '_prdt_data'][expt_type].to_numpy()
    for sttg in vac_group_keys + ['min', 'max', 'no_vac']:
        anal_data[sttg] = expt_data[expt_type][param_type][expt_type +'_prdt_data'][time_sttg + '_prdt_' + sttg + '_' + target].to_numpy()
    return anal_data

def generate_vc_alloc_data(expt_data, expt_type, time_sttg = 'one_time', target = 'c',
                           func_type = 'Weibull', mean_inf = 2, mean_rem = 3,
                           inf_pow = 4, rem_pow = 8, delay_day = 4):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow) + '_' + str(delay_day)
    anal_data[expt_type] =  expt_data[expt_type][param_type][expt_type + '_prdt_data'][expt_type].to_numpy()
    for idx in np.arange(41):
        anal_data['alloc_min_' + target + '_' + str(idx)] = expt_data[expt_type][param_type][expt_type + '_alloc_data']['alloc_min_' + target + '_' + str(idx)].to_numpy() * calc_params['populations']
    return anal_data

      
def calc_metric(steady_state, init_state, vac_min, vac_max, metric = 0):
    if metric == 0:
        return (steady_state - vac_min) / (steady_state - init_state)
    elif metric == 1:
        return (vac_max - vac_min) / (steady_state - init_state)
    else:
        return (vac_max - vac_min) / (steady_state - vac_min)
    
def generate_vs_nect_data(expt_data, expt_type, metric_type, time_sttg = 'one_time', target = 'c',
                          func_type = 'Weibull', mean_inf = 2, mean_rem = 3,
                          inf_pow = 4, rem_pow = 8, delay_day = 4):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow) + '_' + str(delay_day)
    anal_data[expt_type] =  expt_data[expt_type][param_type][expt_type + '_prdt_data'][expt_type].to_numpy()
    steady_no_vac, steady_max, steady_min, steady_init =  expt_data[expt_type][param_type][expt_type +'_prdt_data'][time_sttg + '_prdt_no_vac_' + target].to_numpy(),\
                                                          expt_data[expt_type][param_type][expt_type +'_prdt_data'][time_sttg + '_prdt_max_' + target].to_numpy(),\
                                                          expt_data[expt_type][param_type][expt_type +'_prdt_data'][time_sttg + '_prdt_min_' + target].to_numpy(),\
                                                          init_targets[target]
    anal_data['res'] = calc_metric(steady_no_vac, steady_max, steady_min, steady_init, metric_type)
    return anal_data  

def generate_dist_list_data(expt_data, metric_type, time_sttg = 'one_time', target = 'c',
                          func_type = 'Weibull', mean_inf = 2, mean_rem = 3):
    anal_data = {}
    data_tmp = expt_data['dist_list'][func_type+'_'+'i'+str(mean_inf)+'r'+str(mean_rem)]['dist_list_prdt_data']
    steady_no_vac, steady_max, steady_min, steady_init =  data_tmp[time_sttg+'_prdt_no_vac_'+target].to_numpy(), \
                                                          data_tmp[time_sttg+'_prdt_max_'+target].to_numpy(), \
                                                          data_tmp[time_sttg+'_prdt_min_'+target].to_numpy(),\
                                                          init_targets[target]
    anal_data['ratio'] = data_tmp['ratio'].to_numpy()
    anal_data['res'] = calc_metric(steady_no_vac, steady_max, steady_min, steady_init, metric_type)
    return anal_data

