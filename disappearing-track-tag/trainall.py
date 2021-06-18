#!/bin/env python
import sys, os, glob
from GridEngineTools import runParallel

labels_a = [
            "sgtest",
            #"stop",
            #2,
            #3,
            #4,
            #5,
            #6,
         ]
labels_b = [
            "baseline",
            #"boosted",
            #"compressed",
            #"corner",
            #"inverted",
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

#folders = [
#            "2016-short-tracks-may21v2",
#            "2016-long-tracks-may21v2",
#            "2017-short-tracks-may21v2",
#            "2017-long-tracks-may21v2",
#          ]
          
skim_folder = "/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/ntupleanalyzer/skim_88_mcbranches_merged"
mode = "grid"
          
#runParallel(["./trainBDT.py --category short --use_chi2 --dxyinformed --equalSgXsec --path %s"], "grid", condorDir=condorDir, use_more_mem=True, confirm=False, babysit=False)
#runParallel(["./trainBDT.py --category long --dxyinformed --use_chi2 --equalSgXsec --path %s"], "grid", use_more_mem=True, confirm=False, babysit=False)
#runParallel(["./trainBDT.py --category long --use_chi2 --dxyinformed --equalSgXsec --phase 1 --path %s"], "grid", use_more_mem=True, confirm=False, babysit=False)
#runParallel(["./trainBDT.py --category short --use_chi2 --dxyinformed --equalSgXsec --phase 1 --path %s"], "grid", use_more_mem=True, confirm=False, babysit=False)

for phase, year in enumerate([2016, 2017]):
    for category in ["short", "long"]:
        for label_a in labels_a:
            for label_b in labels_b:
                #foldername = "optimize-%s-ndepth%s-ntrees%s" % (i_folder, i_ndepth, i_ntrees)
                #foldername = "sgtest-%s-%s-%s" % (i_folder, i_ndepth, i_ntrees)
                foldername = "%s-%s-tracks-%s-%s" % (year, category, label_a, label_b)
                #if not os.path.exists(foldername + "/output.root"):
        
                #os.system("sed -i 's@multi@grid@' %s/run_on_grid.py" % i_folder)
        
                # copy files
                os.system("mkdir -p " + foldername)
                os.system("mkdir -p " + foldername + "/condor")
                #os.system("cp %s/run_on_grid.py %s/" % (i_folder, foldername))
                
                # start
                #os.system("cd %s; python run_on_grid.py &" % foldername)
                    
                cwd = os.getcwd()
                folder_full = os.getcwd() + "/" + foldername
                
                runParallel(["cd %s; cp ../trainBDT_template.py trainBDT.py; chmod +x trainBDT.py; ./trainBDT.py --category %s --phase %s --use_chi2 --dxyinformed --equalSgXsec --path %s" % (folder_full, category, phase, skim_folder)], mode, condorDir=foldername + "/condor", use_more_mem=True, confirm=False, babysit=False)
                
                os.chdir(cwd) 
                