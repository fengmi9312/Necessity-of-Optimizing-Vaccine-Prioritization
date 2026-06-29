# -*- coding: utf-8 -*-
"""Allocation correlation for population profile perturbations."""


from .figure_dependencies import prototype_pnlt_population_contact


def draw(anal_data, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', True))
    return prototype_pnlt_population_contact.draw_population_alloc_corr(anal_data, show_legend=show_legend)
