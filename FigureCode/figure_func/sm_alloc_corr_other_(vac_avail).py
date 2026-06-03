# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 13:23:06 2026

@author: fengm
"""



from .figure_dependencies import prototype_alloc_corr_other

def draw(anal_data):
    return prototype_alloc_corr_other.draw(anal_data, 'necs_from_param', 'vac_avail')