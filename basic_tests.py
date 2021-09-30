import numpy as np
import pandas as pd
import os.path
import sys
# path where interactions between codes happen
path_interaction = os.path.dirname(os.path.abspath(__file__))
if path_interaction not in sys.path:
    sys.path.append(path_interaction)
import functions as fun
# minimization.py testing


def test_differences():
    """
    TEST
    -------
    - If it returns a positive result despite negative variable

    """
    assert fun.differences(0.5, -0.8) > 0


def test_weighted_sum():
    """
    TEST
    -------
    - If it returns a float value
    - If it returns a positive value
    - If it returns a non zero value
    - If the array's length gives as argument is in a specific range

    """
    dist = np.array(np.random.random_sample((np.random.randint(9,12),)))
    assert isinstance(fun.weighted_sum(0.1,dist), float) == True
    assert fun.weighted_sum(0.3,dist) >= 0
    assert fun.weighted_sum(0.3,dist) != 0
    assert 8 < len(dist) < 13 


def test_minimum():
    """
    TEST
    ----------
    - If it returns a matrix with a specific length (with specific values and with a range of values)
    - If it returns a columns equal to the number of human observers (with specific values and with a range of values)

    """
    r_hum = 4
    r_a = 8
    df = pd.DataFrame(np.ndarray((10,r_a + r_hum), dtype=np.float64))
    df_dist = pd.DataFrame(np.ndarray((r_a, r_hum), dtype=np.float64))
    h = list(df.columns.values)
    h_hum = pd.Series(df_dist.columns)
    h_a = pd.Series(h[len(h_hum):])
    assert len(fun.minimum(df,df_dist,h_hum,h_a)) == 10  
    assert len(h_hum) == fun.minimum(df,df_dist,h_hum,h_a).shape[1]
    
    rand_hum = np.random.randint(1,10)
    rand_a = np.random.randint(1,10)
    df1 = pd.DataFrame(np.ndarray((np.random.randint(9,12),rand_a + rand_hum), dtype=np.float64))
    df1_dist = pd.DataFrame(np.ndarray((rand_a, rand_hum), dtype=np.float64))
    head = list(df1.columns.values)
    head_hum = pd.Series(df1_dist.columns)
    head_a = pd.Series(head[len(head_hum):])

    assert len(fun.minimum(df1,df1_dist,head_hum,head_a)) == 9 or 10 or 11 or 12 
    assert len(head_hum) == fun.minimum(df1,df1_dist,head_hum,head_a).shape[1]
    

def test_correlation():
    """
    TEST
    ----------
    - If it returns the correct number of parameters
    - If it returns a tuple

    """
    row = 8
    hum_arr = np.random.random_sample(row)
    series_hum = pd.Series(hum_arr)
    a_arr = np.random.random_sample(row)
    series_a = pd.Series(a_arr)
    corr = fun.correlation(series_hum,series_a)
    assert len(corr) == 5 
    assert isinstance(corr, tuple) == True
    

