# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:28:51 2025

@author: MIFENG
"""

from .figure_dependencies import prototype_alloc_corr

def draw(anal_data):
    return prototype_alloc_corr.draw(anal_data, 'necs_from_param_by_eta', 'delay', anal_name = 'corr_from_r0_factor_by_eta')