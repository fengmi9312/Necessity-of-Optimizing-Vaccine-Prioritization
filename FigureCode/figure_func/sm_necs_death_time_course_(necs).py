# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:56:49 2026

@author: fengm
"""



from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_populations', 'param', anal_name = 'necs_from_r0_populations', target = 'd', corr_contour = False)
