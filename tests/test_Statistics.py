import numpy as np
import pandas as pd
from scipy.stats import linregress
import sys
sys.path.append('./')
import minimization
import Statistics


def test_meanstd_curve():
    """
    TEST
    -------
    - If meanstd is a 2D matrix
    - If 'diam' is included in the title's list of df_alpha1
    - If it returns correct means
    - If it returns correct standard deviations
    
    """
    np.random.seed(0)
    df_alpha1 = pd.DataFrame(np.random.random_sample((9,7)),columns = ['diam','a1','a2','a3','h1','h2','h3'])
    alpha = 3
    h = pd.Series(['h1','h2','h3'])
    meanstd, df_meanstd = Statistics.meanstd_curve(df_alpha1, alpha, h)
    mean0 = np.mean(df_alpha1.loc[0][alpha+1:])
    diff = np.ndarray((1,3))
    p = -1
    for a in range(alpha+1,7):
        p += 1
        diffq = (df_alpha1.iloc[0][a]-mean0)**2
        diff[0,p] = diffq
    std = np.sqrt(sum(diff[0])/2)
    assert isinstance(meanstd, np.ndarray) == True
    assert 'diam' in df_alpha1.columns.values
    assert mean0 == df_meanstd['mean'][0]
    assert std == df_meanstd['std'][0]
    

def test_meanobs_minimization():
    """
    TEST
    -------
    - If the column in minobs is equal to the column of df_alpha1 with the name in loc (0,0) of minobs_curve
    - If all the elements in the first column in minobs_curve are contained in titles of df_alpha1
    - If minobs has only one column (data of one curve that is referred to the averaged human curve)

    """
    np.random.seed(0)
    df_alpha1 = pd.DataFrame(np.random.random_sample((9,7)),columns = ['diam','a1','a2','a3','h1','h2','h3'])
    meanstd = np.random.random_sample((9,2))
    files1 = pd.DataFrame([['a1','a'],['a2','b'],['a3','c'],['h1','d'],['h2','e'],
                      ['h3','f']], columns= ['alpha', 'P'])
    alpha = 3
    a = pd.Series(['a1','a2','a3'])
    minobs, minobs_curve = Statistics.meanobs_minimization(df_alpha1, meanstd, files1, alpha, a)
    value = minobs_curve['min alpha curve'][0]
    
    assert all(minobs[0].values == df_alpha1[value].values)
    assert all(i in df_alpha1.columns.values for i in minobs_curve['min alpha curve'].values)
    assert len(minobs.columns) == 1
    
    
def test_correlation():
    """
    TEST
    ----------
    - If it returns the correct dataframe dimension
    - If the r value is 0.0 when the datasets are not linearly correlated
    - If the r value is 1.0 when the datasets are perfectly linearly correlated (positive)
    - If the r value is -1.0 when the datasets are perfectly linearly correlated (negative)

    """
    np.random.seed(0)
    hum_df = pd.DataFrame(np.random.random_sample((9,3)), columns = ['h1','h2','h3'])
    hum_series = pd.Series(hum_df.columns)
    alpha_df = pd.DataFrame(np.random.random_sample((9,3)), columns = ['a1', 'a2','a3'])
    alpha_series = pd.Series(alpha_df.columns)
    corr = Statistics.correlation(hum_df, alpha_df, hum_series, alpha_series)
    assert (5,alpha_df.shape[1]) == corr.shape 
    
    hum_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['h1','h2','h3']) 
    alpha_df0 = pd.DataFrame(([1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1],[2,2,2],[1,1,1]), columns = ['a1', 'a2','a3'])    
    alpha_df1 = pd.DataFrame(([1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6],[7,7,7],[8,8,8],[9,9,9]), columns = ['a1', 'a2','a3'])
    alpha_dfm1 = pd.DataFrame(([9,9,9],[8,8,8],[7,7,7],[6,6,6],[5,5,5],[4,4,4],[3,3,3],[2,2,2],[1,1,1]), columns = ['a1', 'a2','a3'])
    corr_0 = Statistics.correlation(hum_df1, alpha_df0, hum_series, alpha_series)
    corr_1 = Statistics.correlation(hum_df1, alpha_df1, hum_series, alpha_series)
    corr_m1 = Statistics.correlation(hum_df1, alpha_dfm1, hum_series, alpha_series)
    assert corr_0.loc['r value'][0] == 0.0
    assert corr_1.loc['r value'][0] == 1.0
    assert corr_m1.loc['r value'].values[0] == -1.0
    

    