# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:58:53 2025

@author: fengm
"""



from .figure_dependencies import prototype_necs_box

def draw(anal_data):
    return prototype_necs_box.draw(anal_data, target = 'd')