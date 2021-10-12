
# CHOanalysis

## Table of Contents
1. General description
2. How to use it

## General description
In this repository a project concerning a Channelized Hotelling Observer model is led.

Starting from a series of .csv documents obtained by a Matlab master code, an accurate analysis is done.
The collected data running the master code give information about the minimum contrast at which a certain diamenter of disks, on a selected phantom, can be seen. The dataset is given for both the human evaluation test and the assessing of the CHO model, changing a noise factor &alpha;.

BY running **CHO.py** module, the whole program is executed automatically and, following the order, a series of functions, categorised according to their task, are used.

First of all, using the functions in **Contrast_detail.py**, for each distinct protocol, contrast-detail curves are graphed, and a plot with human curves and &alpha;-dependent CHO curves is shown.

Then,  taking as reference each single human observer curve, a minimization is performed with a weighted sum of the distances. The minimization is between the CD points of CHO curve and human curve associated to the same diameter.
In this way, the most similar &alpha;-dependent curve to the human reference one is chosen as better. This part is done using functions written in **minimization.py**.

Finally, using the functions in **statistics.py**, a correlation analysis between each human curve and CHO &alpha;-dependent curve is performed and slope, intercept, standard deviation, R value and p value  parameters are obtained.
In addition, by calculating the mean and standard deviation of the minimum contrasts associated with the individual diameters for each observer, it is possible to estimate values to conduct a linearity study and  to obtain an average contrast-detail curve, which is used to extract the curve of the CHO model that minimises it the most. 

## How to use it
In order to use this code to create Contrast-detail curves and to make an analysis there are a few steps to follow:

 1. Clone the code and install the requested packages listed in requirements.txt
	 ```
	git clone 
	https://github.com/Elena-Cantoni/CHOanalysis.git
	cd CHOanalysis
	pip install -r requirements.txt
	```
	
 2. When installed, understand the directory organization:
 
	 - Main script codes: [**CHO.py**](https://github.com/Elena-Cantoni/CHOanalysis/blob/main/CHO.py)
	 - 
	 - Functions code: [**Contrast_detail.py**](https://github.com/Elena-Cantoni/CHOanalysis/blob/main/Contrast_detail.py), [**minimization.py**](https://github.com/Elena-Cantoni/CHOanalysis/blob/main/minimization.py), [**Statistics.py**](https://github.com/Elena-Cantoni/CHOanalysis/blob/main/Statistics.py).
	 - Folders: 
		- [**data**](https://github.com/Elena-Cantoni/CHOanalysis/tree/main/data) is filled with .txt files where you can find the path of each .csv file inside the csv folders included in 'data'. 
		
			*How the files have to be written:*
			***Csv files*** need two columns; it is necessary that the first one is named *'Nominal Diameter (mm)'* and has at least 9 rows and at most 12. 
			***Txt files*** must be organized as follow:
			```
			alpha = path
			alpha (...) = "~/csvFolder/csvFilealpha"
			...
			human (...) = "~/csvFolder/csvFilehuman"
			```
		- [**documents**](https://github.com/Elena-Cantoni/CHOanalysis/tree/main/documents) contains the documentation concerning to function scripts  *'Contrast_detail.py'*, *'minimization.py'* and  *'Statistics.py'*.
		- [**tests**](https://github.com/Elena-Cantoni/CHOanalysis/tree/main/tests)  includes the testing of functions managed in testing documents such as the respective function scripts. The tests performed exploit practical examples and values.
The pytest framework is needed to run the codes, if it is not yet installed, run ``pip install -U pytest`` from the terminal.
	
 3. Execute the **'CHO.py'** script on the terminal with the following command:
 ```python .\CHO.py .\data\NameFile.txt```
 where `.\data\NameFile.txt` is the txt file path needed to run the code and `NameFile.txt` is the txt file name.

	 

	 
4. Enjoy the results and how the project works.

[![Python 3.9.6](https://img.shields.io/badge/python-3.9.6-blue.svg)](https://www.python.org/downloads/release/python-396/)	 

	