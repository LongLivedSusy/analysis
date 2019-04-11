#!/usr/bin/env python

import os,sys
from ROOT import *
from glob import glob

def collect_histos(sampleName):
  
    fout = TFile("./result/%s" %(sampleName.replace('skim','result')),"RECREATE")
    systs = ['Nominal','BtagUp','BtagDown','JesUp','JesDown','JerUp','JerDown','IsrUp','IsrDown']
    for syst in systs : 
	f = 'output_'+syst
	fin = TFile(f+'/'+sampleName)
	h = fin.Get('hAnalysisBins')
	if 'Nominal' in syst :
	    h.SetNameTitle('Signal', '')
	else :
	    h.SetNameTitle('Signal_'+syst, '')
	fout.cd()
	h.Write()

def main():
    if not os.path.exists('./result'):
	os.system('mkdir -p result')
    
    collect_histos('skim_g1800_chi1400_27_200970_step4_100.root')
    

if __name__ == "__main__" :
    main()
