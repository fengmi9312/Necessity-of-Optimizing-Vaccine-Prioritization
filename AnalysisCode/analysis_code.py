# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:10:10 2025

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
from task_info import info
import numpy as np
from data_loader import load_all_data
import basic_params
from copy import deepcopy
import func
import itertools
from scipy.stats import pearsonr
import re
import required_generated_data as rgd

data_of_countries = rgd.data_of_countries
country_ifrs = rgd.country_ifrs

def get_expr_info(task_name):
    m = re.search(r'(\w+)_\((\w+)\)', task_name)
    if m: return m.group(1), m.group(2)


def get_necs_from_r0_factor(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    
    task_names = ['necs_from_param_(delay)', 'necs_from_param_(c_perct)',  'necs_from_param_(vac_avail)',  'necs_from_param_(vac_dur)',  'necs_from_param_(vac_eff)',  
                  'necs_from_fatality_(coef_alpha_0)', 'necs_from_fatality_(coef_alpha_1)', 'necs_from_fatality_(coef_beta_0)', 'necs_from_fatality_(coef_beta_1)',
                  'necs_from_contact_(1)', 'necs_from_contact_(2)', 'necs_from_contact_(13)']
    anal_data = {}
    for task_name, country, target, acc_type, dur in itertools.product(task_names, countries, targets, acc_types, durs):
        expr_name, expr_param = get_expr_info(task_name)
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        country_data = data_of_countries[country]
        anti_target = 'd' if target == 'c' else 'c'
        val_types = ['max', 'min', 'anti_min', 'no_vac', 'necs', 'bnf'] if expr_name != 'necs_from_contact' else ['max', 'min', 'necs']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = []
        for file_idx, param_idx in itertools.product(range(40), range(40)):
            ifrs = country_ifrs[country][expr_param.split('_')[1]][file_idx * 40][param_idx] if expr_name == 'necs_from_fatality' else country_data['ifrs']
            pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * ifrs
            if param_idx == 0: 
                for val_type in val_types:
                    anal_data[f'{sheet_name_preppend}_{val_type}'].append([])
            dist_data = expr_data[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            max_val = dist_data[f"max_{target}_{acc_type}{'_dur' if dur else ''}_{append_name}"].to_numpy() @ pop_coef
            min_val = dist_data[f"min_{target}_{acc_type}{'_dur' if dur else ''}_{append_name}"].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_max'][-1].append(max_val)
            anal_data[f'{sheet_name_preppend}_min'][-1].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs'][-1].append(max_val - min_val)
            if expr_name != 'necs_from_contact': 
                anti_min_val = dist_data[f"min_{anti_target}_{acc_type}{'_dur' if dur else ''}_{append_name}"].to_numpy() @ pop_coef
                no_vac_val = dist_data[f"no_vac_{acc_type}_{append_name}"].to_numpy() @ pop_coef 
                anal_data[f'{sheet_name_preppend}_anti_min'][-1].append(anti_min_val)
                anal_data[f'{sheet_name_preppend}_no_vac'][-1].append(no_vac_val)
                anal_data[f'{sheet_name_preppend}_bnf'][-1].append((anti_min_val - min_val) / (no_vac_val - anti_min_val))
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}'])
    return anal_data


def get_necs_line_from_r0(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    task_names = ['necs_line_from_fatality_(coef_alpha_0_0)', 'necs_line_from_fatality_(coef_alpha_0_13)', 'necs_line_from_fatality_(coef_alpha_0_26)', 'necs_line_from_fatality_(coef_alpha_0_39)',
                  'necs_line_from_fatality_(coef_alpha_1_0)', 'necs_line_from_fatality_(coef_alpha_1_13)', 'necs_line_from_fatality_(coef_alpha_1_26)', 'necs_line_from_fatality_(coef_alpha_1_39)', 
                  'necs_line_from_fatality_(coef_beta_0_0)', 'necs_line_from_fatality_(coef_beta_0_13)', 'necs_line_from_fatality_(coef_beta_0_26)', 'necs_line_from_fatality_(coef_beta_0_39)', 
                  'necs_line_from_fatality_(coef_beta_1_0)', 'necs_line_from_fatality_(coef_beta_1_13)', 'necs_line_from_fatality_(coef_beta_1_26)', 'necs_line_from_fatality_(coef_beta_1_39)', 
                  'necs_line_from_param_(delay_10)', 'necs_line_from_param_(delay_0)', 'necs_line_from_param_(delay_13)', 'necs_line_from_param_(delay_26)', 'necs_line_from_param_(delay_39)']
    anal_data = {}
    for task_name, country, target, acc_type, dur in itertools.product(task_names, countries, targets, acc_types, durs):
        expr_name, expr_param = get_expr_info(task_name)
        if dur: sheet_name_preppend = f'{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}_dur'
        else: sheet_name_preppend = f'{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}'
        country_data = data_of_countries[country]
        anti_target = 'd' if target == 'c' else 'c'
        val_types = ['max', 'min', 'anti_min', 'no_vac', 'necs', 'bnf']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = {'res': []}
        for file_idx, param_idx in itertools.product(range(40), range(40)):
            ifrs = country_ifrs[country][expr_param.split('_')[1]][file_idx * 40 + param_idx][int(expr_param.split('_')[-1])] if expr_name == 'necs_line_from_fatality' else country_data['ifrs']
            pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * ifrs
            dist_data = expr_data[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            max_val = dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            min_val = dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_max']['res'].append(max_val)
            anal_data[f'{sheet_name_preppend}_min']['res'].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs']['res'].append(max_val - min_val)
            anti_min_val = dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            no_vac_val = dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ pop_coef
            anal_data[f'{sheet_name_preppend}_anti_min']['res'].append(anti_min_val)
            anal_data[f'{sheet_name_preppend}_no_vac']['res'].append(no_vac_val)
            anal_data[f'{sheet_name_preppend}_bnf']['res'].append((anti_min_val - min_val) / (no_vac_val - anti_min_val))
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}']['res'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}']['res'])
    return anal_data

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    cosine_sim = dot_product / (norm_vec1 * norm_vec2)
    return cosine_sim

def corr_func(alloc, populations, contact_arr, ifr_arr, type_idx = 0):
    # # theta0, theta1 = np.arccos(cosine_similarity(alloc * populations, contact_arr * populations)), np.arccos(cosine_similarity(alloc * populations, ifr_arr * populations))
    # # return 1 - theta0 / (theta0 + theta1)
    
    # if type_idx == 0: return (pearsonr(alloc * populations, contact_arr * populations)[0] - pearsonr(alloc * populations, ifr_arr * populations)[0]) / ((2 - 2 * pearsonr(contact_arr * populations, ifr_arr * populations)[0]) ** 0.5)
    if type_idx == 0: return pearsonr(alloc * populations, contact_arr * populations)[0]
    elif type_idx == 1: return pearsonr(alloc * populations, contact_arr)[0]
    else: return None

def alloc_corr_func(alloc_c, alloc_d, populations):
    return pearsonr(alloc_c * populations, alloc_d * populations)[0]

