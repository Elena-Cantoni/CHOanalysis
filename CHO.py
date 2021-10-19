import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Contrast_detail
import minimization
import Statistics


txt = Path(sys.argv[1])

# External data and name organization
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)

# Contrast-detail dataframe creation
len_df = len(pd.read_csv(files['path'][0]))
m_contrast = np.ndarray((len_df, len(files['path'])+1))
df_alpha = Contrast_detail.cd_dataframe(m_contrast, files, path_s)

# Distances matrix
m_distances = np.ndarray(
    (((len(files['alpha'])-num_alpha)), num_alpha, len(df_alpha)))
m_distances = minimization.tot_distances(
    m_distances, files, num_alpha, df_alpha)

# Weighted sums dataframe
sum_w_dist = np.ndarray((num_alpha, (len(files['alpha'])-num_alpha)))
w = 0.1
df_sum_w_dist = minimization.tot_weighted_sum(
    sum_w_dist, m_distances, files, num_alpha, w)

# Definition of minimum alpha needed to have a CHO curve most similar to human curve for each observer
df_protocol_curvemin, df_table_curvemin = minimization.minimum(
    df_alpha, df_sum_w_dist, human_s, alpha_s)

# Mean and std observer's curve dataframe
points_mean_std, df_points_mean_std = Statistics.meanstd_curve(
    df_alpha, num_alpha, human_s)
# mean observer curve minimization
df_points_curvemin, df_table_points_curvemin = Statistics.meanobs_minimization(
    df_alpha, points_mean_std, files, num_alpha, alpha_s, w)

# Correlation parameters estimated from the averaged human curve
corr = Statistics.correlation(
    df_points_mean_std, df_points_curvemin, pd.Series(
        df_points_mean_std.columns[0]),
    pd.Series(df_points_curvemin.columns[0]))
df_hum_points_corr = pd.DataFrame(corr[0, :, :], index=[
                           'slope', 'intercept', 'r value', 'p value', 'std'])


s_txt = str(sys.argv[1])
# print(type(s_txt))
loc = s_txt.find('cd')

""" Plotting every CHO and human curve for the specified protocol """

fig, ax = plt.subplots(figsize=(12, 9))
for c_d in path_s[1:num_alpha+1]:  # -1
    ax.plot(df_alpha['diam'], df_alpha[c_d], '--o')
lin_col = ['red', 'blue', 'green', 'yellow', 'pink']
colors = -1
for c_d_h in path_s[(num_alpha+1):]:
    colors += 1
    ax.plot(df_alpha['diam'], df_alpha[c_d_h],
            c=lin_col[colors], marker='o', linestyle='-', linewidth=3)
ax.set_title('Contrast-detail curve ' + s_txt[loc:][:-4], fontsize=16,)
ax.set_xlabel('Diameter (mm)', fontsize=12)
ax.set_ylabel('Contrast', fontsize=12)
ax.legend(path_s[1:], fontsize='16')
# ax.set_ylim(0,0.15)
plt.show()

print('\n', 'Acquisition ', s_txt[loc:][:-4], '\n',
      'Minimum distance curves:\n', '\n', df_table_curvemin)

""" Plotting the linearity between CHO minimum visible contrast points and human minimum visible contrast points, 
the error bar of each measure and the uncertainty of the fit are shown. """

plt.figure(figsize=(10, 8))
plt.plot(df_points_curvemin[0],
          df_hum_points_corr[0]['slope'] * df_points_curvemin[0]+df_hum_points_corr[0]['intercept'], c='k', lw=5, label='linear fit')

plt.fill_between(df_points_curvemin[0],
                  ((df_hum_points_corr[0]['slope']+df_hum_points_corr[0]['std'])
                  * df_points_curvemin+df_hum_points_corr[0]['intercept'])[0],
                  ((df_hum_points_corr[0]['slope']-df_hum_points_corr[0]['std'])
                  * df_points_curvemin+df_hum_points_corr[0]['intercept'])[0],
                  color='darkgrey', alpha=0.2, label='uncertainty region')

plt.errorbar(df_points_curvemin[0],
              df_points_mean_std['mean'], df_points_mean_std['std'], fmt='.', color='gray', elinewidth=3, capsize=5)

plt.plot(df_points_curvemin[0],
          df_points_mean_std['mean'], '.', color='k', mew=4, markersize=12, label='averaged points')
# lin_col = ['red','blue','green','yellow','pink']
# h = -1
# for curve in np.array(files['alpha'][num_alpha:]):
#     h +=1
#     plt.plot(df_protocol_curvemin[h] , df_alpha[curve],'X',c = lin_col[h], markersize=10,  label = curve)
plt.title('Linear fit, operation between points ' +
          s_txt[loc:][:-4], fontsize=15)
plt.xlabel('CHO minimum visible contrast', fontsize=15)
plt.ylabel('Human minimum visible contrast', fontsize=15)
plt.legend(fontsize=15)

plt.show()

""" Plotting the mean CD curve with the relative points errorbars and the best associated CHO curve """

fig, ax = plt.subplots(figsize=(12, 9))
lin_col = ['red', 'blue', 'green', 'yellow', 'pink']
colors = -1
for c_d_h in path_s[(int(num_alpha)+1):]:
    colors += 1
    ax.plot(df_alpha['diam'], df_alpha[c_d_h], c=lin_col[colors],
            marker='o', linestyle='-', linewidth=3, alpha=0.6)
ax.plot(df_alpha['diam'], points_mean_std[:, 0], c='black', marker='o',
        linestyle='-', markersize=10, linewidth=4, label='averaged CD observer curve')
ax.plot(df_alpha['diam'], df_points_curvemin[0], '--o',
        c='firebrick', linewidth=2, label=df_table_points_curvemin['min alpha curve'][0] + ' CHO curve')
ax.errorbar(df_alpha['diam'], points_mean_std[:, 0], points_mean_std[:,
            1], fmt='.', ecolor='gray', elinewidth=3, capsize=5)
ax.set_title('Averaged CD curve ' + s_txt[loc:][:-4], fontsize=15)
ax.legend(fontsize=15)
plt.show()

print('\n', df_table_points_curvemin['min alpha curve'][0],
      ' is the CHO curve that minimizes the averaged observers curve.')
