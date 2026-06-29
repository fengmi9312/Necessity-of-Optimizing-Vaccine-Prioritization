# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:36:35 2024

@author: 20481756
"""
import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies'))

import numpy as np
import pandas as pd
from .elements import simu_once
from FrameDependencies.data_loader import load_all_data
from CodeDependencies import func
from CodeDependencies import basic_params
from copy import deepcopy
from FrameDependencies import cache_generator

import scipy.stats as stats


def get_lognormal_sample(central_value, ci_lower, ci_upper, sample_size, confidence = 0.95):
    alpha = 1 - confidence
    z_lower = stats.norm.ppf(alpha / 2)  # Z-score for 2.5th percentile
    z_upper = stats.norm.ppf(1 - alpha / 2)  # Z-score for 97.5th percentile
    sigma = (np.log(ci_upper) - np.log(ci_lower)) / (z_upper - z_lower)
    mu = np.log(central_value)
    return np.random.lognormal(mean=mu, sigma=sigma, size=sample_size)


def execute(expt_param, file_idx):
    pos_idx_dict = {'s': 1, 'w': 2, 'o': 3, 'swo': [1,2,3]}
    n_samples = 25
    np.random.seed(file_idx * n_samples)
    calc_params = deepcopy(basic_params.calc_params)
    srv_func = func.srv_weibull
    country = expt_param
    country_data = load_all_data([country], basic_params.group_div)
    mean_g, std_g = func.fit_g(country_data[country]['confirmed'][:90] / country_data[country]['total_population'], basic_params.beginning[country])
    g_samples = np.random.normal(mean_g, std_g, n_samples)
    mean_alpha, ci_lower_alpha, ci_upper_alpha = 2.826, 1.75, 4.7
    mean_beta, ci_lower_beta, ci_upper_beta = 5.665, 4.7, 6.9
    alpha_samples = get_lognormal_sample(mean_alpha, ci_lower_alpha, ci_upper_alpha, n_samples)
    beta_samples = get_lognormal_sample(mean_beta, ci_lower_beta, ci_upper_beta, n_samples)
    for contact_type in ['none', 's', 'w', 'o', 'swo']:
        calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
        contacts_total = np.array([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']])
        if contact_type != 'none': contacts_total[pos_idx_dict[contact_type]] *= 0
        calc_params['contacts'] = np.sum(contacts_total, axis = 0)
        for param_idx, (g, alpha, beta) in enumerate(zip(g_samples, alpha_samples, beta_samples)):
            srv_gen = srv_func(alpha, beta, basic_params.srv_length, basic_params.step)
            calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
            r0 = func.calc_r0(g, alpha, beta)
            param_name = f'{contact_type}_{param_idx}'
            if not cache_generator.check_cache(expt_param, file_idx, param_name):
                print(f'Begin excuting {param_name}')
                single_res = simu_once.simulate(calc_params, imm_params=('delay', 14 * basic_params.day_div), r0 = r0, optm_targets = ['c', 'd'])
                single_res.update({'transmission_params': {'params': pd.Series([r0, g, alpha, beta], index=['r0', 'growth_rate', 'alpha', 'beta'])}})
                cache_generator.add_cache(expt_param, file_idx, param_name, single_res)
    print('Gather Data')
    res = {}
    for contact_type in ['none', 's', 'w', 'o', 'swo']:
        for param_idx, (g, alpha, beta) in enumerate(zip(g_samples, alpha_samples, beta_samples)):
            param_name = f'{contact_type}_{param_idx}'
            single_res = cache_generator.get_cache(expt_param, file_idx, param_name)
            for data_key in single_res.keys():
                if data_key not in res: res[data_key] = {}
                for key, item in single_res[data_key].items():
                    res[data_key][f'{key}_{{{param_name}}}'] = pd.Series(item)
    cache_generator.del_cache(expt_param, file_idx)
    print('Return Data')
    return res













'''


for country in countries:
    a = first_vac_date(country, vac_data)
    b = nth_day(a, 28)
    c = vac_date(country, b, vac_data)
    c_amount = get_vac_c(country, vac_data, confirmed_data)
    print(f"{country}: | vac_date: {a} | c_amount: {c_amount} | vac_end: {b} | vac_amount: {c}")





import matplotlib.pyplot as plt
countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Italy', 'Japan', 'Israel', 'South Korea', 'Singapore', 'Ireland', 'Austria']
country = 'United States'
print(country)
data_len = 1140
params = {'contacts': di.import_contacts(country_name_transform1(country)), 
          'populations': di.import_populations(country_name_transform1(country))[0], 
          'ifrs': di.import_ifrs(),
          'ylls': di.import_ylls(country_name_transform1(country))}
group_amount = 8
group_div = np.array([2,] * group_amount)
params_adj = di.rescale_params(params, group_div)
contacts_dir = params_adj['contacts']['home'] + params_adj['contacts']['school'] \
             + params_adj['contacts']['work'] + params_adj['contacts']['other_locations']
contacts = contacts_dir + contacts_dir.T
calc_params = {'contacts': contacts, 
              'populations': params_adj['populations'], 
              'ifrs': params_adj['ifrs'],
              'ylls': params_adj['ylls'],
              'k': 1}
res = fit_cum_from_data(get_curves(country_name_transform0(country), confirmed_data)[:data_len], total_populations[country], func.srv_weibull, calc_params)
res1 = get_c(res.x, get_curves(country_name_transform0(country), confirmed_data)[:data_len], total_populations[country], func.srv_weibull, calc_params)
plt.plot(get_curves(country_name_transform0(country), confirmed_data)[:data_len]/ total_populations[country])
plt.plot(np.arange(500 - len(res1), 500), res1 )


def fit_gx(country, start_day = 35, end_day = 300, window_size = 100):
    x = np.arange(start_day, end_day)
    y = np.log(get_curves(country, confirmed_data)[start_day:end_day] / di.import_populations(country)[1])
    threshold_r_squared = 0.98  # Define a threshold for R-squared to identify linearity
    best_r_squared = 0
    best_segment = (0, window_size)
    
    # Slide a window over the data and calculate linearity
    for i in range(len(x) - window_size + 1):
        x_segment = x[i:i + window_size]
        y_segment = y[i:i + window_size]
        slope, intercept, r_value, p_value, std_err = linregress(x_segment, y_segment)
        r_squared = r_value**2
        if r_squared > best_r_squared and r_squared > threshold_r_squared:
            best_r_squared = r_squared
            best_segment = (i, i + window_size)
    
    # Extract the best linear segment
    x_best = x[best_segment[0]:best_segment[1]]
    y_best = y[best_segment[0]:best_segment[1]]
    # Perform linear regression on the best segment
    slope, intercept, _, _, std_err = linregress(x_best, y_best)
    
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    plt.title(country)
    plt.sca(axes[0])
    plt.plot(x_best, x_best * slope + intercept, color = 'tab:red')
    plt.plot(x, y, color = 'black')
    plt.sca(axes[1])
    plt.plot(x, get_curves(country, confirmed_data)[start_day:end_day] / di.import_populations(country)[1])
    
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Calculate the critical value from the normal distribution
    z_value = stats.norm.ppf(1 - alpha / 2)  # Z critical value for a normal distribution
    # Calculate the confidence interval for the slope
    lower_bound = slope - z_value * std_err
    upper_bound = slope + z_value * std_err
    return slope, lower_bound, upper_bound



def fit_cum_from_data(confirmed, total_population, srv_func, _calc_params, init_params = [1, 1, 1]):
    for i in range(len(confirmed)):
        if confirmed[i] > 0.001 * total_population: break
    _confirmed_data = confirmed[i:]
    data_len = len(_confirmed_data)
    _calc_params_delta = deepcopy(_calc_params)
    def _loss_func(_params):
        srv_val = srv_func(_params[1], _params[2], data_len, 1)
        _calc_params_delta['k'] = _params[0]
        _calc_params_delta['srv_inf'], _calc_params_delta['srv_rem'] = srv_val, srv_val
        sir_model = sir_delta([_confirmed_data[0] / total_population,] * len(_calc_params['populations']), **_calc_params_delta)
        for i in range(data_len - 1):
            sir_model.spread_once()
        return ((sir_model.get_c_tot() - _confirmed_data / total_population) ** 2).sum() 
            
    return minimize(_loss_func, init_params, method = 'L-BFGS-B', bounds=[(0.1, None), (0.1, 5), (1, 30)])

def get_c(_params, confirmed, total_population, srv_func, _calc_params):
    for i in range(len(confirmed)):
        if confirmed[i] > 0.001 * total_population: break
    _confirmed_data = confirmed[i:]
    data_len = len(_confirmed_data)
    _calc_params_delta = deepcopy(_calc_params)
    _calc_params_delta['k'] = _params[0]
    srv_val = srv_func(_params[1], _params[2], data_len, 1)
    _calc_params_delta['srv_inf'], _calc_params_delta['srv_rem'] = srv_val, srv_val
    sir_model = sir_delta([_confirmed_data[0] / total_population,] * len(_calc_params['populations']), **_calc_params_delta)
    for i in range(data_len - 1):
        sir_model.spread_once()
    return sir_model.get_c_tot()









data_len = 200

countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Singapore', 'Austria']
for country in countries:
    countryx = country_name_curve(country)
    plt.figure()
    country_confirmed, country_deaths, country_recovered = get_curves(countryx, confirmed_data)[:data_len], get_curves(countryx, deaths_data)[:data_len], get_curves(countryx, recovered_data)[:data_len]
    plt.plot(np.log(country_confirmed))
    plt.title(country)
    plt.axvline(40)
    plt.axvline(61)
  























































import matplotlib.pyplot as plt


countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Italy', 'Japan', 'Israel', 'South Korea', 'Singapore', 'Ireland', 'Austria']

for country in countries:
    country = country_name_curve(country)
    plt.figure()
    plt.plot(get_curves(country, deaths_data) / get_curves(country, recovered_data))












































for country in countries:
    a = first_vac_date(country, vac_data)
    b = nth_day(a)
    c = vac_date(country, b, vac_data)
    print(country + ': ' + a + ' | ' + b + ' | ' + str(c))


  

'''


