#!/bin/env python
from prepareTreeMakerTrees import treeConvertEventToTrackLevel, createFolderSnapshot
from GridEngineTools import runParallel

if __name__ == "__main__":
    
    # do background:
    if False:
        inputFolder = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/DisappTrksNtupleSidecar-cmssw10"
        outputFolder = "/nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7g"
        createFolderSnapshot([inputFolder], outputFolder + "/snapshot")
        treeConvertEventToTrackLevel(outputFolder + "/snapshot", outputFolder, nevents = 100000)

    # do signal:
    if False:
        inputFolder = "/nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/CMSSW10/TREEMAKER"
        outputFolder = "/nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7g"
        treeConvertEventToTrackLevel(inputFolder, outputFolder)

    # combine signal:
    if True:
        commands = ["hadd -f /nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw10/tracks-short/signal.root /nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw10/tracks-short/g1800*.root",
                   "hadd -f /nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw10/tracks-medium/signal.root /nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw10/tracks-medium/g1800*.root",
                   ] 
        runParallel(commands, "grid", cmsbase = "/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_8_0_28/src")
