#this module should work just like hadd
from ROOT import *
import glob, sys
import numpy as np
from shared_utils import *
import os as os_

istest = False
try: folder = sys.argv[1]
except:
    print 'please give folder name as first argument'
    exit(0)

outdir = folder.replace('smallchunks','mediumchunks')

if not os_.path.exists(outdir):
    os_.system("mkdir -p %s"%outdir)
    
MC = []
MC.append('DYJetsToLL_M-50_TuneCUETP8M1')
MC.append('DYJetsToLL_M-50_HT-100to200')
MC.append('DYJetsToLL_M-50_HT-200to400')
MC.append('DYJetsToLL_M-50_HT-400to600')
MC.append('DYJetsToLL_M-50_HT-600to800')
MC.append('DYJetsToLL_M-50_HT-800to1200')
MC.append('DYJetsToLL_M-50_HT-1200to2500')
MC.append('DYJetsToLL_M-50_HT-2500toInf')
MC.append('QCD_HT200to300')
MC.append('QCD_HT300to500')
MC.append('QCD_HT500to700')
MC.append('QCD_HT700to1000')
MC.append('QCD_HT1000to1500')
MC.append('QCD_HT1500to2000')
MC.append('QCD_HT2000toInf')
MC.append('TTJets')
MC.append('WJetsToLNu_TuneCUETP8M1')
MC.append('WJetsToLNu_HT-100To200')
MC.append('WJetsToLNu_HT-200To400')
MC.append('WJetsToLNu_HT-400To600')
MC.append('WJetsToLNu_HT-600To800')
MC.append('WJetsToLNu_HT-800To1200')
MC.append('WJetsToLNu_HT-1200To2500')
MC.append('WJetsToLNu_HT-2500ToInf')
MC.append('ZJetsToNuNu_HT-100To200')
MC.append('ZJetsToNuNu_HT-200To400')
MC.append('ZJetsToNuNu_HT-400To600')
MC.append('ZJetsToNuNu_HT-600To800')
MC.append('ZJetsToNuNu_HT-800To1200')
MC.append('ZJetsToNuNu_HT-1200To2500')
MC.append('ZJetsToNuNu_HT-2500ToInf')
MC.append('WW')
MC.append('WZ')
MC.append('ZZ')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-50_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-150_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-200_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-400_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-600_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-800_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-900_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1000_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1100_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1200_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1300_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1400_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1500_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1600_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1700_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-1800_')
MC.append('SMS-T2bt-LLChipm_ctau-200_mLSP-2000_')

Data=[]
Data.append('Run2016B_SingleMuon')
Data.append('Run2016C_SingleMuon')
Data.append('Run2016D_SingleMuon')
Data.append('Run2016E_SingleMuon')
Data.append('Run2016F_SingleMuon')
Data.append('Run2016G_SingleMuon')
Data.append('Run2016H_SingleMuon')
Data.append('Run2016B_SingleElectron')
Data.append('Run2016C_SingleElectron')
Data.append('Run2016D_SingleElectron')
Data.append('Run2016E_SingleElectron')
Data.append('Run2016F_SingleElectron')
Data.append('Run2016G_SingleElectron')
Data.append('Run2016H_SingleElectron')
#Data.append('Run2016B_MET')
#Data.append('Run2016C_MET')
#Data.append('Run2016D_MET')
#Data.append('Run2016E_MET')
#Data.append('Run2016F_MET')
#Data.append('Run2016G_MET')
#Data.append('Run2016H_MET')

for keyword in MC:
    command = 'python ahadd.py -f %s/unwghtd'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
    print 'command', command
    if not istest: os_.system(command)    
    fuw = TFile(outdir+'/unwghtd'+keyword+'.root')
    fw = TFile(outdir+'/'+keyword+'.root', 'recreate')
    hHt = fuw.Get('hHT_unweighted')
    nentries = hHt.GetEntries()
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
    if not istest: os_.system(command)
    fw.Close()

for keyword in Data:
    command = 'python ahadd.py -f %s/'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
    print 'command', command
    if not istest: os_.system(command)    
    #fw.Close()
