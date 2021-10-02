import os
import sys
import numpy as np
import pandas as pd
# the following path indicate the directory where the files' interaction happens
path_interaction = os.path.dirname(os.path.abspath(__file__))
if path_interaction not in sys.path:
    sys.path.append(path_interaction)
import functions

# depickling and .npy loading
files = pd.read_pickle(path_interaction + '/pkl/files.pkl')
df_alpha = pd.read_pickle(path_interaction + '/pkl/df_alpha.pkl')
alpha_s = pd.read_pickle(path_interaction + '/pkl/alpha_s.pkl')
human_s = pd.read_pickle(path_interaction + '/pkl/human_s.pkl')
num_alpha = np.load(path_interaction + '/pkl/num_alpha.npy')
txt = np.load(path_interaction + '/pkl/txt.npy')
loc = str(txt).find('cd')

""" Distances' estimation between CHO and human points referred to the same diameter """

# matrix filled with distance estimation between CHO curve points and human curve points
m_distances = np.ndarray(
    (((len(files['alpha'])-num_alpha)), num_alpha, len(df_alpha)))
# loops to fill the matrix with the distances between human and CHO measurements for each human respectively
n_hum = -1
for humans in np.array(files['alpha'][int(num_alpha):]):
    n_hum += 1
    #print('numero umano ',n_hum)
    n_col = -1
    for col in np.array(files['alpha'][:int(num_alpha)]):
        n_col += 1
        #print('numero colonna ',n_col,' ',col)
        for row in range(len(df_alpha)):
            #print('numero riga ',row)
            dist = functions.differences(
                df_alpha[col][row], df_alpha[humans][row])
            m_distances[n_hum][n_col][row] = dist

""" Weighted sum estimation for each curve """

# matrix and dataframe of weighted sum of distances
sum_w_dist = np.ndarray((num_alpha, (len(files['alpha'])-num_alpha)))
df_sum_w_dist = pd.DataFrame(
    sum_w_dist, columns=files['alpha'][int(num_alpha):])
# weighted sum loop
for hum in range((len(files['alpha'])-num_alpha)):
    for col in range(num_alpha):
        s = functions.weighted_sum(0.2, m_distances[hum][col])
        sum_w_dist[col][hum] = s


""" Definition of minimum alpha needed to have a CHO curve most similar to human curve for each observer """

print('Acquisition ', str(txt)[loc:][:-4])
protocol_curvemin = functions.minimum(
    df_alpha, df_sum_w_dist, human_s, alpha_s)
df_protocol_curvemin = pd.DataFrame(protocol_curvemin)

# pickling and npy saving
df_sum_w_dist.to_pickle(path_interaction + '/pkl/df_sum_w_dist.pkl')
df_protocol_curvemin.to_pickle(
    path_interaction + '/pkl/df_protocol_curvemin.pkl')
np.save(path_interaction + '/pkl/m_distances.npy', m_distances)
