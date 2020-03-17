import os, sys
from ROOT import *
from glob import glob
from GridEngineTools import runParallel
import argparse

def do_submission(commands, output_folder, condorDir = "condor", executable = "analyzer.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')
    parser.add_argument("--outdir",default='output_smallchunks')

    args = parser.parse_args()
    test = args.test
    output_folder = args.outdir

    #Inputfile txt path
    path = "./inputs/split/"
    samples = ["*"]
    #samples = ["SingleMuon","SingleElectron"]
    #samples = ["SingleMuon"]
    #samples = ["RunIISummer16MiniAODv3.SMS-T2bt*"]
    #samples = ["Run2017B*","Run2017C*","Run2017F","RunIIFall17MiniAODv2*"]
    

    commands=[]
    for sample in samples:
	inputfiles = glob(path+'/*'+sample+'*')
	for inputfile in sorted(inputfiles):
	    command = "python analyzer.py --input %s --output_folder %s;"%(inputfile,output_folder)
	    commands.append(command)

    if test : 
	os.system("mkdir -p output_smallchunks_test")
	print('python analyzer.py --input ./inputs/split/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_000 --output_folder output_smallchunks_test --nev 10000;')
	print('python analyzer.py --input ./inputs/split/Summer16.WJetsToLNu_TuneCUETP8M1_000 --output_folder output_smallchunks_test --nev 10000;')
	print('python analyzer.py --input ./inputs/split/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1__001 --output_folder output_smallchunks_test --nev 10000;')
	print('python analyzer.py --input ./inputs/split/Run2016B_SingleMuon_001 --output_folder output_smallchunks_test --nev 10000;')
	print('python analyzer.py --input ./inputs/split/Run2017B_SingleMuon_000 --output_folder output_smallchunks_test --nev 10000;')
	print('python analyzer.py --input ./inputs/split/RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_000 --output_folder output_smallchunks_test --nev 10000;')
    else :
	do_submission(commands, output_folder)
