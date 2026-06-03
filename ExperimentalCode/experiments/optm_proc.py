# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 19:03:18 2024

@author: fengm
"""
import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta, sir_general
import func
import basic_params
from copy import deepcopy


    
def execute(calc_params,  vac_eff = 0.95, vac_avail = 0.3, c_perct = 0.1, vac_dur = 7, 
         disp = False, tol = 1e-3):
    _calc_params = deepcopy(calc_params)
    growth_rate = 0.36
    r0 = func.calc_r0_from_g(_calc_params['srv_inf'], _calc_params['srv_rem'], growth_rate, _calc_params['step'])
    _calc_params['k'] = r0 / (np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0].max() * \
                            func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    c_steady = func.get_steady_state(_calc_params['k'], _calc_params['populations'], _calc_params['contacts'], 
                                     func.lambda_eff_srv(_calc_params['srv_inf'], _calc_params['srv_rem']), 
                                     _i = _calc_params['i0']) @ _calc_params['populations']
    _calc_params_delta = deepcopy(_calc_params)
    _calc_params_general = deepcopy(_calc_params)
    optm_proc_data = {'vac_alloc': {}}
    vac_step = 0.04
    for idx, delay_day in enumerate([0, 5, 10]):
        _calc_params_delta['delay'] = delay_day * basic_params.day_div
        if delay_day == 0: _calc_params_general['srv_imm'] = np.array([1,0])
        elif delay_day >= 1 and delay_day <= 3: _calc_params_general['srv_imm'] = func.srv_beta(3, 3, delay_day * basic_params.day_div * 2 + 1, _calc_params['step'])
        else: _calc_params_general['srv_imm'] = func.srv_beta(3, 3, 3 * basic_params.day_div * 2 + 1, _calc_params['step'], shift = (delay_day - 3) * basic_params.day_div)
        model_dd = sir_delta(**_calc_params_delta)
        model_gd = sir_general(**_calc_params_general)
        c_init = model_gd.getc_c_tot()
        while True:
            model_dd.spread_once()
            model_gd.spread_once()
            if model_gd.getc_c_tot() >= c_perct * (c_steady - c_init) + c_init: break
        for target in basic_params.targets:
            optm_proc_data['res_sttg_' + str(idx) + '_' + target] = {}
            for optm_dir in ['min', 'max']:
                optm_res = model_dd.optimize_vac_alloc(vac_avail = vac_avail, optm_dir = (optm_dir == 'min'), 
                                            target = target, disp = disp)
                optm_proc_data['vac_alloc'][str(idx) + '_' + target + '_' + optm_dir] = optm_res['alloc']
                optm_proc_data['res_sttg_' + str(idx) + '_' + target][optm_dir] = [model_gd.calc_vac_prdt_target(optm_res['alloc'], target = target),]
            vac_max, vac_min = optm_proc_data['vac_alloc'][str(idx) + '_' + target + '_max'],\
                               optm_proc_data['vac_alloc'][str(idx) + '_' + target + '_min']
            vac_diff = vac_max - vac_min
            for empirical_group_key in basic_params.empirical_groups.keys():
                vac_alloc = func.get_alloc(np.array(model_dd.getc_s()), model_dd.get_populations(), vac_avail, basic_params.empirical_groups[empirical_group_key])
                optm_proc_data['res_sttg_' + str(idx) + '_' + target][empirical_group_key] = [model_gd.calc_vac_prdt_target(vac_alloc, target = target),]
                
# =============================================================================
#             bound_p = np.eye(8)[np.where(np.logical_or((np.abs(vac_min) < tol), (np.abs(vac_min - model_gd.getc_s()) < tol)))[0]]
#             constrain_p = calc_params['populations']
#             joint_space = null_space(np.vstack([constrain_p, bound_p]))
#             joint_p = joint_space.sum(axis = 1)
#             for i in range(8): 
#                 if np.abs(joint_p[i]) < 1e-6: joint_p[i] = 0
#             joint_p_norm = joint_p / np.linalg.norm(joint_p)
#             vec_coe = np.linalg.norm(max_diff) / np.linalg.norm(joint_p_norm) 
#             inv_diff = max_diff - 2 * max_diff @ joint_p_norm * joint_p_norm
# =============================================================================
            optm_proc_data['res_' + str(idx) + '_' + target] = {'coe': [], 'res': []}
            coe_idx = 0
            while True:
                print(vac_step * coe_idx)
                vac_alloc = vac_min + coe_idx * vac_step * vac_diff
                if np.any(vac_alloc > model_gd.getc_s()) or np.any(vac_alloc < 0):
                    break
                optm_proc_data['res_' + str(idx) + '_' + target]['coe'].append(coe_idx * vac_step)
                optm_proc_data['res_' + str(idx) + '_' + target]['res'].append(model_gd.calc_vac_prdt_target(vac_alloc, target = target))
                coe_idx += 1
    return optm_proc_data
