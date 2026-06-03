# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 02:04:48 2025

@author: fengm
"""



from .figure_dependencies import prototype_necs_line_slice

def draw(anal_data):
    return prototype_necs_line_slice.draw(anal_data, 'necs_line_from_fatality',  country = 'United States', target = 'd')