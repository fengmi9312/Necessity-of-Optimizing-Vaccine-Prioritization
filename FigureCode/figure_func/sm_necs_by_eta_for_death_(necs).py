# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""


from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_param_by_eta', 'delay', anal_name = 'necs_from_r0_factor_by_eta', target = 'd', corr_contour = True)