# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 19:45:39 2025

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(code_root)

import numpy as np
import pandas as pd
from Dependencies.CodeDependencies.model import sir_delta, sir_general
from Dependencies.CodeDependencies import func, basic_params
from Dependencies.FrameDependencies.data_loader import load_all_data
from copy import deepcopy


def simulate(calc_params, imm_params = ('delay', 700), k_val = None, r0 = 2, vac_eff = 0.95, vac_avail = 0.3, c_perct = 0.1, vac_dur = 7, get_dur = True, get_curve = False, gg = False, empirical_group_keys = basic_params.empirical_groups.keys(), optm_targets = ['c', 'd', 'y'], prdt_targets = ['c', 'd', 'y']):
    if get_curve: curve_data = {}
    if k_val is None:
        k_val = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        #steady_c = func.get_mixed_steady_state(r0, calc_params['i0'] @ calc_params['populations'])
        #k_val = func.get_k_from_steady(steady_c, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params_delta = deepcopy(calc_params)
    calc_params_general = deepcopy(calc_params)
    calc_params_delta['k'] = k_val
    calc_params_general['k'] = k_val
    calc_params_delta['eta'] = vac_eff
    calc_params_general['eta'] = vac_eff
    calc_params_general['srv_imm'] = func.generate_imm_dist(imm_params[0], imm_params[1], basic_params.day_div)
    if imm_params[0] == 'delay' or imm_params[0] == 'half_domain': calc_params_delta['delay'] = imm_params[1]
    elif imm_params[0] == 'var': calc_params_delta['delay'] = 7 * basic_params.day_div
    else: return None
    steady_c = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    alloc_map = {}
    dist_map = {}
    dur_kwargs = {'vac_dur': vac_dur, 'vac_gap': basic_params.day_div}
    dur_list = [False, True] if get_dur else [False]
    for sttg in list(empirical_group_keys) + [f'{optm_direction}_{optm_target}' for optm_target in optm_targets for optm_direction in ['min', 'max']] + ['no_vac']:
        print(f'Implement Strategy: {sttg}')
        for dur in dur_list:
            model_map = {'dd': sir_delta(**calc_params_delta), 
                         'gd': sir_general(**calc_params_general)}
            if gg: model_map['gg'] = sir_general(**calc_params_general)
            if get_curve: 
                dd_key = f'curve_{sttg}_dd_dur' if dur else f'curve_{sttg}_dd'
                for model_type in model_map.keys(): curve_data[f'curve_{sttg}_{model_type}_dur' if dur else f'curve_{sttg}_{model_type}'] = {}
            if model_map['dd'].getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
                if get_curve:
                    for target in prdt_targets:
                        curve_data[dd_key][f'prdt_{target}'] = [model_map['dd'].calc_prdt_target(target = target, mark = (sttg != 'no_vac')),]
                while True:
                    #if model_map['dd'].get_current_time_int() > 100 and (model_map['dd'].get_c_tot()[-1] - model_map['dd'].get_c_tot()[-100]) / model_map['dd'].get_c_tot()[-1] < 1e-5: return None
                    for key, simu in model_map.items(): simu.spread_once()
                    if model_map['dd'].getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
                    if get_curve:    
                        for target in prdt_targets: 
                            curve_data[dd_key]['prdt_' + target].append(model_map['dd'].calc_prdt_target(target = target, mark = (sttg != 'no_vac')))
            if sttg != 'no_vac':
                if not dur:
                    if sttg in empirical_group_keys:
                        vac_alloc = func.get_alloc(np.array(model_map['gd'].getc_s()), model_map['gd'].get_populations(), vac_avail, basic_params.empirical_groups[sttg])
                        alloc_map[f'{sttg}_dd'] = vac_alloc
                        alloc_map[f'{sttg}_gd'] = vac_alloc
                        dist_map[f'{sttg}_dd'] = model_map['dd'].calc_vac_prdt(alloc_map[f'{sttg}_dd'])
                        dist_map[f'{sttg}_gd'] = model_map['gd'].calc_vac_prdt(alloc_map[f'{sttg}_gd'])
                        if gg: 
                            alloc_map[f'{sttg}_gg'] = vac_alloc
                            dist_map[f'{sttg}_gg'] = model_map['gg'].calc_vac_prdt(alloc_map[f'{sttg}_gg'])
                    else:
                        alloc_map[f'{sttg}_dd'] = model_map['dd'].optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = True, ctol = 1e-16, tol=1e-23, init_strategy = np.eye(16)[-1] if sttg[-1] == 'd' and sttg[:3] == 'min' else None)['alloc']
                        alloc_map[f'{sttg}_gd'] = alloc_map[f'{sttg}_dd']
                        dist_map[f'{sttg}_dd'] = model_map['dd'].calc_vac_prdt(alloc_map[f'{sttg}_dd'])
                        dist_map[f'{sttg}_gd'] = model_map['gd'].calc_vac_prdt(alloc_map[f'{sttg}_gd'])
                        if gg: 
                            alloc_map[f'{sttg}_gg'] = model_map['gg'].optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = False)['alloc']
                            dist_map[f'{sttg}_gg'] = model_map['gg'].calc_vac_prdt(alloc_map[f'{sttg}_gg'])
                else:
                    dist_map[f'{sttg}_dd_dur'] = model_map['dd'].calc_time_course_vac_prdt(alloc_map[f'{sttg}_dd'], **dur_kwargs)[-1]
                    dist_map[f'{sttg}_gd_dur'] = model_map['gd'].calc_time_course_vac_prdt(alloc_map[f'{sttg}_gd'], **dur_kwargs)
                    if gg: dist_map[f'{sttg}_gg_dur'] = model_map['gg'].calc_time_course_vac_prdt(alloc_map[f'{sttg}_gg'], **dur_kwargs)
                if get_curve:
                    for target in prdt_targets:
                        if not dur:curve_data[f'curve_{sttg}_dd'][f'prdt_{target}'].append(model_map['dd'].calc_vac_prdt_target(alloc_map[f'{sttg}_dd'], target = target))
                        else: curve_data[f'curve_{sttg}_dd_dur'][f'prdt_{target}'] += model_map['dd'].calc_time_course_vac_prdt_target(alloc_map[f'{sttg}_dd'], target = target, **dur_kwargs).tolist()
            else:
                dist_map['no_vac_dd'] = model_map['dd'].calc_prdt()
                dist_map['no_vac_gd'] = model_map['gd'].calc_prdt()
                if gg: dist_map['no_vac_gd'] = model_map['gg'].calc_prdt()
                if get_curve:
                    for target in prdt_targets:
                        curve_data[dd_key][f'prdt_{target}'].append(model_map['dd'].calc_prdt_target(target = target, mark = (sttg != 'no_vac')))
    
    if get_curve:
        for sttg in list(empirical_group_keys) + [f'{optm_direction}_{optm_target}' for optm_target in optm_targets for optm_direction in ['min', 'max']] + ['no_vac']:
            for dur in dur_list:
                dd_key = f'curve_{sttg}_dd_dur' if dur else f'curve_{sttg}_dd'
                print(dd_key)
                curve_model_map = deepcopy(model_map)
                if sttg != 'no_vac': 
                    for key, simu in curve_model_map.items():
                        if not dur: simu.add_vaccination(alloc_map[f'{sttg}_{key}'])  
                        else: simu.add_time_course_vaccination(alloc_map[f'{sttg}_{key}'], **dur_kwargs)
                vmark = curve_model_map['dd'].get_current_time_int()
                while True:
                    for key, simu in curve_model_map.items(): simu.spread_once()
                    for target in prdt_targets:
                        curve_data[dd_key]['prdt_' + target].append(curve_model_map['dd'].calc_prdt_target(target = target, mark = (sttg != 'no_vac')))
                    c_time_int = curve_model_map['dd'].get_current_time_int()
                    if c_time_int > 100 \
                    and curve_model_map['dd'].get_c_tot()[-1] - curve_model_map['dd'].get_c_tot()[-100] < 1e-5 \
                    and curve_model_map['gd'].get_c_tot()[-1] - curve_model_map['gd'].get_c_tot()[-100] < 1e-5 \
                    and ((not gg) or curve_model_map['gg'].get_c_tot()[-1] - curve_model_map['gg'].get_c_tot()[-100] < 1e-5) \
                    and (sttg == 'no_vac' or c_time_int >= vmark + 2 * calc_params_delta['delay'] + 1): break
                for model_type in curve_model_map.keys(): curve_data[f'curve_{sttg}_{model_type}_dur' if dur else f'curve_{sttg}_{model_type}']['time_line'] = curve_model_map[model_type].get_time_line()
                for target in basic_params.all_targets:
                    for model_type in curve_model_map.keys(): curve_data[f'curve_{sttg}_{model_type}_dur' if dur else f'curve_{sttg}_{model_type}'][f'curve_{target}'] = curve_model_map[model_type].get_x_tot(target) 
        curve_data.update({'alloc': alloc_map, 'dist': dist_map})
        return curve_data
    else: 
        res_data = {'alloc': alloc_map, 'dist': dist_map}
        return res_data




def execute(expr_param, file_idx):
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    params_list = [(4, 0)]
    country = 'United States'
    countries = [country]
    country_data = load_all_data(countries, basic_params.group_div)
    res_list = []
    for r0_idx, delay_idx in params_list:
        r0 = np.exp(r0_idx * 0.075)
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}_0'
        print(f'Begin excuting {param_name}')
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        param_val = delay_idx * 50
        single_res = simulate(calc_params, imm_params=('delay', param_val), r0 = r0, optm_targets=['c', 'd'])
        growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
        mean_gen = mean_func(alpha_val, beta_val)
        single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen, param_val], index=['r0', 'growth_rate', 't_gen', expr_param])}})
        res_list.append(single_res)
        print(f'Complete {param_name}')
    print('Gather Data')
    res = {}
    for res_idx, (r0_idx, delay_idx) in enumerate(params_list):
        single_res = res_list[res_idx]
        param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{r0_idx}_{delay_idx}'
        for data_key in single_res.keys():
            if data_key not in res: res[data_key] = {}
            for key, item in single_res[data_key].items():
                res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
        print('Return Data')
    return res



res = execute('param', 0)

























