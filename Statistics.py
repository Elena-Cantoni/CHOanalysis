import pandas as pd
import numpy as np
import minimization
from scipy.stats import linregress


def meanstd_curve(df_cd, n_alpha, list_humans):
    """
    Estimates mean and standard deviation points between different human observations of the same image sample.

    Parameters
    ----------
    df_cd : contrast-detil curve dataframe
    n_alpha : int value representing the number of rows where the word 'alpha' appears
    list_humans : series of the title names of the observer curves

    Returns
    -------
    points_mean_std : matrix filled with mean and std of the same diameter points seen by different observers
    df_points_mean_std : dataframe filled with mean and std of the same diameter points seen by different observers

    """
    points_mean_std = np.ndarray((len(df_cd['diam']), 2))
    if len(list_humans) == 1:
        dof = 0
    else: 
        dof = 1
    for points in range(len(df_cd['diam'])):
        mean = np.mean(df_cd.iloc[points][int(n_alpha)+1:])
        points_mean_std[points, 0] = mean
        std = np.std(df_cd.iloc[points][int(n_alpha)+1:],ddof = dof)
        points_mean_std[points, 1] = std

    df_points_mean_std = pd.DataFrame(points_mean_std, columns=['mean', 'std'])

    return points_mean_std, df_points_mean_std


def meanobs_minimization(df_cd, p_mean_std, txt_files, n_alpha, list_alphas, w):
    """
    Finds CHO curve which minimizes the mean observer curve

    Parameters
    ----------
    df_cd : contrast-detil curve dataframe
    p_mean_std : dataframe filled with mean and std of the same diameter points seen by different observers
    txt_files : txt dataframe
    n_alpha : int value representing the number of rows where the word 'alpha' appears
    list_alphas : alpha names series in dataframe
    w : weighting factor

    Returns
    -------
    df_points_curvemin : dataframe including the minimizing CD dataset referred to each human observer
    df_table_points_curvemin : dataframe of minimum distances curves and the referred weighted distances

    """
    m_points_diff = np.ndarray((int(n_alpha), len(df_cd)))
    points_diff = minimization.tot_distances(m_points_diff,txt_files,n_alpha,df_cd,p_mean_std)

    m_points_sum_dist = np.ndarray((int(n_alpha), 1))
    df_points_sum_dist = minimization.tot_weighted_sum(m_points_sum_dist,points_diff,txt_files, n_alpha,w)
    
    df_points_curvemin, df_table_points_curvemin = minimization.minimum(df_cd, df_points_sum_dist, range(
        0, 1), list_alphas)

    return df_points_curvemin, df_table_points_curvemin


def correlation(h_dataset, a_dataset, humans, alphas):
    """
    Estimates the correlation parameters obtained between human and CHO model response. 
    A least-squares regression method is used.
    The results are collected in a dataframe.

    Parameters
    ----------
    h_dataset : CD human curve dataframe
    a_dataset : CD CHO curve dataframe
    humans : series of the title names of the observer curves
    alphas : series of the title names of the different CHO curves with different alpha

    Returns
    -------
    df_corr : 3-D matrix containing correlation parameters (n° humans, n° parameters,°n alphas)

    """
    corr = np.ndarray(
        (len(humans), 5, len(alphas)))
    hum = -1
    for h in humans:
        hum += 1
        al = -1
        for a in alphas:
            al += 1
            slope, intercept, r_value, p_value, std_err = linregress(
                a_dataset[a], h_dataset[h])
            parameters = (slope, intercept, r_value, p_value, std_err)
            corr[hum, :, al] = parameters

    return corr
