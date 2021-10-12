# Statistics
**Statistics.py**is a functions module that performs some mathematical operation that give a more statistical idea about the dataset collected. In particular we will see which steps to calculate the mean human observer curve and the estimation of its minimizing CHO &alpha;-dependent curve. Then, a linearity study is led with the estimation of *p value* and *r value*.
Following the usage's order, a more datailed description about the used functions is given.  

## `meanstd_curve(df_cd, n_alpha, list_humans)`
The function estimates mean and standard deviation points between different human observations of the same image sample.

#### Parameters:
- df_cd : contrast-detil curve dataframe
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

## `meanobs_minimization(df_cd, p_mean_std, txt_files, n_alpha, list_alphas)`
The function allows to find which is the CHO &alpha;-dependent curve that minimizes the averaged human observer curve estimated with the previous described *meanstd_curve* function.

#### Parameters:
- df_cd : contrast-detil curve dataframe
- p_mean_std : matrix filled with mean and std of the same diameter points seen by different observers
- txt_files : txt dataframe
- n_alpha : int value representing the number of rows where the word 'alpha' appears
- list_alphas : alpha names series in dataframe

#### Example:
```
import numpy as np
import pandas as pd 
import Contrast_detail
import Statistics
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
meanstd,df_meanstd = Statistics.meanstd_curve(df_alpha,5,human_s)
df_points_curvemin, df_table_points_curvemin = Statistics.meanobs_minimization(df_alpha,meanstd,files,5,alpha_s)
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
df_corr = Statistics.correlation(df_alpha[human_s],df_alpha[alpha_s],human_s, alpha_s)
print(df_corr)
```
It returns a dataframe (n° humans, paramenters, n°alphas) where the 5 parameters are in the order :  slope, intercept, R value, p-value and  standard deviation of the estimated slope. The following 2-D dataframe represents the result coming from the correlation with only one human, imagine others as the total number of human observers. 

.|0|1|2|3|4
---|---|---|---|---|---
slope|5.64028|4.73565|3.00439|1.53995|2.00519
intercept|-0.14047|-0.145714|-0.139759|-0.0988707|-0.211536
r value|0.954797|0.963753|0.948873|0.750919|0.790655
p value|6.18552e-05|2.88116e-05|9.46313e-05|0.0197061|0.0111864
std|0.663704|0.495498|0.377762|0.51188|0.586888