# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 2026

@author: fengm
"""


from .figure_dependencies import prototype_corr_heatmap


def draw(anal_data):
    return prototype_corr_heatmap.draw(
        anal_data,
        'necs_from_time_course_fixd_by_fatality',
        'param',
        anal_name='corr_from_r0_time_course_by_fatality',
        target='d',
        corr_contour=True,
    )
