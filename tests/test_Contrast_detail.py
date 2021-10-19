import numpy as np
import pandas as pd
import sys
sys.path.append('./')
from pathlib import Path
import Contrast_detail


""" strings testing """

def test_strings_pathexist():
    """
    TEST:
    -------
    - If csv paths defined in txt files exist

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        
        results = Contrast_detail.strings('./data/'+t)
        paths = results[0]['path']
        for csv in paths:
            assert Path(csv).is_file()

def test_strings_correctitles():
    """
    TEST
    -------
    - If dataframe has the right number of columns
    - If the first column is 'alpha'
    - If the second column is 'path'
    - If 'diam' is the first element of path_s
    
    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        head = results[0].columns
        assert len(head) == 2
        assert head[0] == 'alpha'
        assert head[1] == 'path'
        assert results[2][0] == 'diam'

def test_strings_coldiams():
    """
    TEST
    -------
    - If the first columns of csv file named 'alpha...' are all equal
    - If the first columns of csv file named 'human...' are all equal

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        paths = results[0]['path']
        coldiams_a = []
        for csv in paths[:results[1]]:
            csv_df = pd.read_csv(csv)
            coldiams_a += [np.array(csv_df.iloc[:,0])]
        assert all(all(d == coldiams_a[1]) for d in coldiams_a)
        
        coldiams_h = []
        for csv in paths[results[1]:]:
            csv_df = pd.read_csv(csv)
            coldiams_h += [np.array(csv_df.iloc[:,0])]
        assert all(all(d == coldiams_h[1]) for d in coldiams_h)


def test_strings_alphaposition():
    """
    TEST
    -------
    - If num_alpha points to an 'alpha' position
    - If there are not other 'alpha' after num_alpha

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        assert 'alpha' in results[2][results[1]] 
        assert 'alpha' not in results[2][results[1]:] 
    

def test_strings_correctlengths():
    """
    TEST
    -------
    - If (alpha_s + human_s) returns files['alpha'] length
    - If path_s is longer than files['alpha'] by one
    

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        assert len(results[3])+len(results[4]) == len(results[0]['alpha'])
        assert len(results[2]) == len(results[0]['alpha'])+1
         
        
""" cd_dataframe testing"""

def test_cd_dataframe_csvdiams():
    """
    TEST
    -------
    - If column 'diam' in cd_df is equal to the first column in csv file
    

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        assert (cd_df['diam'] == pd.read_csv(results[0]['path'][0])['Nominal Diameter (mm)']).all()
    
def test_cd_dataframe_valdiams(): 
    """
    TEST
    -------
    - If column 'diam' has only positive values
    - If the elements in 'diam' column are all different and ordered
    

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        assert all( i >0 for i in cd_df['diam'])
        for d in range(len(cd_df['diam'])-1):
            assert cd_df['diam'][d]>cd_df['diam'][d+1]
            
def test_cd_dataframe_valcontrs(): 
    """
    TEST
    -------
    - If alpha and human columns have only positive contrast values
    

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        for x in range(1,len(results[2])):
            assert all( i >0 for i in cd_df.iloc[:,x])
    
def test_cd_dataframe_correctvals():
    """
    TEST
    -------
    - If, from csv files filled of ones, it returns cd_df dataframe of ones

    """
    results = Contrast_detail.strings('./documents/example_csv/pathtxt.txt')
    m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
    cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
    for col in range(1,len(results[0]['path'])+1):
        assert all(cd_df.iloc[:,col].values == 1)
    
def test_cd_dataframe_dim():
    """
    TEST
    -------
    - If it returns the correct dataframe dimension

    """
    results = Contrast_detail.strings('./documents/example_csv/pathtxt.txt')
    m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
    cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
    assert cd_df.shape == (9,4)