def get_corr_from_r0_factor(expr_data):  
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_from_param_(delay)', 'necs_from_param_(c_perct)',  'necs_from_param_(vac_avail)',  'necs_from_param_(vac_dur)',  'necs_from_param_(vac_eff)',  
                  'necs_from_fatality_(coef_alpha_0)', 'necs_from_fatality_(coef_alpha_1)', 'necs_from_fatality_(coef_beta_0)', 'necs_from_fatality_(coef_beta_1)']
    for country in countries:
        contact_arr = np.sum([data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
        for task_name, param_idx, target in itertools.product(task_names, range(40), targets):
            expr_name, expr_param = get_expr_info(task_name)
            append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'optimal': [], 'worst': []}
            if target == 'c': 
                sheet_name_x = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            for file_idx in range(40):
                alloc_data = expr_data[task_name][file_idx]['alloc']
                anal_data[sheet_name]['optimal'].append(corr_func(alloc_data[f'min_{target}_{append_name}'].to_numpy(), data_of_countries[country]['populations'], contact_arr, data_of_countries[country]['ifrs']))
                anal_data[sheet_name]['worst'].append(corr_func(alloc_data[f'max_{target}_{append_name}'].to_numpy(), data_of_countries[country]['populations'], contact_arr, data_of_countries[country]['ifrs']))
                if target == 'c': anal_data[sheet_name_x]['alloc_corr'].append(alloc_corr_func(alloc_data[f'min_c_{append_name}'].to_numpy(), alloc_data[f'min_d_{append_name}'].to_numpy(), data_of_countries[country]['populations']))
            anal_data[sheet_name]['optimal'] = np.array(anal_data[sheet_name]['optimal'])
            anal_data[sheet_name]['worst'] = np.array(anal_data[sheet_name]['worst'])
            if target == 'c': anal_data[sheet_name_x]['alloc_corr'] = np.array(anal_data[sheet_name_x]['alloc_corr'])
    return anal_data

def get_corr_line_from_r0(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_line_from_fatality_(coef_alpha_0_0)', 'necs_line_from_fatality_(coef_alpha_0_13)', 'necs_line_from_fatality_(coef_alpha_0_26)', 'necs_line_from_fatality_(coef_alpha_0_39)',
                  'necs_line_from_fatality_(coef_alpha_1_0)', 'necs_line_from_fatality_(coef_alpha_1_13)', 'necs_line_from_fatality_(coef_alpha_1_26)', 'necs_line_from_fatality_(coef_alpha_1_39)', 
                  'necs_line_from_fatality_(coef_beta_0_0)', 'necs_line_from_fatality_(coef_beta_0_13)', 'necs_line_from_fatality_(coef_beta_0_26)', 'necs_line_from_fatality_(coef_beta_0_39)', 
                  'necs_line_from_fatality_(coef_beta_1_0)', 'necs_line_from_fatality_(coef_beta_1_13)', 'necs_line_from_fatality_(coef_beta_1_26)', 'necs_line_from_fatality_(coef_beta_1_39)', 
                  'necs_line_from_param_(delay_8)', 'necs_line_from_param_(delay_10)', 'necs_line_from_param_(delay_0)', 'necs_line_from_param_(delay_13)', 'necs_line_from_param_(delay_26)', 'necs_line_from_param_(delay_39)']
    for country in countries:
        contact_arr = np.sum([data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
        for task_name, target in itertools.product(task_names, targets):
            expr_name, expr_param = get_expr_info(task_name)
            sheet_name = f'{task_name}_{target}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'optimal': [], 'worst': []}
            if target == 'c': 
                sheet_name_x = f'{task_name}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}
            for file_idx, param_idx in itertools.product(range(40), range(40)):
                append_name = f"dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}"
                alloc_data = expr_data[task_name][file_idx]['alloc']
                anal_data[sheet_name]['optimal'].append(corr_func(alloc_data[f'min_{target}_{append_name}'].to_numpy(), data_of_countries[country]['populations'], contact_arr, data_of_countries[country]['ifrs']))
                anal_data[sheet_name]['worst'].append(corr_func(alloc_data[f'max_{target}_{append_name}'].to_numpy(), data_of_countries[country]['populations'], contact_arr, data_of_countries[country]['ifrs']))
                if target == 'c': anal_data[sheet_name_x]['alloc_corr'].append(alloc_corr_func(alloc_data[f'min_c_{append_name}'].to_numpy(), alloc_data[f'min_d_{append_name}'].to_numpy(), data_of_countries[country]['populations']))
            anal_data[sheet_name]['optimal'] = np.array(anal_data[sheet_name]['optimal'])
            anal_data[sheet_name]['worst'] = np.array(anal_data[sheet_name]['worst'])
            if target == 'c': anal_data[sheet_name_x]['alloc_corr'] = np.array(anal_data[sheet_name_x]['alloc_corr'])
    return anal_data

def get_alloc_from_r0_factor(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    task_names = ['necs_from_param_(delay)',  'necs_from_param_(c_perct)',  'necs_from_param_(vac_avail)',  'necs_from_param_(vac_dur)',  'necs_from_param_(vac_eff)', 'necs_from_fatality_(coef_alpha_0)', 'necs_from_fatality_(coef_alpha_1)', 'necs_from_fatality_(coef_beta_0)', 'necs_from_fatality_(coef_beta_1)']
    anal_data = {}
    for country, task_name, param_idx, target in itertools.product(countries, task_names, range(40), targets):
        expr_name, expr_param = get_expr_info(task_name)
        append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
        sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
        anal_data[sheet_name] = {}
        for file_idx in range(info[expr_name][expr_param]):
            alloc_data = expr_data[task_name][file_idx]['alloc']
            anal_data[sheet_name][f'min_{target}_{append_name}'] = alloc_data[f'min_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations']
            anal_data[sheet_name][f'max_{target}_{append_name}'] = alloc_data[f'max_{target}_{append_name}'].to_numpy() * data_of_countries[country]['populations']
    return anal_data


def get_necs_from_growth(expr_data):
    expr_name = 'necs_from_growth_gen'
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    anal_data = {}
    for expr_param, country, target, acc_type, dur in itertools.product(expr_params, countries, targets, acc_types, durs):
        sheet_name = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        country_data = data_of_countries[country]
        pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
        task_name = f'{expr_name}_({expr_param})'
        anal_data[sheet_name] = {}
        for r0_idx, file_idx, param_idx in itertools.product(range(4), range(info[expr_name][expr_param]), range(9)):
            if file_idx == 0 and param_idx == 0: 
                anal_data[sheet_name][f'growth_{r0_idx}'] = []
                anal_data[sheet_name][f'necs_{r0_idx}'] = []
            dist_data = expr_data[task_name][file_idx]['dist']
            param_data = expr_data[task_name][file_idx]['transmission_params']
            append_name = f'{{{basic_params.country_abbr[country]}_{r0_idx}_{param_idx}}}'
            anal_data[sheet_name][f'growth_{r0_idx}'].append(param_data.loc['growth_rate', f'params_{append_name}'] * param_data.loc['t_resp', f'params_{append_name}'])
            anal_data[sheet_name][f'necs_{r0_idx}'].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
        for r0_idx in range(4):
            anal_data[sheet_name][f'growth_{r0_idx}'] = np.array(anal_data[sheet_name][f'growth_{r0_idx}'])
            anal_data[sheet_name][f'necs_{r0_idx}'] = np.array(anal_data[sheet_name][f'necs_{r0_idx}'])
    return anal_data

def get_necs_from_growth_s(expr_data): 
    expr_name = 'necs_from_growth_s'
    targets = ['c', 'd']
    countries = ['United States']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_params = ['weibull_0', 'weibull_1', 'weibull_2', 'gamma_0', 'gamma_1', 'gamma_2', 'lognormal_0', 'lognormal_1', 'lognormal_2']
    anal_data = {}
    growth_left_list = np.arange(0, 13)
    for expr_param, country, target, acc_type, dur in itertools.product(expr_params, countries, targets, acc_types, durs):
        sheet_name_prepend = f"{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}{'_dur' if dur else ''}"
        country_data = data_of_countries[country]
        pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
        task_name = f'{expr_name}_({expr_param})'
        for growth_left in growth_left_list:
            sheet_name = f'{sheet_name_prepend}_{growth_left}'
            anal_data[sheet_name] = {}
            anal_data[sheet_name]['r0'] = []
            anal_data[sheet_name]['necs'] = []
            for r0_idx, file_idx, mean_idx in itertools.product(range(40), range(info[expr_name][expr_param]), range(3)):
                dist_data = expr_data[task_name][file_idx]['dist']
                param_data = expr_data[task_name][file_idx]['transmission_params']
                append_name = f'{{{basic_params.country_abbr[country]}_{r0_idx}_{mean_idx}}}'
                growth = param_data.loc['growth_rate', f'params_{append_name}'] * param_data.loc['t_resp', f'params_{append_name}']
                if growth_left <= growth <= growth_left + 0.1:
                    anal_data[sheet_name]['r0'].append(param_data.loc['r0', f'params_{append_name}'])
                    anal_data[sheet_name]['necs'].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
            anal_data[sheet_name]['r0'] = np.array(anal_data[sheet_name]['r0'])
            anal_data[sheet_name]['necs'] = np.array(anal_data[sheet_name]['necs'])
    return anal_data


def get_fraction_from_time_with_example(expr_data):
    expr_name, expr_param = 'necs_from_example', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {}
    country = 'United States'
    sttgs = ['no_vac', 'max_c', 'min_c', 'max_d', 'min_d']
    for delay_idx, r0_idx, sttg, acc_type, dur in itertools.product(range(2), range(3), sttgs, ['dd', 'gd'], [False, True]):
        sheet_name = f"{delay_idx}_{r0_idx}_{sttg}_{acc_type}{'_dur' if dur else ''}"
        anal_data[sheet_name] = {'time_line': expr_data[task_name][r0_idx + delay_idx * 3][f"curve_{sttg}_{acc_type}{'_dur' if dur else ''}"][f'time_line_{{{expr_param}_{basic_params.country_abbr[country]}}}']}
        for target in ['s', 'i', 'r', 'c', 'd']:
            anal_data[sheet_name][f'curve_{target}'] = expr_data[task_name][r0_idx + delay_idx * 3][f"curve_{sttg}_{acc_type}{'_dur' if dur else ''}"][f'curve_{target}_{{{expr_param}_{basic_params.country_abbr[country]}}}']
    return anal_data
    

def get_alloc_from_age_with_example(expr_data):
    expr_name, expr_param = 'necs_from_example', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {'alloc': {}}
    country = 'United States'
    sttgs = ['max_c', 'min_c', 'max_d', 'min_d']
    for delay_idx, r0_idx, sttg in itertools.product(range(2), range(3), sttgs):
        anal_data['alloc'][f"{delay_idx}_{r0_idx}_{sttg}"] = expr_data[task_name][r0_idx + delay_idx * 3]['alloc'][f'{sttg}_dd_{{{expr_param}_{basic_params.country_abbr[country]}}}'] * data_of_countries[country]['populations']
    return anal_data


def get_prdt_from_corr(expr_data):
    from scipy.stats import pearsonr
    expr_name = 'optm_transition'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    country = 'United States'
    country_data = data_of_countries[country]
    pop_coef = country_data['populations'] * country_data['ifrs']
    contact_arr = np.sum([data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
    anal_data = {'res': {}}
    for file_idx in range(41):
        anal_data['res'][f'corr_{file_idx}'] = []
        anal_data['res'][f'prdt_{file_idx}'] = []
        for idx in range(1001):
            anal_data['res'][f'corr_{file_idx}'].append(pearsonr(expr_data[task_name][file_idx]['allocs'][f'alloc_{idx}'] * country_data['populations'], contact_arr)[0])
            anal_data['res'][f'prdt_{file_idx}'].append(expr_data[task_name][file_idx]['dists'][f'dist_{idx}'] @ pop_coef)
    return anal_data
    

def get_prdt_from_xycoef(expr_data):
    expr_name = 'necs_space'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    anal_data = {}
    for sheet_idx in range(2):
        anal_data[f'res_{sheet_idx}'] = expr_data[task_name][sheet_idx]['res']
    expr_name = 'optm_transition'
    expr_param = 'param'
    task_name = f'{expr_name}_({expr_param})'
    country = 'United States'
    country_data = data_of_countries[country]
    anal_data['alloc_res'] = {}
    anal_data['alloc_res']['alloc_0_n'] = expr_data[task_name][0]['allocs']['alloc_1000'] * country_data['populations']
    anal_data['alloc_res']['alloc_0_p'] = expr_data[task_name][0]['allocs']['alloc_0'] * country_data['populations']
    anal_data['alloc_res']['alloc_1_n'] = expr_data[task_name][40]['allocs']['alloc_1000'] * country_data['populations']
    anal_data['alloc_res']['alloc_1_p'] = expr_data[task_name][40]['allocs']['alloc_0'] * country_data['populations']
    return anal_data


def get_necs_from_country(expr_data):
    x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_name = 'necs_from_country'
    anal_data = {}
    for target, acc_type, dur in itertools.product(['c', 'd'], acc_types, durs):
        sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
        anti_target = 'd' if target == 'c' else 'c'
        anal_data[sheet_name] = {}
        for expr_param, contact_type in itertools.product(x_countries, ['none', 's', 'w', 'swo']):
            pop_coef = data_of_countries[expr_param]['populations'] if target == 'c' else data_of_countries[expr_param]['populations'] * data_of_countries[expr_param]['ifrs']
            task_name = f'{expr_name}_({expr_param})'
            necs_key = f'{expr_param}_{contact_type}_necs'
            bnf_key = f'{expr_param}_{contact_type}_bnf'
            anal_data[sheet_name][necs_key] = []
            anal_data[sheet_name][bnf_key] = []
            for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(25)):
                dist_data = expr_data[task_name][file_idx]['dist']
                append_name = f'{{{contact_type}_{param_idx}}}'
                anal_data[sheet_name][necs_key].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
                anal_data[sheet_name][bnf_key].append((dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef) \
                                                      / (dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef))
    return anal_data



def get_bnf_from_example(expr_data):
    country = 'United States'
    country_data = data_of_countries[country]    
    pop_dist = country_data['populations'] 
    ifr_dist = country_data['populations'] * country_data['ifrs']
    expr_name, expr_param = 'necs_from_param', 'delay'
    task_name = f'{expr_name}_({expr_param})'
    example_alloc = {}
    example_res = {}
    example_points = [(8, 4), (32, 4)]
    coef_dist = {'c': pop_dist, 'd': ifr_dist}
    for idx, (r0_idx, delay_idx) in enumerate(example_points):
        dist_data = expr_data[task_name][r0_idx]['dist']
        alloc_data = expr_data[task_name][r0_idx]['alloc']
        append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
        for optm_target, acc_type in itertools.product(['c', 'd'], ['dd', 'gd']):
            example_alloc[f'min_{optm_target}_{idx}_{acc_type}'] = alloc_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() * country_data['populations']
            for res_target in ['c', 'd']:
                example_res[f'min_{optm_target}_res_{res_target}_{idx}_{acc_type}'] = [dist_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() @ coef_dist[res_target]]
        for res_target, acc_type in itertools.product(['c', 'd'], ['dd', 'gd']):
            example_res[f'no_vac_res_{res_target}_{idx}_{acc_type}'] = [dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ coef_dist[res_target]]
    return {'example_alloc': example_alloc, 'example_res': example_res}



def get_dist_diff_from_r0(expr_data):
    country = 'United States'
    country_data = data_of_countries[country]    
    #pop_dist = country_data['populations'] 
    expr_name, expr_param = 'contact_before_protect', 'param'
    task_name = f'{expr_name}_({expr_param})'
    res = {'dist_diff': {}}
    for idx in range(40):
        res['dist_diff'][f'dist_diff_{idx}'] = (expr_data[task_name][0]['post_dist'][f'dist_{idx}']  - expr_data[task_name][0]['pre_dist'][f'dist_{idx}']) / (1  - expr_data[task_name][0]['pre_dist'][f'dist_{idx}'])
    return res


# def get_param_from_country(expr_data):
#     x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
#     expr_name = 'necs_from_country'
#     anal_data = {}
#     for param in ['r0', 'growth_rate', 'alpha', 'beta']:
#         sheet_name = param
#         anal_data[sheet_name] = {}
#         for expr_param in x_countries:
#             task_name = f'{expr_name}_({expr_param})'
#             key = expr_param
#             anal_data[sheet_name][key] = []
#             for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(25)):
#                 param_data = expr_data[task_name][file_idx]['transmission_params']
#                 anal_data[sheet_name][key].append(param_data.loc[param, f'params_{{none_{param_idx}}}'])
#     return anal_data

# def get_param_from_country_updated(expr_data):
#     x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
#     expr_name = 'param_from_country'
#     anal_data = {}
#     for param in ['r0', 'growth_rate', 'alpha', 'beta', 'a', 'b', 'c', 'd', 'best_left', 'best_right']:
#         sheet_name = param
#         anal_data[sheet_name] = {}
#         for expr_param in x_countries:
#             task_name = f'{expr_name}_({expr_param})'
#             key = expr_param
#             anal_data[sheet_name][key] = []
#             for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(25)):
#                 param_data = expr_data[task_name][file_idx]['transmission_params']
#                 anal_data[sheet_name][key].append(param_data.loc[param, f'params_{{none_{param_idx}}}'])
#     return anal_data
    
# def get_fitted_fraction_from_time(expr_data):
#     from data_loader import load_all_data
#     x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea'][:1]
#     expr_name = 'param_from_country'
#     anal_data = {'real_data': {}, 'fitted_data': {}, 'fitted_period': {}}
#     for country in x_countries:
#         expr_param = country
#         task_name = f'{expr_name}_({expr_param})'
#         country_data = load_all_data([country], basic_params.group_div)
#         fitted_data_tmp = []
#         anal_data['real_data'][f'{country}_data'] = country_data[country]['confirmed'][:90] / country_data[country]['total_population']
#         anal_data['real_data'][f'{country}_time'] = np.arange(90)
#         t_arr = np.arange(90 * basic_params.day_div) / basic_params.day_div
#         for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(25)):
#             param_data = expr_data[task_name][file_idx]['transmission_params']
#             a, b, c, d = param_data.loc['a', f'params_{{none_{param_idx}}}'], param_data.loc['b', f'params_{{none_{param_idx}}}'], \
#                          param_data.loc['c', f'params_{{none_{param_idx}}}'], param_data.loc['d', f'params_{{none_{param_idx}}}']
#             fitted_data_tmp.append(a * np.exp(b * (t_arr - c)) + d)
#         fitted_data_tmp = np.array(fitted_data_tmp)
#         anal_data['fitted_data'][f'{country}_time'] = t_arr
#         anal_data['fitted_data'][f'{country}_mean'] = fitted_data_tmp.mean(axis = 0)
#         anal_data['fitted_data'][f'{country}_upper'] = np.percentile(fitted_data_tmp, 97.5, axis = 0)
#         anal_data['fitted_data'][f'{country}_lower'] = np.percentile(fitted_data_tmp, 2.5, axis = 0)
#         best_left = int(expr_data[task_name][0]['transmission_params'].loc['best_left', 'params_{none_0}'])
#         best_right = int(expr_data[task_name][0]['transmission_params'].loc['best_right', 'params_{none_0}'])
#         anal_data['fitted_period'][country] = [best_left, best_right]
#     return anal_data

# def get_sacr_from_r0(expr_data, expr_name, expr_params = None):
#     targets = ['c', 'd']
#     countries = ['United States']
#     acc_types = ['dd', 'gd']
#     durs = [False, True]
#     if expr_params is None: expr_params = info[expr_name].keys()
#     anal_data = {}
#     for expr_param, country, target, acc_type, dur in itertools.product(expr_params, countries, targets, acc_types, durs):
#         if dur: sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}_dur'
#         else: sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_{target}_{acc_type}'
#         task_name = f'{expr_name}_({expr_param})'
#         country_data = data_of_countries[country]
#         pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifrs']
#         anti_target = 'd' if target == 'c' else 'c'
#         anal_data[f'anti_min_{sheet_name_append}'] = []
#         anal_data[f'min_{sheet_name_append}'] = []
#         if expr_param == 'delay': anal_data[f'no_vac_{sheet_name_append}'] = []
#         for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(40)):
#             if param_idx == 0: 
#                 anal_data[f'anti_min_{sheet_name_append}'].append([])
#                 anal_data[f'min_{sheet_name_append}'].append([])
#                 if expr_param == 'delay': anal_data[f'no_vac_{sheet_name_append}'].append([])
#             dist_data = expr_data[task_name][file_idx]['dist']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#             anal_data[f'anti_min_{sheet_name_append}'][-1].append(dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#             anal_data[f'min_{sheet_name_append}'][-1].append(dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#             if expr_param == 'delay': anal_data[f'no_vac_{sheet_name_append}'][-1].append(dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#         anal_data[f'anti_min_{sheet_name_append}'] = np.array(anal_data[f'anti_min_{sheet_name_append}'])
#         anal_data[f'min_{sheet_name_append}'] = np.array(anal_data[f'min_{sheet_name_append}'])
#         if expr_param == 'delay': anal_data[f'no_vac_{sheet_name_append}'] = np.array(anal_data[f'no_vac_{sheet_name_append}'])
#     return anal_data


# def get_alloc_corr_from_r0(expr_data):  
#     from scipy.stats import pearsonr
#     import re
#     pattern = r'(\w+)_\((\w+)\)'
#     countries = ['United States']
#     anal_data = {}
#     for country in countries:
#         for param_idx, task_name in itertools.product(range(40), ['necs_from_param_(delay)', 'necs_from_fatality_(coef_alpha_0)', 'necs_from_fatality_(coef_alpha_1)', 'necs_from_fatality_(coef_beta_0)', 'necs_from_fatality_(coef_beta_1)']):
#             match = re.search(pattern, task_name)
#             if match:
#                 expr_name = match.group(1)
#                 expr_param = match.group(2)
#             append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#             sheet_name = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
#             anal_data[sheet_name] = {'alloc_corr': []}
#             for file_idx in range(info[expr_name][expr_param]):
#                 alloc_data = expr_data[task_name][file_idx]['alloc']
#                 anal_data[sheet_name]['alloc_corr'].append(pearsonr(alloc_data[f'min_c_{append_name}'].to_numpy() * data_of_countries[country]['populations'], \
#                                                                  alloc_data[f'min_d_{append_name}'].to_numpy() * data_of_countries[country]['populations'])[0])
#             anal_data[sheet_name]['alloc_corr'] = np.array(anal_data[sheet_name]['alloc_corr'])
#     return anal_data

# def get_sacr_line_from_r0(expr_data):  
#     from scipy.stats import pearsonr
#     import re
#     pattern = r'(\w+)_\((\w+)\)'
#     countries = ['United States']
#     alpha_val, beta_val = 2.826, 5.665
#     srv_func = func.srv_weibull
#     anal_data = {}
#     ifr_res = {}
#     for country in countries:
#         ifr_res[country] = {'alpha': {}, 'beta': {}}
#         country_data = data_of_countries[country]
#         for equity_idx in [0, 13, 26, 39]:
#             ifr_res[country]['alpha'][str(equity_idx)] = []
#             ifr_res[country]['beta'][str(equity_idx)] = []
#             for file_idx, param_idx in itertools.product(range(40), range(40)):
#                 r0 = np.exp((file_idx + param_idx / 40) * 0.075)
#                 calc_params = deepcopy(basic_params.calc_params)
#                 calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
#                 calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
#                 srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#                 calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
                
#                 k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
#                 steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
#                 steady_d = steady_c_arr @ country_data['ifrs']
#                 equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
#                 diff_ifr = country_data['ifrs'] - equal_ifr
#                 ifr_tmp = equal_ifr + equity_idx * diff_ifr / 40
#                 ifr_res[country]['alpha'][str(equity_idx)].append(ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp))
#                 ifr_res[country]['beta'][str(equity_idx)].append(ifr_tmp)
#         for task_name in ['necs_line_from_param_(delay_10)', 'necs_line_from_param_(delay_0)', 'necs_line_from_param_(delay_13)', 'necs_line_from_param_(delay_26)', 'necs_line_from_param_(delay_39)',
#                           'necs_line_from_fatality_(coef_alpha_0_0)', 'necs_line_from_fatality_(coef_alpha_0_13)', 'necs_line_from_fatality_(coef_alpha_0_26)', 'necs_line_from_fatality_(coef_alpha_0_39)',
#                           'necs_line_from_fatality_(coef_alpha_1_0)', 'necs_line_from_fatality_(coef_alpha_1_13)', 'necs_line_from_fatality_(coef_alpha_1_26)', 'necs_line_from_fatality_(coef_alpha_1_39)',
#                           'necs_line_from_fatality_(coef_beta_0_0)', 'necs_line_from_fatality_(coef_beta_0_13)', 'necs_line_from_fatality_(coef_beta_0_26)', 'necs_line_from_fatality_(coef_beta_0_39)'
#                           'necs_line_from_fatality_(coef_beta_1_0)', 'necs_line_from_fatality_(coef_beta_1_13)', 'necs_line_from_fatality_(coef_beta_1_26)', 'necs_line_from_fatality_(coef_beta_1_39)']:
#             match = re.search(pattern, task_name)
#             if match:
#                 expr_name = match.group(1)
#                 expr_param = match.group(2)
#             sheet_name = f'{task_name}_{basic_params.country_abbr[country]}'
#             anal_data[sheet_name] = {'alloc_corr': [], 'sacr_c': [], 'sacr_d': []}
#             for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(40)):
#                 append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#                 alloc_data = expr_data[task_name][file_idx]['alloc']
#                 anal_data[sheet_name]['alloc_corr'].append(pearsonr(alloc_data[f'min_c_{append_name}'].to_numpy() * country_data['populations'], alloc_data[f'min_d_{append_name}'].to_numpy() * country_data['populations'])[0])
#                 append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#                 dist_data = expr_data[task_name][file_idx]['dist']
#                 cc = dist_data[f'min_c_dd_{append_name}'].to_numpy() @ country_data['populations']
#                 dc = dist_data[f'min_d_dd_{append_name}'].to_numpy() @ country_data['populations']
#                 ifrs = ifr_res[country][expr_param.split('_')[1]][expr_param.split('_')[-1]][file_idx * 40 + param_idx] if expr_name.split('_')[-1] == 'fatality' else country_data['ifrs']
#                 dd = dist_data[f'min_d_dd_{append_name}'].to_numpy() @ (country_data['populations'] * ifrs)
#                 cd = dist_data[f'min_c_dd_{append_name}'].to_numpy() @ (country_data['populations'] * ifrs)
#                 anal_data[sheet_name]['sacr_c'].append((dc - cc) / dc)
#                 anal_data[sheet_name]['sacr_d'].append((cd - dd) / cd)
#             anal_data[sheet_name]['alloc_corr'] = np.array(anal_data[sheet_name]['alloc_corr'])
#             anal_data[sheet_name]['sacr_c'] = np.array(anal_data[sheet_name]['sacr_c'])
#             anal_data[sheet_name]['sacr_d'] = np.array(anal_data[sheet_name]['sacr_d'])
#     return anal_data



# def get_sacr_from_r0_fatality(expr_data):
#     countries = ['United States']
#     acc_types = ['dd', 'gd']
#     durs = [False, True]
#     expr_params = ['coef_alpha_0', 'coef_alpha_1', 'coef_beta_0', 'coef_beta_1']
#     expr_name = 'necs_from_fatality'
#     anal_data = {}
#     alpha_val, beta_val = 2.826, 5.665
#     srv_func = func.srv_weibull
#     for expr_param, country, acc_type, dur in itertools.product(expr_params, countries, acc_types, durs):
#         if dur: d_sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}_dur'
#         else: d_sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_d_{acc_type}'
#         if dur:c_sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}_dur'
#         else: c_sheet_name_append = f'{expr_param}_{basic_params.country_abbr[country]}_c_{acc_type}'
#         task_name = f'{expr_name}_({expr_param})'
#         anal_data[f'min_c_{d_sheet_name_append}'] = []
#         anal_data[f'min_c_{c_sheet_name_append}'] = []
#         anal_data[f'min_d_{d_sheet_name_append}'] = []
#         anal_data[f'min_d_{c_sheet_name_append}'] = []
#         anal_data[f'no_vac_{d_sheet_name_append}'] = []
#         anal_data[f'no_vac_{c_sheet_name_append}'] = []
#         for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(40)):
#             r0 = np.exp(file_idx * 0.075)
#             country_data = data_of_countries[country]
#             calc_params = deepcopy(basic_params.calc_params)
#             calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
#             calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
#             srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#             calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
#             if expr_param.split('_')[1] == 'alpha':
#                 k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
#                 steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) * calc_params['populations']
#                 steady_d = steady_c_arr @ country_data['ifrs']
#             equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
#             diff_ifr = country_data['ifrs'] - equal_ifr
#             ifr_tmp = equal_ifr + param_idx * diff_ifr / 40
#             if expr_param.split('_')[1] == 'alpha': ifrs = ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp)
#             else: ifrs = ifr_tmp
            
#             if param_idx == 0: 
#                 anal_data[f'min_d_{d_sheet_name_append}'].append([])
#                 anal_data[f'min_d_{c_sheet_name_append}'].append([])
#                 anal_data[f'min_c_{d_sheet_name_append}'].append([])
#                 anal_data[f'min_c_{c_sheet_name_append}'].append([])
#                 anal_data[f'no_vac_{d_sheet_name_append}'].append([])
#                 anal_data[f'no_vac_{c_sheet_name_append}'].append([])
#             dist_data = expr_data[task_name][file_idx]['dist']
#             d_pop_coef = country_data['populations'] * ifrs
#             c_pop_coef = country_data['populations']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#             anal_data[f'min_d_{d_sheet_name_append}'][-1].append(dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ d_pop_coef)
#             anal_data[f'min_d_{c_sheet_name_append}'][-1].append(dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ c_pop_coef)
#             anal_data[f'min_c_{d_sheet_name_append}'][-1].append(dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ d_pop_coef)
#             anal_data[f'min_c_{c_sheet_name_append}'][-1].append(dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ c_pop_coef)
#             anal_data[f'no_vac_{d_sheet_name_append}'][-1].append(dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ d_pop_coef)
#             anal_data[f'no_vac_{c_sheet_name_append}'][-1].append(dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ c_pop_coef)
#         anal_data[f'min_d_{d_sheet_name_append}'] = np.array(anal_data[f'min_d_{d_sheet_name_append}'])
#         anal_data[f'min_d_{c_sheet_name_append}'] = np.array(anal_data[f'min_d_{c_sheet_name_append}'])
#         anal_data[f'min_c_{d_sheet_name_append}'] = np.array(anal_data[f'min_c_{d_sheet_name_append}'])
#         anal_data[f'min_c_{c_sheet_name_append}'] = np.array(anal_data[f'min_c_{c_sheet_name_append}'])
#         anal_data[f'no_vac_{d_sheet_name_append}'] = np.array(anal_data[f'no_vac_{d_sheet_name_append}'])
#         anal_data[f'no_vac_{c_sheet_name_append}'] = np.array(anal_data[f'no_vac_{c_sheet_name_append}'])
#     return anal_data


# def get_sacr_from_r0_param(expr_data): 
#     return get_sacr_from_r0(expr_data, 'necs_from_param')

# def get_sacr_from_country(expr_data):
#     x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
#     acc_types = ['dd', 'gd']
#     durs = [False, True]
#     countries_data = load_all_data(x_countries, basic_params.group_div)
#     expr_name = 'necs_from_country'
#     anal_data = {}
#     for acc_type, dur in itertools.product(acc_types, durs):
#         sheet_name = f"{acc_type}{'_dur' if dur else ''}"
#         anal_data[sheet_name] = {}
#         for expr_param in x_countries:
#             c_coef = countries_data[expr_param]['populations'] 
#             d_coef = countries_data[expr_param]['populations'] * countries_data[expr_param]['ifrs']
#             task_name = f'{expr_name}_({expr_param})'
#             anal_data[sheet_name][f'{expr_param}_c'] = []
#             anal_data[sheet_name][f'{expr_param}_d'] = []
#             for file_idx, param_idx in itertools.product(range(info[expr_name][expr_param]), range(25)):
#                 dist_data = expr_data[task_name][file_idx]['dist']
#                 append_name = f'{{none_{param_idx}}}'
#                 cc = dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ c_coef
#                 dc = dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ c_coef
#                 dd = dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ d_coef
#                 cd = dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ d_coef
#                 anal_data[sheet_name][f'{expr_param}_c'].append((dc - cc) / dc)
#                 anal_data[sheet_name][f'{expr_param}_d'].append((cd - dd) / cd)
#     return anal_data





# def get_fig3data(expr_data, country = 'United States', acc_type = 'dd'):
#     country_data = load_all_data([country], basic_params.group_div)[country]    
#     pop_dist = country_data['populations'] 
#     ifr_dist = country_data['populations'] * country_data['ifrs']
    
#     target = 'd'
#     expr_name, expr_param = 'necs_from_param', 'delay'
#     task_name = f'{expr_name}_({expr_param})'
#     necs_with_r0_delay = []
#     for file_idx in range(info[expr_name][expr_param]):
#         necs_with_r0_delay.append([])
#         for delay_idx in range(40):
#             dist_data = expr_data[task_name][file_idx]['dist']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
#             necs_with_r0_delay[-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ ifr_dist - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ ifr_dist)
#     necs_with_r0_delay = np.array(necs_with_r0_delay)
    
#     expr_name, expr_param = 'necs_from_fatality', 'coef_beta_0'
#     task_name = f'{expr_name}_({expr_param})'
#     calc_params = deepcopy(basic_params.calc_params)
#     calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
#     calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
#     #alpha_val, beta_val = 2.826, 5.665
#     #srv_gen = func.srv_weibull(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#     necs_with_fatality = []
#     example_ifr = {}
#     for file_idx in range(info[expr_name][expr_param]):
#         necs_with_fatality.append([])
#         #r0 = np.exp(np.arange(40) * 0.075)[file_idx]
#         #k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(srv_gen, srv_gen))
#         #steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(srv_gen, srv_gen), _i = calc_params['i0']) * calc_params['populations']
#         #steady_d = steady_c_arr @ country_data['ifrs']
#         equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
#         diff_ifr = country_data['ifrs'] - equal_ifr
#         for param_idx, param_val in enumerate(np.arange(40) / 40):
#             ifr_tmp = equal_ifr + param_val * diff_ifr 
#             pop_coef = country_data['populations'] * ifr_tmp #* steady_d / (steady_c_arr @ ifr_tmp) 
#             if file_idx == 10 and param_idx in [0, 20, 39]:
#                 example_ifr[f'ifr_{param_idx}'] = ifr_tmp #* steady_d / (steady_c_arr @ ifr_tmp) 
#             dist_data = edata[task_name][file_idx]['dist']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#             necs_with_fatality[-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#     necs_with_fatality = np.array(necs_with_fatality)
    
    
#     expr_name, expr_param = 'necs_from_param', 'delay'
#     task_name = f'{expr_name}_({expr_param})'
#     example_alloc = {}
#     example_res = {}
#     example_points = [(8, 4), (32, 4)]
#     coef_dist = {'c': pop_dist, 'd': ifr_dist}
#     for idx, (r0_idx, delay_idx) in enumerate(example_points):
#         dist_data = expr_data[task_name][r0_idx]['dist']
#         alloc_data = expr_data[task_name][r0_idx]['alloc']
#         append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
#         for optm_target in ['c', 'd']:
#             example_alloc[f'min_{optm_target}_{idx}'] = alloc_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() * country_data['populations']
#             for res_target in ['c', 'd']:
#                 example_res[f'min_{optm_target}_res_{res_target}_{idx}'] = [dist_data[f'min_{optm_target}_{acc_type}_{append_name}'].to_numpy() @ coef_dist[res_target]]
    
    
    
#     return {'necs_grid': necs_with_r0_delay, 'necs_grid_with_fatality': necs_with_fatality, 'example_res': example_res, 'example_alloc': example_alloc, 'example_ifr': example_ifr}





# def get_fig4data(expr_data, target = 'c', country = 'United States', acc_type = 'dd'):
    
#     from scipy.optimize import fsolve
#     from scipy.stats import norm
#     def generate_dist(peak = 30, equity = 0.2, group_amount = basic_params.group_amount):
#         tau_step = 80 / group_amount
#         if equity == 0:
#             return np.ones(group_amount) / group_amount
#         if equity == 1:
#             return np.eye(group_amount)[peak // group_amount]
        
#         def get_normal_dist(sigma):
#             dist = [norm.sf((i + 1) * tau_step, peak, sigma) - norm.sf(i * tau_step, peak, sigma) for i in range(group_amount)]
#             return np.array(dist) / np.sum(dist)
        
#         def equation(x):
#             return equity - func.calc_equity(get_normal_dist(x[0]))
        
#         param = fsolve(equation, [1,])[0]
#         return get_normal_dist(param)
    
#     country_data = load_all_data([country], basic_params.group_div)[country]    
#     res = {}
#     pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifr']
    
#     expr_name = 'necs_from_contact'
#     res = {}
#     for idx, expr_param in enumerate(['home', 'school', 'work', 'other_locations']):
#         location_idx = 13 if idx == 0 else idx
#         task_name = f'{expr_name}_({location_idx})'
#         res[f'contact_{expr_param}'] = country_data['contacts'][expr_param]
#         res[expr_param] = []
#         for file_idx in range(info[expr_name][str(idx)]):
#             res[expr_param].append([])
#             for param_idx in range(40):
#                 dist_data = expr_data[task_name][file_idx]['dist']
#                 append_name = f'{{{location_idx}_{basic_params.country_abbr[country]}_{param_idx}}}'
#                 res[expr_param][-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#         res[expr_param] = np.array(res[expr_param])
        
#     expr_name = 'necs_from_population'
#     for expr_param in ['peak', 'equity']:
#         task_name = f'{expr_name}_({expr_param})'
#         res[expr_param] = []
#         res[f'example_{expr_param}'] = {}
#         param_list = np.linspace(0, 0.8775, 40) if expr_param == 'equity' else np.linspace(0, 78, 40)
        
#         for param_idx, param_val in enumerate(param_list):
#             pop_dist = generate_dist(**{expr_param: param_val})
#             pop_coef = pop_dist if target == 'c' else pop_dist * country_data['ifr']
#             for file_idx in range(info[expr_name][expr_param]):
#                 if param_idx == 0: res[expr_param].append([])
#                 if file_idx == 10 and param_idx in [5, 20, 35]:
#                     res[f'example_{expr_param}'][f'populations_{param_idx}'] = pop_dist 
#                 dist_data = expr_data[task_name][file_idx]['dist']
#                 append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#                 res[expr_param][file_idx].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#         res[expr_param] = np.array(res[expr_param])
#     return res


# def get_fig5data(expr_data, target = 'c', country = 'United States', acc_type = 'dd'):
#     country_data = load_all_data([country], basic_params.group_div)[country]    
#     res = {}
#     pop_coef = country_data['populations'] if target == 'c' else country_data['populations'] * country_data['ifr']
    
#     expr_name = 'necs_from_param'
#     res = {}
#     for expr_param in ['vac_eff', 'vac_avail', 'c_perct', 'vac_dur']:
#         task_name = f'{expr_name}_({expr_param})'
#         res[expr_param] = []
#         for file_idx in range(info[expr_name][expr_param]):
#             res[expr_param].append([])
#             for delay_idx in range(40):
#                 dist_data = expr_data[task_name][file_idx]['dist']
#                 append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
#                 if expr_param != 'vac_dur': res[expr_param][-1].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#                 else: res[expr_param][-1].append(dist_data[f'max_{target}_{acc_type}_dur_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_dur_{append_name}'].to_numpy() @ pop_coef)
#         res[expr_param] = np.array(res[expr_param])
#     return res
    
# def get_fig6data(expr_data, acc_type = 'dd'):  
#     x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
#     countries_data = load_all_data(x_countries, basic_params.group_div)
#     expr_name = 'necs_from_country'
#     country_res = {}
#     for target in ['c', 'd']:
#         country_res[f'res_{target}'] = {}
#         for expr_param in x_countries:
#             pop_coef = countries_data[expr_param]['populations'] if target == 'c' else countries_data[expr_param]['populations'] * countries_data[expr_param]['ifrs']
#             task_name = f'{expr_name}_({expr_param})'
#             country_res[f'res_{target}'][expr_param] = {}
#             for contact_type in ['none', 's', 'w', 'o', 'swo']:
#                 country_res[f'res_{target}'][expr_param][contact_type] = []
#                 for file_idx in range(info[expr_name][expr_param]):
#                     for param_idx in range(25):
#                         dist_data = edata[task_name][file_idx]['dist']
#                         append_name = f'{{{contact_type}_{param_idx}}}'
#                         country_res[f'res_{target}'][expr_param][contact_type].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#     return country_res
    

# def get_testdata(expr_data, country = 'United States'):
#     country_data = load_all_data([country], basic_params.group_div)[country]    
#     pop_dist = country_data['populations'] 
#     ifr_dist = country_data['populations'] * country_data['ifrs']
    
#     acc_type = 'dd'
#     expr_name, expr_param = 'necs_from_param', 'delay'
#     task_name = f'{expr_name}_({expr_param})'
#     c_res = []
#     d_res = []
#     c_alloc = []
#     d_alloc = []
#     for r0_idx in np.arange(40):
#         c_res.append([])
#         d_res.append([])
#         c_alloc.append([])
#         d_alloc.append([])
#         for delay_idx in np.arange(40):
#             dist_data = expr_data[task_name][r0_idx]['dist']
#             alloc_data = expr_data[task_name][r0_idx]['alloc']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{delay_idx}}}'
#             c_target_c_optm = dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ pop_dist
#             c_target_d_optm = dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ pop_dist
#             d_target_c_optm = dist_data[f'min_c_{acc_type}_{append_name}'].to_numpy() @ ifr_dist
#             d_target_d_optm = dist_data[f'min_d_{acc_type}_{append_name}'].to_numpy() @ ifr_dist
#             c_res[-1].append(c_target_d_optm - c_target_c_optm)
#             d_res[-1].append(d_target_c_optm - d_target_d_optm)
#             c_alloc[-1].append(alloc_data[f'min_c_{acc_type}_{append_name}'].to_numpy() * pop_dist)
#             d_alloc[-1].append(alloc_data[f'min_d_{acc_type}_{append_name}'].to_numpy() * pop_dist)
#     return np.array(c_res), np.array(d_res), c_alloc, d_alloc
    

# def get_test1data(expr_data, country = 'United States', acc_type = 'dd'):
#     country_data = load_all_data([country], basic_params.group_div)[country]    
#     pop_dist = country_data['populations'] 
#     ifr_dist = country_data['populations'] * country_data['ifrs']
#     contact_arr = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0).sum(axis = 1)
#     calc_params = deepcopy(basic_params.calc_params)
#     calc_params.update({key: country_data[key] for key in ['populations', 'ylls']})
#     calc_params['contacts'] = np.sum([country_data['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    
#     from scipy.stats import pearsonr
#     target = 'd'
#     expr_name, expr_param = 'necs_from_fatality', 'coef_beta_0'
#     task_name = f'{expr_name}_({expr_param})'
#     min_alloc = []
#     max_alloc = []
#     necs = []
#     alpha_val, beta_val = 2.826, 5.665
#     srv_gen = func.srv_weibull(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
#     for param_idx, param_val in enumerate(np.arange(40) / 40):
#         min_alloc.append([])
#         max_alloc.append([])
#         necs.append([])
#         for file_idx in range(info[expr_name][expr_param]):
#             r0 = np.exp(np.arange(40) * 0.075)[file_idx]
#             k_val = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * func.lambda_eff_srv(srv_gen, srv_gen))
#             steady_c_arr = func.get_steady_state(k_val, calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(srv_gen, srv_gen), _i = calc_params['i0']) * calc_params['populations']
#             steady_d = steady_c_arr @ country_data['ifrs']
#             equal_ifr = np.ones(basic_params.group_amount) * country_data['ifrs'].sum() / basic_params.group_amount
#             diff_ifr = country_data['ifrs'] - equal_ifr
#             ifr_tmp = equal_ifr + param_val * diff_ifr 
#             pop_coef = country_data['populations'] * ifr_tmp * steady_d / (steady_c_arr @ ifr_tmp) 
#             alloc_data = edata[task_name][file_idx]['dist']
#             append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
#             min_alloc[-1].append(alloc_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#             max_alloc[-1].append(alloc_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
#             necs[-1].append(max_alloc[-1][-1] - min_alloc[-1][-1])

#     return min_alloc, max_alloc, necs


# '''
# import matplotlib.pyplot as plt
# import cmocean
# import seaborn as sns
# from matplotlib.gridspec import GridSpec
# import tkinter as tk
# root = tk.Tk()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.destroy()

# fig, axes = plt.subplots(5, 8)
# for i in range(5):
#     for j in range(8):
#         plt.sca(axes[i][j])
#         plt.plot(necs[i * 8 + j], color = 'tab:red')

    

# unit = 0.65

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




# def plot_fig3(anal_data):
#     dpi = plt.rcParams['figure.dpi']
#     grid_col, grid_row = 64, 97
#     scale_prop, shape_prop = 25, 1
#     fig_width = grid_row * scale_prop * shape_prop * unit / dpi
#     fig_height = grid_col * scale_prop * unit / dpi
#     fig = plt.figure(figsize = [fig_width, fig_height])
#     axes = []
#     gs = GridSpec(grid_col, grid_row, figure = fig)
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:29, 9:39]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:29, 45:75]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:10, 80:93]))
#     axes[-1].append(fig.add_subplot(gs[12:20, 80:93]))
#     axes[-1].append(fig.add_subplot(gs[22:30, 80:93]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[38:59, 22:43]))
#     axes[-1].append(fig.add_subplot(gs[38:59, 71:92]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[36:46, 5:18]))
#     axes[-1].append(fig.add_subplot(gs[51:61, 5:18]))
#     axes[-1].append(fig.add_subplot(gs[36:46, 54:67]))
#     axes[-1].append(fig.add_subplot(gs[51:61, 54:67]))
    
