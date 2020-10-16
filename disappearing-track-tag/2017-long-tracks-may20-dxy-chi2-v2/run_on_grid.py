#!/bin/env python
from GridEngineTools import runParallel
import os

os.system("cp ../trainBDT_template.py trainBDT.py; chmod +x trainBDT.py")
runParallel(["./trainBDT.py --category long --use_chi2 --dxyinformed --phase 1 --path /afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/ntupleanalyzer/skim_51_run2"], "grid", confirm=False, babysit=False)

