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
    commands.append(
    'python sec_vertices.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_SMS-T2bt-LLChipm_ctau-200_mLSP-900and1000/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Summer16_T2bt.root \
	    --radDisCutHigh 4.2 \
	    --dedxcalibfactor 1 \
	    --doDedxSmear \
	    --dedxsmearfactor 0.375 \
	    ')
    
    commands.append(
    'python sec_vertices.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_DYJetsToLL_M-50_TuneCP5_Fall17/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Fall17_DYJetsToLL_M-50.root \
	    --radDisCutHigh 2.7 \
	    --dedxcalibfactor 0.969 \
	    --doDedxSmear \
	    --dedxsmearfactor 0.334 \
	    ')
    
    commands.append(
    'python sec_vertices.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_Run2016G_SingleElectron/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Run2016G_SingleElectron.root \
	    --radDisCutHigh 4.2 \
	    --dedxcalibfactor 1.376 \
	    ')
    
    commands.append(
    'python sec_vertices.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_Run2017F_SingleElectron/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Run2017F_SingleElectron.root \
	    --radDisCutHigh 2.7 \
	    --dedxcalibfactor 1.14 \
	    ')
    
    commands.append(
    'python sec_vertices.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_Run2018C_EGamma/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Run2018C_EGamma.root \
	    --radDisCutHigh 2.7 \
	    --dedxcalibfactor 1.202 \
	    ')
    
    # Submit
    if test :
	print 'Test run'
	os.system(commands[0])
    else : 
	print 'Run?'
	raw_input()
	#os.system(commands[0])
	runParallel(commands, runmode="multi")
