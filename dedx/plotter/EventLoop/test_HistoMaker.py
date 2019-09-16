#!/usr/bin/env python
import os, sys
import subprocess
from glob import glob
from ROOT import *
from GridEngineTools import runParallel

Recompile=True
#Recompile=False

OUTDIR = "./histos_test"

if __name__ == '__main__' :

    if Recompile : 
	print ("============Recompiling HistoMaker...==============")
	subprocess.call("./compile_HistoMaker.sh", stdin=None, stdout=None, stderr=None, shell=True)
    
    if not os.path.exists(OUTDIR):
	#subprocess.Popen("mkdir -p %s"%OUTDIR,stdin=None, stdout=None, stderr=None, shell=True)
	os.system("mkdir -p %s"%OUTDIR)

    # Samples
    #path = "../../skimmer/output_skim_Summer16_Run2016MET_merged/"
    path = "../../skimmer/output_skim_Summer16_merged/"
    #samples = ["Summer16.DYJetsToLL_M-50_TuneCUETP8M1"]
    #samples = ["Summer16.WW_"]
    samples = ["Summer16.g1800_chi1400_27_200970_step4_*AODSIM"]
    inputfiles=[]
    for sample in samples : 
	inputlist = glob(path+"/*%s*.root"%sample)
	inputfiles.extend(inputlist)
    
    inputfiles = sorted(inputfiles)

    commands=[]
    for inputfile in inputfiles: 
	label = inputfile.split("/")[-1]
	isData = False
	isSignal = False
	if "Run" in label : isData = True
	elif "g1800" in label : isSignal = True

	command = "./HistoMaker %s %s h_%s %s %s"%(inputfile,OUTDIR,label,isData,isSignal)
	commands.append(command)
	print "input files : %s, isData :%s, isSignal : %s"%(label,isData,isSignal)
    
    raw_input("Submit continue?")
    #runParallel(commands, "grid", condorDir="condor", dontCheckOnJobs=True)
    runParallel(commands, "multi", condorDir="condor", dontCheckOnJobs=True)
