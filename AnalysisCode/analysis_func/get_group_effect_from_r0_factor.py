# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 00:05:56 2026

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import numpy as np
import itertools

data_of_countries = rgd.data_of_countries

import numpy as np

def pielou_gini(v, use_abs=True, eps=0.0):
    x = np.asarray(v, dtype=float)
    if use_abs:
        x = np.abs(x)
    if eps:
        x = x + eps

    s = x.sum()
    n = x.size
    if n == 0:
        return {"pielou": np.nan, "gini": np.nan, "H": np.nan, "n_eff": np.nan}
    if s <= 0:
        # 全零（或非正）向量：定义为“完全均匀/不可区分”
        return {"pielou": 1.0, "gini": 0.0, "H": 0.0, "n_eff": 1.0}

    # ---- Pielou ----
    p = x / s
    # 处理 p_i=0 的项：约定 0*log(0)=0
    mask = p > 0
    H = -(p[mask] * np.log(p[mask])).sum()
    J = H / np.log(n) if n > 1 else 1.0
    n_eff = float(np.exp(H))

    # ---- Gini（升序公式，O(n log n)）----
    xs = np.sort(x)
    i = np.arange(1, n + 1, dtype=float)
    gini = (2.0 * (i * xs).sum()) / (n * s) - (n + 1.0) / n

    return {"pielou": float(J), "gini": float(gini), "H": float(H), "n_eff": n_eff}


def analyze(expr_data):
    task_name = 'group_effect_(delay)'
    country_data = data_of_countries['United States']
    anal_data = {}
    anal_data[f"{task_name}-us_c"] = {}
    for r0_idx, param_idx in itertools.product(range(40), range(40)):
        if param_idx == 0: anal_data[f"{task_name}-us_c"][str(r0_idx)] = []
        anal_data[f"{task_name}-us_c"][str(r0_idx)].append(pielou_gini(expr_data[task_name][0][f'us_{r0_idx}_c'][str(param_idx)] / country_data['populations'])["gini"])
    anal_data['example'] = {}
    for i in ['low', 'mid', 'high']:
        anal_data['example'][i] = expr_data[task_name][0][f'us_{i}_c']['res'] / country_data['populations']
    return anal_data
