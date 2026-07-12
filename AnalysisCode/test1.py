# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 12:26:06 2025

@author: fengm
"""

from pathlib import Path
import re

folder = Path('analysis_func')
pattern = re.compile(r'^get_(.+)\.py$')

names = []
for file in folder.glob('get_*.py'):
    match = pattern.match(file.name)
    if match:
        names.append(match.group(1))

print(names)