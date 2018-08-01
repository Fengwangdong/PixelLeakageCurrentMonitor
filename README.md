# PixelLeakageCurrentMonitor
This tool is implemented for the communication with CMS OMDS database and customized plotter on the pixel leakage currents. 

First step:
One needs to log on lxplus in order to include the Oracle base dependence. Then get the last data points of pixel currents from the CMS database within the specified time window:

python getCurrentFromDB.py

Second step:
Compute the mean value and RMS of pixel leakage current for each layer during a specific period.

python leakageCurrentReader.py

Third step:
Use pyROOT to plot the leakage current dependence.

python leakageCurrentPlotter.py

Forth step:
Produce the list of module currents for the input of cabling map:

python currentModular.py 

Then one can upload the produced list to the link below to show the colorful cabling map:

http://vocms061.cern.ch/event_display/PixelCablingInterface/pixelcablingweb.php

Enjoy!
