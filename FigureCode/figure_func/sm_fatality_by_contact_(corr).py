# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:31:46 2026

@author: fengm
"""


from .figure_dependencies import prototype_corr_heatmap

def draw(anal_data):
    return prototype_corr_heatmap.draw(anal_data, 'necs_from_fatality_by_contact', 'coef_beta_1', anal_name = 'corr_from_r0_fatality_by_contact', target = 'x', data_type = 'corr_ind', corr_contour = False)