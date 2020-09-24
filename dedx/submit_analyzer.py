import os, sys
from ROOT import *
from glob import glob
from GridEngineTools import runParallel
import argparse

def do_submission(commands, output_folder, condorDir = "condor", executable = "analyzer_dEdx.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')

    args = parser.parse_args()
    test = args.test


    #Inputfile txt path
    path = "./inputs/"
    #inputfiles = sorted(glob(path+'/*.txt'))
    #inputfiles = sorted(glob(path+'/Run2016*.txt'))
    #inputfiles = sorted(glob(path+'/Run2017*.txt'))
    #inputfiles = sorted(glob(path+'/Summer16*.txt'))
    #inputfiles = sorted(glob(path+'/RunIIFall17*.txt'))
    #inputfiles = ["./inputs/Run2016H-SingleMuon.txt"]
    inputfiles = ["./inputs/Run2017B-SingleMuon.txt"]
    #inputfiles = ["./inputs/Summer16.WJetsToLNu_HT-100To200.txt"]
    #inputfiles = ["./inputs/RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800.txt"]
    #inputfiles = ["./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_.txt"]
    
    output_dir = "./output_smallchunks/"
    if not os.path.exists(output_dir):
	os.system("mkdir -p "+output_dir)
	print "Making output_dir :", output_dir
    else : print "output_dir exist :", output_dir
    
    # Number of split per inputfile
    split = True
    nsplit = 100

    commands=[]
    lines=[]
    for inputfile in sorted(inputfiles):
	cnt = 0
        if "SMS" in inputfile : split = False
	with open(inputfile) as f:
	    lines = f.readlines()
	    if split : 
		input_chunks = [lines[i * nsplit:(i + 1) * nsplit] for i in range((len(lines) + nsplit - 1) // nsplit )] 
		for i,chunk in enumerate(input_chunks):
		    output = inputfile.split('/')[-1].replace('.txt','_'+str(i)+'.root')
		    chunk = str(chunk).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
		    command = "python analyzer_dEdx.py --input {} --output_dir {} --output {} ".format(chunk, output_dir, output)
        	    commands.append(command)

	    elif not split : 
		output = inputfile.split('/')[-1].replace('_.txt','.root')
		chunk = str(lines).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
		command = "python analyzer_dEdx.py --input {} --output_dir {} --output {} ".format(chunk, output_dir, output)
        	commands.append(command)
	    else : 
		print('Something wrong in splitting')
		quit()

    if test : 
	os.system("mkdir -p output_smallchunks_test")
	print('python analyzer_dEdx.py --input {} --output_dir {} --output {} --nev 10000;'.format(chunk, "output_smallchunks_test", output))
	os.system('python analyzer_dEdx.py --input {} --output_dir {} --output {} --nev 10000;'.format(chunk, "output_smallchunks_test", output))
    else :
	do_submission(commands, output_dir, condorDir='condor_2017')
