# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:07:24 2024

@author: 20481756
"""

import os
import sys
code_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(code_root, 'Dependencies', 'CodeDependencies'))

import numpy as np
from model import sir_delta
from Dependencies.FrameDependencies.data_loader import load_all_data
import func
import basic_params
from copy import deepcopy


country = 'United States'
country_data = load_all_data([country], basic_params.group_div)

def calc_vac_prdt_grad(self, vac_alloc, mem = True, init_c = None, ctol = 1e-6, gtol = 1e-6, vac_compr = False):
    _vac_alloc = np.minimum(vac_alloc, self._sir_delta__s[self._sir_delta__current_time_int]) * self._sir_delta__eta * self._sir_delta__get_eff()
    lams = self.calc_lams(mem = mem)
    pos = self._sir_delta__time_int
    rt= self._sir_delta__r[pos]
    svu_tmp = self._sir_delta__sv[pos] + self._sir_delta__u[pos] - _vac_alloc
    totmat_tmp = self._sir_delta__contacts * self._sir_delta__populations[None, :] * self._sir_delta__k  
    lam, mem_eff = lams['lambda_eff'], lams['memory_eff']
    c_arr = self.calc_vac_prdt(vac_alloc)
    c_grad_tmp = np.ones([self._sir_delta__group_amount, self._sir_delta__group_amount])
    while True:
        c_grad = - np.eye(self._sir_delta__group_amount) \
        + np.eye(self._sir_delta__group_amount) * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff))[:,None] \
        + (totmat_tmp * (svu_tmp * lam * np.exp(- totmat_tmp@(lam*(c_arr - rt) + mem_eff)))[:,None]) @ c_grad_tmp
        if np.all(abs(c_grad-c_grad_tmp) <= abs(c_grad_tmp) * (np.ones([self._sir_delta__group_amount, self._sir_delta__group_amount])*gtol)): break
        else: c_grad_tmp = c_grad
    return c_grad * (self._sir_delta__eta * self._sir_delta__get_eff())[None, :]

def calc_vac_prdt_grad_dis(self, vac_alloc, step = 0.001):
    prdt = self.calc_vac_prdt(vac_alloc)
    group_amount = self._sir_delta__group_amount
    return np.array([(self.calc_vac_prdt(vac_alloc + np.eye(group_amount)[i] * step) - prdt) / step for i in range(group_amount)]).T
    
    

sir_delta.calc_vac_prdt_grad = calc_vac_prdt_grad
sir_delta.calc_vac_prdt_grad_dis = calc_vac_prdt_grad_dis

def find_x(v1, v2, v3, allowed_indices):
    from scipy.optimize import minimize
    v3_tmp = v3 / np.linalg.norm(v3)
    
    def objective(x):
        return -np.dot(v3_tmp, x)
    
    constraints = [{'type': 'eq', 'fun': lambda x: np.dot(x, v1)}, 
                   {'type': 'eq', 'fun': lambda x: np.dot(x, v2)},
                   {'type': 'eq', 'fun': lambda x: np.linalg.norm(x) - 1}]
    bounds = [(0 if i not in allowed_indices else -np.inf, 0 if i not in allowed_indices else np.inf) for i in range(16)]
    
    x0 = np.ones(16)
    while True:
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints, 
                          options = {'maxiter': 10000})
        if result.success:
            print("sucess:", result.x)
            return result.x
        else:
            print("failure:", result.message)
            x0 = np.random.rand(16)


# def find_perpendicular_vector(v, w, indices):
#     """
#     Find a vector u perpendicular to both v and w, with non-zero elements only at specific indices.

#     Parameters:
#     - v: The first given vector (1D numpy array).
#     - w: The second given vector (1D numpy array).
#     - indices: The set of positions where u can have non-zero elements (list of integers).

#     Returns:
#     - u: A vector perpendicular to both v and w.
#     """
#     n = len(v)
#     u = np.zeros(n)  # Initialize u with zeros
    
