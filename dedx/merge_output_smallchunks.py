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
MC.append('Summer16.DYJetsToLL_M-50_TuneCUETP8M1')
MC.append('Summer16.DYJetsToLL_M-50_HT-100to200')
MC.append('Summer16.DYJetsToLL_M-50_HT-200to400')
MC.append('Summer16.DYJetsToLL_M-50_HT-400to600')
MC.append('Summer16.DYJetsToLL_M-50_HT-600to800')
MC.append('Summer16.DYJetsToLL_M-50_HT-800to1200')
MC.append('Summer16.DYJetsToLL_M-50_HT-1200to2500')
MC.append('Summer16.DYJetsToLL_M-50_HT-2500toInf')
MC.append('Summer16.QCD_HT200to300')
MC.append('Summer16.QCD_HT300to500')
MC.append('Summer16.QCD_HT500to700')
MC.append('Summer16.QCD_HT700to1000')
MC.append('Summer16.QCD_HT1000to1500')
MC.append('Summer16.QCD_HT1500to2000')
MC.append('Summer16.QCD_HT2000toInf')
MC.append('Summer16.TTJets_TuneCUETP8M1')
MC.append('Summer16.TTJets_SingleLeptFromT')
MC.append('Summer16.TTJets_SingleLeptFromTbar')
MC.append('Summer16.TTJets_DiLept_')
MC.append('Summer16.ST_s-channel_4f_leptonDecays')
MC.append('Summer16.ST_t-channel_top_4f_inclusiveDecays')
MC.append('Summer16.ST_t-channel_antitop_4f_inclusiveDecays')
MC.append('Summer16.ST_tW_top_5f_NoFullyHadronicDecays')
MC.append('Summer16.ST_tW_antitop_5f_NoFullyHadronicDecays')
MC.append('Summer16.WJetsToLNu_TuneCUETP8M1')
MC.append('Summer16.WJetsToLNu_HT-100To200')
MC.append('Summer16.WJetsToLNu_HT-200To400')
MC.append('Summer16.WJetsToLNu_HT-400To600')
MC.append('Summer16.WJetsToLNu_HT-600To800')
MC.append('Summer16.WJetsToLNu_HT-800To1200')
MC.append('Summer16.WJetsToLNu_HT-1200To2500')
MC.append('Summer16.WJetsToLNu_HT-2500ToInf')
MC.append('Summer16.ZJetsToNuNu_HT-100To200')
MC.append('Summer16.ZJetsToNuNu_HT-200To400')
MC.append('Summer16.ZJetsToNuNu_HT-400To600')
MC.append('Summer16.ZJetsToNuNu_HT-600To800')
MC.append('Summer16.ZJetsToNuNu_HT-800To1200')
MC.append('Summer16.ZJetsToNuNu_HT-1200To2500')
MC.append('Summer16.ZJetsToNuNu_HT-2500ToInf')
MC.append('Summer16.WW_TuneCUETP8M1')
MC.append('Summer16.WWTo1L1Nu2Q_13TeV_amcatnloFXFX')
MC.append('Summer16.WWTo2L2Nu')
MC.append('Summer16.WZ_TuneCUETP8M1')
MC.append('Summer16.WZTo1L1Nu2Q')
MC.append('Summer16.WZTo1L3Nu')
MC.append('Summer16.ZZ_TuneCUETP8M1')
MC.append('Summer16.WWZ_TuneCUETP8M1')
MC.append('Summer16.WZZ_TuneCUETP8M1')
MC.append('Summer16.ZZZ_TuneCUETP8M1')
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
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1')
#MC.append('RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1')

MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500')
MC.append('RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf')
MC.append('RunIIFall17MiniAODv2.QCD_HT200to300')
MC.append('RunIIFall17MiniAODv2.QCD_HT300to500')
MC.append('RunIIFall17MiniAODv2.QCD_HT500to700')
MC.append('RunIIFall17MiniAODv2.QCD_HT700to1000')
MC.append('RunIIFall17MiniAODv2.QCD_HT1000to1500')
MC.append('RunIIFall17MiniAODv2.QCD_HT1500to2000')
MC.append('RunIIFall17MiniAODv2.QCD_HT2000toInf')
MC.append('RunIIFall17MiniAODv2.TTJets_TuneCP5')
MC.append('RunIIFall17MiniAODv2.TTJets_HT-600to800')
MC.append('RunIIFall17MiniAODv2.TTJets_HT-800to1200')
MC.append('RunIIFall17MiniAODv2.TTJets_HT-1200to2500')
MC.append('RunIIFall17MiniAODv2.TTJets_HT-2500toInf')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500')
MC.append('RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500')
MC.append('RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf')
MC.append('RunIIFall17MiniAODv2.WWTo1L1Nu2Q')
MC.append('RunIIFall17MiniAODv2.WZTo1L1Nu2Q')
MC.append('RunIIFall17MiniAODv2.WZTo1L3Nu')
MC.append('RunIIFall17MiniAODv2.ZZTo2L2Q')
MC.append('RunIIFall17MiniAODv2.WZZ_TuneCP5')

Data=[]
Data.append('Run2016B-SingleMuon')
Data.append('Run2016C-SingleMuon')
Data.append('Run2016D-SingleMuon')
Data.append('Run2016E-SingleMuon')
Data.append('Run2016F-SingleMuon')
Data.append('Run2016G-SingleMuon')
Data.append('Run2016H-SingleMuon')
Data.append('Run2017B-SingleMuon')
Data.append('Run2017C-SingleMuon')
Data.append('Run2017D-SingleMuon')
Data.append('Run2017E-SingleMuon')
Data.append('Run2017F-SingleMuon')
Data.append('Run2018A-SingleMuon')
Data.append('Run2018B-SingleMuon')
Data.append('Run2018C-SingleMuon')
Data.append('Run2018D-SingleMuon')

if __name__ == "__main__" : 
    
    #folder = "./output_smallchunks/"
    folder = "./output_smallchunks_doublesmear/"
    #folder = "./output_smallchunks_MIH/"
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
    
    for keyword in Data:
        command = 'python ahadd.py -f %s/'%outdir+keyword+'.root '+folder+'/*'+keyword+'*.root'
        print 'command', command
        if not istest: os.system(command)    

