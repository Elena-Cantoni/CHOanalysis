from hypothesis.extra.pandas import series, data_frames, column, range_indexes
from hypothesis.extra.numpy import arrays   
from hypothesis import given,settings,strategies as st
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

@given(x0=st.floats(min_value=-50, max_value=50), x1=st.floats(min_value=-50, max_value=50))  # min_value = 1,max_value=10
@settings(max_examples = 50)
def test_differences(x0, x1):
    """
    TEST
    ----------
    - If it returns an absolute value result

    """
    diff = fun.differences(x0, x1)
    assert diff >= 0


@given(w = st.floats(0,1, exclude_min=True),
       dist=arrays(float,st.integers(min_value=9,max_value=12),elements=st.floats(0, 1)))
def test_weighted_sum(w,dist):
    """
    TEST
    ----------
    - If it returns a float value
    - If it returns a positive value or equal to zero 
    - If it returns a weighted factor different from zero

    """
    w_sum = fun.weighted_sum(w,dist)
    assert isinstance(w_sum, float) == True
    assert w_sum >= 0
    assert w!=0


rand_hum = np.random.randint(1,10)
rand_a = np.random.randint(1,10)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
@given(df =data_frames(columns=[column(alphabet[n], dtype=float, elements=st.floats(0,1)) for n in range(rand_hum+rand_a)], index=range_indexes(9,12)),
        df_dist = data_frames(columns =[column(alphabet[n], dtype=float, elements=st.floats(0,1)) for n in range(rand_hum)], index=range_indexes(rand_a,rand_a)))    
def test_minimum(df,df_dist):
    """
    TEST
    ----------
    - If it returns a matrix with a specific length
    - If it returns a columns equal to the number of human observers
    
    """
    head = list(df.columns.values)
    head_hum = pd.Series(df_dist.columns)
    head_a = pd.Series(head[len(head_hum):])
    mincurve = fun.minimum(df,df_dist,head_hum,head_a)
    assert len(mincurve) == 9 or 10 or 11 or 12
    assert len(head_hum) == mincurve.shape[1]


# Statistics.py testing

st_rand_hum = np.random.randint(1,10)
st_rand_alpha = np.random.randint(1,10)
st_rand_contr = np.random.randint(9,12)
st_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
@given(df_h = data_frames(columns=[column(st_alphabet[n], dtype=float, elements=st.floats(0, 1).filter(lambda x: x > 0),unique =True) for n in range(st_rand_hum)], index=range_indexes(st_rand_contr,st_rand_contr)),
       df_a = data_frames(columns=[column(st_alphabet[n], dtype=float, elements=st.floats(0, 1).filter(lambda x: x > 0),unique =True) for n in range(st_rand_alpha)], index=range_indexes(st_rand_contr,st_rand_contr)))
def test_correlation(df_h,df_a):
    """
    TEST
    ----------
    - If it returns the correct matrix dimension
    - If it returns a np.ndarray

    """
    series_h = pd.Series(df_h.columns)
    series_a = pd.Series(df_a.columns)
    corr = fun.correlation(df_h,df_a,series_h,series_a)
    assert corr.shape == (len(series_h),5, len(series_a))
    assert isinstance(corr, np.ndarray) == True











