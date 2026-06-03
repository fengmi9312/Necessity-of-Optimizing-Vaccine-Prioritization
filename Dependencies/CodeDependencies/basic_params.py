# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 17:23:44 2024

@author: 20481756
"""

import numpy as np

day_div = 100
step = 1.0 / day_div
i0 = 1e-3
time0 = 0
group_amount = 16
group_div = np.array([1,] * group_amount)
group_amount = len(group_div)
srv_length = 16000
targets = ['c', 'd', 'y']
all_targets = ['s', 'i', 'r', 'c', 'd', 'y', 'v', 'p']
init_cdy = {'c': i0, 'd': 0, 'y': 0}
calc_params = {'i0': np.ones(len(group_div)) * i0, 'step': step, 'time': time0}
countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
beginning = {'United States': 40, 'United Kingdom': 40, 'France': 35, 'Germany': 35, 'Spain': 30, 'Japan': 40, 'Israel': 35, 'Austria': 30, 'Ireland': 40, 'South Korea': 5} 
country_abbr = {'United States': 'us', 'United Kingdom': 'uk', 'France': 'fr', 'Germany': 'de', 'Spain': 'es', 'Japan': 'jp', 'Israel': 'il', 'Austria': 'at', 'Ireland': 'ie', 'South Korea': 'kr'}
empirical_groups = {'under_20': np.arange(0, 4).tolist(), 
                    '20-49': np.arange(4, 10).tolist(), 
                    '20+': np.arange(4, 16).tolist(), 
                    '60+': np.arange(12, 16).tolist(), 
                    'all_ages': np.arange(0, 16).tolist()}   
##########################################################
'''
# model parameters #
params = {'contacts': di.import_contacts('United States of America'), 
          'populations': di.import_populations('United States of America')[0], 
          'ifrs': di.import_ifrs(), 
          'ylls': di.import_ylls('United States of America')}
params_adj = di.rescale_params(params, group_div)
contacts_dir = params_adj['contacts']['home'] + params_adj['contacts']['school'] \
             + params_adj['contacts']['work'] + params_adj['contacts']['other_locations']
contacts = contacts_dir + contacts_dir.T
calc_params = {'i0': np.ones(len(group_div)) * i0, 
               'populations': params_adj['populations'], 'contacts': contacts, 
               'ifrs': params_adj['ifrs'], 'ylls': params_adj['ylls'], 
               'k': 1, 'srv_inf': None, 'srv_rem': None,
               'eta': eta, 'step': step, 'time': time0}
##########################################################


beta_funcs = {'Weibull': func.get_beta_from_weibull, 
              'Gamma': func.get_beta_from_gamma, 
              'Lognormal': func.get_beta_from_lognormal}
srv_funcs =  {'Weibull': func.srv_weibull, 
              'Gamma': func.srv_gamma, 
              'Lognormal': func.srv_lognormal}
param_funcs = {'Weibull': lambda _val_pow: np.e ** (_val_pow * 0.05),
               'Gamma': lambda _val_pow: np.e ** (_val_pow * 0.1), 
               'Lognormal': lambda _val_pow: _val_pow * 0.04}
mean_funcs = {'Weibull': func.get_mean_from_weibull,
              'Gamma': func.get_mean_from_gamma, 
              'Lognormal': func.get_mean_from_lognormal}
pow_list = {'Weibull': np.arange(0, 33, 4), 
             'Gamma': np.arange(0, 33, 4), 
             'Lognormal': np.arange(4, 37, 4), }
func_mean_list = [('Weibull', 1.5, 3.5), ('Weibull', 2, 3), ('Weibull', 2.5, 2.5), 
                       ('Gamma', 2, 3), ('Lognormal', 2, 3), ]
mean_gen_funcs = {'Weibull': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                  func.get_mean_from_cum(_alpha_inf, _beta_inf, _alpha_rem, _beta_rem),
                  'Gamma': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                  func.get_mean_from_srv(func.get_gen_srv(func.srv_gamma(_alpha_inf, _beta_rem, srv_length, step), 
                  func.srv_gamma(_alpha_rem, _beta_rem, srv_length, step), step), step), 
                  'Lognormal': lambda _alpha_inf, _beta_inf, _alpha_rem, _beta_rem: 
                  func.get_mean_from_srv(func.get_gen_srv(func.srv_lognormal(_alpha_inf, _beta_rem, srv_length, step), 
                  func.srv_lognormal(_alpha_rem, _beta_rem, srv_length, step), step), step)}
pow_special =  {'Weibull': [(-8, -8), (24, 24), (-8, 24), (24, -8), (8, 8), (4, 4), (12, 12), (4, 12), (12, 4)],
            'Gamma': [(-8, -8), (24, 24), (-8, 24), (24, -8), (8, 8), (4, 4), (12, 12), (4, 12), (12, 4)],
            'Lognormal': [(4, 36), (36, 4), (4, 4), (36, 36), (20, 20), (16, 16), (24, 24), (16, 24), (24, 16)],}


'''





