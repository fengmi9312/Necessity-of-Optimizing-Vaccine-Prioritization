# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:19:50 2024

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta, sir_general
import func
import basic_params
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
                        alloc_map[f'{sttg}_dd'] = model_map['dd'].optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = True, tol=1e-23)['alloc']
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

'''
def generate_prdt(calc_params, delay_day, 
                  r0 = 2, vac_eff = 0.95, vac_avail = 0.3, c_perct = 0.1, vac_dur = 7):
    k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max())
    c_steady = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], 
                                     func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), 
                                     _i = calc_params['i0']) @ calc_params['populations']
    _calc_params_delta = deepcopy(calc_params)
    _calc_params_general = deepcopy(calc_params)
    _calc_params_delta['k'] = k_val
    _calc_params_general['k'] = k_val
    _calc_params_delta['eta'] = vac_eff
    _calc_params_general['eta'] = vac_eff
    _calc_params_delta['delay'] = delay_day * basic_params.day_div
    _calc_params_general['srv_imm'] = func.generate_imm_dist(delay_day, basic_params.day_div)
    model_delta = sir_delta(**_calc_params_delta)
    model_general = sir_general(**_calc_params_general)
    c_init = model_delta.getc_c_tot()
    while True:
        if model_delta.getc_c_tot() != model_general.getc_c_tot(): print('model error')
        if model_delta.getc_c_tot() >= c_perct * (c_steady - c_init) + c_init: break
        model_delta.spread_once()
        model_general.spread_once()
    res = {}
    dist_props = {'c': calc_params['populations'], 
                  'd': calc_params['populations'] * calc_params['ifrs'], 
                  'y': calc_params['populations'] * calc_params['ifrs'] * calc_params['ylls']}
    dur_kwargs = {'vac_dur': vac_dur, 'vac_gap': basic_params.day_div}
    for target in basic_params.targets:
        for optm_d in ['min', 'max']:
            optm_res = model_delta.optimize_vac_alloc(vac_avail = vac_avail, target = target, optm_dir = (optm_d == 'min'), disp = False)
            # allocations
            name_tail = optm_d + '_' + target
            res['alloc_' + name_tail] = optm_res['alloc']
            # results with dur == 1
            name_tail = optm_d + '_' + target
            res['dist_dd_' + name_tail] = model_delta.calc_vac_prdt(optm_res['alloc']) * dist_props[target]
            res['prdt_dd_' + name_tail] = optm_res['target']
            res['dist_gd_' + name_tail] = model_general.calc_vac_prdt(optm_res['alloc']) * dist_props[target]
            res['prdt_gd_' + name_tail] = model_general.calc_vac_prdt_target(optm_res['alloc'], target = target)
            # results with dur == 7
            name_tail = optm_d + '_' + 'dur' + str(vac_dur) + '_' + target
            res['dist_dd_' + optm_d + '_' + target] = model_delta.calc_time_course_vac_prdt(optm_res['alloc'], **dur_kwargs)[-1] * dist_props[target]
            res['prdt_dd_' + optm_d + '_' + target] = model_delta.calc_time_course_vac_prdt_target(optm_res['alloc'], target = target, **dur_kwargs)[-1]
            res['dist_gd_' + optm_d + '_' + target] = model_general.calc_time_course_vac_prdt(optm_res['alloc'], **dur_kwargs) * dist_props[target]
            res['prdt_gd_' + optm_d + '_' + target] = model_general.calc_time_course_vac_prdt_target(optm_res['alloc'], target = target, **dur_kwargs)
    for target in basic_params.targets:
        res['prdt_no_vac_' + target] = model_general.calc_prdt_target(target = target)
        res['dist_no_vac_' + target] = model_general.calc_prdt() * dist_props[target]
    for empirical_group_key in list(basic_params.empirical_groups.keys()):
        vac_alloc = func.get_alloc(np.array(model_delta.getc_s()), model_delta.get_populations(), vac_avail, 
                                   basic_params.empirical_groups[empirical_group_key])
        res['alloc_' + empirical_group_key] = vac_alloc
        for target in basic_params.targets:
            # results with dur == 1
            name_tail = empirical_group_key + '_' + target
            res['dist_d_' + name_tail] = model_delta.calc_vac_prdt(vac_alloc) * dist_props[target]
            res['prdt_d_' + name_tail] = model_delta.calc_vac_prdt_target(vac_alloc,target = target)
            res['dist_g_' + name_tail] = model_general.calc_vac_prdt(vac_alloc) * dist_props[target]
            res['prdt_g_' + name_tail] = model_general.calc_vac_prdt_target(vac_alloc,target = target)
            # results with dur == vac_dur
            name_tail = empirical_group_key + '_' + 'dur' + str(vac_dur) + '_' + target
            res['dist_d_' + name_tail] = model_delta.calc_time_course_vac_prdt_target(vac_alloc, **dur_kwargs)[-1] * dist_props[target]
            res['prdt_d_' + name_tail] = model_delta.calc_time_course_vac_prdt_target(vac_alloc, target = target, **dur_kwargs)[-1]
            res['dist_g_' + name_tail] = model_general.calc_time_course_vac_prdt_target(vac_alloc, **dur_kwargs) * dist_props[target]
            res['prdt_g_' + name_tail] = model_general.calc_time_course_vac_prdt_target(vac_alloc, target = target, **dur_kwargs)
    return res
'''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    