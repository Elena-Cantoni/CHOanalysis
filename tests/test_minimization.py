import numpy as np
import pandas as pd
import sys
sys.path.append('./')
import minimization

def test_differences():
    """
    TEST
    -------
    - If it returns a positive result despite negative variable

    """
    assert minimization.differences(0.5, -0.8) > 0
    assert minimization.differences(-0.8, -0.8) == 0
    

def test_tot_distances():
    """
    TEST
    -------
    - If it returns a matrix
    - If it returns the correct matrix dimension
    - If the word 'alpha' is the first column name in files1
    - If y-dimension matrix is smaller than a bigger taken alpha value 
    - If the length of the first column of files1 is equal to alpha+human
    
    """
    
    m_d = np.ndarray((3,3,9))
    files1 = pd.DataFrame([['a1','a'],['a2','b'],['a3','.c'],['h1','d'],['h2','e'],
                          ['h3','f']], columns= ['alpha', 'P'])
    np.random.seed(0)
    df_alpha1 = pd.DataFrame(np.random.random_sample((9,6)),columns = ['a1','a2','a3','h1','h2','h3'])
    d = (1,2,3,4,5,6,7,8,9)
    df_alpha1.insert(0,'D',d)
    alpha = 3
    human = 3
    m_dist = minimization.tot_distances(m_d, files1, alpha, df_alpha1)
    assert isinstance(m_dist,np.ndarray) == True
    assert m_dist.shape == (alpha,human,9)
    assert 'alpha'  in files1.columns[0]
    assert 5 > m_dist.shape[1]
    assert len(files1['alpha']) == alpha + human
        

def test_weighted_sum():
    """
    TEST
    -------
    - If it returns a float value
    - If the weighting factor is in [0,1]
    - If it returns a positive value
    - If it returns a non zero value
    - If (element * w factor) is smaller that the element value
    - If it returns a value smaller that the simple sum of dist row
    
    """
    np.random.seed(0)
    dist = np.array(np.random.random_sample((9,)))
    w= 0.3
    d_tot = minimization.weighted_sum(w,dist)
    assert isinstance(d_tot, float) == True
    assert 0 < w < 1
    assert d_tot > 0 
    assert d_tot != 0
    assert dist[8]*w < dist[8]
    assert d_tot < sum(dist)
    

# def test_tot_weighted_sum():
    
#     m_sum_w_dist = np.nd array
        
