import sys
#path where interactions between codes happen, change it with your local path
sys.path.append('C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import linregress
from Contrast_detail import *#files,df_alpha,a_val,path_s,alpha_s,human_s
from minimization import protocol_curvemin#files, a_val,sum_w_dist,df_sum_w_dist
path_interaction = 'C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis'
sum_w_dist_pkl = pd.read_pickle(path_interaction + '/min_dist.pkl')    
df_protocol_curvemin_pkl = pd.read_pickle(path_interaction + '/protocol_curvemin.pkl')
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
    slope, intercept, r_value, p_value, std_err = linregress(alphas,ref)
    return  slope, intercept,r_value,p_value,std_err       
        

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
        #corr = np.array(corr)
        #print(corr)
        m_correlation[hum,:,a] = corr

