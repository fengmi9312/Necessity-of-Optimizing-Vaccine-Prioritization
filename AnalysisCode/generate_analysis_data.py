# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 12:30:18 2024

@author: fengmi9312
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import basic_params
import tasks
import func

def generate_prdt_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        sheet_name = 'prdt_' + target
        anal_data[sheet_name] = {}
        output_lines = ['time_line', 'curve_'+target, 'prdt_'+target, 'curve_s'] if target == 'c' \
                       else ['time_line', 'curve_'+target, 'prdt_'+target]
        for line_name in output_lines:
            anal_data[sheet_name][line_name + '_all_ages'] = expt_data['sttgs_curves'][0]['curves_all_ages_dd'][line_name].to_numpy() 
            anal_data[sheet_name][line_name + '_no_vac'] = expt_data['sttgs_curves'][0]['curves_no_vac_dd'][line_name].to_numpy()
    return anal_data

def generate_compr_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        sheet_name = 'compr_' + target
        anal_data[sheet_name] = {}
        line_len = min([len(expt_data['sttgs_curves'][0]['curves_' + sttg + '_gd']['time_line']) 
                        for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']])
        line_len = min([line_len, min([len(expt_data['sttgs_curves'][0]['curves_' + sttg + '_gg']['time_line']) 
                                       for sttg in ['min_'+target, 'max_'+target]])])
        anal_data[sheet_name]['time_line'] =  expt_data['sttgs_curves'][0]['curves_no_vac_gd']['time_line'].to_numpy()[:line_len]
        for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']:
            curve_sttg = 'curves_' + sttg + '_gd'
            anal_data[sheet_name]['curve_'+sttg + '_gd'] = expt_data['sttgs_curves'][0][curve_sttg]['curve_'+target].to_numpy()[:line_len]
# =============================================================================
#         for sttg in ['min_'+target, 'max_'+target]:
#             curve_sttg = 'curves_' + sttg + '_gd'
#             anal_data[sheet_name]['curve_'+sttg + '_gd'] = expt_data['sttgs_curves'][1][curve_sttg]['curve_'+target].to_numpy()[:line_len]
# =============================================================================
        sheet_name = 'compr_alloc_' + target
        anal_data[sheet_name] = {}
        for optm_dir in ['min', 'max']:
            optm_type = 'gd'
            anal_data[sheet_name]['alloc_' + optm_dir + '_' + optm_type] = \
            expt_data['sttgs_curves'][1]['alloc_data']['allocs_' + optm_dir + '_' + target + '_' + optm_type].to_numpy() * basic_params.calc_params['populations'] / 0.3
    return anal_data

def generate_illu_data(expt_data):
    anal_data = {}
    param_selected = [4,2,3]
    for target in basic_params.targets:
        for i in range(3):
            sheet_name = 'illu_' + str(i) + '_' + target
            anal_data[sheet_name] = {}
            line_len = min([len(expt_data['sttgs_curves'][param_selected[i]]['curves_' + sttg + '_gd']['time_line']) 
                            for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']])
            line_len = min([line_len, min([len(expt_data['sttgs_curves'][param_selected[i]]['curves_' + sttg + '_gg']['time_line']) 
                                           for sttg in ['min_'+target, 'max_'+target]])])
            anal_data[sheet_name]['time_line'] =  expt_data['sttgs_curves'][param_selected[i]]['curves_no_vac_gd']['time_line'].to_numpy()[:line_len]
            for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']:
                curve_sttg = 'curves_' + sttg + '_gd'
                anal_data[sheet_name]['curve_'+sttg + '_gd'] = expt_data['sttgs_curves'][param_selected[i]][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    return anal_data

def generate_r0examles_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        for i in range(3):
            sheet_name = 'r0examples_' + str(i) + '_' + target
            anal_data[sheet_name] = {}
            line_len = min([len(expt_data['r0_examples'][i]['curves_' + sttg + '_gd']['time_line']) 
                            for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']])
            anal_data[sheet_name]['time_line'] =  expt_data['r0_examples'][i]['curves_no_vac_gd']['time_line'].to_numpy()[:line_len]
            for sttg in list(basic_params.empirical_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']:
                curve_sttg = 'curves_' + sttg + '_gd'
                anal_data[sheet_name]['curve_'+sttg + '_gd'] = expt_data['r0_examples'][i][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    return anal_data
    
def generate_acc_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        sheet_name = 'acc_compr_' + target
        anal_data[sheet_name] = {}
        for idx, x_type in enumerate(['var', 'mean', 'domain']):
            anal_data[sheet_name][x_type] = []
            anal_data[sheet_name][x_type + '_sigma'] = []
            anal_data[sheet_name][x_type + '_varepsilon'] = []
            anal_data[sheet_name][x_type + '_ratio'] = []
            for rank in range(tasks.task_info['acc_compr_with_' + x_type][1]):
                data_tmp = expt_data['acc_compr_with_' + x_type][rank]['prdt_data']
                anal_data[sheet_name][x_type].append(data_tmp[x_type][0])
                anal_data[sheet_name][x_type + '_sigma'].append(data_tmp['prdt_no_vac_' + target][0] - data_tmp['prdt_gg_min_' + target][0])
                anal_data[sheet_name][x_type + '_varepsilon'].append(data_tmp['prdt_gd_min_' + target][0] - data_tmp['prdt_gg_min_' + target][0])
                anal_data[sheet_name][x_type + '_ratio'].append(anal_data[sheet_name][x_type + '_varepsilon'][-1] / anal_data[sheet_name][x_type + '_sigma'][-1])
    return anal_data
    

def generate_ratio_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        sheet_name = 'ratio_' + target
        anal_data[sheet_name] = {}
        for expt_type in ['ratio_weibull_0', 'ratio_weibull_1', 'ratio_weibull_2', 
                        'ratio_gamma_0', 'ratio_gamma_1', 'ratio_gamma_2', 
                        'ratio_lognormal_0', 'ratio_lognormal_1', 'ratio_lognormal_2']:
            anal_data[sheet_name][expt_type + '_tvac'] = []
            anal_data[sheet_name][expt_type + '_g'] = []
            anal_data[sheet_name][expt_type + '_g_tvac'] = []
            anal_data[sheet_name][expt_type + '_necs'] = []
            for idx in range(9):
                data_tmp = expt_data[expt_type][idx]['prdt_data']
                anal_data[sheet_name][expt_type + '_tvac'] += data_tmp['delay_day'].tolist()
                anal_data[sheet_name][expt_type + '_g'] +=  data_tmp['growth_rate'].tolist()
                anal_data[sheet_name][expt_type + '_g_tvac'] +=  (data_tmp['growth_rate'] * data_tmp['delay_day']).tolist()
                anal_data[sheet_name][expt_type + '_necs'] += \
                (data_tmp['prdt_gd_max_' + target] - data_tmp['prdt_gd_min_' + target]).tolist()
        sheet_name = 'ratio_prdt_' + target
        anal_data[sheet_name] = {'g_tvac': []}
        for sttg in list(basic_params.empirical_groups.keys()) + ['min', 'max']:
            anal_data[sheet_name][sttg] = []
        g_idx = 80
        expt_type = 'ratio_lognormal_2'
        for delay_day in [0, 4, 8]:
            data_tmp = expt_data[expt_type][delay_day]['prdt_data']
            anal_data[sheet_name]['g_tvac'].append(delay_day * data_tmp['growth_rate'][g_idx])
            for sttg in list(basic_params.empirical_groups.keys()):
                anal_data[sheet_name][sttg].append(data_tmp['prdt_g_' + sttg + '_' + target][g_idx])
            for sttg in ['min', 'max']:
                anal_data[sheet_name][sttg].append(data_tmp['prdt_gd_' + sttg + '_' + target][g_idx])
    return anal_data

def generate_rgen_data(expt_data):
    anal_data = {}
    for target in basic_params.targets:
        sheet_name = 'ratio_gen_' + target
        anal_data[sheet_name] = {}
        for expt_type in ['ratio_gen_weibull_0', 'ratio_gen_weibull_1', 'ratio_gen_weibull_2', 
                          'ratio_gen_gamma_0', 'ratio_gen_gamma_1', 'ratio_gen_gamma_2', 
                          'ratio_gen_lognormal_0', 'ratio_gen_lognormal_1', 'ratio_gen_lognormal_2']:
            anal_data[sheet_name][expt_type + '_ratio'] = []
            anal_data[sheet_name][expt_type + '_necs'] = []
            data_tmp = expt_data[expt_type][0]['prdt_data']
            anal_data[sheet_name][expt_type + '_ratio'] += (data_tmp['growth_rate'] * data_tmp['delay']).tolist()
            anal_data[sheet_name][expt_type + '_necs'] += \
            (data_tmp['prdt_gd_max_' + target] - data_tmp['prdt_gd_min_' + target]).tolist()
    return anal_data

def generate_proc_data(expt_data):
    anal_data = {}
    data_tmp = expt_data['optm_proc'][0]
    for target in basic_params.targets:
        sheet_name = 'proc_' + target
        anal_data[sheet_name] = {}
        for idx in range(3):
            anal_data[sheet_name]['coe_' + str(idx)] = data_tmp['res_' + str(idx) + '_' + target]['coe']
            anal_data[sheet_name]['res_' + str(idx)] = data_tmp['res_' + str(idx) + '_' + target]['res'] - data_tmp['res_' + str(idx) + '_' + target]['res'][0]
    
    for target in basic_params.targets:
        sheet_name = 'proc_sttg_' + target
        anal_data[sheet_name] = {}
        for sttg in list(basic_params.empirical_groups.keys()) + ['max', 'min']:
            anal_data[sheet_name][sttg] = []
            for idx in range(3):
                anal_data[sheet_name][sttg].append(data_tmp['res_sttg_' + str(idx) + '_' + target][sttg][0])
    sheet_name = 'proc_alloc'
    data_tmp = expt_data['optm_proc'][0]['vac_alloc']
    anal_data[sheet_name] = {key: data_tmp[key] * basic_params.calc_params['populations'] / 0.3 for key in data_tmp.keys()}
    
    return anal_data
    
# =============================================================================
# def generata_necs_data_with_r0(expt_data):
#     import func
#     from copy import deepcopy
#     anal_data = {}
#     vac_avail = 0.3
#     derivate_list = []
#     func_type = 'Weibull'
#     mean_inf, mean_rem = 2, 3
#     alpha_inf, alpha_rem = 1.5, 3
#     beta_inf, beta_rem = basic_params.beta_funcs[func_type](alpha_inf, mean_inf), basic_params.beta_funcs[func_type](alpha_rem, mean_rem)
#     _calc_params = deepcopy(basic_params.calc_params)
#     _calc_params['srv_inf'], _calc_params['srv_rem'] = basic_params.srv_funcs[func_type](alpha_inf, beta_inf, basic_params.srv_length, basic_params.step), \
#                                                              basic_params.srv_funcs[func_type](alpha_rem, beta_rem, basic_params.srv_length, basic_params.step)
#     for r0 in np.linspace(1.1, 3.6, 26):
#         _calc_params['k'] = r0 / (np.linalg.eig(_calc_params['populations'] * _calc_params['contacts'][None, :])[0].max() * \
#                             func.lambda_eff_srv(_calc_params['srv_inf'], _calc_params['srv_rem']))
#         derivate_list.append(func.get_steady_state_derivative(r0, _calc_params['k'], _calc_params['populations'], _calc_params['contacts'], _i = 1e-3))
# 
#     for target in basic_params.targets:
#         sheet_name = 'necs_with_r0_' + target
#         anal_data[sheet_name] = {}
#         for idx, data_tmp in enumerate(expt_data['necs_with_r0']):
#             anal_data[sheet_name][str(idx)] = (data_tmp['prdt']['prdt_gd_max_' + target] - data_tmp['prdt']['prdt_gd_min_' + target]) / (vac_avail * (np.array(derivate_list) @ _calc_params['populations']))
#     return anal_data
# =============================================================================

def generate_necs_data(expt_data, param):
    anal_data = {}
    #vac_avail = 0.3 if param != 'vac_avail' else np.linspace(0.1, 0.9, 26)
    for target in basic_params.targets:
        sheet_name = 'necs_with_' + param + '_' + target
        anal_data[sheet_name] = {}
        for idx, data_tmp in enumerate(expt_data['necs_with_' + param]):
            anal_data[sheet_name][str(idx)] = data_tmp['prdt']['prdt_gd_max_' + target] - data_tmp['prdt']['prdt_gd_min_' + target]
    return anal_data

def generate_equity_data(expt_data, param):
    anal_data = {}
    #vac_avail = 0.3 if param != 'vac_avail' else np.linspace(0.1, 0.9, 26)
    for target in basic_params.targets:
        sheet_name = 'equity_with_' + param + '_' + target
        anal_data[sheet_name] = {}
        for idx, data_tmp in enumerate(expt_data['necs_with_' + param]):
            anal_data[sheet_name][str(idx)] = []
            for i in range(len(data_tmp['prdt'])):
                dist = (data_tmp['dist']['dist_no_vac_' + target + str(i)] - data_tmp['dist']['dist_gd_min_' + target + str(i)]) / data_tmp['dist']['dist_no_vac_' + target + str(i)]
                alloc = data_tmp['alloc']['alloc_min_' + target + str(i)] / data_tmp['alloc']['alloc_all_ages' + str(i)]
                anal_data[sheet_name][str(idx)].append(func.calc_equity(alloc))
    return anal_data


def calc_metric(idx, _data, target):
    if idx == 0:
        return _data['prdt_gd_max_' + target] - _data['prdt_gd_min_' + target]
    elif idx == 1:
        return _data['prdt_no_vac_' + target] - _data['prdt_gd_max_' + target]
    elif idx == 2:
        return _data['prdt_no_vac_' + target] - _data['prdt_gd_min_' + target]
    else:
        return None


def generate_necs_data_with_r0(expt_data, ext = False):
    anal_data = {}
    param_name = 'r0_ext' if ext else 'r0'
    dist_props = {'c': basic_params.calc_params['populations'], 
                  'd': basic_params.calc_params['populations'] * basic_params.calc_params['ifrs'], 
                  'y': basic_params.calc_params['populations'] * basic_params.calc_params['ifrs'] * basic_params.calc_params['ylls']}
    for target in basic_params.targets:
        sheet_name = 'necs_with_' + param_name + '_' + target
        anal_data[sheet_name] = {}
        for idx, data_tmp in enumerate(expt_data['necs_with_' + param_name]):
            anal_data[sheet_name][str(idx)] = calc_metric(0, data_tmp['prdt'], target)
    sheet_name = 'prdt_with_' + param_name
    anal_data[sheet_name] = {}
    data_tmp = expt_data['necs_with_' + param_name][0]
    for meth_target in basic_params.targets:
        for target in basic_params.targets:
            anal_data[sheet_name]['min_' + meth_target + '_' + target + '_9'] = (data_tmp['dist']['dist_gd_min_' + meth_target+'9'] / dist_props[meth_target]) @ dist_props[target]
            anal_data[sheet_name]['max_' + meth_target + '_' + target + '_9'] = (data_tmp['dist']['dist_gd_max_' + meth_target+'9'] / dist_props[meth_target]) @ dist_props[target]
            anal_data[sheet_name]['min_' + meth_target + '_' + target + '_39'] = (data_tmp['dist']['dist_gd_min_' + meth_target+'39'] / dist_props[meth_target]) @ dist_props[target]
            anal_data[sheet_name]['max_' + meth_target + '_' + target + '_39'] = (data_tmp['dist']['dist_gd_max_' + meth_target+'39'] / dist_props[meth_target]) @ dist_props[target]
    sheet_name = 'alloc_with_' + param_name
    anal_data[sheet_name] = {}
    data_tmp = expt_data['necs_with_' + param_name][0]
    for meth_target in basic_params.targets:
        anal_data[sheet_name]['min_' + meth_target + '_9'] = data_tmp['alloc']['alloc_min_' + meth_target+'9'] * basic_params.calc_params['populations'] / 0.3
        anal_data[sheet_name]['max_' + meth_target + '_9'] = data_tmp['alloc']['alloc_max_' + meth_target+'9'] * basic_params.calc_params['populations'] / 0.3
        anal_data[sheet_name]['min_' + meth_target + '_39'] = data_tmp['alloc']['alloc_min_' + meth_target+'39'] * basic_params.calc_params['populations'] / 0.3
        anal_data[sheet_name]['max_' + meth_target + '_39'] = data_tmp['alloc']['alloc_max_' + meth_target+'39'] * basic_params.calc_params['populations'] / 0.3
    
    return anal_data
    
def generate_necs_countries_data(expt_data):
    anal_data = {}
    countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    for target in basic_params.targets:
        #res = expt_data['necs_countries'][0]
        #min_len = min([len(res[f'curve_{optm_d}_{target}']['time_line']) for optm_d in ['max', 'min', 'no_vac']])
        #anal_data[f'country_curves_{target}'] = {'time_line': res['curve_no_vac']['time_line'][:min_len]}
        #for optm_d in ['max', 'min', 'no_vac']:
        #    for curve_type in ['central', 'lower', 'upper']:
        #        anal_data[f'curves_{target}'].update({f'{optm_d}_{curve_type}': res[f'curve_{optm_d}'][f'curve_{target}_{curve_type}'][:min_len]})
        anal_data[f'necs_countries_{target}'] = {}
        for idx, country in enumerate(countries):
            res = expt_data['necs_countries'][idx]['res']
            anal_data[f'necs_countries_{target}'][country] = res[f'max_{target}'] - res[f'min_{target}']
    return anal_data
    


'''
def generate_prdt_data(expt_data, time_sttg = 'one_time', target = 'c'):
    fig_data = {}
    sheet_name = 'prdt_vac'
    fig_data[sheet_name] = {}
    sttg = 'all_ages'
    curve_sttg_vac = time_sttg + '_' + 'curves_' + sttg + '_dd'
    curve_sttg_no_vac = time_sttg + '_' + 'curves_no_vac_dd'
    output_lines = ['time_line', 'curve_'+target, 'prdt_'+target, 'curve_s'] if target == 'c' \
                  else ['time_line', 'curve_'+target, 'prdt_'+target]
    for line_name in output_lines:
        fig_data[sheet_name][line_name] = expt_data['sttgs_curves']['Data_sttgs_curves'][curve_sttg_vac][line_name].to_numpy() 
        fig_data[sheet_name][line_name + '_no_vac'] = expt_data['sttgs_curves']['Data_sttgs_curves'][curve_sttg_no_vac][line_name].to_numpy()
    sheet_name = 'compr_curves'
    fig_data[sheet_name] = {}
    line_len = min([len(expt_data['sttgs_curves']['Data_sttgs_curves'][time_sttg + '_' + 'curves_' + sttg + '_gd']['time_line']) 
                    for sttg in list(basic_params.vac_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']])
    line_len = min([line_len, min([len(expt_data['sttgs_curves']['Data_sttgs_curves'][time_sttg + '_' + 'curves_' + sttg + '_gg']['time_line']) 
                                   for sttg in ['min_'+target, 'max_'+target]])])
    fig_data[sheet_name]['time_line'] =  expt_data['sttgs_curves']['Data_sttgs_curves'][time_sttg + '_curves_no_vac_gd']['time_line'].to_numpy()[:line_len]
    for sttg in list(basic_params.vac_groups.keys()) + ['min_'+target, 'max_'+target, 'no_vac']:
        curve_sttg = time_sttg + '_' + 'curves_' + sttg + '_gg'
        fig_data[sheet_name]['curve_'+sttg + '_gg'] = expt_data['sttgs_curves']['Data_sttgs_curves'][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    for sttg in ['min_'+target, 'max_'+target]:
        curve_sttg = time_sttg + '_' + 'curves_' + sttg + '_gd'
        fig_data[sheet_name]['curve_'+sttg + '_gd'] = expt_data['sttgs_curves']['Data_sttgs_curves'][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    sheet_name = 'optm_alloc'
    fig_data[sheet_name] = {'alloc': expt_data['sttgs_curves']['Data_sttgs_curves']['alloc_data']['allocs_min_' + target + '_gd'].to_numpy() * basic_params.calc_params['populations']}
    return fig_data

def generate_compr_data(expt_data, time_sttg = 'one_time', target = 'c'):
    fig_data = {}
    for idx, x_type in enumerate(['var', 'mean', 'length']):
        sheet_name = x_type + '_error'
        fig_data[sheet_name] = {}
        fig_data[sheet_name][x_type] = np.array([])
        no_vac = np.array([])
        steady_max, steady_min = {}, {}
        for opt_type in ['dd', 'gd', 'gg']:
            steady_max[opt_type] = np.array([])
            steady_min[opt_type] = np.array([])
        steady_all_age = np.array([])
        for rank in range(5):
            data_tmp = expt_data[x_type + '_dist_list'][str(rank)]['dist_list_prdt_data']
            alloc_tmp = expt_data[x_type + '_dist_list'][str(rank)]['dist_list_alloc_data']
            fig_data[sheet_name][x_type] = np.append(fig_data[sheet_name][x_type], data_tmp[x_type].to_numpy())
            no_vac = np.append(no_vac, data_tmp[time_sttg+'_prdt_no_vac_'+target])
            for alloc_type in ['min','max']:
                fig_data[sheet_name]['alloc_error_'+alloc_type] = []
                for x_idx in range(4):
                    alloc_g = alloc_tmp['alloc_g_'+alloc_type+'_'+target+'_' + str(x_idx)].to_numpy()
                    alloc_d = alloc_tmp['alloc_d_'+alloc_type+'_'+target+'_' + str(x_idx)].to_numpy()
                    fig_data[sheet_name]['alloc_error_'+alloc_type].append(((alloc_g - alloc_d)**2).sum() ** 0.5 / (alloc_g ** 2).sum() ** 0.5) 
            for opt_type in ['dd', 'gd', 'gg']:
                steady_max[opt_type] = np.append(steady_max[opt_type], data_tmp[time_sttg+'_prdt_'+opt_type+'_max_'+target].to_numpy())
                steady_min[opt_type] = np.append(steady_min[opt_type], data_tmp[time_sttg+'_prdt_'+opt_type+'_min_'+target].to_numpy())
            steady_all_age = np.append(steady_all_age, data_tmp[time_sttg + '_prdt_g_all_ages_' + target].to_numpy())
        fig_data[sheet_name]['error_min_'+x_type] = (steady_min['gd'] - steady_min['gg']) 
        fig_data[sheet_name]['error_max_'+x_type] = (steady_max['gg'] - steady_max['gd'])
        fig_data[sheet_name]['error_compr_min_'+x_type] = (no_vac - steady_min['gg']) 
        fig_data[sheet_name]['error_compr_max_'+x_type] = (no_vac - steady_max['gg'])
    return fig_data

def generate_necs_data(expt_data, time_sttg = 'one_time', target = 'c', metric = 0):
    param_keys = [['Weibull', 2.5, 2.5], ['Weibull', 2, 3], ['Weibull', 1.5, 3.5]]
    fig_data = {}
    sheet_name = 'r0'
    fig_data[sheet_name] = {}
    param_type = 'Data_r0'
    fig_data[sheet_name]['r0'] = expt_data[sheet_name][param_type][sheet_name+'_prdt_data']['r0'].to_numpy()
    for i in range(26):
        current_time_sttg = time_sttg if sheet_name != 'vac_dur' else 'time_course'
        vac_min, vac_max = expt_data[sheet_name][param_type][sheet_name+'_prdt_data'][current_time_sttg + '_prdt_gd_min_' + target + '_' + str(i)].to_numpy(),\
                           expt_data[sheet_name][param_type][sheet_name+'_prdt_data'][current_time_sttg + '_prdt_gd_max_' + target + '_' + str(i)].to_numpy()
        fig_data[sheet_name][param_type + '_' + str(i)] = vac_max - vac_min
    for i in range(3):
        sheet_name = 'dist_list_' + str(i)
        fig_data[sheet_name] = {}
        for func_type, mean_inf, mean_rem in param_keys:
            data_mark = str(func_type) + "_" + str(mean_inf) + "_" + str(mean_rem)
            fig_data[sheet_name][data_mark + '_ratio'] = []
            data_tmp = expt_data['dist_list'][func_type+'_i'+str(mean_inf)+'r'+str(mean_rem) + '_' + str(i)]['dist_list_prdt_data']
            vac_min, vac_max = data_tmp[time_sttg+'_prdt_gd_min_'+target].to_numpy(),\
                               data_tmp[time_sttg+'_prdt_gd_max_'+target].to_numpy()
            fig_data[sheet_name][data_mark + '_res'] = vac_max - vac_min
            fig_data[sheet_name][data_mark + '_ratio'] = data_tmp['ratio']
    for idx in range(3):
        sheet_name = 'optm_proc_' + str(idx)
        fig_data[sheet_name] = {}
        fig_data[sheet_name]['coe_to_max'] = expt_data['optm_proc']['optm_proc']['res_' + str(idx) + '_' + target]['coe_to_max']
        res = expt_data['optm_proc']['optm_proc']['res_' + str(idx) + '_' + target]['res_to_max']
        fig_data[sheet_name]['res_to_max'] = res - res[0]
    return fig_data

def generate_imp_data(expt_data, time_sttg = 'one_time', target = 'c', metric = 0):
    fig_data = {}
    for sheet_name in ['vac_avail', 'c_perct', 'vac_dur']:
        fig_data[sheet_name] = {}
        param_type = 'Data_' + sheet_name
        fig_data[sheet_name][sheet_name] = expt_data[sheet_name][param_type][sheet_name+'_prdt_data'][sheet_name].to_numpy()
        for i in range(26):
            current_time_sttg = time_sttg if sheet_name != 'vac_dur' else 'time_course'
            vac_min, vac_max = expt_data[sheet_name][param_type][sheet_name+'_prdt_data'][current_time_sttg + '_prdt_gd_min_' + target + '_' + str(i)].to_numpy(),\
                               expt_data[sheet_name][param_type][sheet_name+'_prdt_data'][current_time_sttg + '_prdt_gd_max_' + target + '_' + str(i)].to_numpy()
            fig_data[sheet_name][param_type + '_' + str(i)] = vac_max - vac_min
    return fig_data
    


'''

'''
day_div = 100
eta = 0.95
step = 1.0 / day_div
i0 = 1e-6
time0 = 0
group_amount = 8
group_div = np.array([2,] * group_amount)
group_amount = len(group_div)
srv_length = 16000
targets = ['c', 'd', 'y']
all_targets = ['s', 'i', 'r', 'c', 'd', 'y']
params = {'contacts': di.import_contacts('United States of America'), 
          'populations': di.import_populations('United States of America')[0], 
          'ifrs': di.import_ifrs(), 
          'ylls': di.import_ylls('United States of America')}
params_adj = di.rescale_params(params, group_div)
contacts_dir = params_adj['contacts']['home'] + params_adj['contacts']['school'] \
             + params_adj['contacts']['work'] + params_adj['contacts']['other_locations']
contacts = contacts_dir + contacts_dir.T
calc_params = {'i0': np.ones(len(group_div)) * i0, 
               'populations': params_adj['populations'], 'contacts': contacts, 
               'ifrs': params_adj['ifrs'], 'ylls': params_adj['ylls'], 
               'k': 1, 'srv_inf': None, 'srv_rem': None,
               'delay': 0, 'eta': eta, 'step': step, 'time': time0}
init_targets = {'c': calc_params['i0'] @ calc_params['populations'], 'd': 0, 'y': 0}
'''

'''
def generate_no_vac_prdt_data(expt_data, time_sttg = 'one_time', target = 'c',
                              inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    sttg = 'no_vac'
    curve_sttg = time_sttg + '_' + 'curves_' + sttg
    for line_name in ['time_line', 'curve_'+target, 'prdt_'+target, 'prdt_non_'+target]:
        anal_data[line_name] = expt_data['sttgs_curves'][param_type][curve_sttg][line_name].to_numpy() 
    return anal_data

def generate_rand_vac_prdt_data(expt_data, time_sttg = 'one_time', target = 'c',
                                inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    sttg = 'all_ages'
    curve_sttg = time_sttg + '_' + 'curves_' + sttg
    output_lines = ['time_line', 'curve_'+target, 'prdt_'+target, 'curve_s', 'curve_s_eff'] if target == 'c' \
                  else ['time_line', 'curve_'+target, 'prdt_'+target]
    for line_name in output_lines:
        anal_data[line_name] = expt_data['sttgs_curves'][param_type][curve_sttg][line_name].to_numpy() 
    return anal_data

def generate_sttg_compr_data(expt_data, time_sttg = 'one_time', target = 'c',
                             inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    line_len = min([len(expt_data['sttgs_curves'][param_type][time_sttg + '_' + 'curves_' + sttg]['time_line']) for sttg in vac_group_keys + ['min_'+target, 'no_vac']])
    anal_data['time_line'] =  expt_data['sttgs_curves'][param_type][time_sttg + '_curves_no_vac']['time_line'].to_numpy()[:line_len]
    for sttg in vac_group_keys + ['min_'+target, 'no_vac']:
        curve_sttg = time_sttg + '_' + 'curves_' + sttg
        anal_data['curve_'+sttg] = expt_data['sttgs_curves'][param_type][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    return anal_data

def generate_sttg_compr_alloc_data(expt_data, time_sttg = 'one_time', target = 'c',
                                   inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    anal_data['group_idx'] = np.arange(8)
    anal_data['vac_alloc'] = expt_data['sttgs_curves'][param_type]['alloc_data']['allocs_min_' + target].to_numpy() * calc_params['populations']
    return anal_data

def generate_vc_data(expt_data, expt_type, time_sttg = 'one_time', target = 'c',
                     inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    anal_data[expt_type] =  expt_data[expt_type][param_type][expt_type + '_prdt_data'][expt_type].to_numpy()
    for sttg in vac_group_keys + ['min', 'max', 'no_vac']:
        anal_data[sttg] = expt_data[expt_type][param_type][expt_type +'_prdt_data'][time_sttg + '_prdt_' + sttg + '_' + target].to_numpy()
    return anal_data

def generate_vc_alloc_data(expt_data, expt_type, time_sttg = 'one_time', target = 'c',
                           inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
    #anal_data[expt_type] =  expt_data[expt_type][param_type][expt_type + '_prdt_data'][expt_type].to_numpy()
    for idx in np.arange(41):
        anal_data['alloc_min_' + target + '_' + str(idx)] = expt_data[expt_type][param_type][expt_type + '_alloc_data']['alloc_min_' + target + '_' + str(idx)].to_numpy() * calc_params['populations']
    return anal_data

      
def calc_metric(steady_state, vac_max, vac_min, init_state, metric = 0):
    if metric == 0:
        return (steady_state - vac_min) / (steady_state - init_state)
    elif metric == 1:
        return (vac_max - vac_min) / (steady_state - init_state)
    else:
        return (vac_max - vac_min) / (steady_state - vac_min)
    
def generate_vc_nect_data(expt_data, expt_type, metric_type, time_sttg = 'one_time', target = 'c',
                          inf_pow = 4, rem_pow = 8):
    anal_data = {}
    param_type = 'Data_' + str(inf_pow) + "_" + str(rem_pow)
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

def generate_disc_data(expt_data, time_sttg = 'one_time', target = 'c', metric = 0):
    fig_data = {}
    sheet_name = 'compr'
    fig_data[sheet_name] = {}
    
    func_type, mean_inf, mean_rem = 'Weibull', 2, 3
    for opt_type in ['dd', 'gg', 'gd']:
        fig_data[sheet_name]['ratio_' + opt_type] = []
        fig_data[sheet_name]['res_' + opt_type] = []
        for inf_pow in np.arange(-4, 21, 12):
            for rem_pow in np.arange(-4, 21, 12):
                param_type = func_type + "_" + "i" + str(mean_inf) + "r" + str(mean_rem) + '_' + str(inf_pow) + '_' + str(rem_pow)
                fig_data[sheet_name]['ratio_' + opt_type] += list(expt_data['general_dist_list'][param_type]['dist_list_prdt_data']['ratio'].to_numpy())
                vac_max = expt_data['general_dist_list'][param_type]['dist_list_prdt_data'][time_sttg + '_prdt_'+opt_type+'_max_' + target].to_numpy()
                vac_min = expt_data['general_dist_list'][param_type]['dist_list_prdt_data'][time_sttg + '_prdt_'+opt_type+'_min_' + target].to_numpy()
                steady_state = expt_data['general_dist_list'][param_type]['dist_list_prdt_data'][time_sttg + '_prdt_no_vac_' + target].to_numpy()
                init_state = 0.01
                fig_data[sheet_name]['res_' + opt_type] += list(calc_metric(steady_state, init_state, vac_min, vac_max, metric))
    
    sheet_name = 'alloc_error'
    fig_data[sheet_name] = {}
    fig_data[sheet_name]['ratio'] = []
    fig_data[sheet_name]['res'] = []
    for inf_pow in np.arange(-4, 21, 12):
        for rem_pow in np.arange(-4, 21, 12):
            param_type = func_type + "_" + "i" + str(mean_inf) + "r" + str(mean_rem) + '_' + str(inf_pow) + '_' + str(rem_pow)
            fig_data[sheet_name]['ratio'] += list(expt_data['general_dist_list'][param_type]['dist_list_prdt_data']['ratio'].to_numpy())
            for delay_day in np.arange(1, 10, 2):
                x0 = expt_data['general_dist_list'][param_type]['dist_list_alloc_data']['alloc_g_min_c_' + str(inf_pow) + '_' + str(rem_pow) + '_' + str(delay_day)].to_numpy()
                x1 = expt_data['general_dist_list'][param_type]['dist_list_alloc_data']['alloc_d_min_c_' + str(inf_pow) + '_' + str(rem_pow) + '_' + str(delay_day)].to_numpy()
                fig_data[sheet_name]['res'].append(((x0 - x1)**2).sum() ** 0.5 / (x0 ** 2).sum() ** 0.5)  
    return fig_data

def generate_fig4_data(param_range_data, param_expr_data, param_section = 'data_4_12_4', 
                       time_sttg = 'time_course', target = 'c'):
    fig_data = {}
    
    fig_idx = 'subfig_a'
    sheet_name = fig_idx + '_curves'
    fig_data[sheet_name] = {}
    sttg = 'all_ages'
    curve_sttg = time_sttg + '_' + 'curves_' + sttg
    output_lines = ['time_line', 'curve_'+target, 'prdt_'+target, 'curve_s', 'curve_s_eff'] if target == 'c' \
                   else ['time_line', 'curve_'+target, 'prdt_'+target]
    for line_name in output_lines:
        fig_data[sheet_name][line_name] = param_expr_data[param_section][curve_sttg][line_name].to_numpy() 
        
    fig_idx = 'subfig_b'
    sheet_name = fig_idx + '_curves'
    fig_data[sheet_name] = {}
    line_len = min([len(param_expr_data[param_section][time_sttg + '_' + 'curves_' + sttg]['time_line']) for sttg in vac_group_keys + ['min_'+target, 'no_vac']])
    fig_data[sheet_name]['time_line'] =  param_expr_data[param_section][time_sttg + '_curves_no_vac']['time_line'].to_numpy()[:line_len]
    for sttg in vac_group_keys + ['min_'+target, 'no_vac']:
        curve_sttg = time_sttg + '_' + 'curves_' + sttg
        fig_data[sheet_name]['curve_'+sttg] = param_expr_data[param_section][curve_sttg]['curve_'+target].to_numpy()[:line_len]
    sheet_name = fig_idx + '_alloc'
    fig_data[sheet_name] = {'alloc': param_expr_data[param_section]['allocs_min_' + target]['alloc'].to_numpy() * calc_params['populations']}
    
        
    mean_cum_funcs = {'Weibull': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                      func.get_mean_from_cum(_alpha_inf, _beta_inf, _alpha_rem, _beta_rem),
                      'Gamma': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                      func.get_mean_from_srv(func.get_gen_srv(func.srv_gamma(_alpha_inf, _beta_rem, 16000, 0.01), 
                                       func.srv_gamma(_alpha_rem, _beta_rem, 16000, 0.01), 0.01), 0.01), 
                      'Lognormal': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                      func.get_mean_from_srv(func.get_gen_srv(func.srv_lognormal(_alpha_inf, _beta_rem, 16000, 0.01), 
                                       func.srv_lognormal(_alpha_rem, _beta_rem, 16000, 0.01), 0.01), 0.01)}
    beta_funcs = {'Weibull': func.get_beta_from_weibull, 
                  'Gamma': func.get_beta_from_gamma, 
                  'Lognormal': func.get_beta_from_lognormal}
    param_funcs = {'Weibull': lambda _val_pow: np.e ** (_val_pow * 0.05),
                   'Gamma': lambda _val_pow: np.e ** (_val_pow * 0.1), 
                   'Lognormal': lambda _val_pow: _val_pow * 0.04}
    param_ranges = {'Weibull': np.arange(-8, 25, 4), 
                    'Gamma': np.arange(-8, 25, 4), 
                    'Lognormal': np.arange(4, 37, 4), }
    param_keys = [['Weibull', 2, 3], ['Weibull', 2, 2], ['Weibull', 3, 3],
                  ['Weibull', 3, 2], ['Weibull', 2.5, 2.5], ['Gamma', 2, 3], ['Lognormal', 2, 3]]
    fig_idx = 'subfig_c'
    sheet_name = fig_idx + '_plots'
    fig_data[sheet_name] = {}
    init_target = 0.01 if target == 'c' else 0
    for func_type, mean_inf, mean_rem in param_keys:
        data_mark = str(func_type) + "_" + str(mean_inf) + "_" + str(mean_rem)
        fig_data[sheet_name][data_mark + '_ratio'] = []
        data_tmp = param_range_data[func_type+'_Data_'+'i'+str(mean_inf)+'r'+str(mean_rem)]\
        [func_type+'_Data_'+'i'+str(mean_inf)+'r'+str(mean_rem)]
        fig_data[sheet_name][data_mark + '_res'] = (data_tmp[time_sttg+'_prdt_max_'+target].to_numpy() - data_tmp[time_sttg+'_prdt_min_'+target].to_numpy())\
                                           /(data_tmp[time_sttg+'_prdt_no_vac_'+target].to_numpy() - init_target)
        for delay_day in range(9):
            for inf_pow in param_ranges[func_type]:
                for rem_pow in param_ranges[func_type]:
                    alpha_inf, alpha_rem = param_funcs[func_type](inf_pow), \
                                           param_funcs[func_type](rem_pow)
                    beta_inf, beta_rem = beta_funcs[func_type](alpha_inf, mean_inf), \
                                         beta_funcs[func_type](alpha_rem, mean_rem)
                    fig_data[sheet_name][data_mark + '_ratio'].append(delay_day / mean_cum_funcs[func_type](alpha_inf, beta_inf,
                                                                                                     alpha_rem, beta_rem))
    return fig_data

'''     

        
        