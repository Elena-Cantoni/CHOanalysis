"""Functions script """

import numpy as np
from scipy.stats import linregress


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


def weighted_sum (weight,dist):#weight
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
    #central distances are weighted differently wrt the external distances,
    #it depends on the position of the disk in the phantom
    if len(dist) ==9:
        ind_ex = [6,7,8]
        ind_int =[0,1,2,3,4,5]
    elif len(dist) ==10:
        ind_ex = [0,7,8,9]
        ind_int =[1,2,3,4,5,6]
    elif len(dist) ==11:
        ind_ex = [0,1,8,9,10]
        ind_int =[2,3,4,5,6,7]
    else:
        ind_ex = [0,1,2,9,10,11]
        ind_int =[3,4,5,6,7,8]
        
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


def minimum (dataset, dist_set, list_humans, list_alphas):
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
    curve_min_alpha : matrix including the CD dataset referred to each human observer

    """
    curve_min_alpha = np.ndarray((len(dataset),len(list_humans)))
    print('Minimum distance curves:\n')
    n_hum = -1
    for hum in list_humans:#np.array(files['alpha'][num_alpha:]):
        n_hum +=1
        min_index=dist_set[hum].idxmin()
        min_alpha = list_alphas[min_index]
        min_dist =min(dist_set[hum])
        print(hum, ':\t',min_alpha,' curve',', distance:',min_dist)
        curve_min_alpha[:,n_hum]= dataset[min_alpha]
        
        
    return curve_min_alpha


def correlation(h_dataset, a_dataset, humans, alphas):
    """
    Estimates the correlation parameters obtained between human and CHO model response. 
    A least-squares regression method is used.
    The results are collected in a matrix.

    Parameters
    ----------
    h_dataset : CD human curve dataframe
    a_dataset : CD CHO curve dataframe
    humans : series of the title names of the observer curves
    alphas : series of the title names of the different CHO curves with different alpha

    Returns
    -------
    corr : 3-D matrix containing correlation parameters (n° humans, n° parameters,°n alphas)

    """
    #if len(humans),len(alphas) >1
    corr = np.ndarray(
    (((len(humans))), 5, len(alphas)))
#alpha_s = np.ndarray((Contrast_detail.num_alpha,),object)
    hum = -1
    for h in humans:
        hum += 1
        al =-1
        for a in alphas:
            al += 1
            #col_alpha = dataset[a]
            #print(col_alpha)
            #alpha_s[a] = alpha
            slope, intercept, r_value, p_value, std_err = linregress(a_dataset[a],h_dataset[h])
            parameters = (slope, intercept, r_value, p_value, std_err)
            corr[hum, :, al] = parameters
    
    # slope, intercept, r_value, p_value, std_err = linregress(alphas,human_ref)
    return  corr
#not used
def fit_correlation (m,x,q, test):
    """
    Extracts the linear fit between Observer and preferred CHO curve using the slope and intercept parameters. 

    Parameters
    ----------
    m : Slope factor
    x : CHO alpha-dependent curve dataset
    q : Intercept factor
    test : Human reference curve index

    Returns
    -------
    y : Linear fitting
    mean_m : Slope's arithmetic mean ( all the selected slopes of each single observer curve are used)
    mean_q : Intercept's arithmetic mean ( all the selected intercepts of each single observer curve are used)

    """
    y = m[0,test]*x + q[1,test]
    mean_m = sum(m[0,:])/len(m[0,:])
    mean_q = sum(q[1,:])/len(q[1,:])
    mean_std = np.mean(m[2,:])
        
    return y, mean_m, mean_q, mean_std

