#!/bin/env python
from GridEngineTools import runParallel
import os

os.system("cp ../trainBDT.py .; chmod +x trainBDT.py")
runParallel(["./trainBDT.py --category short"], "grid", confirm=False, babysit=False)

