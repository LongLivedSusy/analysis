#!/usr/bin/env python
import os, sys
import subprocess
from glob import glob
from ROOT import *
from GridEngineTools import runParallel

#Recompile=True
Recompile=False

OUTDIR = "./histos"

if __name__ == '__main__' :

    if Recompile : 
	print ("============Recompiling HistoMaker...==============")
	subprocess.call("./compile_HistoMaker.sh", stdin=None, stdout=None, stderr=None, shell=True)
    
    if not os.path.exists(OUTDIR):
	#subprocess.Popen("mkdir -p %s"%OUTDIR,stdin=None, stdout=None, stderr=None, shell=True)
	os.system("mkdir -p %s"%OUTDIR)

    # Samples
    path = "../../skimmer/python/output_skim_Summer16MC_merged/"
    samples = ["Summer16"]
    #samples = ["Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV"]
    for sample in samples : 
	inputfiles = glob(path+"/*%s*.root"%sample)

    commands=[]
    for inputfile in inputfiles: 
	label = inputfile.split("/")[-1]
	command = "./HistoMaker %s %s h_%s"%(inputfile,OUTDIR,label)
	commands.append(command)
	print "input files : ", label
    
    raw_input("Submit continue?")
    #runParallel(commands, "grid", condorDir="condor", dontCheckOnJobs=True)
    runParallel(commands, "multi", condorDir="condor", dontCheckOnJobs=True)

