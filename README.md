# PixelLeakageCurrentMonitor
This tool is implemented for the communication with CMS OMDS database and customized plotter on the pixel leakage currents. 

First step:
One needs to log on lxplus in order to include the Oracle base dependence. Then get the data points of pixel currents from the CMS database:

python getCurrentFromDB.py

Second step:
Compute the mean value and RMS of pixel leakage current for each layer during a specific period.

python currentReader.py

Third step:
Use pyROOT to plot the leakage current dependence.

python currentPlotter.py

Enjoy!