#     ax = axes[0][0]
#     plt.sca(ax)
#     plt.imshow(anal_data['necs_grid'].T)
#     plt.colorbar(orientation='horizontal', location='top')
#     plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#     plt.xlabel(r'$\ln{R_0}$')
#     ax.set_yticks(np.arange(40)[5::10], np.arange(0, 2000, 50)[5::10] * basic_params.step)
#     plt.ylabel(r'$T_{\mathrm{resp}}$')
    
#     ax = axes[1][0]
#     plt.sca(ax)
#     plt.imshow(anal_data['necs_grid_with_fatality'].T)
#     plt.colorbar(orientation='horizontal', location='top')
#     plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#     plt.xlabel(r'$\ln{R_0}$')
#     ax.set_yticks(np.arange(40)[4::8], np.arange(0, 40)[4::8] / 40)
#     plt.ylabel(r'$\epsilon$')
    
#     for idx, ifr_idx in enumerate([0, 20, 39]):
#         ax = axes[2][idx]
#         plt.sca(ax)
#         plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, anal_data['example_ifr'][f'ifr_{ifr_idx}'], color = 'k', width = 4)
#         plt.ylim(0, 0.21)
#         ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
#         ax.set_yticks(np.arange(0, 21, 10) / 100, np.arange(0, 21, 10))
#         if idx == 2: plt.xlabel('Age', fontsize = 15 * unit)
#         plt.ylabel('Fatality (%)', fontsize = 15 * unit)
    
