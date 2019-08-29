import os, sys
from glob import glob


fgslist = glob('/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/Disptrks_Aug2019_MC_generation_30cm/*/*/*.root')

for fgs in fgslist:
    command = 'gfal-rename -n 1 "file:////'+fgs+'" "srm://dcache-se-cms.desy.de:8443//pnfs/desy.de/cms/tier2/store/user/aksingh/"'
    print 'doing', command
    os.system(command)
