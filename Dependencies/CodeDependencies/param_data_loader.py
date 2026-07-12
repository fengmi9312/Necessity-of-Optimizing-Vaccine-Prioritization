# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:06:09 2024

@author: fengm
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')
import os
folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_curve_data():
    confirmed_data = pd.read_csv(os.path.join(folder_path, 'DataDependencies', 'curves', 'time_series_covid19_confirmed_global.csv'))
    recovered_data = pd.read_csv(os.path.join(folder_path, 'DataDependencies', 'curves', 'time_series_covid19_recovered_global.csv'))
    deaths_data = pd.read_csv(os.path.join(folder_path, 'DataDependencies', 'curves', 'time_series_covid19_deaths_global.csv'))
    return {'confirmed': confirmed_data, 'deaths': deaths_data, 'recovered': recovered_data}

def load_country_curve_data(countries, file_data):
    data = {}
    name_dict = {'United States': 'US', 'South Korea': 'Korea, South'}
    for country in countries:
        data[country] = {}
        if country in name_dict: country_name = name_dict[country]
        else: country_name = country
        for data_type, curve in file_data.items():
            data[country][data_type] = curve[(curve['Country/Region'] == country_name) & (curve['Province/State'].isna())][curve.columns[4:]].to_numpy()[0,:]
    return data

def load_contact_data():
    inverse_name_dict = {'United States of America': 'United States', 'Republic of Korea': 'South Korea', 'United Kingdom of Great Britain': 'United Kingdom'}
    data = {}
    for region_idx, region in enumerate(['all_locations', 'home', 'school', 'work', 'other_locations']):
        for idx in [1, 2]:
            file_data = pd.read_excel(os.path.join(folder_path, 'DataDependencies', 'contact_matrices_152_countries', f'MUestimates_{region}_{idx}.xlsx'), 
                        sheet_name = None, header = None)
            for key, item in file_data.items():
                if region_idx == 0: data[key if key not in inverse_name_dict else inverse_name_dict[key]] = {}
                contact_vals = item.values[None if idx == 2 else 1:].astype('float64')
                data[key if key not in inverse_name_dict else inverse_name_dict[key]][region] = contact_vals
    return data


def load_country_contact_data(countries, contact_file_data, file_population_data):
    res = {}
    population_data = load_country_population_data(countries, file_population_data)
    for country in countries:
        if country in contact_file_data and country in population_data:
            res[country] = {}
            for key, contact_item in contact_file_data[country].items():
                direct_contact = contact_item / population_data[country][None,:]
                res[country][key] = (direct_contact + direct_contact.T) / (2 * direct_contact.shape[0] * direct_contact.shape[1])
    return res

               
def load_population_data():
    return pd.read_excel(os.path.join(folder_path, 'DataDependencies', 'populations', 'WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.xlsx'), 
                         sheet_name = 'ESTIMATES')
    
def load_country_population_structure_data(countries, file_data):
    data = {}
    name_dict = {'United States': 'United States of America', 'South Korea': 'Republic of Korea'}
    ifr_func = interp1d(np.linspace(4.5,94.5,10), 
                    np.array([2/858, 5/1591, 23/13304, 61/22423, 198/34793, 607/42515, 1669/34181, 4544/32323, 7728/37268, 3981/18142]), 
                    kind = 'linear', fill_value =  'extrapolate')
    ifr = ifr_func(np.append([i * 5 + 2 for i in range(15)], 87.5))
    le = {'United States of America':78.5, 'Germany':81.7, 'Brazil':75.9, 'Israel':82.6,
          'United Kingdom': 81.4, 'France': 82.5, 'Spain': 83.2, 'Italy': 83.0, 'Japan': 84.3, 
          'Republic of Korea': 83.3, 'Singapore': 83.2, 'Ireland': 81.8, 'Austria': 81.6}
    mid_age = np.append(np.linspace(2,97,20), 100)
    for country in countries:
        if country in name_dict: country_name = name_dict[country]
        else: country_name = country
        data_array = file_data.loc[(file_data['Unnamed: 2'] == country_name) & (file_data['Unnamed: 7'] == 2020)].values[0][8:]*1000
        rl = np.maximum(0, le[country_name] - np.array([mid_age[i] if i < 15 else sum([mid_age[j] * data_array[j] for j in range(15, 21)]) / sum(data_array[15:]) for i in range(16)]))
        data[country] = {'populations': (np.append(data_array[:15], sum(data_array[15:]))/sum(data_array)).astype('float64'),
                         'ifrs': ifr, 'ylls': rl}
    return data

