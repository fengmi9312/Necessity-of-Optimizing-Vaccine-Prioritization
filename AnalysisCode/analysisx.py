# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:59:25 2025

@author: MIFENG
"""

import os
import importlib 

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analysis_func')
files = os.listdir(directory)
module_names = [os.path.splitext(file)[0] for file in files if file.endswith('.py') and file != '__init__.py' and os.path.isfile(os.path.join(directory, file))]

analysis_func = {key: importlib.import_module(f'AnalysisCode.analysis_func.{key}') for key in module_names}
