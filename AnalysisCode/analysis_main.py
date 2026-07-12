# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:59:25 2025

@author: MIFENG
"""

if __name__ != "__main__":
    raise ImportError("This module cannot be imported.")
    
import os
import sys
code_root, folder_level = os.path.dirname(os.path.abspath(__file__)), 1
for _ in range(folder_level): code_root = os.path.dirname(code_root)
sys.path.append(code_root)


import FigureCode.figure_func as ff
import AnalysisCode.analysis_func as af
from Dependencies.FrameDependencies import load_experimental_data, file_writer
import importlib
import matplotlib.pyplot as plt

expr_data = {}
anal_data = {}   
task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
        'necs_line_from_param': {'delay_8': 40, 'delay_10': 40, 'delay_0': 40, 'delay_13': 40, 'delay_26': 40, 'delay_39': 40},
        'necs_from_contact': {'0': 40, '1': 40, '2': 40, '3': 40, '4': 40, '5': 40, '6': 40, '7': 40, '8': 40, '9': 40, '10': 40, '11': 40, '12': 40, '13': 40},
        'necs_from_population': {'peak': 40, 'equity': 40},
        'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
        'necs_from_fatality_init': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
        'necs_line_from_fatality': {'coef_alpha_0_0': 40, 'coef_alpha_0_13': 40, 'coef_alpha_0_26': 40, 'coef_alpha_0_39': 40, 'coef_alpha_1_0': 40, 'coef_alpha_1_13': 40, 'coef_alpha_1_26': 40, 'coef_alpha_1_39': 40, 
                                    'coef_beta_0_0': 40, 'coef_beta_0_13': 40, 'coef_beta_0_26': 40, 'coef_beta_0_39': 40,'coef_beta_1_0': 40,  'coef_beta_1_13': 40, 'coef_beta_1_26': 40, 'coef_beta_1_39': 40},
        'necs_from_growth_gen': {'weibull_0': 9, 'weibull_1': 9, 'weibull_2': 9, 'gamma_0': 9, 'gamma_1': 9, 'gamma_2': 9, 'lognormal_0': 9, 'lognormal_1': 9, 'lognormal_2': 9},
        'necs_from_growth_s': {'weibull_0': 40, 'weibull_1': 40, 'weibull_2': 40, 'gamma_0': 40, 'gamma_1': 40, 'gamma_2': 40, 'lognormal_0': 40, 'lognormal_1': 40, 'lognormal_2': 40},
        'necs_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'param_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, 
        'necs_from_example': {'delay': 11},
        'necs_space': {'param': 2}, 'optm_transition': {'param': 41}, 'transition_direct_effects': {'param': 1}, 'contact_before_protect': {'param': 1}, 
        'necs_line_from_add': {'param': 20},
        'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
        'direct_effects_line_from_param': {'delay_8': 1, 'delay_10': 1, 'delay_13': 1, 'delay_26': 1, 'coef_beta_1_0': 1, 'coef_beta_1_13': 1, 'coef_beta_1_26': 1, 'coef_beta_1_39': 1}}       

task_dict = {'necs_from_country_35': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40},
             'necs_from_country_70': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}}
task_dict.update({'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1}})
xxx


task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
             'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
             'necs_from_contact': {'1': 40, '2': 40, '13': 40},
             'necs_line_from_param': {'delay_8': 40, 'delay_10': 40, 'delay_13': 40, 'delay_26': 40},
             'necs_line_from_fatality': {'coef_beta_1_0': 40,  'coef_beta_1_13': 40, 'coef_beta_1_26': 40, 'coef_beta_1_39': 40},
             'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
             'direct_effects_line_from_param': {'delay_8': 1, 'delay_10': 1, 'delay_13': 1, 'delay_26': 1, 'coef_beta_1_0': 1, 'coef_beta_1_13': 1, 'coef_beta_1_26': 1, 'coef_beta_1_39': 1},
             'necs_from_param_by_eta':{'delay': 40}, 'necs_from_fatality_by_contact': {'coef_beta_1': 40}}
task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
             'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
             'necs_from_contact': {'1': 40, '2': 40, '13': 40},
             'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
             'direct_effects_from_contact': {'1': 1, '2': 1, '3': 1, '13': 1},
             'direct_effects_line_from_param': {'delay_8': 1, 'delay_10': 1, 'delay_13': 1, 'delay_26': 1, 'coef_beta_1_0': 1, 'coef_beta_1_13': 1, 'coef_beta_1_26': 1, 'coef_beta_1_39': 1},}


task_dict = {'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
             'direct_effects_from_contact': {'1': 1, '2': 1, '13': 1},
             'necs_from_param': {'delay': 40, 'c_perct': 40, 'vac_avail': 40, 'vac_eff': 40, 'vac_dur': 40}, 
             'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40}, 'necs_from_contact': {'1': 40, '2': 40, '13': 40}}
# task_dict = {'necs_from_example': {'delay': 6}, 'param_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40}, }
task_dict = {'direct_effects_from_time_course': {'param': 40}, 'necs_from_time_course_fixd': {'param': 1600}, 'necs_from_time_course': {'param': 1600}, 
             'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
             'necs_from_param_by_eta':{'delay': 40}, 'necs_from_fatality_by_contact': {'coef_beta_1': 40}}


task_dict = {'necs_from_param': {'delay': 40, 'vac_eff': 40, 'vac_avail': 40, 'c_perct': 40, 'vac_dur': 40},
             'necs_from_fatality': {'coef_alpha_0': 40, 'coef_alpha_1': 40, 'coef_beta_0': 40, 'coef_beta_1': 40},
             'necs_from_contact': {'1': 40, '2': 40, '13': 40},
             'direct_effects_from_param': {'delay': 1, 'vac_eff': 1, 'vac_avail': 1, 'c_perct': 1, 'coef_alpha_0': 1, 'coef_alpha_1': 1, 'coef_beta_0': 1, 'coef_beta_1': 1},
             'direct_effects_from_contact': {'1': 1, '2': 1, '3': 1, '13': 1},}

task_dict = {'direct_effects_from_time_course': {'param': 40}, 'necs_from_time_course': {'param': 1600},
             'necs_from_time_course_fixd': {'param': 1600},
             'direct_effects_from_populations': {'param': 40}, 'necs_from_populations': {'param': 1600},
             'necs_from_country': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40},
             'necs_from_country_35': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40},
             'necs_from_country_70': {'United States': 40, 'United Kingdom': 40, 'France': 40, 'Germany': 40, 'Spain': 40, 'Japan': 40, 'Israel': 40, 'Austria': 40, 'Ireland': 40, 'South Korea': 40},}

task_dict = {'direct_effects_from_time_course_with_vac_avail': {'param': 40}, 'necs_from_time_course_fixd_with_vac_avail': {'param': 1600}}
for task_key, task_item in task_dict.items():
    expr_data.update(load_experimental_data.load_certain_edata({task_key: task_item}))

importlib.reload(af)
anal_list = ['alloc_from_age_with_example', 'alloc_from_r0_factor', 'bnf_from_example', 'corr_from_r0_factor', 
             'corr_line_from_r0', 'dist_diff_from_r0', 'fitted_fraction_from_time', 'fraction_from_time_with_example', 
             'necs_from_country', 'necs_from_growth', 'necs_from_growth_s', 'necs_from_r0_factor', 'necs_line_from_r0', 'param_from_country', 'prdt_from_corr', 'prdt_from_xycoef']

anal_list = ['necs_from_r0_populations', 'corr_from_r0_populations', 'necs_from_country', 'necs_from_country_35', 'necs_from_country_70', 
             'necs_from_r0_time_course', 'corr_from_r0_time_course']
anal_list = ['necs_from_r0_time_course_with_vac_avail', 'corr_from_r0_time_course_with_vac_avail']
for anal_name in anal_list:
    anal_data.update({anal_name: getattr(af, f'get_{anal_name}').analyze(expr_data)})


for key, item in anal_data.items():
    file_path = os.path.join(code_root, 'AnalysisData', f'Data_{key}.xlsx')
    file_writer.write_to_file(item, file_path)