#     alloc_colors = ['tab:red', 'black']
#     titles = [r'$\vartheta_\mathrm{best, c}$', r'$\vartheta_\mathrm{best, d}$']
#     for idx in range(2):
#         ax_c = axes[3][idx]
#         ax_c.bar([-0.5, 0.5], [anal_data['example_res'][f'min_c_res_c_{idx}'][0], anal_data['example_res'][f'min_d_res_c_{idx}'][0]], 
#                  width = 0.92, color = 'none', edgecolor = alloc_colors, linewidth = 2 * unit, hatch='///', 
#                  label = [r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, c}$', 
#                           r'$\tilde{\chi}_\mathrm{c}$ with $\vartheta_\mathrm{best, d}$'])
    
#         ax_d =  ax_c.twinx()
#         ax_d.bar([3.5, 4.5], [anal_data['example_res'][f'min_c_res_d_{idx}'][0], anal_data['example_res'][f'min_d_res_d_{idx}'][0]], 
#                  width = 0.92, color = 'none', edgecolor = alloc_colors, linewidth = 2 * unit, hatch='...', 
#                  label = [r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, c}$', 
#                           r'$\tilde{\chi}_\mathrm{d}$ with $\vartheta_\mathrm{best, d}$'])
#         ax_c.set_xticks([0, 4], ['Cumulative Infection', 'Death'])
#         for i, optm_target in enumerate(['c', 'd']):
#             ax = axes[4][idx * 2 + i]
#             plt.sca(ax)
#             plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, 
#                     anal_data['example_alloc'][f'min_{optm_target}_{idx}'],
#                     color = alloc_colors[i], width =4)
#             ax.text(0.02, 0.98, titles[i], fontsize = 15 * unit, color = alloc_colors[i],
#                     horizontalalignment='left', verticalalignment='top', 
#                     transform= ax.transAxes)
#             ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
#             ax.set_yticks(np.arange(0, 11, 5) / 100, np.arange(0, 11, 5))
#             plt.xlabel('Age', fontsize = 15 * unit)
#             plt.ylabel('Fatality (%)', fontsize = 15 * unit)
            
