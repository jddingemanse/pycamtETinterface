# pycamtETinterface
In the package [pycamtET](https://github.com/jddingemanse/pycamtET), relevant data processing tools for Ethiopian meteorological data are bundled. The package pycamtETinterface holds code for a Jupyter-Notebook widget interface that can operate the functions of pycamtET.
Both packages are fully under development, so you can expect regular changes.

## Installation
First, make sure git is installed.
```
conda install git
```
If git is installed, you can install pycamtETinterface with:
```
pip install git+https://github.com/jddingemanse/pycamtETinterface.git
```
pycamtETinterface is strictly meant for usage in jupyter notebook, to provide an interface that operates functions of the package pycamtET. In other words, to work with pycamtETinterface, you must also install the package pycamtET:
```
pip install git+https://github.com/jddingemanse/pycamtET.git
```

## Use example
To use the interface for dekadal analysis, in a jupyter-notebook you must:
- set the path to your datafile (with Ethiopian Meteorology Institute station data), and load/preprocess this data with pycamtET.dataFunctions.dataload()
```
filePath = 'pathToYourDatafile'
from pycamtET import dataFunctions as dFu
dfAll = dFu.dataLoad(filePath)
```
- set the paths to Ethiopian adm0, adm1, adm2 and adm3 shapefiles (nb: if Geopandas is not installed, or shapefiles are not available, the interface will load without mapping abilities)
```
shapeAdm0 = 'pathToETadm0ShapeFile'
shapeAdm1 = 'pathToETadm1ShapeFile'
shapeAdm2 = 'pathToETadm2ShapeFile'
shapeAdm3 = 'pathToETadm3ShapeFile'
from pycamtET.pckgSettings import setSettings
setSettings(adm0Path=shapeAdm0,adm1Path=shapeAdm1,adm2Path=shapeAdm2,adm3Path=shapeAdm3)
```
- set a path where to save any output (set it to None to not save output, set it to 'default' to save it in your Documents/PYCAMT/output folder
```
savePath = 'default'
```
- import the dekadal interface function
```
from pycamtETinterface.interface import interfaceDk
```
- run the interface function with the loaded data and provided savePath (advice: run it in a separate cell; it will create an interface as output to that cell, based on which additional plots as output can be created. To reset the interface, you can simply run this cell again)
```
interfaceDk(dfAll,savePath)
```
