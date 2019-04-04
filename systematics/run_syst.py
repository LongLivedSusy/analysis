#!/bin/env python
import sys, os
from glob import glob
from GridEngineTools import runParallel

def read_syst(txt) :
    list_nsigmas = []
    with open (txt,"r") as fsyst :
	while True : 
	    line = fsyst.readline().strip()
	    if not line : break
	    if line.startswith("#") : continue	# ignore commented line in txt file
	    line = line.split()
	    nsigmas = [int(x) for x in line ]	# convert type : string to integer 
	    list_nsigmas.append(nsigmas)
    return list_nsigmas

def outputDirMaker(sigma) : 
    outputDir = "outputs"
    n = len(sigma)
    if sigma[0] >0  : outputDir+='_btag_%sUp'%sigma[0]
    if sigma[1] >0  : outputDir+='_jes_%sUp'%sigma[1]
    if sigma[2] >0  : outputDir+='_jer_%sUp'%sigma[2]
    if sigma[3] >0  : outputDir+='_isr_%sUp'%sigma[3]
    if sigma[0] <0  : outputDir+='_btag_%sDown'%abs(sigma[0])
    if sigma[1] <0  : outputDir+='_jes_%sDown'%abs(sigma[1])
    if sigma[2] <0  : outputDir+='_jer_%sDown'%abs(sigma[2])
    if sigma[3] <0  : outputDir+='_isr_%sDown'%abs(sigma[3])
    if not os.path.exists(outputDir):
	os.system("mkdir -p "+outputDir)
    else : 
	os.system("rm -rf "+outputDir)
	os.system("mkdir -p "+outputDir)
    return outputDir

def main() :
    
    inputDir = "./inputs"
    
    #inputfiles = glob(inputDir+"/Input_*.txt")
    inputfiles = glob(inputDir+"/Input_pMSSM12_MCMC1_12_865833_step4_TREEMAKER_RA2AnalysisTree.txt")
    
    sigmas = read_syst("Sigma_systematics.txt")

    commands = []

    for sigma in sigmas : 
	outDir=outputDirMaker(sigma)

        for inputfile in inputfiles :
	    command = 'python SkimSystematics.py %s %s "%s"' %(inputfile, outDir, sigma)
	    commands.append(command)
	#os.system(command)
        		
    ### For batch job
    runParallel(commands, runmode='grid', dryrun=False, qsubOptions='-q cms', dontCheckOnJobs=True)    
    #runParallel(commands, runmode='multi', dryrun=False, dontCheckOnJobs=True)    

if __name__ == '__main__' :
    main()

