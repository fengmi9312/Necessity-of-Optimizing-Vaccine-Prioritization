# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:51:22 2025

@author: MIFENG
"""



from .figure_dependencies import prototype_alloc_corr

def draw(anal_data):
    return prototype_alloc_corr.draw(anal_data, 'necs_from_param', 'delay')