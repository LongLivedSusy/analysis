#!/usr/bin/env python
import os, sys
import subprocess
from glob import glob
from ROOT import *
from GridEngineTools import runParallel

Recompile=True
#Recompile=False

OUTDIR = "./histos"

if __name__ == '__main__' :

    if Recompile : 
	print ("============Recompiling HistoMaker...==============")
	subprocess.call("./compile_HistoMaker.sh", stdin=None, stdout=None, stderr=None, shell=True)
    
    if not os.path.exists(OUTDIR):
	#subprocess.Popen("mkdir -p %s"%OUTDIR,stdin=None, stdout=None, stderr=None, shell=True)
	os.system("mkdir -p %s"%OUTDIR)

    # Samples
    #path = "../../skimmer/output_skim_Summer16_Run2016MET_merged/"
    path = "../../skimmer/old/output_skim_Summer16_Run2016MET_merged/"
    #samples = ["*"]
    #samples = ["Run2016*"]
    samples = ["Summer16*"]
    #samples = ["Summer16.g1800_"]
    for sample in samples : 
	inputfiles = glob(path+"/*%s*.root"%sample)
    
    inputfiles = sorted(inputfiles)

    commands=[]
    for inputfile in inputfiles: 
	label = inputfile.split("/")[-1]
	if "Run" in label : isData = True
	else : isData = False
	command = "./HistoMaker %s %s h_%s %s"%(inputfile,OUTDIR,label,isData)
	commands.append(command)
	print "input files : %s, isData :%s"%(label,isData)
    
    raw_input("Submit continue?")
    runParallel(commands, "grid", condorDir="condor", dontCheckOnJobs=True)
    #runParallel(commands, "multi", condorDir="condor", dontCheckOnJobs=True)

