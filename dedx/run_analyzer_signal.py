import os, sys
import argparse
from glob import glob
from GridEngineTools import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--test',default=False,action='store_true')

    args = parser.parse_args()
    test = args.test
    
    commands=[]
    '''
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1.root \
	    --mstop 1300 \
	    --mlsp 200 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1.root \
	    --mstop 1300 \
	    --mlsp 400 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1.root \
	    --mstop 1300 \
	    --mlsp 600 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1.root \
	    --mstop 1300 \
	    --mlsp 800 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1.root \
	    --mstop 1300 \
	    --mlsp 1000 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1.root \
	    --mstop 2500 \
	    --mlsp 1200 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1.root \
	    --mstop 2500 \
	    --mlsp 1400 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1.root \
	    --mstop 2500 \
	    --mlsp 1600 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1.root \
	    --mstop 2500 \
	    --mlsp 1800 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1.root \
	    --mstop 2500 \
	    --mlsp 2000 \
	    --nev -1 \
	    --dedxcalibfactor 1 \
	    ')
    ''' 
    # Private fastsim sample
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1to200.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-200.root \
	    --mstop 1300 \
	    --mlsp 200 \
	    --nev -1 \
	    --dedxcalibfactor 1.125 \
	    ')
     
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400to1000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400.root \
	    --mstop 1300 \
	    --mlsp 400 \
	    --nev -1 \
	    --dedxcalibfactor 1.02 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400to1000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-600.root \
	    --mstop 1300 \
	    --mlsp 600 \
	    --nev -1 \
	    --dedxcalibfactor 0.98 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400to1000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-800.root \
	    --mstop 1300 \
	    --mlsp 800 \
	    --nev -1 \
	    --dedxcalibfactor 0.96 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-400to1000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-1300_mLSP-1000.root \
	    --mstop 1300 \
	    --mlsp 1000 \
	    --nev -1 \
	    --dedxcalibfactor 0.96 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200.root \
	    --mstop 2500 \
	    --mlsp 1200 \
	    --nev -1 \
	    --dedxcalibfactor 0.98 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1400.root \
	    --mstop 2500 \
	    --mlsp 1400 \
	    --nev -1 \
	    --dedxcalibfactor 0.96 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1600.root \
	    --mstop 2500 \
	    --mlsp 1600 \
	    --nev -1 \
	    --dedxcalibfactor 0.95 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1800.root \
	    --mstop 2500 \
	    --mlsp 1800 \
	    --nev -1 \
	    --dedxcalibfactor 0.95 \
	    ')
    
    commands.append(
    'python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_smallchunks_T2btLL \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-2000.root \
	    --mstop 2500 \
	    --mlsp 2000 \
	    --nev -1 \
	    --dedxcalibfactor 0.925 \
	    ')
    # Submit
    if test :
	print 'Test run'
	os.system('python analyzer_chargino.py \
	    --inputfile ./inputs/Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000.txt \
	    --outputdir ./output_test \
	    --outputfile Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-2000.root \
	    --mstop 2500 \
	    --mlsp 2000 \
	    --nev 100 \
	    --dedxcalibfactor 1.025 \
	    ')

    else : 
	print 'Run?'
	raw_input()
	#os.system(commands[0])
	runParallel(commands, runmode="multi")
