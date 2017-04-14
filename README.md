# What is DOE2py?
It is a set of Python scripts that can be used to facilitate the process of running building energy simulations using DOE-2. **This project is a work in progress. Use at your own risks!**

# Useful scripts:
### RunDOE2
Synthax:
`DOE2py.py RunDOE2 path_inp_file path_weather_file DOE2version`

* `path_inp_file`: complete path to the DOE-2 input file, do not include the extension.
* `path_weather_file`: complete path to the DOE-2 input file, include the extension.
* `DOE2version`: name of the version of DOE-2 used for the simulation

### GUI
Synthax:
`DOE2py.py GUI`

Open a small GUI that can be used to select input and weather files as well as copy library files (`Usrlib.dat`, e.g. from eQUEST) to the folder of the version of DOE-2 selected to run the simulation. The copy is done right before the simulation.

### Extract
Synthax: `DOE2py.py Extract report_name1 report_name2 etc ...`

This script extract some user specified DOE-2 report out of a .SIM file. I am using this script to extract the reports requested by GBCI for review of LEED projects. They are written in a SIM file ending in `-ext_rpts.SIM`.

* `report_name1`, `report_name2`, etc. Is the name of the DOE-2 report to extract from the .SIM file.

# Future updates:
* Create *nice* customizable output form using the D2Result.dll file, html?, json?, sqlite? markdown?