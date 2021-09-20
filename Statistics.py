import os
import sys
path_interaction = os.path.dirname(os.path.abspath(__file__))
if path_interaction not in sys.path:
    sys.path.append(path_interaction)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import functions

#depickling and .npy loading
df_sum_w_dist = pd.read_pickle(path_interaction + '/pkl/df_sum_w_dist.pkl')    
df_protocol_curvemin = pd.read_pickle(path_interaction + '/pkl/protocol_curvemin.pkl')
files = pd.read_pickle(path_interaction + '/pkl/files.pkl')
df_alpha = pd.read_pickle(path_interaction + '/pkl/df_alpha.pkl')
alpha_s = pd.read_pickle(path_interaction + '/pkl/alpha_s.pkl')
human_s = pd.read_pickle(path_interaction + '/pkl/human_s.pkl')
path_s = np.load(path_interaction + '/pkl/path_s.npy',allow_pickle=True)
num_alpha = np.load(path_interaction + '/pkl/num_alpha.npy')
txt = np.load(path_interaction + '/pkl/txt.npy')
    
        
""" Correlation parameters of each CHO curve wrt reference observer curve """

m_correlation = np.ndarray((((len(files['alpha'])- int(num_alpha))),5,int(num_alpha)))
#alpha_s = np.ndarray((Contrast_detail.num_alpha,),object)
hum = -1
for human in np.array(files['alpha'][int(num_alpha):]):
    hum +=1
    for a in range(0,int(num_alpha)):
        alpha = files['alpha'][a]
        col_alpha = df_alpha[alpha]
        #alpha_s[a] = alpha
        corr = functions.correlation(df_alpha[human], col_alpha)
        m_correlation[hum,:,a] = corr


""" Minimization distance parameters identification (slope, intercept and standard deviation of linear fit) related to observer curves """

#3-D array filled with indexes of  the alpha-dependent CHO curves which minimize as much as possibile the distances with human reference curve. 
min_index_curve = np.ndarray((len(files['alpha'])-int(num_alpha),),dtype=int)
ind =-1
    
for hum in np.array(files['alpha'][int(num_alpha):]):
    #print(hum)
    ind +=1    
    min_index = df_sum_w_dist[hum].idxmin()
    #print(min_index)
    min_index_curve[ind] = min_index
    
#matrix and dataframe of intercept and slope extracted parameters related to the minimizing CHO curve for each human curve 
hum_linpar = np.ndarray((3,len(human_s)))
df_hum_linpar = pd.DataFrame(hum_linpar,columns=human_s, index = ['slope','intercept','std'])    
h = -1
for z in range(0,len(files['alpha'])-int(num_alpha)):
    h +=1
    slope = m_correlation[h][0][min_index_curve[z]]
    intercept = m_correlation[h][1][min_index_curve[z]]
    stderr = m_correlation[h][2][ min_index_curve[z]]
    hum_linpar[0][h]=slope
    hum_linpar[1][h]=intercept
    hum_linpar[2][h]=stderr


''' Mean and standard deviation between different human observations of the same image sample '''

#matrix filled with mean and std of the same contrasted point seen by different observers
points_mean_std = np.ndarray((len(df_alpha['diam']),2))

for points in range(0,len(df_alpha['diam'])):   
    mean = np.mean(df_alpha.iloc[points][int(num_alpha)+1:])
    points_mean_std[points,0] = mean 
    h = 0
    m_diff = np.ndarray((len(df_alpha['diam']),len(human_s)))
    for hum in range(0,len(human_s)):
        #print(mean)
        h +=1
        diff_square = (df_alpha.iloc[points][int(num_alpha)+h]-mean)**2
        m_diff[points,hum] = diff_square
    std = np.sqrt(sum(m_diff[points,:])/(len(human_s)-1))
    std_mean = std/np.sqrt(len(human_s)-1)
    points_mean_std[points,1] = std     
    

