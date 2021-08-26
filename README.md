# CHOanalysis

In this repository a project concerning a Channelized Hotelling Observer model is led.

Starting from a series of .csv documents obtained by a Matlab master code, an accurate analysis is done.
The collected data running the master code give information about the minimum contrast at which a certain diamenter of disks, on a selected phantom, can be seen. The dataset is given for both the human evaluation test and the assessing of the CHO model, changing a noise factor *alpha*. 
First of all, for each distinct protocol, Contrast-detail curves are graphed, and a plot with human curves and *alpha*
-dependent CHO curves is shown.

Then, taking as reference each single human observer curve a minimization is performed with a weighted sum of the distances. The minimization is between the CD points of CHO curve and human curve associated to the same diameter.
In this way, the most similar *alpha*-dependent curve to the human reference one is chosen as better. 