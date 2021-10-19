import numpy as np
import pandas as pd
import sys
sys.path.append('./')
import Contrast_detail
import minimization


"""differences testing """

def test_differences_positivevals():
    """
    TEST
    -------
    - If it returns a positive result 
    - If it returns a positive result despite two negative variables

    """
    assert minimization.differences(0.5, 0.8) > 0
    assert minimization.differences(-0.8, -0.5) > 0

def test_differences_equalzero():
    """
    TEST
    -------
    - If it returns zero giving two equal negative variables

    """
    assert minimization.differences(-0.8, -0.8) == 0
    

""" tot_distances testing """

def test_tot_distances_matrdim():
    """
    TEST
    -------
    - If it returns a matrix
    - If it returns the correct matrix dimension

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df)
        assert isinstance(m_dist,np.ndarray) 
        assert m_dist.shape == (len(results[2])-results[1]-1,results[1],len(cd_df))

def test_tot_distances_matrvals():
    """
    TEST
    -------
    - If all matrix elements from a specific dataframe are equal to 0.5
    - If all matrix elements from a zero-valued dataframe are equal to 0.0

    """
        
    results = Contrast_detail.strings('./documents/example_csv/pathtxt2.txt')
    m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
    cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
    m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
    m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df)
    for hum in range(len(results[0]['alpha'])-results[1]):
        for alpha in range(results[1]):    
            assert all(m_dist[hum,alpha,:] == 0.5)
    zeros = pd.DataFrame(np.zeros((len(pd.read_csv(results[0]['path'][0])),len(results[0]['path'])+1)),columns =results[2])
    m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
    m_dist = minimization.tot_distances(m_dist,results[0],results[1],zeros)
    for hum in range(len(results[0]['alpha'])-results[1]):
        for alpha in range(results[1]):    
            assert all(m_dist[hum,alpha,:] == 0.0)
        

""" weighted_sum testing """

def test_weighted_sum_analysisvals():
    """
    TEST

    Returns
    -------
    - If w_sum_1 return a float value
    - If w_sum_0 return a float value
    - If w_sum_1 is bigger than zero
    - If w_sum_0 in equal to zero
    

    """
    w = 0.1
    for length in range(9,13):
        row_1 = np.ones(length)
        row_0 = np.zeros(length)
        w_sum_1 = minimization.weighted_sum(w,row_1)
        w_sum_0 = minimization.weighted_sum(w,row_0)
        assert isinstance(w_sum_1, float)
        assert isinstance(w_sum_0, float)
        assert w_sum_1 > 0 
        assert w_sum_0 == 0 

def test_weighted_sum_sums():
    """
    TEST
    -------
    - If the simple sum of the elements is higher than their weighted sum

    """
    w = 0.1
    for length in range(9,13):
        row_1 = np.ones(length)
        w_sum_1 = minimization.weighted_sum(w,row_1)
        simple_sum = np.sum(row_1)
        assert w_sum_1 < simple_sum

def test_weighted_sum_wfactor():
    """
    TEST
    -------
    - If the weighting factor = 0, the sum does not count the values multiplied by w

    """
    row_1 = np.ones(9)
    w_sum_1 = minimization.weighted_sum(0,row_1)
    assert w_sum_1 == 6
   
    
""" tot_weighted_sum testing """

def test_tot_weighted_sum_vals():
    """
    TEST
    -------
    - If it returns elements values equal or bigger than zero

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        assert df_sum_w_dist.values.all() >= 0

def test_tot_weighted_sum_titles():
    """
    TEST
    -------
    - If dataframe columns names are the humans' list
    - If dataframe rows names are the alphas' list
    
    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        print(list(df_sum_w_dist.index))
        assert all(df_sum_w_dist.columns == results[4])
        assert all(df_sum_w_dist.index == range(results[1]))
        
def test_tot_weighted_sum_dim():
    """
    TEST
    -------
    - If sum dataframe dimension is equal to the number of input data
    
    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        assert len(results[0]) == df_sum_w_dist.shape[0] + df_sum_w_dist.shape[1]    

def test_tot_weighted_sum_correctwsum():
    """
    TEST
    -------
    - If the single elemements in sum_w_dist dataframe are equal to the the weighted sum of a specific distance matrix row

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        h = -1
        for hum in np.array(results[4]):
            h += 1
            for a in range(results[1]):
                w_sum = minimization.weighted_sum(0.1,m_dist[h][a][:])
                assert df_sum_w_dist[hum][a] == w_sum
            
    
""" minimum testing """

def test_minimum_dim():
    """
    TEST
    -------
    - If min_tab return the correct dimensions
    - If min_cd return the correct dimensions
    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        assert min_tab.shape == (len(results[4]),2)
        assert min_cd.shape == (len(cd_df),len(results[4]))
    
    
def test_minimum_colexist():
    """
    TEST
    -------
    - If the columns in min_df are present in contrast-detail dataframe titled 'alpha...'

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        for h in range(len(results[4])):
            assert any(all(min_cd[h] == cd_df[i]) for i in results[3])

def test_minimum_mincheck():
    """
    TEST

    Returns
    -------
    - If the selected distance in min_tab really exists
    - If the distance in min_tab is really the minimum one

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        d = -1
        for h in results[4]:
            d += 1
            assert min_tab['distance'][d] in df_sum_w_dist[h].values
            assert all(min_tab['distance'][d] <= i for i in df_sum_w_dist[h])
    
def test_minimum_titlesexist():
    """
    TEST
    -------
    - If strings in min_tab first column are contained in list_alphas

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        assert min_tab['min alpha curve'].any() in results[3] 
        
def test_minimum_correctdist():
    """
    TEST

    Returns
    -------
    - If the distances in min_tab correspond to the correct float values in df_sum_w_dist

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        for h in np.array(results[4]):
            alpha = min_tab['min alpha curve'][h]
            ind = results[3].tolist().index(alpha)
            assert min_tab['distance'][h] == df_sum_w_dist[h][ind]

def test_minimum_consistency():
    """
    TEST
    -------
    - If the the strings in min_tab are the titles of datasets in min_cd associated to the same human

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        m_dist = np.ndarray(((len(results[0]['alpha'])-results[1]), results[1], len(cd_df)))
        m_dist = minimization.tot_distances(m_dist,results[0],results[1],cd_df) 
        m_sum_w_dist = np.ndarray((results[1],len(results[4])))
        df_sum_w_dist = minimization.tot_weighted_sum(m_sum_w_dist,m_dist,results[0], results[1],0.1)
        min_cd, min_tab = minimization.minimum(cd_df,df_sum_w_dist,results[4],results[3])
        h_ind = -1
        for h in np.array(results[4]):
            h_ind += 1
            assert all(cd_df[min_tab['min alpha curve'][h]] == min_cd[h_ind])
    
