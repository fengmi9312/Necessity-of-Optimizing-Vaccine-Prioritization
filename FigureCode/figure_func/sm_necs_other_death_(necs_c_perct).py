# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 15:11:44 2025

@author: fengm
"""


from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_param', 'c_perct', target = 'd', corr_contour = False)