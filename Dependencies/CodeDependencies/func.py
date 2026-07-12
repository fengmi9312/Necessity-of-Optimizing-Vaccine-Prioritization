# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 21:51:18 2020

@author: Tingting
"""

import numpy as np
import scipy.special as sc
import pandas as pd
from filelock import FileLock
import os

def create_folder(folder_path):
    lock = FileLock(folder_path + '.lock')
    with lock:
        os.makedirs(folder_path, exist_ok=True)
    return None

def export_to_file(data, file_dir):
    with pd.ExcelWriter(file_dir) as writer:
        for key in data.keys():
            pd.DataFrame(data[key]).to_excel(writer, sheet_name = key)


def add_list_to_dict(list_name, d):
    if list_name not in d:
        d[list_name] = []

def calc_equity(alloc):
    sorted_alloc = np.append(0, np.sort(alloc).cumsum())
    equal_sorted_alloc = np.linspace(0, sorted_alloc.max(), len(sorted_alloc)) 
    return (equal_sorted_alloc - sorted_alloc).sum() / equal_sorted_alloc[:-1].sum()

def split_int(x, a):
    tmp = [a] * (x // a)
    sum_tmp = sum(tmp)
    if sum_tmp != x:
        tmp.append(x - sum_tmp)
    return np.array(tmp)

def mulf(mat, vec):
    return 1 - ((1 - vec)[None,:]**mat).prod(axis = 1)

def lambda_eff_weibull(_alpha_inf, _beta_inf, _alpha_rem, _beta_rem):
    return ((_beta_rem/_beta_inf)**_alpha_inf)*(_alpha_inf/_alpha_rem)*sc.gamma(_alpha_inf/_alpha_rem)

def lambda_eff_inc_weibull(_alpha_inf, _beta_inf, _alpha_rem, _beta_rem, _tau):
    return ((_beta_rem / _beta_inf) ** _alpha_inf) * (_alpha_inf / _alpha_rem) \
           * (1 - sc.gammainc(_alpha_inf / _alpha_rem, (_tau / _beta_rem)**_alpha_rem)) \
           * sc.gamma(_alpha_inf / _alpha_rem) / np.exp(-(_tau / _beta_rem) ** _alpha_rem)

def get_mean_from_weibull(alpha, beta):
    return beta * sc.gamma(1 + 1.0 / alpha)


def get_mean_from_gamma(alpha, beta):
    return alpha * beta

def get_mean_from_lognormal(alpha, beta):
    return np.exp((alpha ** 2) / 2 + beta)


def get_beta_from_weibull(alpha, mean_value):
    return mean_value / sc.gamma(1 + 1.0 / alpha)

def get_beta_from_gamma(alpha, mean_value):
    return mean_value / alpha

def get_beta_from_lognormal(alpha, mean_value):
    return np.log(mean_value) - (alpha ** 2) / 2

def get_mean_from_cum(_alpha_inf, _beta_inf, _alpha_rem, _beta_rem):
    return _beta_rem * sc.gamma((_alpha_inf + 1) / _alpha_rem) / sc.gamma(_alpha_inf / _alpha_rem)

def srv_exponent(_lambda, _length, _step):
    _tau = np.arange(_length) * _step
    return np.exp(- _lambda * _tau)

def srv_weibull(_alpha, _beta, _length, _step):
    _tau = np.arange(_length) * _step
    return np.exp(- (_tau / _beta) ** _alpha)

def srv_gamma(_alpha, _beta, _length, _step):
    _tau = np.arange(_length) * _step
    return 1 - sc.gammainc(_alpha, _tau / _beta)

def srv_lognormal(_alpha, _beta, _length, _step):
    _tau = np.arange(1, _length) * _step
    return np.append(1, 0.5 - 0.5 * sc.erf((np.log(_tau) - _beta) / (_alpha * (2 ** 0.5))))

def srv_beta(_alpha, _beta, _length, _step, shift = 0):
    _tau = np.arange(_length) * _step
    _actl_len = (_length - 1) * _step
    return np.append(np.ones(shift), 1 - sc.betainc(_alpha, _beta, _tau / _actl_len))

def srv_delta():
    return np.array([1,0])

def lambda_eff_srv(srv_inf, srv_rem):
    _actl_inf_len, _actl_rem_len = len(srv_inf), len(srv_rem)
    for idx, val in enumerate(srv_inf):
        if val <= 0:
            _actl_inf_len = idx
            break
    for idx, val in enumerate(srv_rem):
        if val <= 0:
            _actl_rem_len = idx
            break
    _cum_len = min(_actl_inf_len - 1, _actl_rem_len)
    _haz_inf = 1 - srv_inf[1:_actl_inf_len] / srv_inf[:_actl_inf_len - 1]
    _srv_rem = srv_rem[:_actl_rem_len]
    _haz_cum = _haz_inf[:_cum_len] * _srv_rem[:_cum_len]
    return np.log(1 / (1 - _haz_cum).prod())

def get_mean_from_srv(srv, step):
    return ((srv[:-1] - srv[1:]) * np.arange(len(srv) - 1)).sum() * step

def get_haz_from_srv(srv):
    actl_len = np.where(srv <= 0)[0][0] if np.any(srv <= 0) else len(srv)
    return np.append(1 - srv[1:actl_len] / srv[:actl_len - 1], np.ones(len(srv) - actl_len))

def get_dist_from_srv(srv):
    return srv[:-1] - srv[1:]

def get_srv_from_haz(haz):
    return np.append(1, (1 - haz).cumprod())

def get_gen_srv(srv_inf, srv_rem, step):
    _actl_inf_len, _actl_rem_len = len(srv_inf), len(srv_rem)
    for idx, val in enumerate(srv_inf):
        if val <= 0:
            _actl_inf_len = idx
            break
    for idx, val in enumerate(srv_rem):
        if val <= 0:
            _actl_rem_len = idx
            break
    _cum_len = min(_actl_inf_len - 1, _actl_rem_len)
    _haz_inf = 1 - srv_inf[1:_actl_inf_len] / srv_inf[:_actl_inf_len - 1]
    _srv_rem = srv_rem[:_actl_rem_len]
    _haz_cum = _haz_inf[:_cum_len] * _srv_rem[:_cum_len]
    _tot_haz = _haz_cum.sum()
    return np.append(1, 1 - _haz_cum.cumsum() / _tot_haz)


def generate_imm_dist(param_type, param, day_div):
    step = 1 / day_div
    if param_type == 'delay':
        if param == 0: return np.array([1,0])
        elif param >= 1 and param <= 3 * day_div: 
            return srv_beta(3, 3, param * 2 + 1, step)
        else: 
            return srv_beta(3, 3, 3 * day_div * 2 + 1, step, shift = param - 3 * day_div)
    elif param_type == 'var':
        alphabeta = 0.25 * 3 / param - 0.5
        return srv_beta(alphabeta, alphabeta, 3 * day_div * 2 + 1, step, shift = (7 - 3) * day_div)
    elif param_type == 'half_domain':
        return srv_beta(3, 3, param * 2 + 1, step) if param != 0 else np.array([1, 0])
    else: return None


def get_head(pos, actl_len):
    tmp_head = pos - actl_len
    if tmp_head < 0:
        return None
    else:
        return tmp_head

def get_tail(pos, actl_len):
    return min(pos + 1, actl_len)

def get_alloc(s_arr, age_populations, vac_avail, group):
    if group is None or len(group) == 0:
        return None
    remaining_vac_group = [gr for gr in np.arange(0,len(age_populations)).tolist() if gr not in group]
    alloc = np.zeros(len(age_populations))
    for i in range(2):
        if i == 0:
            group_tmp = group
        else:
            group_tmp = remaining_vac_group
        if len(group_tmp) > 0:
            remaining_amount = vac_avail - (alloc @ age_populations).sum()
            if s_arr[group_tmp] @ age_populations[group_tmp] == 0:
                proportion = np.zeros(len(group_tmp))
            else:
                proportion = (s_arr[group_tmp] * age_populations[group_tmp]) / (s_arr[group_tmp] @ age_populations[group_tmp])
            alloc[group_tmp] = proportion * min(remaining_amount, s_arr[group_tmp] @ age_populations[group_tmp]) / age_populations[group_tmp]
    return alloc

def get_mixed_steady_state(r0, init_i = 0, init_r = 0, c_tol = 1e-6):
    c = 1
    while True:
        c_tmp = 1 - (1 - init_i - init_r) * np.exp(- r0 * (c - init_r))
        if abs(c_tmp - c) < abs(c) * c_tol: break
        else: c = c_tmp
    return c_tmp

def get_r0_from_mixed_steady(steady_c, init_i = 0, init_r = 0):
    return np.log((1 - init_i - init_r) / (1 - steady_c)) / (steady_c - init_r)

def get_steady_state(_k, _populations, _contacts, _lam, _i = 0, _r = 0, ctol = 1e-6):
    group_amount = len(_populations)
    if type(_lam) == np.ndarray:
        rlam = _lam[None, :]
    else:
        rlam = _lam
    
    c_tmp = np.ones(group_amount)
    _totmat_lam = _contacts * _populations[None, :] * _k * rlam
    while True:
        c_tmp_tmp = 1 - (1 - _r - _i) * np.exp(-_totmat_lam@(c_tmp  - _r))
        if np.all(abs(c_tmp_tmp-c_tmp) <= abs(c_tmp) * ctol):
            break
        else:
            c_tmp = c_tmp_tmp
    return c_tmp_tmp

def find_g(s_inf, s_rem, _r0, _step):
    from scipy.optimize import minimize, Bounds
    actl_inf_len = np.where(s_inf <= 0)[0][0] if np.any(s_inf <= 0) else len(s_inf)
    actl_rem_len = np.where(s_rem <= 0)[0][0] if np.any(s_rem <= 0) else len(s_rem)
    cum_len = min(actl_inf_len - 1, actl_rem_len)
    h_inf = 1 - s_inf[1:actl_inf_len] / s_inf[:actl_inf_len - 1]
    h_cum = h_inf[:cum_len] * s_rem[:cum_len]
    lam = np.log(1 / (1 - h_cum).prod())
    def _loss(_x):
        return (1 / _r0 - (np.exp(- _x[0] * np.arange(cum_len) * _step) * h_cum).sum() / lam) ** 2
    while True:
        res =  minimize(_loss, [0,], bounds = Bounds(-np.ones(1) * np.inf, np.ones(1) * np.inf), method = 'SLSQP', tol = 1e-16)
        if res.success: break
    return res.x[0]

def find_g_from_gen(s_gen, _r0, _step):
    from scipy.optimize import minimize, Bounds
    cum_len = np.where(s_gen <= 0)[0][0] if np.any(s_gen <= 0) else len(s_gen) - 1
    h_cum = s_gen[:cum_len] - s_gen[1:cum_len + 1]
    def _loss(_x):
        return (1 / _r0 - (np.exp(- _x[0] * np.arange(cum_len) * _step) * h_cum[:cum_len]).sum()) ** 2
    while True:
        res =  minimize(_loss, [0,], bounds = Bounds(-np.ones(1) * np.inf, np.ones(1) * np.inf), method = 'SLSQP', tol = 1e-16)
        if res.success: break
    return res.x[0]  


def calc_r0_from_g(s_inf, s_rem, _g, _step):
    actl_inf_len = np.where(s_inf <= 0)[0][0] if np.any(s_inf <= 0) else len(s_inf)
    actl_rem_len = np.where(s_rem <= 0)[0][0] if np.any(s_rem <= 0) else len(s_rem)
    cum_len = min(actl_inf_len - 1, actl_rem_len)
    h_inf = 1 - s_inf[1:actl_inf_len] / s_inf[:actl_inf_len - 1]
    h_cum = h_inf[:cum_len] * s_rem[:cum_len]
    return  np.log(1 / (1 - h_cum).prod()) / (np.exp(- _g * np.arange(cum_len) * _step) * h_cum).sum()

        
def get_k_from_steady(_steady, _populations, _contacts, _lam, _i = 0, _r = 0, ctol = 1e-6, ktol = 1e-6):
    x0 = 1.0 / (_lam * np.linalg.eig(_contacts * _populations[None, :])[0].max())
    while True:
        res = binary_search(lambda x: get_steady_state(x, _populations, _contacts, _lam, _i, _r, ctol) @ _populations, _steady, x0, 2 * x0, lbound = 0, tol = ktol)
        if res['success']:
           return res['x']

def binary_search(func, y, xl, xr, lbound = -np.inf, rbound = np.inf, tol = 1e-6):
    def overbound(_x):
            if _x < lbound:
                return -1
            elif _x > rbound:
                return 1
            else:
                return 0    
            
    res = {'message': None, 'fun': None, 'x': None, 'success': False}
    if xl >= xr or lbound >= rbound or overbound(xl) or overbound(xr):
        res['message'] = 'the parameters are illegal.'
        return res
    yl = func(xl)
    yr = func(xr)
    if yl == yr:
        res['message'] = 'func(xl) is equal to func(xr).'
        return res
    elif yl < yr:
        xlower  = xl
        xhigher = xr
        ylower = yl
        yhigher = yr
    else:
        xlower  = xr
        xhigher = xl
        ylower = yr
        yhigher = yl
    overboundmark = False
    while True:
        if overboundmark and (y < ylower or y > yhigher):
            res['message'] = 'beyound bounds.'
            return res
        if y < ylower:
            delta_x = xlower - xhigher
            xhigher = xlower
            xlower = xlower + 2 * delta_x
            if overbound(xlower) == 1:
                xlower = rbound
                overboundmark = True
            elif overbound(xlower) == -1:
                xlower = lbound
                overboundmark = True
            else:
                pass
        elif y > yhigher:
            delta_x = xhigher - xlower
            xlower = xhigher
            xhigher = xhigher + 2 * delta_x
            if overbound(xhigher) == 1:
                xhigher = rbound
                overboundmark = True
            elif overbound(xhigher) == -1:
                xhigher = lbound
                overboundmark = True
            else:
                pass
        else:
            break
        ylower = func(xlower)
        yhigher = func(xhigher)   
    if abs((ylower - y) / y) < tol:
        res['message'] = 'the x has been found'
        res['success'] = True
        res['fun'] = ylower
        res['x'] = xlower
        return res
    if abs((yhigher - y) / y) < tol:
        res['message'] = 'the x has been found'
        res['success'] = True
        res['fun'] = yhigher
        res['x'] = xhigher
        return res
    while True:
        ytmp = func((xlower + xhigher) / 2)
        if abs((ytmp - y) / y) < tol:
            res['message'] = 'the x has been found'
            res['success'] = True
            res['fun'] = ytmp
            res['x'] = (xlower + xhigher) / 2
            return res
        else:
            if ytmp > y:
                xhigher = (xlower + xhigher) / 2
            else:
                xlower = (xlower + xhigher) / 2
        



def calc_r0(g, alpha_gen, beta_gen, dist_length = 10000, step = 0.01):
    res = 0
    for i in range(dist_length):
        res += np.exp(-g * i * step) * (np.exp(- (i * step / beta_gen) ** alpha_gen) - np.exp(- ((i + 1) * step / beta_gen) ** alpha_gen))
    return 1 / res


from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from scipy.stats import norm
def fit_g(confirmed, beginning_day, window_size = 30, get_all_params = False):
    def exponential_growth(t, a, b, c, d):
        return a * np.exp(b * (t - c)) + d
    
    days = np.arange(len(confirmed))
    best_r2 = -np.inf  # Initialize best R² value
    best_segment = None  # Initialize best segment
    
    # Sliding window to evaluate segments
    for start in range(beginning_day, len(confirmed) - window_size + 1):
        end = start + window_size
        days_segment = days[start:end]
        cases_segment = confirmed[start:end]
        
        # Fit the exponential growth model to the selected segment
        try:
            params, cov_matrix = curve_fit(exponential_growth, days_segment, cases_segment, p0=[1, 0.2, 0, 1], bounds = ([-np.inf, 0.05, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf]))
            a, b, c, d = params
            cases_fit = exponential_growth(days_segment, a, b, c, d)
            
            # Calculate R² value
            r2 = r2_score(cases_segment, cases_fit)
            
            # Update best segment if current R² is better
            if r2 > best_r2:
                best_r2 = r2
                best_segment = (start, end)
                best_params = params
                best_cov_matrix = cov_matrix
        except RuntimeError:
            # Ignore segments where the fitting fails
            continue
    
    # Extract the best segment and fit parameters
    start, end = best_segment
    a, b, c, d = best_params
    days_best_segment = days[start:end]
    confirmed_best_segment = confirmed[start:end]
    confirmed_best_fit = exponential_growth(days_best_segment, a, b, c, d)
    
    # Calculate standard errors of the parameters
    perr = np.sqrt(np.diag(best_cov_matrix))
    '''
    # Calculate the 95% confidence intervals for the parameters using the normal distribution
    alpha = 0.05  # 95% confidence level
    zval = norm.ppf(1.0 - alpha / 2.0)  # z-value for the confidence level
    
    ci = zval * perr
    '''
    if get_all_params: return best_params, perr, best_segment
    else: return b, perr[1]































        
        
    