# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:03:37 2024

@author: 20481756
"""


import inspect
import os
import pickle
from . import folder_func


def check_cache(expt_param, file_idx, param_idx):
    caller_file_path = os.path.abspath(inspect.currentframe().f_back.f_globals['__file__'])
    file_name, file_extension = os.path.splitext(os.path.basename(caller_file_path))
    folder_path = os.path.dirname(caller_file_path)
    
    cache_folder_path = os.path.join(folder_path, 'cache', f'cache_{file_name}_({expt_param})[{file_idx}]')
    temporary_cache_path = os.path.join(cache_folder_path, f'temporary_cache_{file_name}_({expt_param})[{file_idx}]{{{param_idx}}}.pkl')
    if os.path.isfile(temporary_cache_path): return False
    
    cache_path = os.path.join(cache_folder_path, f'cache_{file_name}_({expt_param})[{file_idx}]{{{param_idx}}}.pkl')
    if os.path.isfile(cache_path): return True
    
def add_cache(expt_param, file_idx, param_idx, variables):
    caller_file_path = os.path.abspath(inspect.currentframe().f_back.f_globals['__file__'])
    file_name, file_extension = os.path.splitext(os.path.basename(caller_file_path))
    folder_path = os.path.dirname(caller_file_path)
    
    cache_root_path = os.path.join(folder_path, 'cache')
    folder_func.create_folder(cache_root_path)
    
    cache_folder_path = os.path.join(cache_root_path, f'cache_{file_name}_({expt_param})[{file_idx}]')
    folder_func.create_folder(cache_folder_path)
    
    temporary_cache_path = os.path.join(cache_folder_path, f'temporary_cache_{file_name}_({expt_param})[{file_idx}]{{{param_idx}}}.pkl')
    if os.path.isfile(temporary_cache_path): os.remove(temporary_cache_path)
    cache_path = os.path.join(cache_folder_path, f'cache_{file_name}_({expt_param})[{file_idx}]{{{param_idx}}}.pkl')
    if os.path.isfile(cache_path): os.remove(cache_path)
    
    with open(temporary_cache_path, 'wb') as cache_file:
        pickle.dump(variables, cache_file)
    
    try:
        os.rename(temporary_cache_path, cache_path)
    except FileNotFoundError:
        print(f"The file {temporary_cache_path} does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to rename {temporary_cache_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def get_cache(expt_param, file_idx, param_idx):
    caller_file_path = os.path.abspath(inspect.currentframe().f_back.f_globals['__file__'])
    file_name, file_extension = os.path.splitext(os.path.basename(caller_file_path))
    folder_path = os.path.dirname(caller_file_path)
    
    cache_path = os.path.join(folder_path, 'cache' , f'cache_{file_name}_({expt_param})[{file_idx}]', f'cache_{file_name}_({expt_param})[{file_idx}]{{{param_idx}}}.pkl')
    if not os.path.isfile(cache_path): return None
    
    with open(cache_path, 'rb') as cache_file:
        variables = pickle.load(cache_file)
        
    return variables
    
import shutil
def del_cache(expt_param, file_idx):
    caller_file_path = os.path.abspath(inspect.currentframe().f_back.f_globals['__file__'])
    file_name, file_extension = os.path.splitext(os.path.basename(caller_file_path))
    folder_path = os.path.dirname(caller_file_path)
    
    cache_folder_path = os.path.join(folder_path, 'cache' , f'cache_{file_name}_({expt_param})[{file_idx}]')
    cache_folder_lock_path = os.path.join(folder_path, 'cache' , f'cache_{file_name}_({expt_param})[{file_idx}].lock')
    if os.path.exists(cache_folder_path): 
        shutil.rmtree(cache_folder_path)
        if os.path.exists(cache_folder_lock_path):
            os.remove(cache_folder_lock_path)
    
    
    
    
    
    
    
    
    