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
df_sum_w_dist_pkl = pd.read_pickle(path_interaction + '/pkl/min_dist.pkl')    
df_protocol_curvemin_pkl = pd.read_pickle(path_interaction + '/pkl/protocol_curvemin.pkl')
files = pd.read_pickle(path_interaction + '/pkl/files.pkl')
df_alpha = pd.read_pickle(path_interaction +'/pkl/df_alpha.pkl')
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



'''Mean and standard deviation between different human observations of the same image sample '''

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
    

""" CHO curve which minimizes the mean observer curve """

points_diff = np.ndarray((a_val,len(df_alpha)))
n_col =-1
for col in np.array(files['alpha'][:a_val]) :
    n_col +=1
    #print('numero colonna ',n_col,' ',col)
    for row in range(0,len(df_alpha)):
        #print('numero riga ',row)
        dist = differences(df_alpha[col][row],points_mean_std [row,0])
        points_diff[n_col][row]=dist 

points_sum_dist = np.ndarray((a_val,1))
df_points_sum_dist = pd.DataFrame(points_sum_dist)
for col in range(0,a_val):#-1
    #print('col ',col)
    s = weighted_sum(df_alpha,1,points_diff[col])
    #print(s)
    points_sum_dist[col,0] = s
        
points_curvemin = minimum(df_alpha,df_points_sum_dist ,range(0,1),alpha_s)#files['alpha'][a_val:], files['alpha'])

#correlation
hum_points_corr = correlation(points_mean_std[:,0],df_alpha[points_curvemin[1]])

""" Plotting the linearity between CHO minimum visible contrast points and human minimum visible contrast points, 
#the error bar of each measure and the uncertainty of the fit are shown. """

plt.figure(figsize=(10,8))
plt.plot(df_alpha[points_curvemin[1]],hum_points_corr[0] *df_alpha[points_curvemin[1]]+hum_points_corr[1],c ='k', lw = 5, label = 'linear fit')
plt.fill_between(df_alpha[points_curvemin[1]],((hum_points_corr[0]+hum_points_corr[2])*df_alpha[points_curvemin[1]]+hum_points_corr[1]),
                 ((hum_points_corr[0]-hum_points_corr[2])*df_alpha[points_curvemin[1]]+ hum_points_corr[1]), color = 'darkgrey', alpha = 0.2, label= 'uncertainty region')
plt.errorbar(df_alpha[points_curvemin[1]],points_mean_std[:,0],points_mean_std[:,1],fmt ='.',color='gray', elinewidth=3, capsize = 5)
plt.plot(df_alpha[points_curvemin[1]],points_mean_std[:,0],'.',color = 'k',mew=4, markersize=12, label = 'averaged points')
# lin_col = ['red','blue','green','yellow','pink']
# h = -1
# for curve in np.array(files['alpha'][a_val:]):
#     h +=1
#     plt.plot(df_protocol_curvemin_pkl[h] , df_alpha[curve],'X',c = lin_col[h], markersize=10,  label = curve)
plt.title('Linear fit, operation between points', fontsize=15)
plt.xlabel('CHO minimum visible contrast', fontsize=15)
plt.ylabel('Human minimum visible contrast', fontsize=15)
plt.legend(fontsize=15)

""" Plotting the mean CD curve with the relative points errorbars and the best associated CHO curve """

fig,ax = plt.subplots(figsize=(12,9))
lin_col = ['red','blue','green','yellow','pink']
colors = -1
for c_d_h in path_s[(a_val+1):]:
    colors +=1
    ax.plot(df_alpha['diam'],df_alpha[c_d_h],c = lin_col[colors],marker='o',linestyle='-', linewidth=3,alpha = 0.7)
ax.plot(df_alpha['diam'],points_mean_std[:,0],c = 'black',marker='o',linestyle='-', markersize= 10,linewidth=4,label= 'averaged CD observer curve')
ax.plot(df_alpha['diam'],df_alpha[points_curvemin[1]],'--o',c = 'orange', label='CHO ' + points_curvemin[1]+ ' curve')
ax.errorbar(df_alpha['diam'],points_mean_std[:,0],points_mean_std[:,1],fmt ='.',ecolor='gray', elinewidth=3, capsize = 5)
#ax.set_xlim(0.6,4.1)
#ax.set_ylim(0,0.175)
ax.legend(fontsize= 15)