#!/bin/env python
import sys, os, glob
import multiprocessing
from GridEngineTools import runParallel

runmode = "grid"

output_folder = "output_qcd_masked"

os.system("mkdir -p %s" % output_folder)
commands = []

ntuples_folder = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2"

cmssw8_samples = [
                    "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Run2016B-03Feb2017_ver2-v2.SingleElectron",
                    "Run2016B-03Feb2017_ver2-v2.SingleMuon",
                    "Run2016C-03Feb2017-v1.SingleElectron",
                    "Run2016C-03Feb2017-v1.SingleMuon",
                 ]

for sample in cmssw8_samples:

    ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + "*.root"))
    
    if len(ifile_list)==0:
        continue

    print "Looping over %s files (%s)" % (len(ifile_list), sample)

    files_per_job = 3
    file_segments = [ifile_list[x:x+files_per_job] for x in range(0,len(ifile_list),files_per_job)]

    for inFile_segment in file_segments:
            
        out_tree = output_folder + "/" + inFile_segment[0].split("/")[-1].split(".root")[0] + "_fakes.root"
        commands.append("./fakerate_looper.py %s %s 0 0" % (str(inFile_segment).replace(", ", ",").replace("[", "").replace("]", ""), out_tree))

raw_input("submit %s jobs?" % len(commands))
os.system("cp fakerate_looper.py %s/" % output_folder)
runParallel(commands, runmode, dontCheckOnJobs=True, burst_mode=False)

