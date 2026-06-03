# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 13:14:13 2025

@author: MIFENG
"""

import re
import numpy as np
from scipy.stats import pearsonr

def get_expr_info(task_name):
    m = re.search(r'(\w+)_\((\w+)\)', task_name)
    if m: return m.group(1), m.group(2)
    
    

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
    elif type_idx == 1: return pearsonr(alloc * populations, ifr_arr * populations)[0]
    elif type_idx == 2: return (pearsonr(alloc * populations, contact_arr * populations)[0] - pearsonr(alloc * populations, ifr_arr * populations)[0]) / 2
    else: return None

def alloc_corr_func(alloc_c, alloc_d, populations):
    return pearsonr(alloc_c * populations, alloc_d * populations)[0]

def calc_eff(vac_avail, vac_volumn, vac_order):
    res = np.zeros(len(vac_order))
    for i in vac_order:
        if vac_avail >= vac_volumn[i]:
            res[i] = vac_volumn[i]
            vac_avail -= res[i]
        else:
            res[i] = vac_avail
            vac_avail -= res[i]
            break
    return res
