#!/bin/env python
import sys, os
from glob import glob
from GridEngineTools import runParallel

def read_syst(txt) :
    list_systs = []
    with open (txt,"r") as fsyst :
	while True : 
	    line = fsyst.readline().strip()
	    if not line : break
	    if line.startswith("#") : continue	# ignore commented line in txt file
	    line = line.split()
	    list_systs.append(line)

    return list_systs


if __name__ == '__main__' :
    
    inputfiles = glob("../dedx/inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.txt")
    
    systs = read_syst("./syst_sigmas.txt")

    commands = []

    for syst in systs : 
        for inputfile in inputfiles :
	    outputDir = 'output_'+syst[0]
	    sigmas = syst[1:]
	    if not os.path.exists(outputDir):
		os.system("mkdir -p "+outputDir)
	    
	    command = 'python SkimSystematics.py %s %s "%s"' %(inputfile, outputDir, sigmas)
	    commands.append(command)
    
    print commands[0]
    #os.system(commands[0])  #For local test
        		
    ### For batch job
    #runParallel(commands, runmode='grid', dryrun=False, qsubOptions='-q cms', dontCheckOnJobs=True)    
    #runParallel(commands, runmode='multi', dryrun=False, dontCheckOnJobs=True)    

