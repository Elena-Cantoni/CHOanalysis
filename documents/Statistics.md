# Statistics
**Statistics.py** is a functions module that performs some mathematical operations that give a more statistical idea about the dataset collected. In particular we will see which steps are needed to calculate the mean human observer curve and the estimation of its minimizing CHO &alpha;-dependent curve. Then, a linearity study is led with the estimation of *p value* and *r value*.
Following the usage's order, a more datailed description about the used functions is given.  

## `meanstd_curve(df_cd, n_alpha, list_humans)`
The function estimates mean and standard deviation points between different human observations of the same image sample.

#### Parameters:
- df_cd : contrast-detial curve dataframe
- n_alpha : int value representing the number of rows where the word 'alpha' appears
- list_humans : series of the title names of the observer curves

#### Example:
```
import pandas as pd 
import numpy as np
import Contrast_detail 
import Statistics
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
meanstd,df_meanstd = Statistics.meanstd_curve(df_alpha,5,human_s) 
print(meanstd,'\n',df_meanstd)
```
It returns a matrix and a dataframe filled with the same elements. The dataframe is given as example, it is constituted by two columns (mean and std) and n°diameter rows.
mean|std
---|---
0|0.023285|0.008629
1|0.018602|0.014454
2|0.031819|0.010107
3|0.042800|0.008198
4|0.079487|0.021790
5|0.171285|0.058996
6|0.199431|0.089467
7|0.310358|0.076950
8|0.442954|0.119914

## `meanobs_minimization(df_cd, p_mean_std, txt_files, n_alpha, list_alphas, w)`
The function allows to find which is the CHO &alpha;-dependent curve that minimizes the averaged human observer curve estimated with the previously described *meanstd_curve* function.

#### Parameters:
- df_cd : contrast-detial curve dataframe
- p_mean_std : dataframe filled with mean and std of the same diameter points seen by different observers
- txt_files : txt dataframe
- n_alpha : int value representing the number of rows where the word 'alpha' appears
- list_alphas : alpha names series in dataframe
-w : weighting factor

#### Example:
```
import numpy as np
import pandas as pd 
import Contrast_detail
import Statistics
txt = '.\data\cd_CORO_LAAG_0004.txt'
w = 0.1
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
meanstd,df_meanstd = Statistics.meanstd_curve(df_alpha,5,human_s)
df_points_curvemin, df_table_points_curvemin = Statistics.meanobs_minimization(df_alpha,meanstd,files,5,alpha_s,w)
print(df_points_curvemin,'\n', df_table_points_curvemin )
```
It returns the same results of *minimum* function defined in *minimization.py* with the exception that the only human curve represents the averaged human curve.

## `correlation(h_dataset, a_dataset, humans, alphas)`
The function  studies the correlation parameters estimated correlating human and CHO model response. 
A  ``linregress`` function is used.

#### Parameters:
- h_dataset : CD human curve dataframe
- a_dataset : CD CHO curve dataframe
- humans : series of the title names of the observer curves
- alphas : series of the title names of the different CHO curves with different &alpha;

#### Example:
``` 
import pandas as pd
import numpy as np
import Contrast_detail
import Statistics
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
corr = Statistics.correlation(df_alpha[human_s],df_alpha[alpha_s],human_s, alpha_s)
print(corr)
```
It returns a 3-D matrix (n° humans, paramenters, n°alphas) where the 5 parameters are in the order :  slope, intercept, R value, p-value and  standard deviation of the estimated slope. The following 2-D dataframe represents one slice of the 3-D dataframe corresponding to n° human = 1. 

```
[[ 5.64028261e+00,4.73564686e+00,3.00439374e+00,
1.53994884e+00,2.00518515e+00],
[ -1.40469543e-01,-1.45714044e-01,-1.39759189e-01,
-9.88707388e-02,-2.11535745e-01],
[ 9.54797113e-01,9.63753394e-01,9.48872686e-01,
7.50918720e-01,7.90655245e-01],
[ 6.18552260e-05,2.88116476e-05,9.46313135e-05,
1.97061071e-02,1.11863821e-02],
[ 6.63704370e-01,4.95497556e-01,
3.77761859e-01,5.11879667e-01,5.86888143e-01]]
```
