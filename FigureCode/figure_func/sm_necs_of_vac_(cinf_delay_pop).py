# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 01:39:04 2026

@author: fengm
"""




from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_param', 'delay', data_type = 'vac_pop_necs', corr_contour = False)