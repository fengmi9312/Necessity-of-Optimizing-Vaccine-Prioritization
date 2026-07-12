# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""


from .figure_dependencies import prototype_rnecs_slice

def draw(anal_data):
    return prototype_rnecs_slice.draw(anal_data, 'necs_from_param', 'delay', param_idx = 8, country = 'United States', target = 'c', acc_type = 'dd', dur = False)