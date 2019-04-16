import wx
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import utils

k_calc_type = ""

def construct_df(raw):
    data = raw
    raw['avg'] = raw[['maxC']].mean(axis=1)     # NOT USING AVERAGE ANYMORE, WANT TO GET AS WARM AS IT COULD BE.
                                                # FOR THE WORST.
    return data

def construct_year_data(df, year):
    return df.loc[df['yyyy'] == year]

def get_month_data(data, year, mm): #10oC
    df = construct_df(data)
    year_data = construct_year_data(df, year)

    if year_data.loc[df['mm'] == mm].empty == False:
        temp = year_data.loc[df['mm'] == mm].iloc[0]['avg']
    else:
        temp=0
    return temp

def get_month_data_max(data, year, mm): #10oC
    df = construct_df(data)
    year_data = construct_year_data(df, year)

    if year_data.loc[df['mm'] == mm].empty == False:
        temp = year_data.loc[df['mm'] == mm].iloc[0]['maxC']
    else:
        temp = 0

    return temp

def get_month_data_min(data, year, mm): #10oC
    df = construct_df(data)
    year_data = construct_year_data(df, year)

    if year_data.loc[df['mm'] == mm].empty == False:
        temp = year_data.loc[df['mm'] == mm].iloc[0]['minC']
    else:
        temp = 0

    return temp


def construct_season_avg(data, year, season):
    seasons = {
        "winter": utils.mean([get_month_data(data, year-1, 12),get_month_data(data, year, 1),get_month_data(data, year, 2)]),
        "spring": utils.mean([get_month_data(data, year, 3), get_month_data(data, year, 4), get_month_data(data, year, 5)]),
        "summer": utils.mean([get_month_data(data, year, 6), get_month_data(data, year, 7), get_month_data(data, year, 8)]),
        "autumn": utils.mean([get_month_data(data, year, 9), get_month_data(data, year, 10), get_month_data(data, year, 11)]),
    }

    return seasons.get(season) #gets actual value

def construct_season_avg_max(data, year, season):
    seasons = {
        "winter": utils.mean([get_month_data_max(data, year-1, 12),get_month_data_max(data, year, 1),get_month_data_max(data, year, 2)]),
        "spring": utils.mean([get_month_data_max(data, year, 3), get_month_data_max(data, year, 4), get_month_data_max(data, year, 5)]),
        "summer": utils.mean([get_month_data_max(data, year, 6), get_month_data_max(data, year, 7), get_month_data_max(data, year, 8)]),
        "autumn": utils.mean([get_month_data_max(data, year, 9), get_month_data_max(data, year, 10), get_month_data_max(data, year, 11)]),
    }

    return seasons.get(season) #gets actual value

def construct_season_avg_min(data, year, season):
    seasons = {
        "winter": utils.mean([get_month_data_min(data, year-1, 12),get_month_data_min(data, year, 1),get_month_data_min(data, year, 2)]),
        "spring": utils.mean([get_month_data_min(data, year, 3), get_month_data_min(data, year, 4), get_month_data_min(data, year, 5)]),
        "summer": utils.mean([get_month_data_min(data, year, 6), get_month_data_min(data, year, 7), get_month_data_min(data, year, 8)]),
        "autumn": utils.mean([get_month_data_min(data, year, 9), get_month_data_min(data, year, 10), get_month_data_min(data, year, 11)]),
    }

    return seasons.get(season) #gets actual value


def calculate_knn_mid(data, k, year, season):
    k_side = k // 2
    k_range=[]
    for i in range(k):
        if i != k_side:
            k_range.append(construct_season_avg(data, year + (i - k_side), season))

    return utils.mean(k_range) #gets predicted value

def calculate_knn_forcast(data, k, year, season): #calc future values
    k_range=[]
    for i in range(k):
        k_range.append(construct_season_avg(data, year - (k-i), season))

    return utils.mean(k_range) #gets predicted value

def get_max_temperature(data, month, year):
    df = construct_df(data)
    year_data = construct_year_data(df, year)
    if year_data.loc[df['mm'] == month].empty == False:
        temp = year_data.loc[df['mm'] == month].iloc[0]['maxC']
    else:
        temp = 0

    return temp

def get_min_temperature(data, month, year):
    df = construct_df(data)
    year_data = construct_year_data(df, year)
    temp=0
    if year_data.loc[df['mm'] == month].empty == False:
        temp = year_data.loc[df['mm'] == month].iloc[0]['minC']
    else:
        temp = 0

    return temp

def get_average_temperature(data, month, year):
    temps = []
    temps.append(get_max_temperature(data, month, year))
    temps.append(get_min_temperature(data, month, year))
    return utils.mean(temps)

def get_average_max(data, years_to_check, year_to_start, season):
    avg = 0
    for i in range(years_to_check):
        avg += construct_season_avg_max(data, year_to_start-i, season)

    return avg / years_to_check

def get_average_min(data, years_to_check, year_to_start, season):
    avg = 0
    for i in range(years_to_check):
        avg += construct_season_avg_min(data, year_to_start-i, season)

    return avg / years_to_check

