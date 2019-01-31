#!/bin/env python
from glob import glob
import os

for folder in glob("./tmva/cmssw10*"):
    os.chdir(folder)
    os.system("./run_on_grid.py")
    os.chdir("../..")
