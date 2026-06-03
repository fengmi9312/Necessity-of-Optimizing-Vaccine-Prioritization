# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:28:51 2025

@author: MIFENG
"""

from .figure_dependencies import prototype_penalty

def draw(anal_data):
    return prototype_penalty.draw(anal_data, 'necs_from_fatality_by_contact', 'coef_beta_1', anal_name = 'necs_from_r0_fatality_by_contact')