#     return fig, axes


# def plot_fig4(anal_data):
#     dpi = plt.rcParams['figure.dpi']
#     grid_col, grid_row = 64, 112
#     scale_prop, shape_prop = 25, 1
#     fig_width = grid_row * scale_prop * shape_prop * unit / dpi
#     fig_height = grid_col * scale_prop * unit / dpi
#     fig = plt.figure(figsize = [fig_width, fig_height])
#     axes = []
#     gs = GridSpec(grid_col, grid_row, figure = fig)
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:10, 2:10]))
#     axes[-1].append(fig.add_subplot(gs[2:10, 13:21]))
#     axes[-1].append(fig.add_subplot(gs[13:21, 2:10]))
#     axes[-1].append(fig.add_subplot(gs[13:21, 13:21]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[2:21, 25:44]))
#     axes[-1].append(fig.add_subplot(gs[2:21, 47:66]))
#     axes[-1].append(fig.add_subplot(gs[2:21, 69:88]))
#     axes[-1].append(fig.add_subplot(gs[2:21, 91:110]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[30:37, 15:27]))
#     axes[-1].append(fig.add_subplot(gs[39:46, 15:27]))
#     axes[-1].append(fig.add_subplot(gs[48:55, 15:27]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[33:52, 32:51]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[30:37, 67:79]))
#     axes[-1].append(fig.add_subplot(gs[39:46, 67:79]))
#     axes[-1].append(fig.add_subplot(gs[48:55, 67:79]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[33:52, 84:105]))
    
