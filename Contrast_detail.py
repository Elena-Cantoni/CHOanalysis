import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #for plotting
import os.path


#csv about nominal diameter and contrast and human 75% contrast visibility
txt_acq_95_27_norm  = "~/cd_acq_95_27_norm.txt"
txt_acq_95_22_norm = "~/cd_acq_95_22_norm.txt"
txt_acq_95_22_med = "~/cd_acq_95_22_med.txt"
txt_FL_LAAG_0001 = "~/cd_FL_LAAG_0001.txt"
txt_FL_LAAG_0002 = "~/cd_FL_LAAG_0002.txt"
txt_CORO_LAAG_0003 = "~/cd_CORO_LAAG_0003.txt"
txt_CORO_LAAG_0004 = "~/cd_CORO_LAAG_0004.txt"
#txt_acq14_5_12 = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/cd_acq14_5_12.txt"

#change the following path with the folder local path on your personal computer
local_path = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/data"
#local_path1 = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis"
os.environ["HOME"] = local_path
files = pd.read_csv(txt_CORO_LAAG_0004, delimiter = "=")
path = [files['path']]
path = path[0]

for n_p in range(0,len(path)):
    p = os.path.expanduser(path[n_p])
    
    #os.environ["HOME"] = local_path
    p = os.path.expanduser(path[n_p])
    files['path'][n_p] = p

path_s = [np.append(['diam'],[files['alpha']])] 
path_s = path_s[0]

# contrast matrix at different alpha
m_contr = np.ndarray

# dataframe filling
for p in range(0,len(files['path'])):
    
    a = pd.read_csv(files['path'][0])
    
    if p == 0:
        m_contr = np.ndarray((len(a),len(files['path'])+1))
        
    col = np.array(a['Nominal Diameter (mm)'])
    m_contr[:,0] = col
    
    a = pd.read_csv(files['path'][p])
    col = np.array(a)                                                   
    m_contr[:,p+1] = col[:,1]

# contrast dataframe changing alpha, first col = diameters
df_alpha = pd.DataFrame(m_contr, columns = path_s) 
    
# plotting
for a in range(0,len(path_s)-1):
    if "alpha" in path_s[a]:
        a_val = path_s[a]
        a_val = a

fig,ax = plt.subplots(figsize=(12,9))
for c_d in path_s[1:a_val+1]:# -1
    ax.plot(df_alpha['diam'],df_alpha[c_d],'--o')
lin_col = ['red','blue','green','yellow']
colors = -1
for c_d_h in path_s[(a_val+1):]:
    colors +=1
    ax.plot(df_alpha['diam'],df_alpha[c_d_h],c = lin_col[colors],marker='o',linestyle='-', linewidth=3)
ax.set_title('Contrast-detail curve', fontsize=16,)
ax.set_xlabel('Diameter (mm)',fontsize=12)
ax.set_ylabel('Contrast',fontsize=12)
ax.legend(path_s[1:],fontsize='x-large')
plt.show()




