#!/bin/env python
import sys, os, glob
from GridEngineTools import runParallel
from itertools import combinations

labels_a = [
            #"sgtest",
            #"jul21",
            #"aug21",
            #"aug21v3",
            #"aug21v4",
            #"aug21v5",
            "sep21v1",
            #"sgsamples",
            #"stop",
            #2,
            #3,
            #4,
            #5,
            #6,
         ]

labels_b = [
            "baseline",
            #"noDeltaPt",
            #"noPixelHits",
            #"noPixelHits-noDeltaPt",
            #"boosted",
            #"compressed",
            #"corner",
            #"inverted",
            #"both",
            #"onlyT1qqqq",
            #"onlyT2bt",
            #"noRelIso",           
            #"useLayers",
            #"noPixelHits-noDeltaPt",
            #"noPixelHits-useLayers",
            #"TighterDxy",
            #"noJetVeto",
            #"noVetoes",
            #"oldWeights",
            #"oldWeights-noJetVeto",
            #"oldWeights-noVetoes",
            #25,
            #50,
            #75,
            #100,
            #150,
            #200,
            #250,
            #300,
            #400,
            #600,
         ]

vars = [
            #"noDxy",
            #"noDz",
            #"noRelIso",
            #"noPixelHits",
            #"noDeltaPt",
            #"noChi2perNdof",
            "withDxy",
            "withDz",
            "withRIso",
            "withPHits",
            "withDPt",
            "withChi2",
        ]

unique_combinations = []
for i in range(1, len(vars) + 1):
    unique_combinations += ["-".join(map(str, comb)) for comb in combinations(vars, i)]   
print unique_combinations

#labels_b += unique_combinations

skim_folder = "/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/ntupleanalyzer/skim_88_mcbranches_merged"
mode = "grid"

for year in [
              2016,
              2017,
            ]:

    if year == 2016:
        phase = 0
    else:
        phase = 1

    for category in [
                      "short",
                      "long",
                    ]:

        for label_a in labels_a:
            for label_b in labels_b:
                
                if label_b == "":
                    foldername = "%s-%s-tracks-%s" % (year, category, label_a)
                else:
                    foldername = "%s-%s-tracks-%s-%s" % (year, category, label_a, label_b)

                print foldername
                
                os.system("mkdir -p " + foldername)
                os.system("mkdir -p " + foldername + "/condor")
                
                cwd = os.getcwd()
                folder_full = os.getcwd() + "/" + foldername
                
                cmd = "cd %s; cp ../trainBDT_template.py trainBDT.py; cp ../trainall.py trainall.py; chmod +x trainBDT.py; ./trainBDT.py --category %s --phase %s --path %s" % (folder_full, category, phase, skim_folder)
                if mode == "grid":
                    runParallel([cmd], "grid", condorDir=foldername + "/condor", use_more_mem=True, confirm=False, babysit=False)
                else:
                    os.system("%s &> condor/0.sh.o &" % cmd)
                    
                os.chdir(cwd)
                
