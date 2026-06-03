# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:06:53 2025

@author: MIFENG
"""



from .figure_dependencies import prototype_necs_line_slice

def draw(anal_data):
    return prototype_necs_line_slice.draw(anal_data, 'necs_line_from_param', country = 'United States', target = 'd')