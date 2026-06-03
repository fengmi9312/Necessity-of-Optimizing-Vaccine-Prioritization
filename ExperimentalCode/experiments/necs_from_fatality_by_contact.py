# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 18:22:36 2026

@author: fengm
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(code_root)
import numpy as np
from Dependencies.CodeDependencies import func
from Dependencies.CodeDependencies import basic_params
import pandas as pd
from copy import deepcopy
from Dependencies.CodeDependencies.param_data_loader import load_all_data
from scipy.optimize import minimize, LinearConstraint, Bounds
from Dependencies.CodeDependencies.model import sir_delta

def optimize_vac_alloc(calc, vac_avail, target = 'c', init_strategy = None, weights = None,
                       optm_dir = True, ctol = 1e-10, tol = 1e-20, disp = False, double_optm = False, **kwargs):
    if vac_avail <= 0 or calc._sir_delta__s_tot[calc._sir_delta__current_time_int] == 0:
        return {'target': calc.calc_vac_prdt_target(np.zeros(calc._sir_delta__group_amount), target = target), 
                'alloc': np.zeros(calc._sir_delta__group_amount)}
    elif vac_avail >= calc._sir_delta__s_tot[calc._sir_delta__current_time_int]:
        return {'target': calc.calc_vac_prdt_target(calc._sir_delta__s[calc._sir_delta__current_time_int], target = target), 
                'alloc': calc._sir_delta__s[calc._sir_delta__current_time_int]}
    else: pass
    np.random.seed(0)
    if weights is None:
        get_res = lambda vac_alloc: calc.calc_vac_prdt_target(vac_alloc, target, ctol = ctol) if optm_dir else -calc.calc_vac_prdt_target(vac_alloc, target, ctol = ctol)
    else:
        get_res = lambda vac_alloc: calc.calc_vac_prdt(vac_alloc, ctol = ctol) @ weights if optm_dir else -calc.calc_vac_prdt(vac_alloc, ctol = ctol) @ weights
    linear_constraint = LinearConstraint(deepcopy(calc._sir_delta__populations), np.array([vac_avail]), np.array([vac_avail]))
    constraint = [linear_constraint,]
    bound = Bounds(np.zeros(calc._sir_delta__group_amount), deepcopy(calc._sir_delta__s[calc._sir_delta__current_time_int]))
    
    init_strategies = [init_strategy] if init_strategy is not None else []
    if optm_dir: dgr_arr = calc._sir_delta__contacts.sum(axis = 1)
    else: dgr_arr = 1 / calc._sir_delta__contacts.sum(axis = 1)
    dgr = vac_avail * dgr_arr / dgr_arr.sum()
    init_strategies.append(np.minimum(calc._sir_delta__s[calc._sir_delta__current_time_int],  dgr / calc._sir_delta__populations))
    if weights is None:
        if target == 'c':
            dgr_arr = np.ones(calc._sir_delta__group_amount)
        elif target == 'd':
            if optm_dir: dgr_arr = calc._sir_delta__ifrs 
            else: dgr_arr = 1 / calc._sir_delta__ifrs
        elif target == 'y':
            if optm_dir: dgr_arr = calc._sir_delta__ifrs * calc._sir_delta__ylls 
            else: dgr_arr = 1 / (calc._sir_delta__ifrs * calc._sir_delta__ylls)
    else:
        if optm_dir: dgr_arr = weights
        else: dgr_arr = 1 / weights
    dgr = vac_avail * dgr_arr / dgr_arr.sum()
    init_strategies.append(np.minimum(calc._sir_delta__s[calc._sir_delta__current_time_int],  dgr / calc._sir_delta__populations))
    res_list = []
    for basic_init_alloc in init_strategies:
        init_alloc = basic_init_alloc
        while True:
            res = minimize(get_res, init_alloc, method='SLSQP', jac = None, tol = tol,
                           constraints = constraint, bounds = bound, 
                           options={'disp': False, 'maxiter':2000}, **kwargs)
            if res.success:
                if disp: print('Successful Optimization!')
                break
            else:
                if disp: print('Unsuccessful Optimization, optimize again...')
                init_alloc = np.random.rand() * basic_init_alloc
        res_list.append({'target': res.fun if optm_dir else -res.fun, 'alloc': res.x})
    if double_optm: return res_list
    else:
        min_index = min(range(len(res_list)), key=lambda i: res_list[i]['target'])
        return res_list[min_index]

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




