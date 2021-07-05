#this module should work just like hadd
from ROOT import *
import glob, sys, os
import commands
import numpy as np
from natsort import natsorted, ns
import json
from shared_utils import *

istest = False

MC = []
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1')
MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1')

#MC.append('Summer16PrivateFastSim.SMS-T2bt-LLChipm_ctau-200_mStop-2500_mLSP-1200to2000')

if __name__ == "__main__" : 
    
    folder = "./output_smallchunks_T2btLL_mstop2500_mlsp1200/"
    outdir = folder.replace('smallchunks','mediumchunks')
    
    if not os.path.exists(outdir):
        os.system("mkdir -p %s"%outdir)

    for keyword in MC:
        command = 'python ahadd.py -f %s/unwghtd'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
        print 'command', command
        if not istest: os.system(command)    
        fuw = TFile(outdir+'/unwghtd'+keyword+'.root')
        fw = TFile(outdir+'/'+keyword+'.root', 'recreate')
        #hHt = fuw.Get('hHT_unweighted')
        h_nev = fuw.Get('h_nev')
        nentries = h_nev.GetEntries()
        keys = fuw.GetListOfKeys()
        for key in keys:
        	name = key.GetName()
        	if not len(name.split('/'))>0: continue
        	hist = fuw.Get(name)
        	hist.Scale(1.0/nentries)
        	fw.cd()
        	hist.Write()
        fuw.Close()
        command = 'rm %s/unwghtd'%outdir+keyword+'.root'
        print command
        if not istest: os.system(command)
        fw.Close()
