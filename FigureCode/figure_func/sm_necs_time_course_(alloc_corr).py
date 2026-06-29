# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 2026

@author: fengm
"""


from .figure_dependencies import prototype_alloc_corr


def draw(anal_data):
    return prototype_alloc_corr.draw(
        anal_data,
        'necs_from_time_course_fixd',
        'param',
        anal_name='corr_from_r0_time_course',
    )
