# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 13:30:57 2025

@author: fengm
"""


if __name__ != "__main__":
    raise ImportError("This module cannot be imported.")
    
    

import os
import sys
code_root, folder_level = os.path.dirname(os.path.abspath(__file__)), 1
for _ in range(folder_level): code_root = os.path.dirname(code_root)
sys.path.append(code_root)
import importlib

import FigureCode.figure_func as ff

from AnalysisCode import analysis
anal_list = ['necs_line_from_r0', 'corr_line_from_r0']
anal_list = ['bnf_from_example']
anal_list = ['fraction_from_time_with_example']
anal_list = ['fitted_fraction_from_time', 'necs_from_country', 'param_from_country', 'necs_from_r0_factor']
anal_list = ['alloc_from_age_with_example', 'alloc_from_r0_factor', 'bnf_from_example', 'corr_from_r0_factor', 
             'corr_line_from_r0', 'dist_diff_from_r0', 'fitted_fraction_from_time', 'fraction_from_time_with_example', 
             'necs_from_country', 'necs_from_growth', 'necs_from_growth_s', 'necs_from_r0_factor', 'necs_line_from_r0', 'param_from_country', 'prdt_from_corr', 'prdt_from_xycoef', 'group_effect_from_r0_factor']

# anal_data = analysis.get_anal_data(['necs_from_r0_factor', 'corr_from_r0_factor'])
# anal_data.update(analysis.get_anal_data(['alloc_from_age_with_example', 'fraction_from_time_with_example']))
# anal_data.update(analysis.get_anal_data(['necs_line_from_r0', 'corr_line_from_r0']))
anal_data = {}xxx

anal_list = ['corr_from_r0_fatality_by_contact', 'necs_from_r0_fatality_by_contact', 'corr_from_r0_factor', 'necs_line_from_r0', 'corr_line_from_r0', 'necs_from_r0_factor', 'corr_from_r0_factor', 'necs_from_r0_factor_by_eta', 'corr_from_r0_factor_by_eta']

anal_list = ['corr_from_r0_factor', 'necs_from_r0_factor', 'corr_line_from_r0', 'necs_line_from_r0', 'prdt_from_corr', 'bnf_from_example', 'corr_from_r0_fatality_by_contact', 'necs_from_r0_fatality_by_contact','necs_from_r0_factor_by_eta', 'corr_from_r0_factor_by_eta', 'necs_from_country', 'param_from_country', 'fitted_fraction_from_time']

# anal_data.update(analysis.get_anal_data(['necs_from_r0_time_course', 'corr_from_r0_time_course', 'necs_from_r0_factor', 'corr_from_r0_factor', 
#                                          'necs_from_r0_time_course_by_fatality', 'corr_from_r0_time_course_by_fatality', 'necs_from_r0_time_course_by_fatality_ext', 'corr_from_r0_time_course_by_fatality_ext']))

# anal_data.update(analysis.get_anal_data(['necs_from_r0_time_course', 'corr_from_r0_time_course', 'necs_from_r0_factor', 'corr_from_r0_factor']))


# anal_data.update(analysis.get_anal_data(['alloc_from_age_with_example', 'fraction_from_time_with_example']))

anal_data.update(analysis.get_anal_data(['necs_from_r0_factor', 'corr_from_r0_factor', ]))

fig_dict = {'illustration': ['necs_illustration'],
            'necs_cinf': ['necs_cinf', 'corr_cinf', 'necs_slice', 'example', 'rnecs_slice', 'rnecs_cinf'],
            'necs_death': ['necs_death_delta', 'necs_death_gamma', 'corr_death_delta', 'corr_death_gamma', 'necs_slice_gamma', 'optm_space', 'optm_transition'],
            'cross_obj': ['example_low_r0', 'example_high_r0', 'penalty_delta', 'penalty_gamma', 'alloc_corr_delta', 'alloc_corr_gamma'],
            'sm_necs_other': ['cinf_vac_avail', 'cinf_vac_eff', 'cinf_c_perct', 'cinf_vac_dur', 'death_vac_avail', 'death_vac_eff', 'death_c_perct', 'death_vac_dur'],
            'res_country': ['fitting', 'param', 'necs_cinf', 'necs_death', 'pnlt']}

fig_dict = {'sm_fatality_by_contact': ['corr', 'fatality', 'necs', 'slice'],
            'sm_fatality_by_contact_to_pnlt': ['pnlt', 'alloc_corr'], 
            'sm_necs_death': ['corr_death_delta'],
            'sm_necs_from_contact_for_cinf': ['corr', 'necs'],
            'sm_necs_from_contact_for_deaths': ['corr', 'necs'],
            'sm_param_by_eta': ['eta_dist'],
            'sm_necs_by_eta_for_cinf': ['corr', 'necs', 'slice'],
            'sm_necs_by_eta_for_death': ['corr', 'necs', 'slice'],
            'sm_necs_by_eta_to_pnlt': ['alloc_corr', 'pnlt'],
            'sm_us_params': ['contacts', 'fatality_by_gamma', 'populations'],
            'sm_contacts_params': ['uk', 'fr', 'de', 'es', 'jp', 'il', 'at', 'ie', 'kr'],
            'sm_populations_params': ['uk', 'fr', 'de', 'es', 'jp', 'il', 'at', 'ie', 'kr'],
            'sm_us_contacts_params': ['home', 'school', 'work', 'other_locations'],
            'sm_necs_of_vac': ['cinf_delay', 'death_delay', 'death_fatality'],
            'sm_res_country': ['fitting', 'param', 'necs_cinf', 'necs_death', 'pnlt'],
            'sm_pnlt_by_contact_and_eta': ['contact_alloc_corr', 'contact_pnlt', 'eta_alloc_corr', 'eta_pnlt',],
            'sm_necs_other': ['cinf_vac_eff', 'cinf_c_perct', 'death_vac_eff', 'death_c_perct'],
            'sm_corr_other': ['cinf_vac_eff', 'cinf_c_perct', 'death_vac_eff', 'death_c_perct'],
            'sm_necs_roll': ['cinf', 'death']}

import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "mathtext.default": "it",
})


# mpl.rcParams['mathtext.fontset'] = 'cm'   # Computer Modern, 很像 LaTeX
# mpl.rcParams['mathtext.default'] = 'it'   # 数学变量默认斜体

fig_dict = {'sm_fatality_by_contact_to_pnlt': ['pnlt', 'alloc_corr'],
            'sm_necs_from_contact_for_cinf': ['corr', 'necs'],
            'sm_necs_from_contact_for_death': ['corr', 'necs'],
            'sm_necs_by_eta_to_pnlt': ['alloc_corr', 'pnlt'],
            'sm_contacts_params': ['uk', 'fr', 'de', 'es', 'jp', 'il', 'at', 'ie', 'kr'],
            'sm_populations_params': ['uk', 'fr', 'de', 'es', 'jp', 'il', 'at', 'ie', 'kr'],
            'sm_us_contacts_params': ['home', 'school', 'work', 'other_locations'],}

fig_dict = {'necs_death': ['necs_death_delta', 'necs_death_gamma', 'corr_death_gamma', 'necs_slice_gamma', 'optm_transition'],
            'cross_obj': ['example_low_r0', 'example_high_r0', 'penalty_delta', 'penalty_gamma', 'alloc_corr_delta', 'alloc_corr_gamma'],
            'sm_necs_death': ['corr_death_delta'],
            'sm_fatality_by_contact': ['fatality', 'necs', 'corr', 'slice'],
            'sm_necs_from_contact_for_cinf': ['corr', 'necs'],
            'sm_necs_from_contact_for_death': ['corr', 'necs'],
            'sm_necs_by_eta_for_cinf': ['corr', 'necs', 'slice'],
            'sm_necs_by_eta_for_death': ['corr', 'necs', 'slice'],
            'sm_pnlt_by_contact_and_eta': ['contact_alloc_corr', 'contact_pnlt', 'eta_alloc_corr', 'eta_pnlt',],
            'sm_necs_other_cinf': ['necs_vac_eff', 'necs_c_perct', 'corr_vac_eff', 'corr_c_perct'],
            'sm_necs_other_death': ['necs_vac_eff', 'necs_c_perct', 'corr_vac_eff', 'corr_c_perct'],
            'sm_necs_roll': ['cinf', 'death'],
            'sm_res_country': ['necs_cinf', 'necs_death', 'pnlt', 'param', 'fitting']}

seleted_key = 'necs_cinf'
selected_fig_dict = {'sm_pop_necs': ['cinf_delay', 'death_delay', 'death_fatality'],
                     'sm_necs_of_vac': ['cinf_delay_pop', 'death_delay_pop', 'death_fatality_pop'],} #{seleted_key: fig_dict[seleted_key]}
selected_fig_dict = {'sm_contacts_params': ['at', 'de', 'es', 'fr', 'ie', 'il', 'jp', 'kr', 'uk'],
                     'sm_fatality_by_contact': ['fatality'],
                     'sm_populations_params': ['at', 'de', 'es', 'fr', 'ie', 'il', 'jp', 'kr', 'uk'],
                     'sm_us_params': ['contacts', 'fatality_by_gamma', 'populations']}
selected_fig_dict = {'sm_necs_cinf_time_course': ['necs', 'necs_x'], 'sm_necs_death_time_course': ['necs', 'necs_x']}
selected_fig_dict = {'res_country': ['necs_death'], 'sm_res_country_0': ['necs_death'], 'sm_res_country_1': ['necs_death'],}
selected_fig_dict = {'sm_necs_cinf_time_course': ['corr_fixd'], 'sm_necs_death_time_course': ['corr_fixd']}


selected_fig_dict = {'sm_necs_time_course': ['pnlt', 'alloc_corr', 'necs_fixd_cinf', 'corr_fixd_cinf', 'necs_fixd_death', 'corr_fixd_death'] }
selected_fig_dict = {'sm_necs_populations': ['necs_cinf', 'necs_death', 'necs_death_adj', 'corr_cinf', 'corr_death', 'pop_example', 'pw_ifr'] }

selected_fig_dict = {'sm_res_country_1': ['necs_cinf', 'necs_death_adj', 'cinf_pnlt', 'death_pnlt'], }
selected_fig_dict = {'sm_necs_contacts': ['necs_cinf', 'corr_cinf', 'necs_death', 'corr_death'], }
selected_fig_dict = {'sm_pnlt_from_populations_and_contacts': ["pnlt_contact_1", "pnlt_contact_13", "alloc_corr_contact_1", "alloc_corr_contact_13", "pnlt_populations", "alloc_corr_populations"]}

selected_fig_dict = {'sm_necs_other_cinf': ['necs_vac_eff', 'corr_vac_eff'],
                     'sm_necs_other_death': ['necs_vac_eff', 'corr_vac_eff'],}
save_fig = True
import matplotlib.pyplot as plt
importlib.reload(ff)
for fig_name, sub_name_list in selected_fig_dict.items():
    for sub_name in sub_name_list:
        fig, _ = getattr(ff, f'{fig_name}_({sub_name})').draw(anal_data)
        if save_fig:
            fig.savefig(os.path.join(code_root, 'Figure', fig_name, f'{sub_name}.pdf'), dpi=300)
            plt.close(fig)
            
            
# plt.figure()
# plt.plot(anal_data['necs_from_r0_time_course']['necs_from_time_course_fixd_(param)-us_c_dd_necs'].to_numpy()[:, 20])