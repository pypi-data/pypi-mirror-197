"""
This module contains functions that operate in the dataframe
created based on GDAS/ECMWF analysis data
"""
import pandas as pd
import numpy as np
from statsmodels import robust


#@deprecated
def select_dataframe_epoch(dataframe_atmo_profile, epoch_text):
    """Select data for a specific epoch"""
    epoch = get_epoch(epoch_text)
    new_dataframe_atmo_profile = dataframe_atmo_profile[dataframe_atmo_profile.month.isin(epoch)]
    return new_dataframe_atmo_profile


#@deprecated
def select_dataframe_by_year(dataframe_atmo_profile, years):
    """Select data for specific years"""
    new_dataframe_atmo_profile = dataframe_atmo_profile[dataframe_atmo_profile.year.isin(years)]
    return new_dataframe_atmo_profile


#@deprecated
def select_dataframe_by_month(dataframe_atmo_profile, months):
    """Select data for specific months"""
    new_dataframe_atmo_profile = dataframe_atmo_profile[dataframe_atmo_profile.month.isin(months)]
    return new_dataframe_atmo_profile


#@deprecated
def select_dataframe_by_hour(dataframe_atmo_profile, hours):
    """Select data for specific hours"""
    new_dataframe_atmo_profile = dataframe_atmo_profile[dataframe_atmo_profile.hour.isin(hours)]
    return new_dataframe_atmo_profile


# TODO move to doc/examples
def create_wind_speed_dataframe(dataframe_atmo_profile, normalized=False):
    """
    Function to create a wind speed dataframe in order to plot it afterwards as a wind rose plot

    :param dataframe_atmo_profile: dataframe containing wind direction information
    :param normalized (optional):
    :return: dataframe_atmo_profile_winds
    """
    wd_centre_bins = np.arange(7.5, 360, 15)
    ws_hist = []
    for d in wd_centre_bins:
        ws_hist.append(
            np.histogram(
                dataframe_atmo_profile.wind_speed[
                    (dataframe_atmo_profile.wind_direction >= d - 7.5)
                    & (dataframe_atmo_profile.wind_direction < d + 7.5)
                ],
                bins=[0, 5, 10, 20, 30, 40, 50, 100],
            )[0]
        )

    dataframe_atmo_profile_winds = pd.DataFrame(
        columns=["wind_direction", "0-5", "5-10", "10-20", "20-30", "30-40", "40-50", "> 50"]
    )
    ws_new_list = []
    for j in range(len(ws_hist[0])):
        li = []
        for i in range(len(ws_hist)):
            li.append(ws_hist[i][j])
        ws_new_list.append(li)

    for i, j in zip(dataframe_atmo_profile_winds.keys()[1:], range(len(ws_new_list))):
        dataframe_atmo_profile_winds[i] = ws_new_list[j]
    if normalized:
        dataframe_atmo_profile_winds_normalized = dataframe_atmo_profile_winds.div(
            dataframe_atmo_profile_winds.sum(axis=1), axis=0
        )
        dataframe_atmo_profile_winds_normalized["wind_direction"] = wd_centre_bins
        return dataframe_atmo_profile_winds_normalized
    else:
        dataframe_atmo_profile_winds["wind_direction"] = wd_centre_bins
        return dataframe_atmo_profile_winds


# TODO refactor
def compute_averages_std_simple(input_array):
    """
    This function computes the average, standard deviation and peak to peak (plus and minus)
    for an input 1D array

    Input:
        1-D input_array (array-like)

    Output:
        average, stand_dev, peak_to_peak_p, peak_to_peak_m (array-like)
    """

    average = np.average(input_array)
    stand_dev = robust.mad(input_array)
    peak_to_peak_p = np.max(input_array) - np.average(input_array)
    peak_to_peak_m = np.average(input_array) - np.min(input_array)
    return average, stand_dev, peak_to_peak_p, peak_to_peak_m


# TODO refactor
def avg_std_dataframe(group, param):
    """

    :param group: dataframe grouped by a certain parameter
    :param param: the parameter by which the dataframe is grouped
    :return:
        avg: the mean value for each grouped level
        std: the standard deviation for each grouped level
        mad: the mean absolute deviation for each group level
        p2p_p: the peak-to-peak maximum value for each grouped level
        p2p_m: the peak-to-peak minimum value for each grouped level
    """

    avg = group[param].mean()
    std = group[param].std()
    mad = group[param].mad()
    p2p_p = group[param].max() - avg
    p2p_m = avg - group[param].min()

    return avg, std, mad, p2p_p, p2p_m


# TODO refactor
def compute_averages_std(input_array):
    """
    This function computes the average, standard deviation and peak to peak (plus and minus)
    for a multidimensional input array

    Input: input_array (array-like)

    Output: average, stand_dev, peak_to_peak_p, peak_to_peak_m (all array-like)
    """

    average = []
    stand_dev = []
    peak_to_peak_p = []
    peak_to_peak_m = []

    if len(np.shape(input_array)) == 1:
        average.append(np.average(input_array))
        stand_dev.append(robust.mad(input_array))
        peak_to_peak_p.append(np.max(input_array - np.average(input_array)))
        peak_to_peak_m.append(np.average(input_array) - np.min(input_array))
    else:
        r = len(input_array[0])
        for i in np.arange(r):
            average.append(np.average(input_array[:, i]))
            stand_dev.append(robust.mad(input_array[:, i]))
            peak_to_peak_p.append(np.max(input_array[:, i] - np.average(input_array[:, i])))
            peak_to_peak_m.append(np.average(input_array[:, i]) - np.min(input_array[:, i]))

    average = np.asarray(average)
    stand_dev = np.asarray(stand_dev)
    peak_to_peak_p = np.asarray(peak_to_peak_p)
    peak_to_peak_m = np.asarray(peak_to_peak_m)
    return average, stand_dev, peak_to_peak_p, peak_to_peak_m
