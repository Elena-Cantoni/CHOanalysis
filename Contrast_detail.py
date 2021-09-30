
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # for plotting
import sys
import os
# import tkinter
from tkinter import Tk, Button
from tkinter.filedialog import askdirectory, askopenfilename
# the following path indicate the dierectiry where the files' interaction happens
path_interaction = os.path.dirname(os.path.abspath(__file__))
if path_interaction not in sys.path:
    sys.path.append(path_interaction)

parent = Tk()
# Create a button that will destroy the main window when clicked
exit_button = Button(parent, text='Continue', command=parent.destroy)
exit_button.pack()

local_data_path = askdirectory(parent=parent, title='Select data folder')

#local_data_path = os.path.join(path_interaction , "data")
os.environ["USERPROFILE"] = local_data_path

txt = askopenfilename(parent=parent, title='Select .txt file')
parent.mainloop()

loc = txt.find('cd')
files = pd.read_csv(txt, delimiter="=")
path = [files['path']]
path = path[0]

for n_p in range(0, len(path)):
    p = os.path.expanduser(path[n_p])

    p = os.path.expanduser(path[n_p])
    files['path'][n_p] = p

path_s = [np.append(['diam'], [files['alpha']])]
path_s = path_s[0]

for a in range(0, len(path_s)-1):
    if "alpha" in path_s[a]:
        num_alpha = path_s[a]
        num_alpha = a

alpha_s = [files['alpha'][:num_alpha]]
alpha_s = alpha_s[0]
human_s = [files['alpha'][num_alpha:]]
human_s = human_s[0]

# contrast matrix at different alpha
m_contrast = np.ndarray

# contrast matrix filling
for p in range(0, len(files['path'])):

    a = pd.read_csv(files['path'][0])

    if p == 0:
        m_contrast = np.ndarray((len(a), len(files['path'])+1))

    col = np.array(a['Nominal Diameter (mm)'])
    m_contrast[:, 0] = col

    a = pd.read_csv(files['path'][p])
    col = np.array(a)
    m_contrast[:, p+1] = col[:, 1]

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
#plt.show(block = False)
plt.show()
