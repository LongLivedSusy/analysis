#!/bin/env python
import sys, os, glob
import multiprocessing
from GridEngineTools import runParallel

# apply TMVA result: output BDT classifier into tree

runmode = "grid"

def applyBDT(inpath, outpath, bdt_folder):

    os.system("mkdir -p %s" % outpath)
    print "Copying files..."
    os.system("cp -r %s/* %s/" % (inpath, outpath))

    commands = []

    for iFile in glob.glob(outpath + "/*.root"):

        commands.append("./apply_weights.py %s %s" % (iFile, bdt_folder))

    print commands
    runParallel(commands, runmode, cmsbase="/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_8_0_28/src", dontCheckOnJobs=True)


if __name__ == "__main__":
   
    applyBDT("/nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7d/tracks-mini-short",
             "/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/tracks-mini-short-bdt",
             "/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel3-200-4-short-nodxyVtx")

    applyBDT("/nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7d/tracks-mini-medium",
             "/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/tracks-mini-medium-bdt",
             "/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel2-200-4-medium-nodxyVtx")

