#!/usr/bin/env python
import os, sys
import subprocess
from glob import glob
from ROOT import *
from GridEngineTools import runParallel

Recompile=True
#Recompile=False

OUTDIR = "./histos"
#OUTDIR = "./histos_test"

if __name__ == '__main__' :

    if Recompile : 
	print ("============Recompiling HistoMaker...==============")
	subprocess.call("./compile_HistoMaker.sh", stdin=None, stdout=None, stderr=None, shell=True)
    
    if not os.path.exists(OUTDIR):
	#subprocess.Popen("mkdir -p %s"%OUTDIR,stdin=None, stdout=None, stderr=None, shell=True)
	os.system("mkdir -p %s"%OUTDIR)

    # Samples
    path = "../../skimmer/skim_16DataMCv4_merged/"
    #samples = ["*"]
    #samples = ["Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]
    samples = ["*Summer16*","Run2016*MET*"]
    
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
	if "Run201" in label : 
	    isData = True
	elif "g1800" in label or "SMS" in label : 
	    isData = False
	    isSignal = True
	
	command = "./HistoMaker %s %s h_%s %s %s"%(inputfile,OUTDIR,label,isData,isSignal)
	commands.append(command)
	print "input files : %s, isData :%s, isSignal : %s"%(label,isData,isSignal)
    
    runParallel(commands, "grid", condorDir="condor", dontCheckOnJobs=True)
    #runParallel(commands, "multi", condorDir="condor", dontCheckOnJobs=True)

