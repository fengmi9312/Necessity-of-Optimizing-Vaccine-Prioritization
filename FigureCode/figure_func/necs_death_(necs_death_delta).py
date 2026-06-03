# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 00:36:03 2025

@author: fengm
"""


from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_param', 'delay', data_type = 'necs', country = 'United States', target = 'd', acc_type = 'dd', dur = False, corr_contour = False)