def load_country_total_population_data(countries, file_data):
    data = {}
    name_dict = {'United States': 'United States of America', 'South Korea': 'Republic of Korea'}
    for country in countries:
        if country in name_dict: country_name = name_dict[country]
        else: country_name = country
        data_array = file_data.loc[(file_data['Unnamed: 2'] == country_name) & (file_data['Unnamed: 7'] == 2020)].values[0][8:]*1000
        data[country] = sum(data_array)
    return data


def load_country_population_data(countries, file_data):
    data = {}
    name_dict = {'United States': 'United States of America', 'South Korea': 'Republic of Korea'}
    for country in countries:
        if country in name_dict: country_name = name_dict[country]
        else: country_name = country
        data_array = file_data.loc[(file_data['Unnamed: 2'] == country_name) & (file_data['Unnamed: 7'] == 2020)].values[0][8:]*1000
        data[country] = data_array[:16] / sum(data_array[:16])
    return data

def rescale_population(data, scale_arr):
    scale_arr = np.array(scale_arr)
    contacts_tot = {}
    for region in ['all_locations', 'home', 'school', 'work', 'other_locations']:
        contacts_tot[region] = data['contacts'][region] * data['populations'][:, None]
    ifrs_tot = data['ifrs'] * data['populations']
    ylls_tot = data['ylls'] * data['populations']
    scale_cum_arr = np.append(0, scale_arr.cumsum())
    contacts_n = {}
    populations_n = []
    ifrs_n = []
    ylls_n = []
    for i in range(1, len(scale_cum_arr)):
        populations_n.append(data['populations'][scale_cum_arr[i - 1]:scale_cum_arr[i]].sum())
        ifrs_n.append(ifrs_tot[scale_cum_arr[i - 1]:scale_cum_arr[i]].sum())
        ylls_n.append(ylls_tot[scale_cum_arr[i - 1]:scale_cum_arr[i]].sum())
    populations_n = np.array(populations_n)
    ifrs_n = np.array(ifrs_n / populations_n)
    ylls_n = np.array(ylls_n / populations_n)
    for region in ['all_locations', 'home', 'school', 'work', 'other_locations']:
        contacts_n[region] = []
        for i in range(1, len(scale_cum_arr)):
            contacts_n[region].append([])
            for j in range(1, len(scale_cum_arr)):
                contacts_n[region][i - 1].append(contacts_tot[region][scale_cum_arr[i - 1]:scale_cum_arr[i], scale_cum_arr[j - 1]:scale_cum_arr[j]].sum())
        contacts_n[region] = np.array(contacts_n[region] / populations_n[:, None])
    return {'contacts':contacts_n, 'populations':populations_n, 'ifrs': ifrs_n, 'ylls':ylls_n}

def load_all_data(countries, scale_arr):
    data = {}
    curve_data = load_country_curve_data(countries, load_curve_data())
    population_data = load_population_data()
    contact_data = load_country_contact_data(countries, load_contact_data(), population_data)
    population_structure_data = load_country_population_structure_data(countries, population_data)
    total_population_data = load_country_total_population_data(countries, population_data)
    for country in countries:
        data[country] = {}
        data[country].update(curve_data[country])
        data_tmp = {}
        data_tmp.update({'contacts': contact_data[country]})
        data_tmp.update(population_structure_data[country])
        data[country].update(rescale_population(data_tmp, scale_arr))
        data[country].update({'total_population': total_population_data[country]})
    return data


countries = ['United States', 'United Kingdom', 'France', 'Germany', 'Spain', 'Japan', 'Israel', 'Austria', 'Ireland', 'South Korea']
x = load_all_data(countries, [2] * 8)
