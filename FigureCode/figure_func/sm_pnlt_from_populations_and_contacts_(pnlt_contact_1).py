# -*- coding: utf-8 -*-
"""Cross-objective penalties for contact perturbation 1."""


from .figure_dependencies import prototype_pnlt_population_contact


def draw(anal_data, **kwargs):
    show_legend = kwargs.pop('show_legend', kwargs.pop('legend', False))
    return prototype_pnlt_population_contact.draw_contact_penalty(anal_data, '1', show_legend=show_legend)
