# -*- coding: utf-8 -*-
"""
Merge direct_effects_from_time_course experiment outputs.
"""

def analyze(expr_data):
    anal_data = {}
    for file_data in expr_data['direct_effects_from_time_course_(param)']:
        for sheet_name, sheet_data in file_data.items():
            anal_data[sheet_name] = sheet_data
    return anal_data
