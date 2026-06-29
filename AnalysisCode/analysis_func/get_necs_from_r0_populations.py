# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 11:38:13 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools
from .analysis_dependencies import anal_func

data_of_countries = rgd.data_of_countries



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
    acc_types = ['dd']

    task_names = ['necs_from_populations_(param)']
    anal_data = {}
    r0_amount = 40
    param_amount = 40

    for task_name, country, target, acc_type in itertools.product(task_names, countries, targets, acc_types):
        expr_name, expr_param = anal_func.get_expr_info(task_name)
        sheet_name_preppend = f"{task_name}-{basic_params.country_abbr[country]}_{target}_{acc_type}"
        country_data = data_of_countries[country]
        anti_target = 'd' if target == 'c' else 'c'
        val_types = ['max', 'min', 'anti_min', 'no_vac', 'necs', 'cost']
        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = []

        for r0_idx, param_idx in itertools.product(range(r0_amount), range(param_amount)):
            ifrs = country_data['ifrs']
            age_dist = make_age_dist(param_idx, 40, 16, 0.75)
            pop_coef = age_dist if target == 'c' else age_dist * ifrs
            if param_idx == 0:
                for val_type in val_types:
                    anal_data[f'{sheet_name_preppend}_{val_type}'].append([])

            file_idx = r0_idx * param_amount + param_idx
            dist_data = expr_data[task_name][file_idx]['dist']
            append_name = f'{{{expr_param}_{basic_params.country_abbr[country]}_{param_idx}}}'
            max_val = dist_data[f"max_{target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            min_val = dist_data[f"min_{target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            anti_min_val = dist_data[f"min_{anti_target}_{acc_type}_{append_name}"].to_numpy() @ pop_coef
            no_vac_val = dist_data[f"no_vac_{acc_type}_{append_name}"].to_numpy() @ pop_coef

            anal_data[f'{sheet_name_preppend}_max'][-1].append(max_val)
            anal_data[f'{sheet_name_preppend}_min'][-1].append(min_val)
            anal_data[f'{sheet_name_preppend}_necs'][-1].append(max_val - min_val)
            anal_data[f'{sheet_name_preppend}_anti_min'][-1].append(anti_min_val)
            anal_data[f'{sheet_name_preppend}_no_vac'][-1].append(no_vac_val)
            anal_data[f'{sheet_name_preppend}_cost'][-1].append((anti_min_val - min_val) / (no_vac_val - min_val))

        for val_type in val_types:
            anal_data[f'{sheet_name_preppend}_{val_type}'] = np.array(anal_data[f'{sheet_name_preppend}_{val_type}'])
    return anal_data
