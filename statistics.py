import sys
#path where interactions between codes happen, change it with your local path
sys.path.append('C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import linregress
from Contrast_detail import *#files,df_alpha,a_val,path_s,alpha_s,human_s
from minimization import *#files, a_val,sum_w_dist,df_sum_w_dist

path_interaction = 'C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis'
df_sum_w_dist_pkl = pd.read_pickle(path_interaction + '/min_dist.pkl')    
df_protocol_curvemin_pkl = pd.read_pickle(path_interaction + '/protocol_curvemin.pkl')
files = pd.read_pickle(path_interaction + '/files.pkl')
df_alpha = pd.read_pickle(path_interaction +'/df_alpha.pkl')
#studying correlation between human and CHO model
def correlation(ref, alphas):
    """
    Estimates the correlation parameters obtained between human and CHO model response. 
    A least-squares regression method is used

    Parameters
    ----------
    ref : human curve datasets
    alphas : CHO curve datasets with different alpha

    Returns
    -------
    slope : Slope of the regression line
    intercept : Intercept of the regression line
    r_value : Correlation factor
    std_err : Standard Deviation of the estimated slope

    """
    r_corr = pearsonr(ref,alphas)
    slope, intercept, r_value, p_value, std_err= linregress(alphas,ref)
    return  slope, intercept,std_err,r_value,p_value

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
    
        
#### correlation parameters of each CHO curve wrt reference observer curve
m_correlation = np.ndarray((((len(files['alpha'])-a_val)),5,a_val))
alpha_s = np.ndarray((a_val,),object)
hum = -1
for human in np.array(files['alpha'][a_val:]):
    hum +=1
    #print(hum)
    for a in range(0,a_val):
        alpha = files['alpha'][a]
        col_alpha = df_alpha[alpha]
        alpha_s[a] = alpha
        corr = correlation(df_alpha[human], col_alpha)
        m_correlation[hum,:,a] = corr


#### minimization distance parameters identification (slope and intercept of linear fit) related to observer curves        
#3-D array filled with indexes of  the alpha-dependent CHO curves which minimize as much as possibile the distances with human reference curve. 
min_index_curve = np.ndarray((len(files['alpha'])-a_val,),dtype=int)
ind =-1
    
for hum in np.array(files['alpha'][a_val:]):
    print(hum)
    ind +=1    
    min_index = df_sum_w_dist_pkl[hum].idxmin()
    print(min_index)
    min_index_curve[ind] = min_index
    
#matrix and dataframe of intercept and slope extracted parameters related to the minimizing CHO curve for each human curve 
hum_linpar = np.ndarray((3,len(human_s)))
df_hum_linpar = pd.DataFrame(hum_linpar,columns=human_s, index = ['slope','intercept','std'])    
h = -1
for z in range(0,len(files['alpha'])-a_val):
    h +=1
    slope = m_correlation[h][0][ min_index_curve[z]]
    intercept = m_correlation[h][1][ min_index_curve[z]]
    stderr = m_correlation[h][2][ min_index_curve[z]]
    #print(m_correlation[h][0][ min_index_curve[z]])
    #print(m_correlation[h][1][ min_index_curve[z]])
    hum_linpar[0][h]=slope
    hum_linpar[1][h]=intercept
    hum_linpar[2][h]=stderr



'''Mean and standard deviation between different human observations of the same image sample'''

#matrix filled with mean and std of the same contrasted point seen by different observers
points_mean_std = np.ndarray((len(df_alpha['diam']),2))

for points in range(0,len(df_alpha['diam'])):
    #print(points)    
    mean = np.mean(df_alpha.iloc[points][a_val+1:])
    points_mean_std[points,0] = mean 
    h = 0
    m_diff = np.ndarray((len(df_alpha['diam']),len(human_s)))
    for hum in range(0,len(human_s)):
        #print(mean)
        h +=1
        diff_square = (df_alpha.iloc[points][a_val+h]-mean)**2
        m_diff[points,hum] = diff_square
    std = np.sqrt(sum(m_diff[points,:])/(len(human_s)-1))
    std_mean = std/np.sqrt(len(human_s)-1)
    points_mean_std[points,1] = std     

