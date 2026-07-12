# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 00:44:40 2025

@author: fengm
"""


from .figure_dependencies import prototype_necs_slice

def draw(anal_data):
    return prototype_necs_slice.draw(anal_data, 'necs_line_from_param', 'delay_8', data_type = 'necs', country = 'United States', target = 'd', acc_type = 'dd', dur = False, text = '4')