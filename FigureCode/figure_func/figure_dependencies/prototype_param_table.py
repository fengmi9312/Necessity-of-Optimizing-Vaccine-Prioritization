# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 02:51:47 2025

@author: fengm
"""


import os
import sys
code_root, folder_level = os.path.dirname(os.path.abspath(__file__)), 3
for _ in range(folder_level): code_root = os.path.dirname(code_root)
import numpy as np
import matplotlib.pyplot as plt
from . import figure_setting
import pandas as pd


def draw(anal_data, **kwargs):
    ####################################################
    scale_prop = 10
    grid_attrs = [[{'pos': (0, 0), 'size': (45, 45)}]]
    margin_attr = {'top': 0, 'bottom': 1, 'left': 2, 'right': 2}
    fig, axes = figure_setting.generate_grid(grid_attrs, margin_attr, scale_prop)
    ######################################################
    ####################################################
    
    from plottable import ColumnDefinition, Table
    from plottable.plots import circled_image
    country_abbr = {
    'Ireland': 'IRL',
    'Japan': 'JPN',
    'United Kingdom': 'UK',
    'France': 'FRA',
    'Germany': 'DEU',
    'United States': 'US',
    'Spain': 'ESP',
    'Austria': 'AUT',
    'Israel': 'ISR',
    'South Korea': 'KOR',
    }
    countries = ['Ireland', 'Japan', 'United Kingdom', 'France', 'Germany', 'United States', 'Spain', 'Austria', 'Israel', 'South Korea']
    res = {}
    col_names = {'flag': 'Flag', 'growth_rate': 'Growth Rate (95% CI)', 'r0': r'$R_0$ (95% CI)'}
    round_num = {'growth_rate': 3, 'r0': 3}
    for col_type in ['flag', 'growth_rate','r0']:
        res[col_names[col_type]] = []
        for country in countries:
            if col_type == 'flag':
                res[col_names[col_type]].append(os.path.join(code_root, 'Dependencies', 'CountryFlags', f'{country}.png'))
            else:
                data_tmp = anal_data['necs_from_country_70'][col_type][country]
                res[col_names[col_type]].append(f"{np.round(np.mean(data_tmp), round_num[col_type])} ({np.round(np.percentile(data_tmp, 2.5), round_num[col_type])} – {np.round(np.percentile(data_tmp, 97.5), round_num[col_type])})")
    country_labels = [f"{country} ({country_abbr[country]})" for country in countries]
    df = pd.DataFrame(res, index = country_labels)
    df = df.rename_axis('Country')
    ax = axes[0][0]
    plt.sca(ax)
    col_defs = ([ColumnDefinition(name="Flag", title="", textprops={"ha": "center"}, width=0.25, plot_fn=circled_image,),
                 ColumnDefinition(name="Country", textprops={"ha": "left", "weight": "bold"}, width=0.8,),
                 ColumnDefinition(name='Growth Rate (95% CI)', textprops={"ha": "center"}, width=0.75,),
                 ColumnDefinition(name=r'$R_0$ (95% CI)', textprops={"ha": "center"}, width=0.75,),])
     
    # plt.rcParams["font.family"] = ["DejaVu Sans"]
    # plt.rcParams["savefig.bbox"] = "tight"
    
    Table(df, column_definitions=col_defs, row_dividers=True, footer_divider=True, ax=ax, textprops={"fontsize": 8.5}, 
          row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))}, col_label_divider_kw={"linewidth": 1, "linestyle": "-"}, 
          column_border_kw={"linewidth": 1, "linestyle": "-"}).autoset_fontcolors(colnames=[])
    return fig, axes
