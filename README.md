
# CHOanalysis

## Table of Contents
1. General description
2. How to use it
3. Limitations


## General description
In this repository a project concerning a Channelized Hotelling Observer model is led.

Starting from a series of .csv documents obtained by a Matlab master code, an accurate analysis is done.
The collected data running the master code give information about the minimum contrast at which a certain diamenter of disks, on a selected phantom, can be seen. The dataset is given for both the human evaluation test and the assessing of the CHO model, changing a noise factor &alpha;.

First of all, in **Contrast_detail.py**, for each distinct protocol, Contrast-detail curves are graphed, and a plot with human curves and &alpha;-dependent CHO curves is shown.

Then, in **minimization.py**, taking as reference each single human observer curve, a minimization is performed with a weighted sum of the distances. The minimization is between the CD points of CHO curve and human curve associated to the same diameter.
In this way, the most similar &alpha;-dependent curve to the human reference one is chosen as better. 

In **statistics.py** a correlation analysis between each human curve and CHO &alpha;-dependent curve is performed and slope, intercept, standard deviation, R value and p value  parameters are obtained.
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
 
	 - Main script codes: **'Contrast_detail.py'**, **'minimization.py'**, **'Statistics.py'**.
	 - Functions code: **'functions.py'**.
	 - Functions documentation: **'functions.md**
	 - Testing codes: 
		> - **'basic_tests.py'** which includes every function test with prectical examples and values.
		>
		> -  **'tests.py'** that tests all the function using strategies defined in hypothesis library.
		>The pytest framework is needed to run the codes, if it is not yet installed, run ``pip install -U pytest`` from the terminal.
	 - Folders: 
		>- **'data'** is filled with .txt files where you can find the path of each .csv file inside the csv folders included in 'data'. Csv files need two columns; it is necessary that the first one is named *'Nominal Diameter (mm)'* and at least 9 rows and at most 12. Txt files must be organized as follow:
			>		
			```
			alpha = path
			alpha (...) = "~/csvFolder/csvFilealpha"
			...
			human (...) = "~/csvFolder/csvFilehuman"
			```
					             
		>- **'pkl'** contains .pkl and .npy files saved during the code execution.
		
 3. Execute the three scripts in the follower order  on your terminal: 
	 >i.  Contrast_detail.py
	 >ii. minimization.py
	 >iii. Statistics.py 
	 
	 Running Contrast_detail.py, two dialog windows are opened. The first one requires the selection of the local directory where finding data (.txt, .csv). An example is given choosing 'data' folder in CHOanalysis directory. The second dialog window wants  the .txt file chosen as input for the code. From the given dataset choose .txt file in 'data folder. Then, before continuing, press the "continue" button in the tk dialogue box.
	 
4. Enjoy the results and how the project works.

## Limitations
Opening dialogue boxes, using the tkinter library, generates a crashing bug on Windows 64 bit with the current version of Python (see below).
This issue does not hinder the execution of the program, which still works.
	 


#### Python version used for this project : 3.9.6 

	