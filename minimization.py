import sys
#path where interactions between codes happen, change it with your local path
path_interaction = 'C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis'
sys.path.append(path_interaction)
import numpy as np
import pandas as pd
import Contrast_detail
#from Contrast_detail import path_interaction,a_val, path_s, alpha_s,human_s


#depickling
files = pd.read_pickle(path_interaction + '/pkl/files.pkl')
df_alpha = pd.read_pickle(path_interaction +'/pkl/df_alpha.pkl')



#df_distance = pd.DataFrame(distances,columns=files['alpha'])
#index = -(len(path_s)-1-a_val)#(len(files['alpha'])-a_val)


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
    diff = abs(cho_point - hum_point)
    
    return diff

def weighted_sum (dataset,centr,d):
    """
    
    Makes a weighted sum of all the distances between two curves

    Parameters
    ----------
    dataset : dataset of interest
    centr : weighting factor  which multiplies the central point values
    d :  pandas dataframe distance column

    Returns
    -------
    d_tot : float value which represents the total weighted sum of points distances 

    """
    #each distance is weighted differently, it depends on the position of the disk in the phantom
    if len(dataset) ==9:
        ind_ex = [6,7,8]
        ind_int =[0,1,2,3,4,5]
    elif len(dataset) ==10:
        ind_ex = [0,7,8,9]
        ind_int =[1,2,3,4,5,6]
    elif len(dataset) ==11:
        ind_ex = [0,1,8,9,10]
        ind_int =[2,3,4,5,6,7]
    else:
        ind_ex = [0,1,2,9,10,11]
        ind_int =[3,4,5,6,7,8]
        
    d_centr = sum(centr*d[ind_int])
    mean_centr = d_centr/len(ind_int)
    weights = np.array
    for w in ind_ex:
        w_element = mean_centr/d[w]
        weights = [np.append(w_element,weights)]
    weights = np.delete(weights[0],-1)  
    d_ext = sum(weights*d[ind_ex]) 
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
    list_humans : list of the title names of the observer curves
    list_alphas : list of the title names of the different CHO curves with different alpha

    Returns
    -------
    curve_min_alpha : matrix including the CD dataset referred to each human observer

    """
    curve_min_alpha = np.ndarray((len(dataset),len(list_humans)))
    print('Minimum distance curves:\n')
    n_hum = -1
    for hum in list_humans:#np.array(files['alpha'][a_val:]):
        n_hum +=1
        min_index=dist_set[hum].idxmin()
        min_alpha = list_alphas[min_index]
        print(min_alpha)
        min_dist =min(dist_set[hum])
        print(hum, ':\t',min_alpha,' curve',', distance:',min_dist)
        curve_min_alpha[:,n_hum]= dataset[min_alpha]
        
        
    return curve_min_alpha, min_alpha

#matrix filled with distance estimation between CHO curve points and human curve points
distances = np.ndarray((((len(files['alpha'])-a_val)),Contrast_detail.a_val,len(df_alpha)))
# loops to fill the matrix with the distances between human and CHO measurement for each human respectively
n_hum = -1
for humans in np.array(files['alpha'][Contrast_detail.a_val:]):
    n_hum +=1
    #print('numero umano ',n_hum)
    n_col = -1
    for col in np.array(files['alpha'][:Contrast_detail.a_val]) :
        n_col +=1
        #print('numero colonna ',n_col,' ',col)
        for row in range(0,len(df_alpha)):
            #print('numero riga ',row)
            dist = differences(df_alpha[col][row],df_alpha[humans][row])
            distances[n_hum][n_col][row]=dist
            

#matrix and dataframe of weighted sum of distances
sum_w_dist = np.ndarray((Contrast_detail.a_val,(len(files['alpha'])-Contrast_detail.a_val)))
df_sum_w_dist  = pd.DataFrame(sum_w_dist ,columns=files['alpha'][Contrast_detail.a_val:])#files['alpha'][a_val:])
#weighted sum loop
for hum in range(0,(len(files['alpha'])-Contrast_detail.a_val)):
    #print('hum ',hum)
    for col in range(0,Contrast_detail.a_val):#-1
        #print('col ',col)
        s = weighted_sum(df_alpha,1,distances[hum][col])
        #print(s)
        sum_w_dist[col][hum] = s
        


#definition of minimum alpha needed to have a CHO curve most similar to human curve for each observer
print('Acquisition ', txt[5:][:-4])
protocol_curvemin = minimum(df_alpha,df_sum_w_dist,Contrast_detail.human_s,Contrast_detail.alpha_s)#files['alpha'][a_val:], files['alpha'])
df_protocol_curvemin = pd.DataFrame(protocol_curvemin[0])

#serialization of a Python object structure (dataframes), conversion into a byte stream.
df_sum_w_dist.to_pickle(path_interaction +'/pkl/min_dist.pkl')    
df_protocol_curvemin.to_pickle(path_interaction +'/pkl/protocol_curvemin.pkl') 



