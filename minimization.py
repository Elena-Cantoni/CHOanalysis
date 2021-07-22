import sys
import numpy as np
import pandas as pd
from Contrast_detail import files,df_alpha

#path where interactions between codes happen
#sys.path.append('C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis')


#distance estimation between CHO curve points and human curve points
distances = np.ndarray((len(df_alpha),len(df_alpha.columns)-1))
df_distance = pd.DataFrame(distances,columns=files['alpha'])


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


# loop to fill the dataframe with the distances    
for col in np.array(files['alpha']) : 
    for row in range(0,len(df_alpha)):
        dist = differences(df_alpha[col][row],df_alpha['human curve'][row])
        df_distance[col][row]=dist
        
df_distance.insert(0,'diam',df_alpha['diam']) 
del df_distance['human curve'] 

if len(df_alpha) ==10:
    ind_ex = [8,9]
    ind_int =[0,1,2,3,4,5,6,7]
elif len(df_alpha) ==11:
    ind_ex = [0,9,10]
    ind_int =[1,2,3,4,5,6,7,8]
else:
    ind_ex = [0,1,10,11]
    ind_int =[2,3,4,5,6,7,8,9]
    
def weighted_sum (centr,d):
    """
    
    Makes a weighted sum of all the distances between 

    Parameters
    ----------
    centr : weighting factor  which multiplies the central point values
    d :  pandas dataframe distance column

    Returns
    -------
    d_tot : float value which represents the total weighted sum of points distances 

    """
    
    
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
#,weights, s_centr, s_ext

sum_w_dist = np.array#(range(0,len(files['alpha'])))

for col in np.array(files['alpha'][:-1]):

    s = weighted_sum(1,df_distance[col])
    sum_w_dist = [np.append(s,sum_w_dist)]
    
sum_w_dist = list(np.delete(sum_w_dist[0],-1))
sum_w_dist = sorted(sum_w_dist, reverse=True)

df_sum_w = pd.DataFrame(sum_w_dist,index = files['alpha'][:-1])
#df_sum_w = pd.Index(files['alpha'])
#df_sum_w.insert(0,'alpha',files['alpha'])

min_curve=df_sum_w[0].idxmin()
print("Minimum distance: ",min(df_sum_w[0]))#,' with ', min_curve)


