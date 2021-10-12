import numpy as np
import pandas as pd


def differences(cho_point, hum_point):
    """
    Computes the difference between corrispective points of CHO and human curves  

    Parameters
    ----------
    cho_point : pandas dataframe element, CHO curve point varying alpha value
    hum_point : pandas dataframe element, human curve point

    Returns
    -------
    diff : absolute value of the distance between the two point of interest

    """
    diff = np.abs(cho_point - hum_point)

    return diff


def tot_distances(m_dist, txt_files, n_alpha, df_cd):
    """
    Estimates matrix filled with distances between CHO and human points referred to the same diameter.

    Parameters
    ----------
    m_dist : empty matrix to be filled
    txt_files : txt dataframe
    n_alpha : int value representing the number of rows where the word 'alpha' appears
    df_cd : contrast-detil curve dataframe

    Returns
    -------
    m_dist : distances 3D-matrix (humans,alpha curves,diameters)

    """
    n_hum = -1
    for humans in np.array(txt_files['alpha'][int(n_alpha):]):
        n_hum += 1
        n_col = -1
        for col in np.array(txt_files['alpha'][:int(n_alpha)]):
            n_col += 1
            for row in range(len(df_cd)):
                dist = differences(
                    df_cd[col][row], df_cd[humans][row])
                m_dist[n_hum][n_col][row] = dist

    return m_dist


def weighted_sum(weight, dist):  # weight
    """

    Makes a weighted sum of all the distances between two curves

    Parameters
    ----------

    weight = float weighting value
    dist :  matrix distance row

    Returns
    -------
    d_tot : float value which represents the total weighted sum of points distances 

    """
    # central distances are weighted differently wrt the external distances,
    # it depends on the position of the disk in the phantom
    if len(dist) == 9:
        ind_ex = [6, 7, 8]
        ind_int = [0, 1, 2, 3, 4, 5]
    elif len(dist) == 10:
        ind_ex = [0, 7, 8, 9]
        ind_int = [1, 2, 3, 4, 5, 6]
    elif len(dist) == 11:
        ind_ex = [0, 1, 8, 9, 10]
        ind_int = [2, 3, 4, 5, 6, 7]
    else:
        ind_ex = [0, 1, 2, 9, 10, 11]
        ind_int = [3, 4, 5, 6, 7, 8]

    d_centr = sum(dist[ind_int])
    mean_centr = d_centr/len(ind_int)
    #weights = np.array
    # for w in ind_ex:
    #     w_element = mean_centr/dist[w]
    #     weights = [np.append(weights,w_element)]
    # weights = np.delete(weights[0],0)
    d_ext = sum(weight*dist[ind_ex])
    #d_ext = len(ind_ex)*mean_centr
    d_tot = d_centr+d_ext

    return d_tot


def tot_weighted_sum(m_sum_w_dist, m_dist, txt_files, n_alpha, w):
    """
    Estimates weighted sum of the distances for each curve and fills a dataframe

    Parameters
    ----------
    m_sum_w_dist : empty matrix to be filled
    m_dist : distances 3D-matrix
    txt_files : txt dataframe
    n_alpha : int value representing the number of rows where the word 'alpha' appears
    w = weighing factor

    Returns
    -------
    df_sum_w_dist : weighted sums dataframe

    """
    # weighted sum loop
    for hum in range((len(txt_files['alpha'])-n_alpha)):
        for col in range(n_alpha):
            s = weighted_sum(w, m_dist[hum][col])
            m_sum_w_dist[col][hum] = s
    df_sum_w_dist = pd.DataFrame(
        m_sum_w_dist, columns=txt_files['alpha'][int(n_alpha):])

    return df_sum_w_dist


def minimum(dataset, dist_set, list_humans, list_alphas):
    """
    Extracts the CHO Contrast-detail curve for which the correspective distance with the Human CD curve 
    is the minimum one. The operation is done using every human curve

    Parameters
    ----------
    dataset : CD curve dataframe
    dist_set : dataframe of weighted distance sums
    list_humans : series of the title names of the observer curves
    list_alphas : series of the title names of the different CHO curves with different alpha

    Returns
    -------
    df_curve_min_alpha : dataframe including the minimizing CD dataset referred to each human observer
    df_table_table_curvemin : dataframe of minimum distances curves and the referred weighted distances

    """
    curve_min_alpha = np.ndarray((len(dataset), len(list_humans)))
    table_curvemin = np.ndarray((len(list_humans), 2), dtype=object)

    n_hum = -1
    for hum in list_humans:
        n_hum += 1
        min_index = dist_set[hum].idxmin()
        min_alpha = list_alphas[min_index]
        min_dist = min(dist_set[hum])
        table_curvemin[n_hum, 0] = min_alpha
        table_curvemin[n_hum, 1] = min_dist
        df_table_curvemin = pd.DataFrame(
            table_curvemin, columns=['min alpha curve', 'distance'], index=list_humans)
        curve_min_alpha[:, n_hum] = dataset[min_alpha]
        df_curve_min_alpha = pd.DataFrame(curve_min_alpha)

    return df_curve_min_alpha, df_table_curvemin
