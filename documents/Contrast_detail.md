
# Contrast_detail
**Contrast_detail.py** is a function module concerning the selection of data and creation of contrast-detail curves dataset.
Following the usage's order, a more datailed description about the used functions is given.

## `strings(path_txt)`
This function is used to extract data from external files  and to organize their nomenclature. What the function returns  is very useful for the next steps and it will be often used as argoment of the following functions.

#### Parameters:
- path_txt = txt file path string 

#### Example:
``` 
import numpy as np
import pandas as pd
import Contrast_detail
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
print(files,'\n', num_alpha,'\n', path_s,'\n', alpha_s,'\n', human_s)
``` 
It returns:
- files : txt dataframe

.|alpha|path
---|---|---
0|alpha 1.5| ./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_1e5a.csv
1|alpha 2.5|  ./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_2e5a.csv
2|alpha 5|    ./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_5a.csv
3|alpha 10|   ./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_10a.csv
4|alpha 15|   ./data/CORO_LAAG_0004/CHO_CORO_LAAG_0004_15a.csv
5|human curve 1|  ./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_El...
6|human curve 2|  ./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_Ma...
7|human curve 3|  ./data/CORO_LAAG_0004/Hum_CORO_LAAG_0004_CD_Va...

- num_alpha : float value
- path_s : titles list in dataframe 
`['diam' 'alpha 1.5' 'alpha 2.5' 'alpha 5' 'alpha 10' 'alpha 15'
 'human curve 1' 'human curve 2' 'human curve 3']`
- alpha_s : alpha  names series in dataframe
`('alpha 1.5' 'alpha 2.5' 'alpha 5' 'alpha 10' 'alpha 15')`,
- human_s : human names series in dataframe
`('human curve 1' 'human curve 2' 'human curve 3')`

## `cd_dataframe(m_contr, txt_files, names_string)`
This function generates a contrast-detail dataframe containing all the external data (from .csv files) that are contrasts for each diameter relative to the results obtained from human observers and from the application of the CHO model varying the alpha noise parameter.

#### Parameters:
- m_contr : empty matrix to be filled
- txt_files : txt dataframe
- names_string : titles list in dataframe

#### Example:
``` 
import numpy as np
import pandas as pd
from numpy import genfromtxt
import Contrast_detail
txt = '.\data\cd_CORO_LAAG_0004.txt'
files, num_alpha, path_s, alpha_s, human_s = Contrast_detail.strings(txt)
m_contrast = genfromtxt('./documents/example_csv/m_contrast.csv', delimiter=',')
df_alpha = Contrast_detail.cd_dataframe(m_contrast,files,path_s)
print(df_alpha)
```
It returns a dataframe of the shape:

.|diam|alpha 1.5|alpha 2.5|alpha 5|alpha 10|alpha 15|human curve 1|human curve 2|human curve 3
---|---|---|---|---|---|---|---|---|---|---
0|4.00|0.034585|0.037691|0.047681|0.066423|0.128000|     0.016644|0.020173|0.033039
1|2.80|0.031673|0.037982|0.056970|0.067400|0.128000|0.016441|0.005350|0.034014
2|2.00|0.027309|0.034467|0.056465|0.128000|0.128000|0.036675|0.020200|0.038581
3|1.40|0.025326|0.035390|0.068419|0.127941|0.128000|0.033727|0.045000|0.049674
4|1.00|0.036731|0.046883|0.078445|0.128000|0.128000|0.079462|0.057709|0.101289
5|0.70|0.057989|0.070608|0.109542|0.238000|0.238000|0.125995|0.238000|0.149860
6|0.50|0.048096|0.055790|0.075927|0.117954|0.163326|0.178849|0.122048|0.297395
7|0.35|0.071155|0.083790|0.123040|0.205550|0.237996|0.222614|0.366356|0.342104
8|0.25|0.093162|0.114775|0.181184|0.238000|0.238000|0.428281|0.331051|0.569530