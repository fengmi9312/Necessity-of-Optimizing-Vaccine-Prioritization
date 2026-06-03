# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 18:48:52 2026

@author: fengm
"""


from .figure_dependencies import prototype_corr_heatmap

def draw(anal_data):
    return prototype_corr_heatmap.draw(anal_data, 'necs_from_param_by_eta', 'delay', anal_name = 'corr_from_r0_factor_by_eta', target = 'c', corr_contour = True)