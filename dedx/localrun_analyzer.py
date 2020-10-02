import os, sys
from ROOT import *
from glob import glob
import argparse

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",default=False,action='store_true')

    args = parser.parse_args()
    test = args.test


    #Inputfile txt path
    path = "./inputs/"
    inputfiles = [
	    "./inputs/Run2016B-SingleMuon.txt",
	    #"./inputs/Summer16.WJetsToLNu_HT-100To200.txt",
	    #"./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.txt",
	    #"./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1.txt",
	    ]
   
    output_dir = "./output_smallchunks_localrun/"
    if not os.path.exists(output_dir):
	os.system("mkdir -p "+output_dir)
	print "Making output_dir :", output_dir
    else : print "output_dir exist :", output_dir
   
    #nev=-1
    nev=50000

    #lines=[]
    for inputfile in sorted(inputfiles):
	with open(inputfile) as f:
	    lines = f.readlines()
	    output = inputfile.split('/')[-1].replace('.txt','.root')
	    #chunk = str(lines).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
	    chunk = str(lines[0:5]).replace('\\n','').replace(", "," ").replace("[","").replace("]","")
	    command = "python analyzer_leptontrack.py --input {} --output_dir {} --output {} --nev {} ".format(chunk, output_dir, output, nev)
	    
	    if "FastSim" in inputfile : 
		command = command + '--fast'
	    
	    print command
	    os.system(command)
