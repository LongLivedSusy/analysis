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

def main() :
    
    inputDir = "./inputs"
    
    #inputfiles = glob(inputDir+"/Input_*.txt")
    inputfiles = glob(inputDir+"/Input_g1800_chi1400_27_200970_step4_100.txt")
    #inputfiles = glob(inputDir+"/Input_pMSSM12_MCMC1_12_865833_step4_TREEMAKER_RA2AnalysisTree.txt")
    
    systs = read_syst("./Sigma_systematics.txt")

    commands = []

    for syst in systs : 
        for inputfile in inputfiles :
	    outputDir = 'output_'+syst[0]
	    sigmas = syst[1:]
	    if not os.path.exists(outputDir):
		os.system("mkdir -p "+outputDir)
	    
	    command = 'python SkimSystematics.py %s %s "%s"' %(inputfile, outputDir, sigmas)
	    commands.append(command)
	#os.system(command)  #For local test
        		
    ### For batch job
    runParallel(commands, runmode='grid', dryrun=False, qsubOptions='-q cms', dontCheckOnJobs=True)    
    #runParallel(commands, runmode='multi', dryrun=False, dontCheckOnJobs=True)    

if __name__ == '__main__' :
    main()