#     cmap = plt.cm.rainbow
    
#     for idx, location in enumerate(['home', 'school', 'work', 'other_locations']):
#         ax = axes[0][idx]
#         plt.sca(ax)
#         plt.imshow(anal_data[f'contact_{location}'].T)
#         plt.gca().invert_yaxis()
#         if idx == 2 or idx == 3: 
#             plt.xlabel('Age')
#             ax.set_xticks([0, 5, 10, 15], ['0-4', '25-30', '50-55', '75-80'])
#         else:
#             ax.set_xticks([])
#         if idx == 0 or idx == 2: 
#             plt.ylabel('Age')
#             ax.set_yticks([0, 5, 10, 15], ['0-4', '25-30', '50-55', '75-80'])
#         else:
#             ax.set_yticks([])
#         plt.xticks(rotation = 45)
        
#         ax = axes[1][idx]
#         plt.sca(ax)
#         plt.plot(np.arange(0, 40), [anal_data[location][i][0] - anal_data[location][i][-1] for i in range(40)], color = cmap(i / 40))
#         plt.xlabel(r'$\varepsilon$')
#         plt.ylabel('Necessity')
        
    
#     for idx, peak_idx in enumerate([5, 20, 35]):
#         ax = axes[2][idx]
#         plt.sca(ax)
#         plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, anal_data['example_peak'][f'populations_{peak_idx}'], width = 4)
#         ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
#         plt.xlabel('Age')
    
