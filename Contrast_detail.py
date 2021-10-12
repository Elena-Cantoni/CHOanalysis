import numpy as np
import pandas as pd


def strings(path_txt):
    """
    Extracts data from external files and organises their nomenclature 

    Parameters
    ----------
    path_txt : txt path string

    Returns
    -------
    files : txt dataframe
    num_alpha : int value representing the number of rows where the word 'alpha' appears
    path_s :  titles list in dataframe
    alpha_s : alpha names series in dataframe
    human_s : human names series in dataframe

    """
    files = pd.read_csv(path_txt, delimiter="=")
    path = [files['path']]
    path = path[0]
    path_s = [np.append(['diam'], [files['alpha']])]
    path_s = path_s[0]

    for a in range(len(path_s)-1):
        if "alpha" in path_s[a]:
            # ATTENTION! num_alpha defined only if "alpha" is in path_s[a] for some a
            num_alpha = path_s[a]
            num_alpha = a

    alpha_s = [files['alpha'][:num_alpha]]
    alpha_s = alpha_s[0]
    human_s = [files['alpha'][num_alpha:]]
    human_s = human_s[0]

    return files, num_alpha, path_s, alpha_s, human_s


def cd_dataframe(m_contr, txt_files, names_string):
    """
    Generates a contrast-detail dataframe containing all the external data (from .csv files) 
    that are contrasts for each diameter relative to the results obtained from human observers 
    and from the application of the CHO model varying the alpha noise parameter.

    Parameters
    ----------
    m_contr : empty matrix to be filled
    txt_files : txt dataframe
    names_string : titles list in dataframe

    Returns
    -------
    cd_df : contrast-detail curve dataframe

    """
    a_df = pd.read_csv(txt_files['path'][0])
    col_0 = np.array(a_df['Nominal Diameter (mm)'])
    m_contr[:, 0] = col_0

    for p in range(len(txt_files['path'])):
        a = pd.read_csv(txt_files['path'][p])
        cols = np.array(a)
        m_contr[:, p+1] = cols[:, 1]

    # contrast dataframe changing alpha, first col = diameters
    cd_df = pd.DataFrame(m_contr, columns=names_string)

    return cd_df
