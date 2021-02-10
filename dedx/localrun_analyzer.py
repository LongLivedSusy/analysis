import os, sys
from ROOT import *
from glob import glob
import argparse

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')

    args = parser.parse_args()
    test = args.test

    #executable = 'analyzer_DY_wip.py'
    executable = 'analyzer_DY_MIH.py'

    #Inputfile txt path
    inputfiles = [
	    "./inputs/Run2016B-SingleMuon.txt",
	    #"./inputs/Run2017C-SingleMuon.txt",
	    #"./inputs/Run2018B-SingleMuon.txt",
	    #"./inputs/Run2018D-SingleMuon.txt",
	    #"./inputs/Summer16.WJetsToLNu_TuneCUETP8M1.txt",
	    #"./inputs/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
	    #"./inputs/RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1to200.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1100and300.txt",
	    #"./inputs/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8.txt",
	    ]
   
    #output_dir = "./output_smallchunks_localrun/T2bt_mStop1300_mLSP1"
    output_dir = "./output_test/"
    if not os.path.exists(output_dir):
	os.system("mkdir -p "+output_dir)
	print "Making output_dir :", output_dir
    else : print "output_dir exist :", output_dir
   
    #nev=-1
    nev=5000

    #lines=[]
    for inputfile in sorted(inputfiles):
	with open(inputfile) as f:
	    lines = f.readlines()
	    output = inputfile.split('/')[-1].replace('.txt','.root')
	    #chunk = str(lines).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
	    chunk = str(lines[0:10]).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
	    command = "python {} --input {} --output_dir {} --output {} --nev {}".format(executable, chunk, output_dir, output, nev)
	    
	    if "FastSim" in inputfile : 
		command = command + ' --fast'
	    if "SMS" in inputfile : 
		command = command + ' --signal'
	    
	    print command
	    os.system(command)
