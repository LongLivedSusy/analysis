#!/bin/env python
from GridEngineTools import runParallel
runParallel(["./runTMVA.sh"], "grid", cmsbase="/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_8_0_28/src", dontCheckOnJobs=True, use_more_mem=True, use_more_time=43200)