#     ax = axes[3][0]
#     plt.sca(ax)
#     plt.imshow(anal_data['peak'].T)
#     plt.colorbar()
#     plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#     plt.xlabel(r'$\ln{R_0}$')
#     ax.set_yticks(np.arange(40)[4::8], np.arange(0, 40)[4::8] *2)
#     plt.ylabel('$peak$')
    
#     for idx, equity_idx in enumerate([5, 20, 35]):
#         ax = axes[4][idx]
#         plt.sca(ax)
#         plt.bar(np.arange(basic_params.group_amount) * 5 + 2.5, anal_data['example_equity'][f'populations_{equity_idx}'], width = 4)
#         ax.set_xticks(np.arange(0, 81, 40), np.arange(0, 81, 40))
#         plt.xlabel('Age')
        
        
#     ax = axes[5][0]
#     plt.sca(ax)
#     plt.imshow(anal_data['equity'].T)
#     plt.colorbar()
#     plt.gca().invert_yaxis()
#     ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#     plt.xlabel(r'$\ln{R_0}$')
#     ax.set_yticks(np.arange(40)[4::8], np.arange(0, 40)[4::8] * 9 / 400)
#     plt.ylabel('$Equity$')
    
#     return fig, axes
    
    
    
    


# def plot_fig5(anal_data):
#     dpi = plt.rcParams['figure.dpi']
#     grid_col, grid_row = 2, 2
#     scale_prop, shape_prop = 1000, 1
#     fig_width = grid_row * scale_prop * shape_prop * unit / dpi
#     fig_height = grid_col * scale_prop * unit / dpi
#     fig = plt.figure(figsize = [fig_width, fig_height])
#     axes = []
#     gs = GridSpec(grid_col, grid_row, figure = fig)
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[0:1, 0:1]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[0:1, 1:2]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[1:2, 0:1]))
#     axes.append([])
#     axes[-1].append(fig.add_subplot(gs[1:2, 1:2]))
    
