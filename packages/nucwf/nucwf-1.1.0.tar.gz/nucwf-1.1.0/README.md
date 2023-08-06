# NUCWF

Library for online accessing, reading and writing A=3 and A=4 wave functions.

When using the data files or software, please cite the original work:



## Installation 

The source code and examples are available at 
https://jugit.fz-juelich.de/a.nogga/nucwavef.git

The easiest way to install is using pip: 
```
pip install nucwf 
```

## Usage
The package provides an interface to download the data files from our repository and to read the files and test.
More advanced options will be documented elsewhere.
Jupyter notebook downloading an example data base in `examples`.
This directory also includes some example scripts to modify the database locally.

For downloading specific files to a local directory, e.g.,  `$HOME/work/wftest` use 
```
import os 
from nucwf import access
testdf=access.database(workdir=os.environ["HOME"]+"/work/wftest")
```
This downloads a pandas dataframe with the available wave function files and stores it into  `testdf` . The pandas dataframe can be printed using 
```
import pandas as pd  
pd.set_option('display.max_columns', None)
print(testdf.pddf)
```

Downloading wave function files of, e.g., row 4  of the table is done by 
```
import os 
# get file info from table 
row=testdf.pddf.loc[[4]]
wfid=row.to_dict('records')[0]
# retrieve file
hashname,uniquename=testdf.get_file(**wfid)
# print name and file size 
print("hashname:    ",hashname)
print("filesize:    ",os.path.getsize(hashname))
print("uniquename:  ",uniquename)
```
The files are downloaded and gunzipped. They are partly also compressed using the ZFP compressors (see https://github.com/LLNL/zfp).
Using the files might require to install the corresponding HDF plugins (https://github.com/LLNL/H5Z-ZFP).
The local files will be first stored under their `hashname`.
However, the python method also returns a suggestion for a unique file name `uniquename`
that includes the parameters of the file.  If wanted, users may rename the file using the provided `uniquename`. 

The database contains two kinds to files: A=3 and A=4 wave functions.
You can read in and get some basic properties using the wavefilea4 constructor
```
wfa4=access.wavefilea4(hashname,printlevel=1)
```

A=3 wave functions can be tested similarly using the wavefilea3 constructor
```
wfa3=access.wavefilea3(hashname,printlevel=1)
```