""" CHO curve which minimizes the mean observer curve """

points_diff = np.ndarray((int(num_alpha),len(df_alpha)))
n_col =-1
for col in np.array(files['alpha'][:int(num_alpha)]) :
    n_col +=1
    #print('numero colonna ',n_col,' ',col)
    for row in range(0,len(df_alpha)):
        #print('numero riga ',row)
        dist = functions.differences(df_alpha[col][row],points_mean_std [row,0])
        points_diff[n_col][row]=dist 

points_sum_dist = np.ndarray((int(num_alpha),1))
df_points_sum_dist = pd.DataFrame(points_sum_dist)
for col in range(0,int(num_alpha)):
    #print('col ',col)
    s = functions.weighted_sum(points_diff[col])
    points_sum_dist[col,0] = s
        
points_curvemin = functions.minimum(df_alpha,df_points_sum_dist ,range(0,1),alpha_s)#files['alpha'][num_alpha:], files['alpha'])
series_points_curvemin = pd.Series(points_curvemin[:,0])

#correlation
hum_points_corr = functions.correlation(points_mean_std[:,0],series_points_curvemin)


""" Plotting the linearity between CHO minimum visible contrast points and human minimum visible contrast points, the error bar of each measure and the uncertainty of the fit are shown. """

plt.figure(figsize=(10,8))
plt.plot(series_points_curvemin,hum_points_corr[0] *points_curvemin+hum_points_corr[1],c ='k', lw = 5, label = 'linear fit')

plt.fill_between(series_points_curvemin,((hum_points_corr[0]+hum_points_corr[2])*series_points_curvemin+hum_points_corr[1]),
                 ((hum_points_corr[0]-hum_points_corr[2])*series_points_curvemin+hum_points_corr[1]), color = 'darkgrey', alpha = 0.2, label= 'uncertainty region')

plt.errorbar(series_points_curvemin,points_mean_std[:,0],points_mean_std[:,1],fmt ='.',color='gray', elinewidth=3, capsize = 5)
plt.plot(series_points_curvemin,points_mean_std[:,0],'.',color = 'k',mew=4, markersize=12, label = 'averaged points')
# lin_col = ['red','blue','green','yellow','pink']
# h = -1
# for curve in np.array(files['alpha'][num_alpha:]):
#     h +=1
#     plt.plot(df_protocol_curvemin[h] , df_alpha[curve],'X',c = lin_col[h], markersize=10,  label = curve)
plt.title('Linear fit, operation between points '+ str(txt)[5:][:-4], fontsize=15)
plt.xlabel('CHO minimum visible contrast', fontsize=15)
plt.ylabel('Human minimum visible contrast', fontsize=15)
plt.legend(fontsize=15)


""" Plotting the mean CD curve with the relative points errorbars and the best associated CHO curve """

fig,ax = plt.subplots(figsize=(12,9))
lin_col = ['red','blue','green','yellow','pink']
colors = -1
for c_d_h in path_s[(int(num_alpha)+1):]:
    colors +=1
    ax.plot(df_alpha['diam'],df_alpha[c_d_h],c = lin_col[colors],marker='o',linestyle='-', linewidth=3,alpha = 0.6)
ax.plot(df_alpha['diam'],points_mean_std[:,0],c = 'black',marker='o',linestyle='-', markersize= 10,linewidth=4,label= 'averaged CD observer curve')
ax.plot(df_alpha['diam'],series_points_curvemin,'--o',c = 'firebrick',linewidth=2, label='CHO curve')
ax.errorbar(df_alpha['diam'],points_mean_std[:,0],points_mean_std[:,1],fmt ='.',ecolor='gray', elinewidth=3, capsize = 5)
#ax.set_xlim(0.6,4.1)
#ax.set_ylim(0,0.175)
ax.set_title('Averaged CD curve '+ str(txt)[5:][:-4], fontsize=15)
ax.legend(fontsize= 15)
plt.show()