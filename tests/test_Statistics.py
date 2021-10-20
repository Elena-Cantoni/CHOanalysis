import numpy as np
import pandas as pd
from scipy.stats import linregress
import sys
sys.path.append('./')
import Contrast_detail
import minimization
import Statistics

""" meanstd_curve testing """

def test_meanstd_curve_dim():
    """
    TEST
    -------
    - If the two results have equal shape and return the correct dimensions

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])  
        assert df_meanstd.shape == meanstd.shape == (len(cd_df),2)


def test_meanstd_curve_equalvals():
    """
    TEST
    -------
    - If meanstd matrix and df_meanstd dataframe are filled with the same elements

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])   
        assert all(meanstd == df_meanstd)

def test_meanstd_curve_titles():
    """
    TEST
    -------
    - If the column 0 of dataframe is named 'mean'
    - If the column 1 of dataframe is named 'std'

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
        assert df_meanstd.columns[0] == 'mean'
        assert df_meanstd.columns[1] == 'std'
    
def test_meanstd_curve_mean():
    """
    TEST
    -------
    - If it returns the correct mean value
    - If it returns the correct result doing manually the mean

    """
    results = Contrast_detail.strings('./documents/example_csv/pathtxt2.txt')
    m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
    cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
    meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
    assert all(df_meanstd['mean'].values == 0.5)
    
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results1 = Contrast_detail.strings('./data/'+t)
        m_contrast1 = np.ndarray((len(pd.read_csv(results1[0]['path'][0])), len(results1[0]['path'])+1))
        cd_df1 = Contrast_detail.cd_dataframe(m_contrast1,results1[0],results1[2])
        meanstd1, df_meanstd1 = Statistics.meanstd_curve(cd_df1, results1[1], results1[4])
        for row in range(len(cd_df1)):
            s = sum(cd_df1.iloc[row][results1[1]+1:])
            mean = s/len(results1[4])
            assert meanstd1[row,0] == mean

    
def test_meanstd_curve_std():
    """
    TEST
    -------
    - If it returns the correct standard deviation in case of more than one human
    - If it returns the correct standard deviation in case of one human

    """
    results = Contrast_detail.strings('./documents/example_csv/pathtxt2.txt')
    m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
    cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
    meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
    assert all(df_meanstd['std'].values == 0.0)
    results1 = Contrast_detail.strings('./documents/example_csv/pathtxt.txt')
    m_contrast1 = np.ndarray((len(pd.read_csv(results1[0]['path'][0])), len(results1[0]['path'])+1))
    cd_df1 = Contrast_detail.cd_dataframe(m_contrast1,results1[0],results1[2])
    meanstd1, df_meanstd1 = Statistics.meanstd_curve(cd_df1, results1[1], results1[4])
    assert all(df_meanstd1['std'].values == 0.0)


""" meanobs_minimization testing """

def test_meanobs_minimization_dim():
    """
    TEST
    -------
    - If points_min_tab return the correct dimensions
    - If points_min_cd return the correct dimensions

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
        points_min_cd, points_min_tab = Statistics.meanobs_minimization(cd_df,df_meanstd,results[0],results[1],results[3],0.1)
        assert points_min_tab.shape == (1,2)
        assert points_min_cd.shape == (len(cd_df),1)
    
    
def test_meanobs_minimization_column():
    """
    TEST
    -------
    - If the column returned in points_min_cd in contained in cd_df

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
        points_min_cd, points_min_tab = Statistics.meanobs_minimization(cd_df,df_meanstd,results[0],results[1],results[3],0.1)
        assert any(all(points_min_cd[0] == cd_df[i]) for i in results[3])

def test_meanobs_minimization_consistency():
    """
    TEST
    -------
    - If the the string in min_tab is the title of dataset in min_cd associated to the same human

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        meanstd, df_meanstd = Statistics.meanstd_curve(cd_df, results[1], results[4])
        points_min_cd, points_min_tab = Statistics.meanobs_minimization(cd_df,df_meanstd,results[0],results[1],results[3],0.1)
        assert all(cd_df[points_min_tab['min alpha curve'][0]] == points_min_cd[0])
    

""" correlation testing """

def test_correlation_dim():
    """
    TEST
    -------
    - If the returned matrix has the right dimension

    """
    txt = ['cd_CORO_LAAG_0004.txt','cd_FL_LAAG_0001.txt']
    for t in txt:
        results = Contrast_detail.strings('./data/'+t)
        m_contrast = np.ndarray((len(pd.read_csv(results[0]['path'][0])), len(results[0]['path'])+1))
        cd_df = Contrast_detail.cd_dataframe(m_contrast,results[0],results[2])
        corr = Statistics.correlation(cd_df[results[4]],cd_df[results[3]],results[4], results[3])
        assert corr.shape == (len(results[4]),5,len(results[3]))

def test_correlation_r0():
    """
    TEST
    -------
    - If the r value is 0.0 when the datasets are not linearly correlated

    """
    hum_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['h1','h2','h3']) 
    alpha_df0 = pd.DataFrame(([1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1]), columns = ['a1', 'a2','a3'])    
    corr_0 = Statistics.correlation(hum_df1, alpha_df0, hum_df1.columns, alpha_df0.columns)
    for h in range(len(hum_df1.columns)): 
        for al in range(len(alpha_df0.columns)):
            assert corr_0[h][2][al] == 0.0
            
            
def test_correlation_r1():
    """
    TEST
    -------
    - If the r value is 1.0 when the datasets are perfectly linearly correlated (positive)

    """
    hum_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['h1','h2','h3']) 
    alpha_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['a1', 'a2','a3'])
    corr_1 = Statistics.correlation(hum_df1, alpha_df1, hum_df1.columns, alpha_df1.columns)
    for h in range(len(hum_df1.columns)): 
        for al in range(len(alpha_df1.columns)):
            assert corr_1[h][2][al] == 1.0
            
    
def test_correlation_rm1():
    """
    TEST
    -------
    - If the r value is -1.0 when the datasets are perfectly linearly correlated (negative)
    
    """
    hum_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['h1','h2','h3']) 
    alpha_dfm1 = pd.DataFrame(([9,9,9],[8,8,8],[7,7,7],[6,6,6],[5,5,5],[4,4,4],[3,3,3],[2,2,2],[1,1,1]), columns = ['a1', 'a2','a3'])
    corr_m1 = Statistics.correlation(hum_df1, alpha_dfm1, hum_df1.columns, alpha_dfm1.columns)
    for h in range(len(hum_df1.columns)): 
        for al in range(len(alpha_dfm1.columns)):
            assert corr_m1[h][2][al] == -1.0
            