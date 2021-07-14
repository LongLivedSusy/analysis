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
    'python sec_vertices_work.py \
	    --inputfile \'/pnfs/desy.de/cms/tier2/store/user/spak/EDM_output_SMS-T2bt-LLChipm_ctau-200_mLSP-900and1000/*.root\' \
	    --outputdir ./SV_rootfiles/ \
	    --outputfile vertex_Summer16_T2bt.root \
	    --radDisCutHigh 4.2 \
	    --dedxcalibfactor 1 \
	    --doDedxSmear \
	    --dedxsmearfactor 0.375 \
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
