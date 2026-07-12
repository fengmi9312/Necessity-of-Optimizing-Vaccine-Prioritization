# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""



from .figure_dependencies import prototype_necs_slice

def draw(anal_data):
    return prototype_necs_slice.draw(anal_data, 'necs_line_from_param', 'delay_0', data_type = 'necs', country = 'United States', target = 'c', acc_type = 'dd', dur = False, text = '0')