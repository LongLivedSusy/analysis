#!/bin/env python
from GridEngineTools import runParallel
import os

os.system("cp ../trainBDT_template.py trainBDT.py; chmod +x trainBDT.py")
runParallel(["./trainBDT.py --category long --dxyinformed"], "grid", confirm=False, babysit=False)

