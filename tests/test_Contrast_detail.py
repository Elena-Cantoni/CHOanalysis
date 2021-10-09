import numpy as np
import pandas as pd
import sys
sys.path.append('./')
import Contrast_detail


def test_cd_dataframe():
    """
    

    TEST
    -------
    -If it returns the correct dimensions
    -If 'path_s1' length is equal to the number of rows of 'contr' and it is smaller fo one wrt the length of the dataframe 'files1'
    -If the first dataframe column is named 'diam'
    
    """
    #np.random.seed(0)
    contr = np.ndarray((9,9))
    files = pd.DataFrame([['alpha1','./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_1e5a.csv'],
                          ['alpha2','./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_2e5a.csv'],
                          ['alpha3','./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_5a.csv'],
                          ['alpha4','./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_10a.csv'],
                          ['alpha5','./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_15a.csv'],
                          ['h1','./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_Elena.csv'],
                          ['h2','./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_Marco03092021.csv'],
                          ['h3','./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_Valeria.csv']], columns= ['alpha', 'path'])
    path_s = pd.Series(['diam','alpha1','alpha2','alpha3','alpha4','alpha5','h1','h2','h3'])
    path_s2 = pd.Series(['diam','a1','a2','a3','a4','a5','h1','h2','h3'])  
    
    df_alpha = Contrast_detail.cd_dataframe(contr, files, path_s)
    
    assert df_alpha.shape == (9,9)
    assert len(path_s) == contr.shape[0] == len(files)+1
    assert df_alpha.columns[0] == 'diam'