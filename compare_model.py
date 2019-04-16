import linear_regression as l_r
import knn
import utils
import numpy as np

def get_lr_comparison(data, year):
    # return average accuracy based on year
        # exp. get lr for 2019, get difference with data from 2018 real and lr 2018 return average difference percentage
    winter = l_r.plot(data, year, 'winter')
    spring = l_r.plot(data, year, 'spring')
    summer = l_r.plot(data, year, 'summer')
    autumn = l_r.plot(data, year, 'autumn')

    real_winter = knn.construct_season_avg_max(data, year, 'winter')
    real_spring = knn.construct_season_avg_max(data, year, 'spring')
    real_summer = knn.construct_season_avg_max(data, year, 'summer')
    real_autumn = knn.construct_season_avg_max(data, year, 'autumn')

    winter_accuracy = abs(winter - real_winter)
    spring_accuracy = abs(spring - real_spring)
    summer_accuracy = abs(summer - real_summer)
    autumn_accuracy = abs(autumn - real_autumn)

    return utils.mean([winter_accuracy,spring_accuracy,summer_accuracy,autumn_accuracy])


def get_knn_comparison(data, year):
    winter = knn.calculate_knn_forcast(data, 5, year, 'winter')
    spring = knn.calculate_knn_forcast(data, 5, year, 'spring')
    summer = knn.calculate_knn_forcast(data, 5, year, 'summer')
    autumn = knn.calculate_knn_forcast(data, 5, year, 'autumn')

    real_winter = knn.construct_season_avg_max(data, year, 'winter')
    real_spring = knn.construct_season_avg_max(data, year, 'spring')
    real_summer = knn.construct_season_avg_max(data, year, 'summer')
    real_autumn = knn.construct_season_avg_max(data, year, 'autumn')

    winter_accuracy = abs(winter - real_winter)
    spring_accuracy = abs(spring - real_spring)
    summer_accuracy = abs(summer - real_summer)
    autumn_accuracy = abs(autumn - real_autumn)

    return utils.mean([winter_accuracy, spring_accuracy, summer_accuracy, autumn_accuracy])


def produce_comparision(data, year):
    data = [get_lr_comparison(data, int(year)-1), get_knn_comparison(data, int(year)-1)] #get the most accurate

    if data[0] < data[1]:
        return 'lr'
    elif data[1] < data[0]:
        return 'knn'

    return ''
    # plot the best with a prompt to tell the user which has been chosen