def execute(expr_param, file_idx):
    if expr_param not in ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']: return None
    c_perct = 0.1
    vac_avail = 0.3
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    mean_func = func.get_mean_from_weibull
    countries = ['United States']
    country_data = load_all_data(countries, basic_params.group_div)
    r0 = np.exp(np.arange(40) * 0.075)[file_idx]
    param_list = np.arange(40) / 39
    sttgs = ['min_x', 'max_x', 'no_vac']
    res = {}
    for country_idx, country in enumerate(countries):
        calc_params = deepcopy(basic_params.calc_params)
        calc_params['delay'] = 700 if expr_param.split('_')[-1] == '1' else 0
        calc_params['eta'] = 0.95
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
        srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
        calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
        prdt_weights = assign_by_rank(calc_params['ifrs'], calc_params['contacts'].sum(axis = 1))
        calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
        if expr_param.split('_')[1] == 'alpha':
            steady_c_arr = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
            steady_d = steady_c_arr @ prdt_weights
        
        growth_rate = func.find_g_from_gen(srv_gen, r0, calc_params['step'])
        mean_gen = mean_func(alpha_val, beta_val)
        simu_once = sir_delta(**calc_params)
        init_c = calc_params['i0'] @ calc_params['populations']
        steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
        if simu_once.getc_c_tot() < c_perct * (steady_c - init_c) + init_c:
            while True:
                simu_once.spread_once()
                if simu_once.getc_c_tot() >= c_perct * (steady_c - init_c) + init_c: break
        equal_weights = np.ones(basic_params.group_amount) * prdt_weights.sum() / basic_params.group_amount
        diff_weights = prdt_weights - equal_weights
        for param_idx, param_val in enumerate(param_list):
            weights_tmp = equal_weights + param_val * diff_weights
            if expr_param.split('_')[1] == 'alpha': calc_weights = weights_tmp * steady_d / (steady_c_arr @ weights_tmp)
            else: calc_weights = weights_tmp
            param_name = f'{expr_param}_{basic_params.country_abbr[country]}_{param_idx}'
            print(f'Begin excuting {param_name}')
            alloc_map, dist_map, weight_map = {}, {}, {}
            for sttg in sttgs:
                if sttg != 'no_vac':
                    alloc_map[f'{sttg}_dd'] = optimize_vac_alloc(simu_once, vac_avail = vac_avail, weights = calc_weights, optm_dir = (sttg[:3] == 'min'), target = sttg[-1], disp = True, tol=1e-23)['alloc']
                    dist_map[f'{sttg}_dd'] = simu_once.calc_vac_prdt(alloc_map[f'{sttg}_dd'])
                else:
                    dist_map[f'{sttg}_dd'] = simu_once.calc_prdt()
                weight_map[f'{sttg}_dd'] = calc_weights
            
            single_res = {'alloc': alloc_map, 'dist': dist_map, 'weights': weight_map}
            single_res.update({'transmission_params': {'params': pd.Series([r0, growth_rate, mean_gen], index=['r0', 'growth_rate', 't_gen'])}})
            for data_key in single_res.keys():
                if data_key not in res: res[data_key] = {}
                for item_key, item in single_res[data_key].items():
                    res[data_key][f'{item_key}_{{{param_name}}}'] = pd.Series(item)
            print(f'Complete {param_name}')
    print('Return Data')
    return res


