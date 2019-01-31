#!/bin/env python
import sys, os, glob
import multiprocessing
from GridEngineTools import runParallel
import ROOT

def treeConvertEventToTrackLevel(treepath, outputFolder, nevents = "", samples = False, cmsbase = "/afs/desy.de/user/k/kutznerv/cmssw/CMSSW_8_0_28/src", runmode = "grid", debug = False):

    # get sample names from file names:
    if not samples:
        
        samples = []
        all_files = glob.glob(treepath + "/*.root")

        for iFile in all_files:
            sample_name = "_".join(iFile.split("_RA2AnalysisTree.root")[0].split("_")[:-1]).split("/")[-1]
            if sample_name not in samples:
                samples.append(sample_name)
        
        print "Using sample names:", samples

    # convert event-level trees to track-level trees

    commands = []
    nevents_original = nevents

    for category in ["short", "medium"]:

        output_path = "%s/tracks-%s" % (outputFolder, category)

        os.system("mkdir -p %s " % output_path)

        for sample in samples:

            infiles = treepath + "/" + sample + "\*.root"
            outfile = output_path + "/" + sample + ".root"

            # don't restrict number of signal events:
            if "signal" in sample:
                if nevents != "":
                    nevents_original = nevents
                nevents = ""
            else:
                nevents = nevents_original

            cmd = "./convert_to_tracklevel.py %s %s %s %s" % (infiles, outfile, category, nevents)
            commands.append(cmd)

    print commands
    
    if debug:
        # run only one command locally
        runmode = "multi"
        commands = [ commands[-1] ]

    runParallel(commands, runmode, cmsbase = cmsbase)


def createFolderSnapshot(inputFolders, trackLevelTreeOutput):

    # create folder listing snapshot in case not all jobs are done yet
    for inputFolder in inputFolders:
        os.system("mkdir -p %s" % trackLevelTreeOutput)
        os.system("ln -s %s/* %s/" % (inputFolder, trackLevelTreeOutput))

    
