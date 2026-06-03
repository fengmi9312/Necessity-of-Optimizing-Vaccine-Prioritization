# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 02:01:16 2025

@author: fengm
"""



from .figure_dependencies import prototype_necs_heatmap

def draw(anal_data):
    return prototype_necs_heatmap.draw(anal_data, 'necs_from_fatality', 'coef_beta_1', data_type = 'necs', country = 'United States', target = 'd', acc_type = 'dd', dur = False)