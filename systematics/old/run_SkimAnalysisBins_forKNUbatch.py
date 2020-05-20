#!/bin/env python
import sys, os
from glob import glob
from GridEngineTools import runParallel

def main() :
    
    inputDir = "./inputs"
    #outputDir = "./output"
    outputDir = "./output_test"
    
    #inputfiles = glob(inputDir+"/Input_*.txt")
    inputfiles = glob(inputDir+"/Input_g1800_chi1400_27_200970_step4_100.txt")
    if not os.path.exists(outputDir) : 
	os.system("mkdir -p "+outputDir)
    else: 
	os.system("rm -rf "+outputDir)
	os.system("mkdir -p "+outputDir)
	
    #syst_args = ""	    # for systematics(eg. --dojetsyst --nsigmajes 1)
    #syst_args = "-dobtagsf -nsigmabtagsf 1"	    # for systematics(eg. --dojetsyst --nsigmajes 1)
    syst_args = "-doISR -nsigmaISR 1"	    # for systematics(eg. --dojetsyst --nsigmajes 1)
    
    commands = []
    
    for inputfile in inputfiles :
	outfilename = inputfile.replace(inputDir,outputDir).replace('Input_','skim_').replace('txt','root')
	command = 'python SkimAnalysisBins_forKNUbatch.py -fin %s -fout %s %s' %(inputfile, outfilename, syst_args)
	commands.append(command)

    	# local test
    	os.system(command)

    ### For batch job
    #runParallel(commands, runmode='grid', dryrun=True, qsubOptions='-q cms', dontCheckOnJobs=True)    
    #runParallel(commands, runmode='multi', dryrun=False, dontCheckOnJobs=True)    

if __name__ == '__main__' :
    main()

