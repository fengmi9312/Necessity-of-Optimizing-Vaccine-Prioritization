# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:18:21 2025

@author: MIFENG
"""


from .figure_dependencies import prototype_penalty

def draw(anal_data):
    return prototype_penalty.draw(anal_data, 'necs_from_param', 'delay')