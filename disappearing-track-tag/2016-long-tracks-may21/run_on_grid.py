#!/bin/env python
from GridEngineTools import runParallel
import os

os.system("cp ../trainBDT_template.py trainBDT.py; chmod +x trainBDT.py")
runParallel(["./trainBDT.py --category long --dxyinformed --use_chi2 --path /afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/ntupleanalyzer/skim_83_merged"], "grid", confirm=False, babysit=False)

