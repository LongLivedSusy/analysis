#this module should work just like hadd
from ROOT import *
import glob, sys, os
import commands
import numpy as np
from natsort import natsorted, ns
import json
from shared_utils import *

istest = False
#istest = True

BigChunk={}
BigChunk['DYJets']=[
'Summer16.DYJetsToLL_M-50_TuneCUETP8M1',
'Summer16.DYJetsToLL_M-50_HT-100to200',
'Summer16.DYJetsToLL_M-50_HT-200to400',
'Summer16.DYJetsToLL_M-50_HT-400to600',
'Summer16.DYJetsToLL_M-50_HT-600to800',
'Summer16.DYJetsToLL_M-50_HT-800to1200',
'Summer16.DYJetsToLL_M-50_HT-1200to2500',
'Summer16.DYJetsToLL_M-50_HT-2500toInf',
]

BigChunk['QCD']=[
'Summer16.QCD_HT200to300',
'Summer16.QCD_HT300to500',
'Summer16.QCD_HT500to700',
'Summer16.QCD_HT700to1000',
'Summer16.QCD_HT1000to1500',
'Summer16.QCD_HT1500to2000',
'Summer16.QCD_HT2000toInf',
]

BigChunk['TTJets']=[
'Summer16.TTJets_TuneCUETP8M1',
#'Summer16.TTJets_SingleLeptFromT',
#'Summer16.TTJets_SingleLeptFromTbar',
#'Summer16.TTJets_DiLept_',
#'Summer16.ST_s-channel_4f_leptonDecays',
#'Summer16.ST_t-channel_top_4f_inclusiveDecays',
#'Summer16.ST_t-channel_antitop_4f_inclusiveDecays',
#'Summer16.ST_tW_top_5f_NoFullyHadronicDecays',
#'Summer16.ST_tW_antitop_5f_NoFullyHadronicDecays',
]

BigChunk['WJetsToLNu']=[
'Summer16.WJetsToLNu_TuneCUETP8M1',
'Summer16.WJetsToLNu_HT-100To200',
'Summer16.WJetsToLNu_HT-200To400',
'Summer16.WJetsToLNu_HT-400To600',
'Summer16.WJetsToLNu_HT-600To800',
'Summer16.WJetsToLNu_HT-800To1200',
'Summer16.WJetsToLNu_HT-1200To2500',
'Summer16.WJetsToLNu_HT-2500ToInf',
]

BigChunk['ZJetsToNuNu']=[
'Summer16.ZJetsToNuNu_HT-100To200',
'Summer16.ZJetsToNuNu_HT-200To400',
'Summer16.ZJetsToNuNu_HT-400To600',
'Summer16.ZJetsToNuNu_HT-600To800',
'Summer16.ZJetsToNuNu_HT-800To1200',
'Summer16.ZJetsToNuNu_HT-1200To2500',
'Summer16.ZJetsToNuNu_HT-2500ToInf',
]

BigChunk['VV']=[
'Summer16.WW_TuneCUETP8M1',
#'Summer16.WWTo1L1Nu2Q_13TeV_amcatnloFXFX',
#'Summer16.WWTo2L2Nu',
'Summer16.WZ_TuneCUETP8M1',
#'Summer16.WZTo1L1Nu2Q',
#'Summer16.WZTo1L3Nu',
'Summer16.ZZ_TuneCUETP8M1',
]

BigChunk['VVV']=[
'Summer16.WWZ_TuneCUETP8M1',
'Summer16.WZZ_TuneCUETP8M1',
'Summer16.ZZZ_TuneCUETP8M1',
]

BigChunk['Run2016']=[
'Run2016B-SingleMuon',
'Run2016C-SingleMuon',
'Run2016D-SingleMuon',
'Run2016E-SingleMuon',
'Run2016F-SingleMuon',
'Run2016G-SingleMuon',
'Run2016H-SingleMuon',
]

BigChunk['Run2017']=[
'Run2017B-SingleMuon',
'Run2017C-SingleMuon',
'Run2017D-SingleMuon',
'Run2017E-SingleMuon',
'Run2017F-SingleMuon',
]

BigChunk['Run2018']=[
'Run2018A-SingleMuon',
'Run2018B-SingleMuon',
'Run2018C-SingleMuon',
'Run2018D-SingleMuon',
]

if __name__ == "__main__" : 
    
    folder = "./output_mediumchunks/"
    outdir = folder.replace('mediumchunks','bigchunks')
    
    if not os.path.exists(outdir):
        os.system("mkdir -p %s"%outdir)


    for keyword in BigChunk.keys():
	command = 'python ahadd.py -f %s/'%outdir+keyword+'.root '
	for subkey in BigChunk[keyword]:
	    command+=folder+'/*'+subkey+'*.root '
        
        print 'command', command
        if not istest: os.system(command)    

