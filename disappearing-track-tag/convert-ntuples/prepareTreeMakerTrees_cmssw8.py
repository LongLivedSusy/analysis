#!/bin/env python
from prepareTreeMakerTrees import treeConvertEventToTrackLevel, createFolderSnapshot

if __name__ == "__main__":
    
    # do background:
    inputFolder = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/DisappTrksNtupleSidecarI7"
    outputFolder = "/nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecar-cmssw8"
    createFolderSnapshot([inputFolder], outputFolder + "/snapshot")
    treeConvertEventToTrackLevel(outputFolder + "/snapshot", outputFolder, nevents = 100000)

    
