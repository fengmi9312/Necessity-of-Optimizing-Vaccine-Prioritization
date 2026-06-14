# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:42:01 2024

@author: fengm
"""


info = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
        'necs_from_param_init': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
        'necs_line_from_param': {'delay_8': 40, 'delay_10': 40, 'delay_16': 40, 'delay_0': 40, 'delay_13': 40, 'delay_26': 40, 'delay_39': 40},
        'necs_line_from_param_init': {'delay_0': 40},
        'necs_from_contact': {'0': 40, '1': 40, '2': 40, '3': 40, '4': 40, '5': 40, '6': 40, '7': 40, '8': 40, '9': 40, '10': 40, '11': 40, '12': 40, '13': 40},
        'necs_from_population': {'peak': 40, 'equity': 40},
        'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
        'necs_from_fatality_by_contact': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
        'necs_from_param_by_eta': {'delay': 40},
        'necs_from_fatality_init': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
        'necs_line_from_fatality': {'coef_alpha_0_0': 40, 'coef_alpha_0_13': 40, 'coef_alpha_0_26': 40, 'coef_alpha_0_39': 40, 'coef_alpha_1_0': 40, 'coef_alpha_1_13': 40, 'coef_alpha_1_26': 40, 'coef_alpha_1_39': 40, 
                                    'coef_beta_0_0': 40, 'coef_beta_0_13': 40, 'coef_beta_0_26': 40, 'coef_beta_0_39': 40,'coef_beta_1_0': 40,  'coef_beta_1_13': 40, 'coef_beta_1_26': 40, 'coef_beta_1_39': 40},
        'necs_from_growth_gen': {'weibull_0': 9, 'weibull_1': 9, 'weibull_2': 9, 'gamma_0': 9, 'gamma_1': 9, 'gamma_2': 9, 'lognormal_0': 9, 'lognormal_1': 9, 'lognormal_2': 9},
        'necs_from_growth_s': {'weibull_0': 40, 'weibull_1': 40, 'weibull_2': 40, 'gamma_0': 40, 'gamma_1': 40, 'gamma_2': 40, 'lognormal_0': 40, 'lognormal_1': 40, 'lognormal_2': 40},
        'necs_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'necs_from_country_70': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'necs_from_country_35': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'param_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'necs_from_example': {'delay': 12},
        'acc_comp': {'var': 20, 'delay': 20, 'half_domain': 20},
        'necs_space': {'param': 2, 'delay_0': 2, 'delay_7': 2}, 'optm_transition': {'param': 41}, 'transition_direct_effects': {'param': 1}, 'contact_before_protect': {'param': 1}, 
        'necs_line_from_add': {'param': 20}, 'necs_line_from_add_init': {'param': 20},
        'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
        'direct_effects_line_from_param': {'delay_8': 1, 'delay_10': 1, 'delay_13': 1, 'delay_26': 1, 'coef_beta_1_0': 1, 'coef_beta_1_13': 1, 'coef_beta_1_26': 1, 'coef_beta_1_39': 1},
        'direct_effects_from_contact': {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, '10': 1, '11': 1, '12': 1, '13': 1}, 
        'group_effect': {'delay': 1}, 
        'necs_from_time_course': {'param': 1600}, 'necs_from_time_coursex': {'param': 1600},
        'direct_effects_from_time_course': {'param': 40}}       

def check_info(func_name, task_param):
    if func_name not in info:
        return False
    else:
        if task_param not in info[func_name]: return False
        else: return True
        
def get_file_amount(func_name, task_param):
    return info[func_name][task_param]
