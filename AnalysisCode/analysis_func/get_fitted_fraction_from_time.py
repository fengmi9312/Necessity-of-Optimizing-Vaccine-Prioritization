# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:34:29 2025

@author: fengm
"""


from Dependencies.CodeDependencies import basic_params
from .analysis_dependencies import required_generated_data as rgd
import itertools
import numpy as np

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea'][:1]
    expr_name = 'param_from_country'
    anal_data = {'real_data': {}, 'fitted_data': {}, 'fitted_period': {}}
    for country in x_countries:
        expr_param = country
        task_name = f'{expr_name}_({expr_param})'
        fitted_data_tmp = []
        anal_data['real_data'][f'{country}_data'] = data_of_countries[country]['confirmed'][:90] / data_of_countries[country]['total_population']
        anal_data['real_data'][f'{country}_time'] = np.arange(90)
        t_arr = np.arange(90 * basic_params.day_div) / basic_params.day_div
        for file_idx, param_idx in itertools.product(range(40), range(25)):
            param_data = expr_data[task_name][file_idx]['transmission_params']
            a, b, c, d = param_data.loc['a', f'params_{{none_{param_idx}}}'], param_data.loc['b', f'params_{{none_{param_idx}}}'], \
                          param_data.loc['c', f'params_{{none_{param_idx}}}'], param_data.loc['d', f'params_{{none_{param_idx}}}']
            fitted_data_tmp.append(a * np.exp(b * (t_arr - c)) + d)
        fitted_data_tmp = np.array(fitted_data_tmp)
        anal_data['fitted_data'][f'{country}_time'] = t_arr
        anal_data['fitted_data'][f'{country}_mean'] = fitted_data_tmp.mean(axis = 0)
        anal_data['fitted_data'][f'{country}_upper'] = np.percentile(fitted_data_tmp, 97.5, axis = 0)
        anal_data['fitted_data'][f'{country}_lower'] = np.percentile(fitted_data_tmp, 2.5, axis = 0)
        best_left = int(expr_data[task_name][0]['transmission_params'].loc['best_left', 'params_{none_0}'])
        best_right = int(expr_data[task_name][0]['transmission_params'].loc['best_right', 'params_{none_0}'])
        anal_data['fitted_period'][country] = [best_left, best_right]
    return anal_data