# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:47:14 2024

@author: fengmi9312
"""


import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))
sys.path.append(os.path.join(code_root, 'ExperimentalCode'))
import pandas as pd
from task_info import info
import output_name

def load_edata(expr_name, task_param):
    task_name = f'{expr_name}_({task_param})'
    res = []
    for file_idx in range(info[expr_name][task_param]):
        res.append(pd.read_excel(output_name.analysis_file(task_name, file_idx), index_col = 0, sheet_name = None))
    print(task_name + ' imported')
    return res

def load_certain_edata(key_dict):
    res = {}
    for expr_name, task_params in key_dict.items():
        for task_param in task_params:
            task_name = f'{expr_name}_({task_param})'
            res[task_name] = load_edata(expr_name, task_param)
    return res

def load_all_edata():
    return load_certain_edata({expr_name: list(task_params.keys()) for expr_name, task_params in info.items()})




'''


def import_vc_data(expt_type = 'vac_avail'):
    experimental_data = {}
    folder_name_map = {'vac_avail': 'VacAvailData',
                       'vac_dur': 'VacDurData',
                       'c_perct': 'CPerctData',
                       'r0': 'R0Data',}
    param_type = 'Data_' + expt_type
    experimental_data[param_type] = \
    pd.read_excel('../ExperimentalData/' + folder_name_map[expt_type] 
                  + '/' + param_type + '.xlsx', 
                  index_col = 0, sheet_name = None)
    print(expt_type + ' imported')
    return experimental_data


def import_sttgs_curves_data():
    experimental_data = {}
    experimental_data['Data_sttgs_curves'] = \
    pd.read_excel('../ExperimentalData/SttgsCurvesData/Data_sttgs_curves.xlsx', 
                  index_col = 0, sheet_name = None)
    print('sttgs_curves' + ' imported')
    return experimental_data


def import_dist_list_data():
    experimental_data = {}
    param_keys = [('Weibull', 2.5, 2.5), ('Weibull', 2, 3), ('Weibull', 1.5, 3.5)]
    for func_type, mean_inf, mean_rem in param_keys:
        for r0_idx in range(3):
            param_type = func_type + '_' + 'i' + str(mean_inf) + 'r' + str(mean_rem) + '_' + str(r0_idx)
            experimental_data[param_type] = \
            pd.read_excel('../ExperimentalData/DistListData' 
                          + '/Data_' + param_type + '.xlsx', 
                          index_col = 0, sheet_name = None)
    print('dist_list' + ' imported')
    return experimental_data


def import_general_dist_list_data():
    experimental_data = {}
    func_type, mean_inf, mean_rem = 'Weibull', 2, 3
    for inf_pow in [-4, 8, 20]:
        for rem_pow in [-4, 8, 20]:
            param_type = func_type + "_" + "i" + str(mean_inf) + "r" + str(mean_rem) + '_' + str(inf_pow) + '_' + str(rem_pow)
            experimental_data[param_type] = \
            pd.read_excel('../ExperimentalData/GeneralDistListData' 
                          + '/Data_' + param_type + '.xlsx', 
                          index_col = 0, sheet_name = None)
    print('general_dist_list' + ' imported')
    return experimental_data

def import_resp_dist_list_data(sesp_type):
    folder_name_map = {'var_dist_list': 'VarDistListData',
                       'mean_dist_list': 'MeanDistListData',
                       'length_dist_list': 'LengthDistListData'}
    experimental_data = {}
    for rank in range(5):
        experimental_data[str(rank)] = \
        pd.read_excel('../ExperimentalData/' + folder_name_map[sesp_type] +
                      '/Data_' + str(rank) + '.xlsx', 
                      index_col = 0, sheet_name = None)
    print('resp_dist_list' + ' imported')
    return experimental_data

def import_optm_proc_data():
    experimental_data = {'optm_proc': pd.read_excel( "../ExperimentalDataTmp/OptmProcData/Data_optm_proc.xlsx",
                        index_col = 0, sheet_name = None)}
    return experimental_data

'''
