# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 19:14:51 2024

@author: fengm
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import re
import os
import tasks

for task_name in tasks.task_info.keys():
    os.makedirs(os.path.join(code_root, 'ExperimentalDataTmp', ''.join(part.capitalize() for part in re.split(r'_(?![^\(]*\))', task_name))), exist_ok=True)