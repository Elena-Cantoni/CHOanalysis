import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #for plotting

#csv about nominal diameter and contrast and human 75% contrast visibility
p1e5 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_1.5_5_12.csv"
p5 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_5_5_12.csv"
p10 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_10_5_12.csv"
p15 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_15_5_12.csv"
p30 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_30_5_12.csv"
pCD ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/Hum_Acq14_CD_5_12.csv"

s_path = ['diam','p1e5','p5','p10','p15','p30','pCD']  
path = [p1e5,p5,p10,p15,p30,pCD] #to be adapted 

# matrice dei contrasti a diversi alfa
m_contr = np.ndarray((12,len(path)+1)) 
# dataframe dei contrasti a diversi alpha, prima col = diametri
df_alpha = pd.DataFrame(m_contr, columns = s_path) 

for p in path:
    a = pd.read_csv(path[0])
    col = np.array(a['Nominal Diameter (mm)'])#iloc[:,0])
    print(col)
    m_contr[:,0] = col
    a = pd.read_csv(p)
    col = np.array(a.iloc[:,1])                                                     ################################################à
    m_contr[:,path.index(p)+1] = col

#num_plots = len(m_contr[1,:])-1    
#colormap = plt.cm.gist_ncar
#plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots)))) 


n_plots = len(m_contr[1,:])
fig,ax = plt.subplots(figsize=(12,9))
for c_d in range(1,n_plots):
    print(c_d)
    ax.plot(df_alpha[0],df_alpha[c_d],'--o')#,label = 'Alpha = 1.5') #1.5
ax.plot(df_alpha[0],df_alpha[n_plots-1],'r-o', lw = 2.5)#,label = 'Alpha = 1.5') #1.5
