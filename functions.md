
# functions.py

**functions.py** is a module where funtions used in **minimization.py** and **Statistics.py** are collected.
Following the usage's order, a more datailed description about their functionality is given.
The reported results depend on the used dataset.

## `differences(cho_point, hum_point)`
The function is seen, firstly, in *minimization.py* then in *Statistics.py*. It calculates the absolute difference between the contrast values estimated by the CHO model and the human observer for the same diameters. 
It is typically used inside a loop which moves between all the contrasts defined for each model with different &alpha; and for each experimental observer.
#### Parameters:
- cho_point : pandas dataframe element, contrast CHO curve point
- hum_point : pandas dataframe element, contrast human curve point
#### Example:
``` 
import pandas as pd
import functions as fun 
df_alpha = pd.read_pickle('pkl\df_alpha.pkl')
p_cho = df_alpha['alpha 5'][0]
p_human = df_alpha['human curve 1'][0]
diff = fun.differences(p_cho, p_human)
print(diff)
```
It returns a float value: ```0.0310362886005352```

## ```weighted_sum(dist)```
The function is used in *minimization.py* and in *Statistics.py*. It performs a weighted sum over all the diameters of interest between all the distances calculated with **differences ** regarding a specific CHO curve and a specific human curve.
According to the number of achieved  diameters, the three outermosts are characterized by a lower weighting factor wrt the values referred to the innermost diameters which are weighted with a factor 1. It is assumed that the maximum number of diameters is 12 and different weighting conditions are imposed because  it can vary between 9 and 12.
#### Parameters:
- weight : float weighting value 
- dist : matrix distance row
#### Example:
``` 
import numpy as np
import functions as fun 
m_distances = np.load('pkl/m_distances.npy')
m_distance_row = m_distances[0][0]
w_sum = fun.weighted_sum(0.1, m_distance_row)
print(w_sum)
```
It returns a float value which represents the total weighted sum of points distances: ```0.2234090167415727```

## `minimum(dataset, dist_set, list_humans, list_alphas)`
The function is used in *minimization.py* and in *Statistics.py* and concerns to the capability to estimate which CHO &alpha;-dependent curve minimizes the weighted distances with respect to the associated observers.
#### Parameters:
- dataset : CD curve dataframe
- dist_set : dataframe of weighted distance sums
- list_humans : series of the title names of the observer curves
- list_alphas : series of the title names of the different CHO curves with different alpha
#### Example:
``` 
import pandas as pd
import functions as fun
df_alpha = pd.read_pickle('pkl\df_alpha.pkl')
df_sum_w_dist = pd.read_pickle('pkl\df_sum_w_dist.pkl')  
human_s = pd.read_pickle('pkl\human_s.pkl')
alpha_s = pd.read_pickle('pkl/alpha_s.pkl')
min_curves = fun.minimum(df_alpha, df_sum_w_dist, human_s, alpha_s)
print(min_curves)
```
The execution returns a matrix organized in n° humans columns, each column represents the minimum CHO curve associated to that human observer.
.|0|1|2
---|---|---|---
0|4.768074576204330006e-02|3.769145066279999678e-02|4.768074576204330006e-02
1|5.696990729309790030e-02|3.798223716185759880e-02|5.696990729309790030e-02
2|5.646481424873379951e-02|3.446745150973300198e-02|5.646481424873379951e-02
3|6.841882762760240211e-02|3.538982213767759982e-02|6.841882762760240211e-02
4|7.844460687212860550e-02|4.688261199217769876e-02|	7.844460687212860550e-02
5|1.095415566632360060e-01|7.060834294365089803e-02|1.095415566632360060e-01
6|7.592683891332729917e-02|5.579017770603680176e-02|7.592683891332729917e-02
7|1.230404822480749977e-01|8.378957522874870556e-02|1.230404822480749977e-01
8|1.811841482293879979e-01|1.147752190135419986e-01|1.811841482293879979e-01

## `correlation(h_dataset, a_dataset, humans, alphas)`
The function appears in *Statistics.py* module and it studies the correlation parameters estimated correlating human and CHO model response. 
A  ``linregress`` function is used.
#### Parameters:
- h_dataset : CD human curve dataframe
- a_dataset : CD CHO curve dataframe
- humans : series of the title names of the observer curves
- alphas : series of the title names of the different CHO curves with different &alpha;
#### Example:
``` 
import pandas as pd
import functions as fun
df_alpha = pd.read_pickle('pkl\df_alpha.pkl')
human_s = pd.read_pickle('pkl\human_s.pkl')
alpha_s = pd.read_pickle('pkl/alpha_s.pkl')
corr = fun.correlation(df_alpha[human_s],df_alpha[alpha_s],human_s,alpha_s)
print(corr)
```
It returns a 3-D matrix (n° humans, parameters, n°alphas) where the 5 parameters are in the order :  slope, intercept, standard deviation of the estimated slope , R value and p-value. The following 2-D matrix represents the result coming from the correlation with only one human, imagine others as the total number of human observers. 

.|0|1|2|3|4
---|---|---|---|---|---
0|5.64028|4.73565|3.00439|1.53995|2.00519
1|-0.14047|-0.145714|-0.139759|-0.0988707|-0.211536
2|0.954797|0.963753|0.948873|0.750919|0.790655
3|6.18552e-05|2.88116e-05|9.46313e-05|0.0197061|0.0111864
4|0.663704|0.495498|0.377762|0.51188|0.586888