import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  
from tkinter import Tk, Button     # for opening dialog windows
from tkinter.filedialog import askdirectory, askopenfilename
# the following path indicate the directory where the files' interaction happens
path_interaction = os.path.dirname(os.path.abspath(__file__))

""" Dialog windows selection and environmental variable's manipulation to read incoming document """

parent = Tk()
# Create a button that will destroy the main window when clicked
exit_button = Button(parent, text='Click me to continue', command=parent.destroy)
exit_button.pack()

local_data_path = askdirectory(parent=parent, title='Select data folder')

os.environ["USERPROFILE"] = local_data_path     # on Windows
os.environ["HOME"] = local_data_path            # on Linux

txt = askopenfilename(parent=parent, title='Select .txt file')
parent.mainloop()

loc = txt.find('cd')
files = pd.read_csv(txt, delimiter="=")
path = [files['path']]
path = path[0]

for n_p in range(len(path)):
    p = os.path.expanduser(path[n_p])
    files['path'][n_p] = p

path_s = [np.append(['diam'], [files['alpha']])]
path_s = path_s[0]

for a in range(len(path_s)-1):
    if "alpha" in path_s[a]:
        num_alpha = path_s[a]   #ATTENTION! num_alpha defined only if "alpha" is in path_s[a] for some a
        num_alpha = a

alpha_s = [files['alpha'][:num_alpha]]
alpha_s = alpha_s[0]
human_s = [files['alpha'][num_alpha:]]
human_s = human_s[0]

""" Creation of a dataframe of contrasts for each diameter relative to the results obtained from
 human observers and from the application of the CHO model varying the alpha noise parameter. """

a_df = pd.read_csv(files['path'][0])
m_contrast = np.ndarray((len(a_df),len(files['path'])+1))
col_0 = np.array(a_df['Nominal Diameter (mm)'])      
m_contrast[:, 0] = col_0

for p in range(len(files['path'])):
    a = pd.read_csv(files['path'][p])
    cols = np.array(a)
    m_contrast[:, p+1] = cols[:, 1]
    
# contrast dataframe changing alpha, first col = diameters
df_alpha = pd.DataFrame(m_contrast, columns=path_s)

# pickling and npy saving
files.to_pickle(path_interaction + '/pkl/files.pkl')
df_alpha.to_pickle(path_interaction + '/pkl/df_alpha.pkl')
alpha_s.to_pickle(path_interaction + '/pkl/alpha_s.pkl')
human_s.to_pickle(path_interaction + '/pkl/human_s.pkl')
np.save(path_interaction + '/pkl/path_s.npy', path_s)
np.save(path_interaction + '/pkl/num_alpha.npy', num_alpha)
np.save(path_interaction + '/pkl/txt.npy', txt)

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
ax.set_title('Contrast-detail curve ' + txt[loc:][:-4], fontsize=16,)
ax.set_xlabel('Diameter (mm)', fontsize=12)
ax.set_ylabel('Contrast', fontsize=12)
ax.legend(path_s[1:], fontsize='16')
# ax.set_ylim(0,0.15)
plt.show()
