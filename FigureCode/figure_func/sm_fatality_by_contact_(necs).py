# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:31:46 2026

@author: fengm
"""



from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_fatality_by_contact', 'coef_beta_1', anal_name = 'necs_from_r0_fatality_by_contact', target = 'x', corr_data_type = 'corr_ind', corr_contour = False)