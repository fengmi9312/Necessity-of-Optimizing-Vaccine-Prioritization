# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:05:15 2023

@author: admin
"""


from refinement import execute_refinement
import sys

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        task_idx = 1
        task_amount = 40
        expr_name, task_param = 'necs_from_growth_s', 'weibull_0'
    elif  sys.platform.startswith('linux'):
        if len(sys.argv) != 5:
            sys.exit(1)
        task_idx = int(sys.argv[1])
        task_amount = int(sys.argv[2])
        expr_name, task_param = sys.argv[3], sys.argv[4]
    else:
        sys.exit(0)
    execute_refinement(expr_name, task_param, task_idx, task_amount)