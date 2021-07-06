import os, sys
from ROOT import *
from glob import glob
from GridEngineTools import runParallel
import argparse

def do_submission(commands, output_folder, condorDir = "condor", executable = "analyzer.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm, babysit=False)


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')

    args = parser.parse_args()
    test = args.test

    executable = 'analyzer_DY.py'
    #executable = 'analyzer_DY_doublesmear.py'
    #executable = 'analyzer_DY_MIH.py'

#Inputfile txt path 
    path = "./inputs/"
    #inputfiles = sorted(glob(path+'/Run2016*-SingleMuon.txt')+glob(path+'/Summer16*.txt'))
    #inputfiles = sorted(glob(path+'/*.txt'))
    #inputfiles = sorted(glob(path+'/Run2016*.txt'))
    #inputfiles = sorted(glob(path+'/Run2017*.txt'))
    #inputfiles = sorted(glob(path+'/Run2018*.txt'))
    #inputfiles = sorted(glob(path+'/Summer16*.txt'))
    #inputfiles = sorted(glob(path+'/RunIIFall17*.txt'))
    #inputfiles = sorted(glob(path+'/Run2016*-SingleMuon.txt')+glob(path+'/Run2017*-SingleMuon.txt')+glob(path+'/Run2018*-SingleMuon.txt'))
    inputfiles = sorted(glob(path+'/Summer16*.txt')+glob(path+'/RunIIFall17*.txt'))
    #inputfiles = sorted(glob(path+'/RunIISummer16MiniAODv3.SMS*.txt'))
    #inputfiles = ["./inputs/Run2016H-SingleMuon.txt"]
    #inputfiles = ["./inputs/Run2016H-SingleElectron.txt"]
    #inputfiles = ["./inputs/Run2017B-SingleMuon.txt"]
    #inputfiles = ["./inputs/Run2018D-EGamma.txt"]
    #inputfiles = ["./inputs/Summer16.WJetsToLNu_HT-100To200.txt"]
    #inputfiles = ["./inputs/Summer16.DYJetsToLL_M-50_TuneCUETP8M1.txt"]
    #inputfiles = ["./inputs/RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5.txt"]
   
    #condorDir = 'condor_data'
    condorDir = 'condor_mc'
    #condorDir = 'condor_2016'
    #condorDir = 'condor_2017'
    #condorDir = 'condor_2018'
    #condorDir = 'condor_Summer16'
    #condorDir = 'condor_Fall17'
    #condorDir = 'condor_RunIISignal'
    #condorDir = 'condor_RunIIFall17_FastSim_T1qqqq'
    
    output_dir = "./output_smallchunks/"
    #output_dir = "./output_smallchunks_MIH/"
    if not os.path.exists(output_dir):
	os.system("mkdir -p "+output_dir)
	print "Making output_dir :", output_dir
    else : print "output_dir exist :", output_dir
    
    # Number of split per inputfile
    split = True
    nsplit = 100
    isfast = False

    commands=[]
    lines=[]
    for inputfile in sorted(inputfiles):
	cnt = 0
        #if "SMS" in inputfile : split = False
        if "FastSim" in inputfile : isfast = True
	with open(inputfile) as f:
	    lines = f.readlines()
	    if split : 
		input_chunks = [lines[i * nsplit:(i + 1) * nsplit] for i in range((len(lines) + nsplit - 1) // nsplit )] 
		for i,chunk in enumerate(input_chunks):
		    output = inputfile.split('/')[-1].replace('.txt','_'+str(i)+'.root')
		    chunk = str(chunk).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
		    command = "python {} --input {} --output_dir {} --output {} ".format(executable, chunk, output_dir, output)
		    if isfast : 
			command += "--fast"
        	    commands.append(command)

	    elif not split : 
		output = inputfile.split('/')[-1].replace('.txt','.root')
		chunk = str(lines).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
		command = "python {} --input {} --output_dir {} --output {} ".format(executable, chunk, output_dir, output)
		if isfast :
		    command += " --fast"
        	commands.append(command)
	    else : 
		print('Something wrong in splitting')
		quit()
    
    # Submit
    if not test : do_submission(commands, output_dir, condorDir=condorDir, executable=executable)
