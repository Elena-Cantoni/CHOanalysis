import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #for plotting



#csv about nominal diameter and contrast and human 75% contrast visibility
txt_acq_95_27_norm = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/data/cd_acq_95_27_norm.txt"
txt_acq_95_22_norm = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/data/cd_acq_95_22_norm.txt"
txt_acq_95_22_med = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/data/cd_acq_95_22_med.txt"
txt_acq14_5_12 = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/cd_acq14_5_12.txt"
files = pd.read_csv(txt_acq_95_27_norm, delimiter = "=")
path = [files['path']]
path = path[0]

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
fig,ax = plt.subplots(figsize=(12,9))
for c_d in path_s[1:-1]:
    ax.plot(df_alpha['diam'],df_alpha[c_d],'--o')
ax.plot(df_alpha['diam'],df_alpha['human curve'],'r-o', lw = 2.5)
ax.set_title('Contrast-detail curve', fontsize=16,)
ax.set_xlabel('Diameter (mm)',fontsize=12)
ax.set_ylabel('Contrast',fontsize=12)
ax.legend(path_s[1:],fontsize='x-large')
plt.show()