#     ylabels = {'vac_eff': 'Vaccine Efficacy', 'vac_avail': 'Vaccine Availability', 'c_perct': 'Percentile', 'vac_dur': 'Vaccination Duration'}
#     yticks = {'vac_eff': np.arange(22, 102, 2) / 100,   'vac_avail': np.linspace(0.12, 0.9, 40),  'c_perct': np.linspace(0.215, 0.8, 40),  'vac_dur': np.arange(1, 41)}
#     for idx, expr_param in enumerate(['vac_eff', 'vac_avail', 'c_perct', 'vac_dur']):
#         ax = axes[idx][0]
#         plt.sca(ax)
#         plt.imshow(anal_data[expr_param].T)
#         plt.colorbar()
#         plt.gca().invert_yaxis()
#         ax.set_xticks(np.arange(40)[4::8], np.arange(40)[4::8] * 3 / 40)
#         plt.xlabel(r'$\ln{R_0}$')
#         ax.set_yticks(np.arange(40)[4::8], yticks[expr_param][4::8])
#         plt.ylabel(ylabels[expr_param])
        
#     return fig, axes





# def surface(x, y, res, xlabel, ylabel):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     x = np.arange(40) * 0.075
#     y = np.arange(40) / 40
#     X, Y = np.meshgrid(x, y)
#     Z = np.array(res)
#     ax.plot_surface(X, Y, Z, cmap='rainbow')
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     return fig, ax


# def test(data):
#     import matplotlib.pyplot as plt
#     import seaborn as sns
#     import pandas as pd
#     import numpy as np
    
#     # Assuming your dict looks like:
#     # data = {
#     #     'CountryA': {'none': [...], 's': [...], 'w': [...], 'o': [...], 'swo': [...]},
#     #     'CountryB': {'none': [...], 's': [...], 'w': [...], 'o': [...], 'swo': [...]}
#     # }
    
#     # Convert the nested dict to a DataFrame format suitable for plotting
#     def prepare_data(data_dict):
#         rows = []
#         for country in data_dict:
#             for category in ['none', 's', 'w', 'o', 'swo']:
#                 for value in data_dict[country][category]:
#                     rows.append({
#                         'Country': country,
#                         'Category': category,
#                         'Value': value
#                     })
#         return pd.DataFrame(rows)
    
#     # Convert your data
#     df = prepare_data(data)
    
#     # Set figure size
#     plt.figure(figsize=(15, 8))
    
#     # Create violin plot
#     sns.violinplot(data=df, 
#                    x='Country', 
#                    y='Value', 
#                    hue='Category',
#                    palette='Set2',  # You can change the color palette
#                    split=False)
    
#     # Customize the plot
#     plt.title('Distribution of Values by Country and Category', pad=20)
#     plt.xlabel('Country')
#     plt.ylabel('Value')
    
#     # Rotate x-axis labels if needed
#     plt.xticks(rotation=45)
    
#     # Adjust legend
#     plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    
#     # Adjust layout to prevent label cutoff
#     plt.tight_layout()
    
#     plt.show()

# res_fig2 = get_fig2data(edata)
# res_fig3 = get_fig3data(edata)
# res_fig4 = get_fig4data(edata)
# res_fig5 = get_fig5data(edata)
# res_fig6 = get_fig6data(edata)

# plot_fig2(res_fig2)
# plot_fig3(res_fig3)
# plot_fig4(res_fig4)
# plot_fig5(res_fig5)
# plot_fig6(res_fig6)

# '''