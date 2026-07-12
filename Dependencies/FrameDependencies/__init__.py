# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:59:58 2025

@author: MIFENG
"""


import os
import importlib

# Get the directory of the current file (__init__.py)
package_dir = os.path.dirname(__file__)

# Loop through all files in the package directory
for module_name in os.listdir(package_dir):
    # Check if the file is a Python file (excluding __init__.py)
    if module_name != '__init__.py' and  module_name != '__pycache__' and module_name.endswith('.py') and not module_name.startswith('.'):
        # Remove the .py extension to get the module name
        module_name = os.path.splitext(module_name)[0]
        
        # Import the module dynamically
        importlib.import_module(f'.{module_name}', package=__name__)