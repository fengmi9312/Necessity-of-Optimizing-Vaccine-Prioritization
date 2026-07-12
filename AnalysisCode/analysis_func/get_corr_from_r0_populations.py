# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 11:34:32 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func
from copy import deepcopy
from scipy.stats import pearsonr


def make_age_dist(
    idx: int,
    n: int,
    n_group: int,
    sigma_rel: float = 0.5,
) -> np.ndarray:
    """
    Generate an age distribution.

    idx = 0      -> concentrated in young age groups
    idx = n - 1  -> concentrated in old age groups

    sigma_rel controls relative spread on [0, 1].
    """
    if not 0 <= idx < n:
        raise ValueError("idx must be in range(n)")
    if n <= 1:
        raise ValueError("n must be greater than 1")
    if n_group <= 1:
        raise ValueError("n_group must be greater than 1")
    if sigma_rel <= 0:
        raise ValueError("sigma_rel must be positive")

    age_pos = np.linspace(0, 1, n_group)
    center = idx / (n - 1)

    weights = np.exp(-0.5 * ((age_pos - center) / sigma_rel) ** 2)
    age_dist = weights / weights.sum()

    return age_dist


def analyze(expr_data):
    targets = ['c', 'd']
    countries = ['United States']
    anal_data = {}
    task_names = ['necs_from_populations_(param)']
    r0_amount = 40
    param_amount = 40

    for country in countries:
        calc_params = deepcopy(basic_params.calc_params)
        calc_params.update({key: rgd.data_of_countries[country][key] for key in ['ifrs', 'ylls']})
        calc_params['contacts'] = np.sum([rgd.data_of_countries[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis=0)

        for task_name, param_idx, target in itertools.product(task_names, range(param_amount), targets):
            expr_name, expr_param = anal_func.get_expr_info(task_name)
            direct_effects_task_name = 'direct_effects_from_populations_(param)'
            append_name = f'dd_{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            sheet_name = f'{task_name}_{target}_{param_idx}_{basic_params.country_abbr[country]}'
            anal_data[sheet_name] = {'optimal_ind': [], 'optimal_dir': [], 'worst_ind': [], 'worst_dir': [], 'effect_corr': [], 'min_max_corr': [], 'optimal_indx': [], 'optimal_dirx': [], 'worst_indx': [], 'worst_dirx': [], 'effect_corrx': []}

            if target == 'c':
                sheet_name_x = f'{task_name}_{param_idx}_{basic_params.country_abbr[country]}'
                anal_data[sheet_name_x] = {'alloc_corr': []}

            vac_avail = 0.3
            age_dist = make_age_dist(param_idx, 40, 16, 0.75)
            for r0_idx in range(r0_amount):
                file_idx = r0_idx * param_amount + param_idx
                ifrs = calc_params['ifrs']
                coef_target = {'c': age_dist, 'd': age_dist * ifrs}
                alloc_data = expr_data[task_name][file_idx]['alloc']
                alloc_optimal = alloc_data[f'min_{target}_{append_name}'].to_numpy()
                alloc_worst = alloc_data[f'max_{target}_{append_name}'].to_numpy()
                contact_arr = calc_params['contacts'].sum(axis=1)
                direct_effects_coef = expr_data[direct_effects_task_name][r0_idx][f'{basic_params.country_abbr[country]}_{r0_idx}'][str(param_idx)]

                anal_data[sheet_name]['effect_corrx'].append(anal_func.cosine_similarity(direct_effects_coef * coef_target[target], age_dist * contact_arr))
                anal_data[sheet_name]['optimal_indx'].append(anal_func.cosine_similarity(alloc_optimal * age_dist, contact_arr * age_dist))
                anal_data[sheet_name]['optimal_dirx'].append(anal_func.cosine_similarity(alloc_optimal * age_dist, direct_effects_coef * coef_target[target]))
                anal_data[sheet_name]['worst_indx'].append(anal_func.cosine_similarity(alloc_worst * age_dist, contact_arr * age_dist))
                anal_data[sheet_name]['worst_dirx'].append(anal_func.cosine_similarity(alloc_worst * age_dist, direct_effects_coef * coef_target[target]))

                s_vol = expr_data[direct_effects_task_name][r0_idx][f's_{basic_params.country_abbr[country]}_{r0_idx}'][str(param_idx)].to_numpy() * age_dist
                contact_eff = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-contact_arr)) / age_dist
                direct_effects_eff = anal_func.calc_eff(vac_avail, s_vol, np.argsort(-direct_effects_coef)) / age_dist

                anal_data[sheet_name]['effect_corr'].append(anal_func.cosine_similarity(direct_effects_eff * coef_target[target], age_dist * contact_eff))
                anal_data[sheet_name]['optimal_ind'].append(anal_func.cosine_similarity(alloc_optimal * age_dist, contact_eff * age_dist))
                anal_data[sheet_name]['optimal_dir'].append(anal_func.cosine_similarity(alloc_optimal * age_dist, direct_effects_eff * coef_target[target]))
                anal_data[sheet_name]['worst_ind'].append(anal_func.cosine_similarity(alloc_worst * age_dist, contact_eff * age_dist))
                anal_data[sheet_name]['worst_dir'].append(anal_func.cosine_similarity(alloc_worst * age_dist, direct_effects_eff * coef_target[target]))

                anal_data[sheet_name]['min_max_corr'].append(anal_func.cosine_similarity(alloc_optimal * age_dist, alloc_worst * age_dist))
                if target == 'c':
                    anal_data[sheet_name_x]['alloc_corr'].append(pearsonr(alloc_data[f'min_c_{append_name}'].to_numpy() * age_dist, alloc_data[f'min_d_{append_name}'].to_numpy() * age_dist)[0])
    return anal_data
