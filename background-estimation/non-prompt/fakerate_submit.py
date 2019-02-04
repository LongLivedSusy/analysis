#!/bin/env python
import sys, os, glob
import multiprocessing
from GridEngineTools import runParallel

runmode = "grid"
output_folder = "output_fakerate"
files_per_job = 5
files_per_sample = -1

os.system("mkdir -p %s" % output_folder)
commands = []

def create_command_list(ntuples_folder, samples):

    for sample in samples:

        ifile_list = sorted(glob.glob(ntuples_folder + "/" + sample + "*.root"))
        
        if files_per_sample != -1:
            ifile_list = ifile_list[:files_per_sample]
        
        if len(ifile_list)==0:
            continue

        print "Looping over %s files (%s)" % (len(ifile_list), sample)

        # check if (not) running over QCD events:
        if "QCD" in sample or "JetHT" in sample:
            current_files_per_job = 2
        else:
            current_files_per_job = files_per_job
        
        file_segments = [ifile_list[x:x+current_files_per_job] for x in range(0,len(ifile_list),current_files_per_job)]

        for inFile_segment in file_segments:
                
            out_tree = output_folder + "/" + inFile_segment[0].split("/")[-1].split(".root")[0] + "_fakes.root"
            commands.append("./fakerate_looper.py %s %s 0 0" % (str(inFile_segment).replace(", ", ",").replace("[", "").replace("]", ""), out_tree))

cmssw8_samples = [
                    "Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                    "Summer16.WW_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.ZZ_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.WZ_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Run2016B-03Feb2017_ver2-v2.SingleElectron",
                    "Run2016B-03Feb2017_ver2-v2.SingleMuon",
                    "Run2016C-03Feb2017-v1.SingleElectron",
                    "Run2016C-03Feb2017-v1.SingleMuon",
                    "Run2016D-03Feb2017-v1.SingleElectron",
                    "Run2016D-03Feb2017-v1.SingleMuon",
                    "Run2016E-03Feb2017-v1.SingleElectron",
                    "Run2016E-03Feb2017-v1.SingleMuon",
                    "Run2016F-03Feb2017-v1.SingleElectron",
                    "Run2016F-03Feb2017-v1.SingleMuon",
                    "Run2016G-03Feb2017-v1.SingleElectron",
                    "Run2016G-03Feb2017-v1.SingleMuon",
                    "Run2016H-03Feb2017_ver2-v1.SingleElectron",
                    "Run2016H-03Feb2017_ver2-v1.SingleMuon",
                 ]

cmssw9_samples = [
                    "Run2016C-17Jul2018-v1.JetHT",
                    "Run2016E-17Jul2018-v1.JetHT",
                    "Run2016F-17Jul2018-v1.JetHT",
                    "Run2016G-17Jul2018-v1.JetHT",
                    "Run2016H-17Jul2018-v1.JetHT",
                 ]

create_command_list("/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2", cmssw8_samples)
create_command_list("/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v2", cmssw9_samples)

raw_input("submit %s jobs?" % len(commands))
os.system("cp fakerate_looper.py %s/" % output_folder)
runParallel(commands, runmode, dontCheckOnJobs=True, burst_mode=False)


