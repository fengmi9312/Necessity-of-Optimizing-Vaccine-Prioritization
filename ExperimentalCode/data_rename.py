# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:12:47 2024

@author: fengm
"""

import os
selected_items =  {'Weibull': [(-8, -8), (24, 24), (-8, 24), (24, -8), (8, 8), 
                               (4, 4), (12, 12), (4, 12), (12, 4)],
                   'Gamma': [(-8, -8), (24, 24), (-8, 24), (24, -8), (8, 8), 
                             (4, 4), (12, 12), (4, 12), (12, 4)],
                   'Lognormal': [(4, 36), (36, 4), (4, 4), (36, 36), (20, 20), 
                                 (16, 16), (24, 24), (16, 24), (24, 16)],}
func_type = 'Weibull'
folder_name_map = {'vac_avail': 'VacAvailData',
                   'vac_dur': 'VacDurData',
                   'c_perct': 'CPerctData',
                   'c_steady': 'CSteadyData',
                   'sttgs_curves': 'SttgsCurvesData',}
delay_day = 4
expt_type = 'c_perct'
folder_path = "../ExperimentalDataTmp/" + folder_name_map[expt_type]
for inf_pow, rem_pow in selected_items[func_type]:
    current_name = "Data_" + str(inf_pow) + "_" + str(rem_pow) + "_" + str(delay_day) + ".xlsx"
    new_name = "Data_" + str(inf_pow) + "_" + str(rem_pow) + ".xlsx"
    current_path = os.path.join(folder_path, current_name)
    new_path = os.path.join(folder_path, new_name)
    try:
        os.rename(current_path, new_path)
        print("File renamed successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied to rename the file.")
    except Exception as e:
        print("An error occurred:", e)