#     # Extract the relevant parts of v and w for the given indices
#     v_sub = v[indices]
#     w_sub = w[indices]
    
#     # Ensure we have enough indices to solve the system
#     if len(indices) < 2:
#         raise ValueError("At least two indices are required to satisfy the perpendicularity conditions.")
    
#     # Formulate the linear system: A * x = 0
#     A = np.array([v_sub, w_sub])  # Coefficients for the linear equations
#     free_var_index = indices[0]  # Choose the first index as the free variable
    
#     # Solve for the other variables in terms of the free variable
#     u_sub = np.zeros(len(indices))
#     u_sub[0] = 1  # Set the free variable to a non-zero value (e.g., 1)
    
#     # Use the other equation to compute the remaining variables
#     remaining_indices = indices[1:]
#     A_reduced = A[:, 1:]  # Ignore the free variable column
#     u_sub[1:] = -np.linalg.pinv(A_reduced) @ A[:, 0] * u_sub[0]
    
#     # Map back to the full vector u
#     for idx, value in zip(indices, u_sub):
#         u[idx] = value
    
#     return u

# import matplotlib.pyplot as plt



def execute(expr_param, file_idx):
    if expr_param != 'param': return None
    alloc_step = 0.002
    r0 = [1.7, 1.74][file_idx]
    alpha_val, beta_val = 2.826, 5.665
    srv_func = func.srv_weibull
    calc_params = deepcopy(basic_params.calc_params)
    calc_params.update({key: country_data[country][key] for key in ['populations', 'ifrs', 'ylls']})
    calc_params['contacts'] = np.sum([country_data[country]['contacts'][region] for region in ['home', 'school', 'work', 'other_locations']], axis = 0)
    srv_gen = srv_func(alpha_val, beta_val, basic_params.srv_length, basic_params.step)
    calc_params['srv_inf'], calc_params['srv_rem'] = srv_gen, srv_gen
    calc_params['k'] = r0 / (np.max(np.linalg.eig(calc_params['populations'][None, :] * calc_params['contacts'])[0]) * func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']))
    calc_params['eta'] = 0.95
    calc_params['delay'] = 4 * basic_params.day_div
    simu = sir_delta(**calc_params)
    steady_c = func.get_steady_state(calc_params['k'], calc_params['populations'], calc_params['contacts'], func.lambda_eff_srv(calc_params['srv_inf'], calc_params['srv_rem']), _i = calc_params['i0']) @ calc_params['populations']
    init_c = calc_params['i0'] @ calc_params['populations']
    while True:
        simu.spread_once()
        if simu.getc_c_tot() >= 0.1 * (steady_c - init_c) + init_c: break
    res = simu.optimize_vac_alloc(vac_avail = 0.3, optm_dir = True, target = 'd', double_optm=True)
    alloc_coef = simu._sir_delta__get_eff() * simu._sir_delta__eta
    alloc_idx = [i for i in range(16) if 0.1 < res[0]['alloc'][i] < 0.9 * simu.getc_s()[i]]
    u1 = (res[1]['alloc'] - res[0]['alloc']) / np.linalg.norm(res[1]['alloc'] - res[0]['alloc'])
    u2 = find_x(res[1]['alloc'] - res[0]['alloc'], calc_params['populations'], calc_params['populations'] @ simu.calc_vac_prdt_grad(res[0]['alloc']), alloc_idx)
    u2 /= np.linalg.norm(u2)
    
    alloc_coefs = []
    prdts = []
    idx = 0
    y_coef_idx = 0
    coef_idx_line_a = []
    while True:
        y_coef = alloc_step * y_coef_idx
        x_coef_idx = idx
        x_coef = alloc_step * x_coef_idx
        alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
        if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
        alloc_coefs.append([x_coef_idx, y_coef_idx])
        prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
        coef_idx_line_a.append([x_coef_idx, y_coef_idx])
        print(x_coef, y_coef)
        idx += 1
    
    for coef_idx_i, coef_idxes in enumerate(coef_idx_line_a):
        if coef_idx_i == 0: coef_idx_line_b = []
        elif coef_idx_i == len(coef_idx_line_a) - 1: coef_idx_line_c = []
        else: pass
        x_coef_idx = coef_idxes[0]
        x_coef = alloc_step * x_coef_idx
        for i in [True, False]:
            idx = -1 if i else 0
            while True:
                y_coef_idx = idx
                y_coef = alloc_step * y_coef_idx
                alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
                if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
                alloc_coefs.append([x_coef_idx, y_coef_idx])
                prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
                if coef_idx_i == 0: coef_idx_line_b.append([x_coef_idx, y_coef_idx])
                if coef_idx_i == len(coef_idx_line_a) - 1: coef_idx_line_c.append([x_coef_idx, y_coef_idx])
                else: pass
                print(x_coef, y_coef)
                if i: idx -= 1
                else: idx += 1
    
    for coef_idx_line_idx, coef_idx_line in enumerate([coef_idx_line_b, coef_idx_line_c]):
        if len(coef_idx_line) <= 1: continue
        for coef_idx_i, coef_idxes in enumerate(coef_idx_line):
            y_coef_idx = coef_idxes[1]
            idx = -1 if coef_idx_line_idx == 0 else 1
            while True:
                x_coef_idx = idx
                x_coef = (coef_idxes[0] + x_coef_idx) * alloc_step
                alloc = res[0]['alloc'] + x_coef * u1 + y_coef * u2
                if np.any(alloc > simu.getc_s()) or np.any(alloc < 0): break
                alloc_coefs.append([x_coef_idx, y_coef_idx])
                prdts.append(simu.calc_vac_prdt_target(alloc, 'd'))
                print(x_coef, y_coef)
                if coef_idx_line_idx == 0: idx -= 1
                else: idx += 1    
    return {'res':{'x_coef': np.array(alloc_coefs)[:, 0], 'y_coef': np.array(alloc_coefs)[:, 1], 'prdt': prdts}, 'alloc_coef': {'alloc_coef': alloc_coef}}


# alloc_coefs, prdts = execute('param', 1)
# import matplotlib.pyplot as plt

# x_coords = [pos[0] for pos in alloc_coefs]
# y_coords = [pos[1] for pos in alloc_coefs]
# z_values = prdts

# # Step 2: Determine the grid size, handling floats
# x_min, x_max = min(x_coords), max(x_coords)
# y_min, y_max = min(y_coords), max(y_coords)

# # Set grid resolution (e.g., 100 points per axis for interpolation)
# grid_resolution = 100
# x_grid = np.linspace(x_min, x_max, grid_resolution)
# y_grid = np.linspace(y_min, y_max, grid_resolution)

# # Step 3: Create a 2D grid and populate it with NaN
# grid = np.full((grid_resolution, grid_resolution), np.nan)

# # Map x, y positions to grid
# for (x, y), z in zip(alloc_coefs, z_values):
#     x_idx = np.searchsorted(x_grid, x) - 1  # Find closest grid index
#     y_idx = np.searchsorted(y_grid, y) - 1  # Find closest grid index
#     if 0 <= x_idx < grid_resolution and 0 <= y_idx < grid_resolution:
#         grid[x_idx, y_idx] = z
        
# plt.figure(figsize=(10, 8))
# # Step 4: Plot the grid with imshow
# plt.imshow(
#     grid.T,
#     origin="lower",
#     cmap="viridis",
#     extent=(x_min, x_max, y_min, y_max),
#     interpolation="nearest",  # Nearest interpolation for better clarity
#     aspect="auto",  # Adjust aspect ratio to fit grid dimensions
# )

# # Add color bar and labels
# plt.colorbar(label="Value")
# plt.xlabel("X-axis")
# plt.ylabel("Y-axis")
# plt.title("Imshow Figure with Float Positions")

# plt.plot([0], [0], marker = '.', color = 'tab:red', markersize = 35)
# plt.plot([max(x_coords)], [0], marker = '.', color = 'tab:gray', markersize = 35)
# # Show plot
# plt.show()







