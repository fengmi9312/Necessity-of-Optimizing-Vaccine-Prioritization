# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""


from .figure_dependencies import prototype_corr_heatmap

def draw(anal_data):
    return prototype_corr_heatmap.draw(anal_data, 'necs_from_fatality', 'coef_beta_1', country = 'United States', target = 'd')