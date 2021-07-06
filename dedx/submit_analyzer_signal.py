import os, sys
from ROOT import *
from glob import glob
import argparse
from GridEngineTools import *

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')

    args = parser.parse_args()
    test = args.test

    # Number of split per inputfile
    #split = True
    split = False
    nsplit = 100
    #isfast = False

    executable = 'analyzer_chargino.py'

    #Inputfile txt path
    inputfiles = [
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.txt",
	    "./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.txt",
	    
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1to200.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100and300.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400to1000.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt",
	    ]
  
    condorDir = 'condor'
    #chosenMass = [[1300,200]]
    #chosenMass = [[2500,1200]]
    #chosenMass = [[2500,1400]]
    #chosenMass = [[2500,1600]]
    #chosenMass = [[2500,1800]]
    chosenMass = [[2500,2000]]
    nev=-1
    #nev=10000
    commands=[]
    lines=[]
    for mass in chosenMass : 
	mstop, mlsp = mass[0], mass[1]
	output_dir = "./output_smallchunks_T2btLL_mstop{}_mlsp{}".format(mstop,mlsp)
    	if not os.path.exists(output_dir):
    	    os.system("mkdir -p "+output_dir)
    	    print "Making output_dir :", output_dir
    	else : print "output_dir exist :", output_dir
    	
	for inputfile in sorted(inputfiles):
    	    cnt = 0
    	    #if "FastSim" in inputfile : isfast = True
    	    with open(inputfile) as f:
    	        lines = f.readlines()
    	        if split :
    	            input_chunks = [lines[i * nsplit:(i + 1) * nsplit] for i in range((len(lines) + nsplit - 1) // nsplit )]
    	            for i,chunk in enumerate(input_chunks):
    	                output = inputfile.split('/')[-1].replace('.txt','_'+str(i)+'.root')
    	                chunk = str(chunk).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
    	                command = "python {} --input {} --output_dir {} --output {} --nev {} --mstop {} --mlsp {}".format(executable, chunk, output_dir, output, nev, mstop, mlsp)
    	                #if isfast : command += "--fast"
    	                commands.append(command)

    	        elif not split :
    	            output = inputfile.split('/')[-1].replace('.txt','.root')
    	            chunk = str(lines).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
    	            command = "python {} --input {} --output_dir {} --output {} --nev {} --mstop {} --mlsp {}".format(executable, chunk, output_dir, output, nev, mstop, mlsp)
    	            #if isfast : command += " --fast"
    	            commands.append(command)
    	        else :
    	            print('Something wrong in splitting')
    	            quit()

    # Submit
    if test : 
	print 'Test command: ',commands[0]
    else :
	if split : 
	    #runParallel(commands, runmode="grid", condorDir=condorDir, dontCheckOnJobs=True, use_more_mem=False, use_more_time=False, confirm = True, babysit=False)
            runParallel(commands, runmode="multi", condorDir=condorDir, dontCheckOnJobs=True, use_more_mem=False, use_more_time=False, confirm = True, babysit=False)
	else : os.system(commands[0])
