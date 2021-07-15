import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #for plotting
import timeit

# execution time function 
def func_t():
    pass

#csv about nominal diameter and contrast and human 75% contrast visibility
#p1e5 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_1.5_5_12.csv"
#p5 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_5_5_12.csv"
#p10 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_10_5_12.csv"
#p15 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_15_5_12.csv"
#p30 ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/CHO_Acq14_30_5_12.csv"
#pCD ="D://TESI_TIROCINIO/CHO_EFOMP_2021/GE_Discovery740/14/Hum_Acq14_CD_5_12.csv"
txt_acq14_5_12 = "C://Users/canto/Google Drive/UNIBO MAGISTRALE_/Software and computing for applied physics/CHOanalysis/cd_acq14_5_12.txt"
files = pd.read_csv(txt_acq14_5_12, delimiter = "=")
path = [files['path']]
path = path[0]

s_path = ['diam','alpha = 1.5','alpha = 5','alpha = 10','alpha = 15','alpha = 30','hum']  
#path = [p1e5,p5,p10,p15,p30,pCD] #to be adapted 

# contrast matrix at different alpha
m_contr = np.ndarray((12,len(files['path'])+1)) 
# contrast dataframe changing alpha, first col = diameters
df_alpha = pd.DataFrame(m_contr, columns = s_path) 

# dataframe filling
for p in range(1,len(files['path'])):
    a = pd.read_csv(files['path'][0])
    col = np.array(a['Nominal Diameter (mm)'])
    m_contr[:,0] = col
    a = pd.read_csv(files['path'][p])
    col = np.array(a)                                                   
    m_contr[:,p+1] = col[:,1]
    
# plotting
fig,ax = plt.subplots(figsize=(12,9))
for c_d in s_path[1:-1]:
    ax.plot(df_alpha['diam'],df_alpha[c_d],'--o')
ax.plot(df_alpha['diam'],df_alpha['hum'],'r-o', lw = 2.5)
ax.set_title('Contrast-detail curve', fontsize=16,)
ax.set_xlabel('Diameter (mm)',fontsize=12)
ax.set_ylabel('Contrast',fontsize=12)
ax.legend(s_path[1:],fontsize='x-large')

execution_time = timeit.timeit(func_t, number=1)
print(execution_time)


