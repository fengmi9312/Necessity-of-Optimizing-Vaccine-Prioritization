
from .analysis_dependencies import required_generated_data as rgd
import itertools

data_of_countries = rgd.data_of_countries

def analyze(expr_data):
    x_countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
    acc_types = ['dd', 'gd']
    durs = [False, True]
    expr_name = 'necs_from_country_140'
    anal_data = {}
    for target, acc_type, dur in itertools.product(['c', 'd'], acc_types, durs):
        sheet_name = f"{target}_{acc_type}{'_dur' if dur else ''}"
        anti_target = 'd' if target == 'c' else 'c'
        anal_data[sheet_name] = {}
        #anal_data[f'alloc_{sheet_name}'] = {}
        for expr_param, contact_type in itertools.product(x_countries, ['none', 's', 'w', 'swo']):
            pop_coef = data_of_countries[expr_param]['populations'] if target == 'c' else data_of_countries[expr_param]['populations'] * data_of_countries[expr_param]['ifrs']
            task_name = f'{expr_name}_({expr_param})'
            necs_key = f'{expr_param}_{contact_type}_necs'
            pnlt_key = f'{expr_param}_{contact_type}_pnlt'
            anal_data[sheet_name][necs_key] = []
            anal_data[sheet_name][pnlt_key] = []
            for file_idx, param_idx in itertools.product(range(40), range(25)):
                dist_data = expr_data[task_name][file_idx]['dist']
                append_name = f'{{{contact_type}_{param_idx}}}'
                anal_data[sheet_name][necs_key].append(dist_data[f'max_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef)
                anal_data[sheet_name][pnlt_key].append((dist_data[f'min_{anti_target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef) \
                                                      / (dist_data[f'no_vac_{acc_type}_{append_name}'].to_numpy() @ pop_coef - dist_data[f'min_{target}_{acc_type}_{append_name}'].to_numpy() @ pop_coef))
                #alloc_data = expr_data[task_name][file_idx]['alloc']
                #anal_data[f'alloc_{sheet_name}'][str(file_idx * 25 + param_idx)] = alloc_data[f'min_{target}_{acc_type}_{append_name}'] * data_of_countries[expr_param]['populations']
    for param in ['r0', 'growth_rate', 'alpha', 'beta']:
        sheet_name = param
        anal_data[sheet_name] = {}
        for expr_param in x_countries:
            task_name = f'{expr_name}_({expr_param})'
            key = expr_param
            anal_data[sheet_name][key] = []
            for file_idx, param_idx in itertools.product(range(40), range(25)):
                param_data = expr_data[task_name][file_idx]['transmission_params']
                anal_data[sheet_name][key].append(param_data.loc[param, f'params_{{none_{param_idx}}}'])
    return anal_data
