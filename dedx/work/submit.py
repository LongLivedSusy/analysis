import os, sys
from ROOT import *
from glob import glob
from GridEngineTools import runParallel

def do_submission(commands, output_folder, condorDir = "condor", executable = "looper.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


if __name__ == "__main__":
    
    #Inputfile txt path
    path = "./inputs/split/"
    samples = ["Summer16.ZJetsToNuNu*"]
    
    output_folder = 'outputs_smallchunks'
   
    commands=[]
    for sample in samples:
	inputfiles = glob(path+'/'+sample)
	for inputfile in sorted(inputfiles):
	    INPUT = inputfile
	    command = "python analyzer.py --input %s --output_folder %s;"%(INPUT,output_folder)
	    commands.append(command)

    print commands[1]
    

    #do_submission(commands, output_folder)
    
    
    
