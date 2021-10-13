# minimization 
**minimization.py** is a functions module where the data collected in contrast-detail dataset ( obtained from the module *Contrast_detail.py*) are subjected to a series of operations which calculate distances between CHO curve points and human observer curve points with the aim to find, after a weighted sum of those distances,  the CHO curve that minimizes the human curves in consideration.
Following the usage's order, a more datailed description about the used functions is given.  
  


## `differences(cho_point, hum_point)`
The function calculates the absolute difference between the contrast values estimated by the CHO model and the human observer for the same diameters. 

#### Parameters:
- cho_point : pandas dataframe element, contrast CHO curve point
- hum_point : pandas dataframe element, contrast human curve point

#### Example:
``` 
import pandas as pd
import numpy as np
import minimization
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
diff = minimization.differences(df_alpha['alpha 5'][0],df_alpha['human curve 1'][0])
print(diff)
```
It returns a float value: ```0.0310362886005352```

## `tot_distances(m_dist, txt_files, n_alpha, df_cd):`
It estimates matrix filled with distances between CHO and human points referred to the same diameter. The loops used inside the function move between all the contrasts defined for each model with different $\alpha$ and for each experimental observer.

#### Parameters:
- m_dist : empty matrix to be filled
- txt_files : txt dataframe
- n_alpha : int value representing the number of rows where the word 'alpha' appears
- df_cd : contrast-detil curve dataframe

#### Example:
```
import numpy as np
import pandas as pd
import minimization
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv')
files = pd.read_csv('./documents/example_csv/files.csv')
m_distances = np.ndarray((((len(files['alpha'])-5)), 5, len(df_alpha)))
m_dist = minimization.tot_distances(m_distances,files,5,df_alpha)
print(m_dist)
```
It returns a 3D matrix with (x = diameters, y = alphas, z = humans). As shown below, an example, selecting one human, is given: 
```
[[0.01794054, 0.01523263, 0.00936567, 0.00840046, 0.04273038,0.06800622, 0.13075326, 0.15145885, 0.33511899],
[0.02104699, 0.02154147, 0.00220749, 0.00166288, 0.03257922,0.05538654, 0.12305929, 0.13882435, 0.31350542],
[0.03103629, 0.04052914, 0.01978987, 0.03469189, 0.00101722, 0.01645332, 0.10292263, 0.09957344, 0.24709649],
[0.04977865, 0.05095899, 0.09132506, 0.09421413, 0.04853774, 0.11200512, 0.06089503, 0.01706398, 0.19028105],
[0.11135554, 0.11155923, 0.09132506, 0.09427287, 0.04853787, 0.11200512, 0.01552384, 0.01538194, 0.19028064]]
```

## ```weighted_sum(weight,dist)```
The function performs a weighted sum over all the diameters of interest between all the distances calculated with **differences ** regarding a specific CHO curve and a specific human curve.
According to the number of achieved  diameters, the three outermosts are characterized by a lower weighting factor wrt the values referred to the innermost diameters which are weighted with a factor 1. It is assumed that the maximum number of diameters is 12 and different weighting conditions are imposed because  it can vary between 8 and 12.
#### Parameters:
- weight : float weighting value 
- dist : matrix distance row

#### Example:
``` 
import numpy as np 
import pandas as pd 
import minimization 
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv') 
files = pd.read_csv('./documents/example_csv/files.csv') 
m_distances = np.ndarray((((len(files['alpha'])-5)), 5, len(df_alpha)))
m_dist = minimization.tot_distances(m_distances,files,5,df_alpha)
m_distance_row = m_dist[0][0]
w_sum = minimization.weighted_sum(0.1, m_distance_row)
print(w_sum)
```
It returns a float value which represents the total weighted sum of points distances: ```0.2234090167415727```

## ```tot_weighted_sum(m_sum_w_dist, m_dist, txt_files, n_alpha, w)```
Estimates weighted sum of the distances for each curve and fills a dataframe.
An overall estimation is led with this function. A weighted sum of distances for each CHO curve  with respect to human observer curve is done and a dataframe is filled.

#### Parameters:
   - m_sum_w_dist : empty matrix to be filled
   - m_dist : distances 3D-matrix
   - txt_files : txt dataframe
   - n_alpha : int value representing the number of rows where the word 'alpha' appears
   - w = weighing factor
   
#### Example:
``` 
import numpy as np 
import pandas as pd 
import minimization 
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv') 
files = pd.read_csv('./documents/example_csv/files.csv') 
m_distances = np.ndarray((((len(files['alpha'])-5)), 5, len(df_alpha)))
m_dist = minimization.tot_distances(m_distances,files,5,df_alpha)
m_w_sum = np.ndarray((5,(len(files['alpha'])-5)))
df_w_sum = minimization.tot_weighted_sum(m_w_sum,m_dist,files,5,0.1)
print(df_w_sum)
```
It returns a dataframe so organized: rows= alphas, columns = humans.
alpha|human curve 1|human curve 2|human curve 3
---|---|---|---
0|0.223409|0.329212|0.295596
1|0.191963|0.308757|0.256143
2|0.188477|0.331936|0.220277
3|0.473644|0.395127|0.414059
4|0.591174|0.517837|0.528513

## `minimum(dataset, dist_set, list_humans, list_alphas)`
The function concerns to the capability to estimate which CHO &alpha;-dependent curve minimizes the weighted distances wrt the associated observers.

#### Parameters:
- dataset : CD curve dataframe
- dist_set : dataframe of weighted distance sums
- list_humans : series of the title names of the observer curves
- list_alphas : series of the title names of the different CHO curves with different alpha
- 
#### Example:
``` 
import pandas as pd
import numpy as np
import Contrast_detail
import minimization
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
df_alpha = pd.read_csv('./documents/example_csv/df_alpha.csv') 
df_sum_w_dist = pd.read_csv('./documents/example_csv/df_sum_w_dist.csv') 
df_curvemin, df_table_curvemin = minimization.minimum(df_alpha, df_sum_w_dist, human_s, alpha_s)
print(df_curvemin,'\n', df_table_curvemin)
```
The execution returns two dataframes.

- The first one is organized in n° humans columns, each column represents the minimum CHO curve associated to that human observer. 

0|1|2
---|---|---
0|0.047681|0.037691|0.047681
1|0.056970|0.037982|0.056970
2|0.056465|0.034467|0.056465
3|0.068419|0.035390|0.068419
4|0.078445|0.046883|0.078445
5|0.109542|0.070608|0.109542
6|0.075927|0.055790|0.075927
7|0.123040|0.083790|0.123040
8|0.181184|0.114775|0.181184

- The second one contains the minimum distances curves and the referred weighted distances.

alpha|min alpha curve|distance
---|---|---
human curve 1|alpha 5|0.188477
human curve 2|alpha 2.5|0.308757
human curve 3|alpha 5|0.220277
