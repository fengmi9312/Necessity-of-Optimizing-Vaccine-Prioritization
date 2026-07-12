# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 2026

@author: fengm
"""


from .figure_dependencies import prototype_penalty


def draw(anal_data):
    return prototype_penalty.draw(
        anal_data,
        'necs_from_time_course_fixd_by_fatality',
        'param',
        anal_name='necs_from_r0_time_course_by_fatality',
    )
