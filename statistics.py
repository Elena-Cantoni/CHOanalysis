import sys
#path where interactions between codes happen, change it with your local path
sys.path.append('C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import linregress
from Contrast_detail import files,df_alpha,a_val
from minimization import df_sum_w_dist

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
    intercept : TYPE
        DESCRIPTION.
    r_value : TYPE
        DESCRIPTION.
    std_err : TYPE
        DESCRIPTION.

    """
    r_corr = pearsonr(ref,alphas)
    slope, intercept, r_value, p_value, std_err = linregress(alphas,ref)
    return  slope, intercept,r_value,p_value,std_err


m_correlation = np.ndarray((5,a_val))
alpha_s = np.ndarray((a_val,),object)
for a in range(0,a_val):
    alpha = files['alpha'][a]
    col_alpha = df_alpha[alpha]
    alpha_s[a] = alpha
    corr = correlation(df_alpha['human curve'], col_alpha)
    corr = np.array(corr)
    print(corr)
    m_correlation[:,a] = corr
df_correlation = pd.DataFrame(m_correlation, columns = alpha_s, 
                              index = ['slope','intercept','r value','p value','std_err'])
