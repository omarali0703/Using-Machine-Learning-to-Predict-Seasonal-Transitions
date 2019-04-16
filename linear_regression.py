import numpy as np
import matplotlib.pyplot as plt

# get all season data for all years before prediction
# get predict the next
# plot that on graph

import knn as knn


def get_season_data(data, year, season): # season, data, year to get data from
    data_range = []

    min = data['yyyy'].min()

    for i in range(min+1, year):
        d = knn.construct_season_avg_max(data, i, season)
        data_range.append(d)

    return data_range


def get_month_data(data, year, mm):
    data_range = []

    min = int(data['yyyy'].min())

    for i in range(min+1, year):
        d = knn.get_month_data_max(data, i, mm)
        data_range.append(d)

    return data_range


def get_year_range(data, year):
    min = data['yyyy'].min()
    return list(range(min+1, year))


def estimate_coef(x, y):
    # number of observations/points 
    n = np.size(x)

    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector 
    y_pred = b[0] + b[1] * x

    # plotting the regression line 
    plt.plot(x, y_pred, color="g")

    # putting labels 
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot 
    plt.show()


def plot(data, year, season):
    x = np.array(get_year_range(data, year))
    y = np.array(get_season_data(data, year, season))

    # estimating coefficients
    b = estimate_coef(x, y)

    # plotting regression line
    # plot_regression_line(x, y, b)
    return b[0] + b[1] * year


def predict_month(data, year, mm):
    x = np.array(get_year_range(data, year))
    y = np.array(get_month_data(data, year, mm))
    b = estimate_coef(x, y)

    return b[0] + b[1] * year

