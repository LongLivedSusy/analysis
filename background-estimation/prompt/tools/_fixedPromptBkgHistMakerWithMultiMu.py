import os, sys
import time
import numpy as np
from ROOT import *
from utils import *
from glob import glob
from random import shuffle
import random
gROOT.SetStyle('Plain')
gROOT.SetBatch(1)

debugmode = False

specialTauPiValidation = False

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_3*_RA2AnalysisTree.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_78_RA2AnalysisTree.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=10000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-gk", "--useGenKappa", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-SmearLeps4Zed", "--SmearLeps4Zed", type=str, default='True')
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
args = parser.parse_args()
nfpj = args.nfpj
SmearLeps4Zed_ = bool(args.SmearLeps4Zed=='True')
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
analyzer = args.analyzer
pileup = args.pileup
useGenKappa = args.useGenKappa
verbosity = args.verbosity
print 'useGenKappa =', useGenKappa


genMatchEverything = False
RelaxGenKin = True
ClosureMode = True #false means run as if real data
SmearLeps = False
UseFits = False
UseDeep = False
verbose = False
sayalot = False
candPtCut = 30
candPtUpperCut = 6499
if SmearLeps4Zed_: kappasmearlevellabel = 'YesZSmear'
else: kappasmearlevellabel = 'NoZSmear'


mZ = 91
isdata = 'Run20' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames or 'aksingh' in inputFileNames: 
	is2016, is2017, is2018 = True, False, False
elif 'Run2017' in inputFileNames or 'Fall17' in inputFileNames or 'somethingelse' in inputFileNames: 
	is2016, is2017, is2018 = False, True, False
elif 'Run2018' in inputFileNames or 'Autumn18' in inputFileNames or 'somthin or other' in inputFileNames: 
	is2016, is2017, is2018 = False, True, True

if is2016: phase = 0
else: phase = 1



if phase==0: 
	BTAG_CSVv2 = 0.8484
	BTAG_deepCSV = 0.6324
if phase==1: 
	BTAG_CSVv2 = 0.8838
	BTAG_deepCSV = 0.4941

if UseDeep: btag_cut = BTAG_deepCSV
else: btag_cut = BTAG_CSVv2

if phase==0: mvathreshes=[.1,.25]
else: mvathreshes=[0.15,0.0]

print 'phase', phase

if isdata: ClosureMode = False

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier

c = TChain("TreeMaker2/PreSelection")
for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)
	
nentries = c.GetEntries()
#nentries = 100

c.Show(0)


newfname = 'PromptBkgHists_'+identifier+kappasmearlevellabel+'.root'
if useGenKappa: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'creating file', fnew_.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

hMtPionMatched = TH1F('hMtPionMatched','hMtPionMatched',50,0,200)
histoStyler(hMtPionMatched,kOrange+1)
hMtPionUnMatched = TH1F('hMtPionUnMatched','hMtPionUnMatched',50,0,200)
histoStyler(hMtPionUnMatched,kRed+1)



inf = 999999

regionCuts = {}
varlist_                         = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'Log10DedxMass','NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'DeDxAverage','BinNumber']
regionCuts['NoCutsPixOnly']      = [(0,inf), (0.0,inf), (0,inf), (0,inf), (1,inf), (1,inf), (0,0),       (0.0,inf),        (-inf,inf),         (0,inf),     (0,inf),  (0,inf),  (candPtCut,inf), (0,2.4),      (-inf,inf),  (-1,inf)]
regionCuts['NoCutsPixAndStrips'] = [(0,inf), (0.0,inf), (0,inf), (0,inf), (1,inf), (0,0),   (1,inf),     (0.0,inf),        (-inf,inf),         (0,inf),     (0,inf),  (0,inf),  (candPtCut,inf), (0,2.4),      (-inf,inf),  (-1,inf)]
regionCuts['Baseline']           = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (-inf,inf),         (0,0 ),      (0,inf),  (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf),  (-1,inf)]

regionCuts['BaselinePixOnly']    = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,inf),     (0.3,inf),        (-inf,inf),         (0,0),       (0,inf),   (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
regionCuts['BaselinePixAndStrips']=[(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (-inf,inf),         (0,0),       (0,inf),   (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrElPixOnly'] = [(100,inf), (100,300), (2,inf), (1,5),   (1,1),   (1,inf), (0,0),     (0.3,inf),        (-inf,inf),         (1,1),       (0,inf),   (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
##regionCuts['TtbarCtrMuPixOnly']= [(100,inf), (100,300), (2,inf), (1,5),   (1,1),   (1,inf), (0,inf),   (0.3,inf),        (-inf,inf),         (0,0),       (1,1),     (0,0),    (candPtCut,inf), (0,2.4),     (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrElPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),  (1,1),   (0,inf), (1,0),     (0.3,inf),        (-inf,inf),         (1,1),       (0,0),     (0,0),    (candPtCut,inf), (0,2.4),     (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrMuPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),  (1,1),   (0,inf), (1,inf),   (0.3,inf),        (-inf,inf),         (0,0),       (1,1),     (0,0),    (candPtCut,inf), (0,2.4),     (-inf,inf), (-1,inf)]

#regionCuts['LowMhtBasePixAndStrips']=[(0,inf),(150,inf),(1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (-inf,inf),        (0,0  ),     (0,0),    (candPtCut,inf), (0,2.4), (-1,inf)]

'''
varlist_                         = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'Log10DedxMass', 'NElectrons', 'NMuons', 'NHardMuons', 'NSoftMuons', 'NPions', 'TrkPt', 'TrkEta',           'DeDxAverage','BinNumber']
regionCuts['NoCutsPixOnly']      = [(0,inf), (0.0,inf), (0,inf), (0,inf), (1,inf), (1,inf), (0,0),       (0.0,inf),        (-inf,inf),        (0,inf),     (0,inf),     (0,inf),     (0,inf),     (0,inf),  (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
regionCuts['NoCutsPixAndStrips'] = [(0,inf), (0.0,inf), (0,inf), (0,inf), (1,inf), (0,0),   (1,inf),     (0.0,inf),        (-inf,inf),        (0,inf),     (0,inf),     (0,inf),     (0,inf),     (0,inf),  (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
regionCuts['Baseline']           = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (-inf,inf),        (0,0 ),     (0,inf),     (0,inf),     (0,inf),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]

regionCuts['BaselinePixOnly']    = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,inf),     (0.3,inf),        (-inf,inf),          (0,0),     (0,inf),     (0,inf),     (0,inf),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
regionCuts['BaselinePixAndStrips']=[(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (-inf,inf),          (0,0),     (0,inf),     (0,inf),     (0,inf),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrElPixOnly']  = [(100,inf), (100,300), (2,inf), (1,5),   (1,1),   (1,inf), (0,0),     (0.3,inf),        (-inf,inf),        (1,1),     (0,inf),     (0,inf),       (0,inf),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
##regionCuts['TtbarCtrMuPixOnly']  = [(100,inf), (100,300), (2,inf), (1,5),  (1,1),   (1,inf), (0,inf),   (0.3,inf),        (-inf,inf),        (0,0),     (0,inf),     (0,inf),       (1,1),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrElPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),   (1,1),   (0,inf), (1,0),     (0.3,inf),        (-inf,inf),        (1,1),     (0,inf),     (0,inf),       (0,0),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
#regionCuts['TtbarCtrMuPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),   (1,1),   (0,inf), (1,inf),     (0.3,inf),        (-inf,inf),      (0,0),     (0,inf),     (0,inf),       (1,1),     (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
'''

print 'binning', binning 

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
	for var in varlist_:
		histname = 'El'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Mu'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)        
		histname = 'Pi'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)        		
		histname = 'Fake'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)  
	   

logmasscutL = TMath.Log10(450)
logmasscutS = TMath.Log10(150)
binnumbers = {}
listagain = ['Ht',  'Mht',    'NJets','BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets','Log10DedxMass', 'NElectrons', 'NMuons', 'NPions', 'TrkPt','TrkEta','BinNumber']
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (-1,logmasscutL))] = 1
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (logmasscutL,inf))] = 2
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (-1,logmasscutS))] = 3
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (logmasscutS,inf))] = 4
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (-1,logmasscutL))] = 5
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (logmasscutL,inf))] = 6
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (-1,logmasscutS))] = 7
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (logmasscutS,inf))] = 8
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (-1,logmasscutL))] = 9
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (logmasscutL,inf))] = 10
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (-1,logmasscutS))] = 11
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (logmasscutS,inf))] = 12
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (-1,logmasscutL))] = 13
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (logmasscutL,inf))] = 14
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (-1,logmasscutS))] = 15
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (logmasscutS,inf))] = 16
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.5,inf),          (-1,logmasscutL))] = 17
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.5,inf),          (logmasscutL,inf))] = 18
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.5,inf),          (-1,logmasscutS))] = 19
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.5,inf),          (logmasscutS,inf))] = 20
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (-1,logmasscutL))] = 21
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (logmasscutL,inf))] = 22
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (-1,logmasscutS))] = 23
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (logmasscutS,inf))] = 24
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutL))] = 25
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutL,inf))] = 26
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (-1,logmasscutS))] = 27
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (logmasscutS,inf))] = 28
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 29
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 30
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 31
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 32
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 33
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 34
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 35
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 36
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 37
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 38
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 39
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 40
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (-1,logmasscutS))] = 41
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (logmasscutS,inf))] = 42
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (-1,logmasscutL))] = 43
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (logmasscutL,inf))] = 44
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 45
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 46
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 47
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 48
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 49
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 50
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 51
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 52
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 53
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 54
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 55
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 56
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (-1,logmasscutS))] = 57
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (logmasscutS,inf))] = 58
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (-1,logmasscutL))] = 59
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (logmasscutL,inf))] = 60
binnumbers[((0,inf),(0,400),  (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=61
binnumbers[((0,inf),(400,inf),(0,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=62



def getBinNumber(fv):
	for binkey in binnumbers:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumbers[binkey]
	return -1



def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
	iomits = []
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
			return False
	return True


if 'TTJets_TuneCUET' in inputFileNames:  madranges = [(0,600)]
elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneCUET' in inputFileNames: madranges = [(0, 100), (600,800)]
elif 'WJetsToLNu_HT' in inputFileNames: madranges = [(100, inf)]
else: madranges = [(0, inf)]


fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
else: 
	#hMask = fMask.Get('hEtaVsPhiDTRun2016')
	hMask = ''

if isdata: 
	fsmearname_short = 'usefulthings/DataDrivenSmear_Run2016_PixOnly.root'
	fsmearname_long = 'usefulthings/DataDrivenSmear_Run2016_PixAndStrips.root'	
else: 
	fsmearname_short = 'usefulthings/DataDrivenSmear_DYJets_PixOnly.root'
	fsmearname_long = 'usefulthings/DataDrivenSmear_DYJets_PixAndStrips.root'
	
fsmear_short = TFile(fsmearname_short)
fsmear_long = TFile(fsmearname_long)

dResponseHist_el_short = {}
dResponseHist_el_long = {}
dResponseHist_mu_short = {}
dResponseHist_mu_long = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
	for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
	   newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
	   print 'attempting to get', "htrkresp"+str(newHistKey)
	   if '(1.4442,' in str(newHistKey): continue
	   dResponseHist_el_short[newHistKey] = fsmear_short.Get("htrkresp"+str(newHistKey)+'El')
	   dResponseHist_mu_short[newHistKey] = fsmear_short.Get("htrkresp"+str(newHistKey)+'Mu')
	   dResponseHist_el_long[newHistKey] = fsmear_long.Get("htrkresp"+str(newHistKey)+'El')
	   dResponseHist_mu_long[newHistKey] = fsmear_long.Get("htrkresp"+str(newHistKey)+'Mu')       	   

def getSmearFactor(Eta, Pt, dResponseHist):
	for histkey in  dResponseHist:
	   if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
		   SF_trk = 10**(dResponseHist[histkey].GetRandom())
		   return SF_trk #/SF_ele
	print 'returning 1'
	return 1
	

dResponseHist_el_short = {}
dResponseHist_mu_long = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
	for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
	   newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
	   print 'attempting to get', "htrkresp"+str(newHistKey)
	   if '(1.4442,' in str(newHistKey): continue
	   dResponseHist_el_short[newHistKey] = fsmear_short.Get("htrkresp"+str(newHistKey)+'El')
	   dResponseHist_mu_short[newHistKey] = fsmear_short.Get("htrkresp"+str(newHistKey)+'Mu')       
	   dResponseHist_el_long[newHistKey] = fsmear_long.Get("htrkresp"+str(newHistKey)+'El')
	   dResponseHist_mu_long[newHistKey] = fsmear_long.Get("htrkresp"+str(newHistKey)+'Mu')       	   

def getSmearFactor(Eta, Pt, dResponseHist):
	for histkey in  dResponseHist:
	   if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
		   SF_trk = 10**(dResponseHist[histkey].GetRandom())
		   return SF_trk #/SF_ele
	print 'returning 1'
	return 1
	
	
import os
if phase==0:
	#pixelXml =       '/nfs/dust/cms/user/kutznerv/disapptrks/track-tag/cmssw8-newpresel3-200-4-short-updated/weights/TMVAClassification_BDT.weights.xml'
	#pixelstripsXml = '/nfs/dust/cms/user/kutznerv/disapptrks/track-tag/cmssw8-newpresel2-200-4-medium-updated/weights/TMVAClassification_BDT.weights.xml'
	#pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks/weights/TMVAClassification_BDT.weights.xml'
	#pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks/weights/TMVAClassification_BDT.weights.xml'
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
else:
	#pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks/weights/TMVAClassification_BDT.weights.xml'
	#pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks/weights/TMVAClassification_BDT.weights.xml'
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'	
readerPixelOnly = TMVA.Reader()
readerPixelStrips = TMVA.Reader()
prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
prepareReaderPixel_loose(readerPixelOnly, pixelXml)
#prepareReaderPixelStrips(readerPixelStrips, pixelstripsXml)
#prepareReaderPixel(readerPixelOnly, pixelXml)


if isdata: 
	if phase==0:
		fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly_'+kappasmearlevellabel+'.root'
		fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips_'+kappasmearlevellabel+'.root' 
		fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly_'+kappasmearlevellabel+'.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips_'+kappasmearlevellabel+'.root'
	else:
		fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly_'+kappasmearlevellabel+'.root'
		#fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips'+kappasmearlevellabel+'.root' 
		#fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly'+kappasmearlevellabel+'.root'
		#fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips'+kappasmearlevellabel+'.root'		

else: 
	if phase==0:
		fileKappaPixOnly = 'usefulthings/KappaSummer16.AllMC_PixOnly_'+kappasmearlevellabel+'.root'#should be updated to All
		fileKappaPixAndStrips = 'usefulthings/KappaSummer16.AllMC_PixAndStrips_'+kappasmearlevellabel+'.root'
		fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly_'+kappasmearlevellabel+'.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips_'+kappasmearlevellabel+'.root' 
	else:
		fileKappaPixOnly = 'usefulthings/KappaFall17.AllMC_PixOnly_'+kappasmearlevellabel+'.root'#should be updated to All
		fileKappaPixAndStrips = 'usefulthings/KappaFall17.AllMC_PixAndStrips_'+kappasmearlevellabel+'.root'
		fileKappaPixOnlyGen = 'usefulthings/KappaFall17.WJets_PixOnly_'+kappasmearlevellabel+'.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaFall17.WJets_PixAndStrips_'+kappasmearlevellabel+'.root' 


fKappaPixOnly  = TFile(fileKappaPixOnly)
fKappaPixAndStrips  = TFile(fileKappaPixAndStrips)
fKappaPixOnlyGen  = TFile(fileKappaPixOnlyGen)
fKappaPixAndStripsGen  = TFile(fileKappaPixAndStripsGen)


fElProbePt_KappasPixOnly = {}
fGenElProbePt_KappasPixOnly = {}
fMuProbePt_KappasPixOnly = {}
fGenMuProbePt_KappasPixOnly = {}
fPiProbePt_KappasPixOnly = {}
fGenPiProbePt_KappasPixOnly = {}

fElProbePt_KappasPixAndStrips = {}
fGenElProbePt_KappasPixAndStrips = {}
fMuProbePt_KappasPixAndStrips = {}
fGenMuProbePt_KappasPixAndStrips = {}
fPiProbePt_KappasPixAndStrips = {}
fGenPiProbePt_KappasPixAndStrips = {}


for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
	if etakey == (1.4442, 1.566): continue
	specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')
	oldNumName = "hElProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
	newKappaFuncName = (UseFits*'f1'+newKappaName).replace('.','p')
	fElProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
	fElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
	oldGenNumName = "hGenElProbePtDT"+specialpart+"_num"
	newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
	newGenKappaFuncName = UseFits*'f1'+newGenKappaName.replace('.','p')
	fGenElProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
	fGenElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long')

	oldNumName = "hMuProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
	newKappaFuncName = UseFits*'f1'+newKappaName.replace('.','p')
	fMuProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
	fMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
	oldGenNumName = "hGenMuProbePtDT"+specialpart+"_num"
	newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
	newGenKappaFuncName = UseFits*'f1'+newGenKappaName.replace('.','p')
	fGenMuProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
	fGenMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long') 

	oldNumName = "hPiProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
	newKappaFuncName = (UseFits*'f1'+newKappaName).replace('.','p')
	fPiProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()

	print 'looking for ', newKappaFuncName, 'in', fKappaPixAndStrips.GetName()
	fPiProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
	oldGenNumName = "hGenPiProbePtDT"+specialpart+"_num"
	newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
	newGenKappaFuncName = UseFits*'f1'+newGenKappaName.replace('.','p')
	fGenPiProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
	fGenPiProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long') 	
 

if useGenKappa: 
	kappadictElPixOnly = fGenElProbePt_KappasPixOnly
	kappadictMuPixOnly = fGenMuProbePt_KappasPixOnly    
	kappadictPiPixOnly = fGenPiProbePt_KappasPixOnly    	

	kappadictElPixAndStrips = fGenElProbePt_KappasPixAndStrips
	kappadictMuPixAndStrips = fGenMuProbePt_KappasPixAndStrips        
	kappadictPiPixAndStrips = fGenPiProbePt_KappasPixAndStrips        	
else: 
	kappadictElPixOnly = fElProbePt_KappasPixOnly
	kappadictMuPixOnly = fMuProbePt_KappasPixOnly  
	kappadictPiPixOnly = fPiProbePt_KappasPixOnly  	

	kappadictElPixAndStrips = fElProbePt_KappasPixAndStrips
	kappadictMuPixAndStrips = fMuProbePt_KappasPixAndStrips	
	kappadictPiPixAndStrips = fPiProbePt_KappasPixAndStrips        


dKappaBinList = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdges[:-1]):
		for iEtaBinEdge, EtaBinEdge in enumerate(EtaBinEdges[:-1]):
				newHistKey = ((EtaBinEdge,EtaBinEdges[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdges[iPtBinEdge + 1]))
				dKappaBinList[newHistKey] = [iPtBinEdge+1,iEtaBinEdge+1]
	
	
shortMaxKappaPt = 2000
def fetchKappa(Eta, Pt_, KappaDict=fGenElProbePt_KappasPixOnly, maxpt = 2000):
	Pt = min(Pt_,maxpt)
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
		if abs(Eta) >= etakey[0] and abs(Eta) <= etakey[1]:
			#return KappaDict[etakey].Eval(Pt)
			if UseFits: kappa = KappaDict[etakey].Eval(Pt)
			else:
				ipt = KappaDict[etakey].GetXaxis().FindBin(Pt)
				kappa = KappaDict[etakey].GetBinContent(ipt)
			return kappa
	print etakey, Eta
	print 'didnt get anything meaningful', Eta, Pt
	return 1


import time
t1 = time.time()
i0=0

triggerIndecesV2 = {}
triggerIndecesV2['SingleElCocktail'] = [14, 15, 16, 17, 18, 19, 20, 21]
#triggerIndecesV2['MhtMet6pack'] = [108,110,114,123,124,125,126,128,129,130,131,132,133,122,134]#123
triggerIndecesV2["SingleMuCocktail"] = [24,25,26,27,28,30,31,32]

triggerIndeces = triggerIndecesV2

def PassTrig(c,trigname):
	for trigidx in triggerIndeces[trigname]: 
		if c.TriggerPass[trigidx]==1: 
			return True
	return False

matchedpinum = 0.0001
unmatchedpinum = 0.0001
print nentries, 'evets to be analyzed'
for ientry in range(nentries):
	if verbose:
		if not ientry in [17681]: continue
	if debugmode:
		if not ientry in [187]: continue		
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]

	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
	if isdata: weight = 1
	else: 
		weight = c.CrossSection*c.puWeight
		#weight = c.puWeight
		weight = 1.0
	hHtWeighted.Fill(c.HT,weight)



	if not isdata:
	  isValidHtRange = False
	  for madrange in madranges:
		if (c.madHT>madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	  #####if not isValidHtRange: continue

	genels = []
	genmus = []
	genpis = []		
	if ClosureMode:
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue 
			if not c.GenParticles_Status[igp] == 1: continue        
			#if not abs(c.GenParticles_ParentId[igp]) == 24: continue
			if abs(c.GenParticles_PdgId[igp])==11: genels.append(gp)
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append(gp)            
		for igp, gp in enumerate(c.GenTaus_LeadTrk):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue
			if not bool(c.GenTaus_had[igp]): continue
			if not c.GenTaus_NProngs[igp]==1: continue###
			#print igp, 'found tau', bool(c.GenTaus_had[igp])==True, 'nprongs', c.GenTaus_NProngs[igp]
			#print 'isoPionTracks', c.isoPionTracks
			genpis.append(gp)

	if specialTauPiValidation:
		if not len(genpis)<2: continue
		#if not len(genpis)>0: continue
	if c.MET>100:
		if not c.CaloMET/c.MET<5.0: continue
	#if not c.JetID: continue
	

	basicTracks = []
	disappearingTracks = []    
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if verbose: print itrack, 'before baseline pt', track.Pt(), 'eta', track.Eta()        
		if not isBaselineTrack(track, itrack, c, hMask): continue
		if verbose: print itrack, 'pt', track.Pt(), 'eta', track.Eta()
		if debugmode: print ientry, itrack, 'still rocking, baby', track.Pt()
		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     
		if debugmode: print ientry, itrack, 'basic bitch!', track.Pt()
		dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips, mvathreshes)
		if not dtstatus>0: continue
		if debugmode: print ientry, itrack, 'still got this', track.Pt()
		drlep = 99
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break            
		if not passeslep: continue 
		print ientry, 'found disappearing track w pT =', track.Pt(), dtstatus
		if dtstatus==1: nShort+=1
		if dtstatus==2: nLong+=1         
		if verbose: print ievent, itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta()     
		if isMatched(track, genels, 0.02):
			print ientry, '---->is electron'
		elif isMatched(track, genmus, 0.02):
			print ientry, '---->is muon'		
		elif isMatched(track, genpis , 0.02):
			print ientry, '---->is pi'
			for igp, gp in enumerate(c.GenTaus_LeadTrk):
				print igp, bool(c.GenTaus_had[igp]==True), c.GenTaus_NProngs[igp] 
		else:
			print 'is fake'
		if dtstatus==1: disappearingTracks.append([track,dtstatus,c.tracks_deDxHarmonic2pixel[itrack]])
		if dtstatus==2: disappearingTracks.append([track,dtstatus,c.tracks_deDxHarmonic2strips[itrack]])		


	SmearedElectrons = []
	RecoElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if debugmode: print ientry, iel,'ele with Pt' , ele.Pt()
		if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
		if not abs(ele.Eta())<2.4: continue
		if debugmode: print 'passed eta and Pt'
		if not c.Electrons_passIso[iel]: continue
		if not c.Electrons_tightID[iel]: continue
		if debugmode: print 'passed that nice tight id'
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(ele)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				#if not c.tracks_trackerLayersWithMeasurement[trk[2]]==c.tracks_pixelLayersWithMeasurement[trk[2]]: continue
				if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if debugmode: print 'matched to a nice basic track'		
		if ele.Pt()>candPtCut: RecoElectrons.append([ele, c.Electrons_charge[iel]])
		#print ientry, 'found electron', ele.Pt()
		
		'''
		if isMatched(ele, genels, 0.02):
			print ientry, 'this CR electron determined to be an electron'
		else:
			print ientry, 'this CR electron AINT no electron', c.Electrons_MTW[iel]		
		'''
				
		if not c.Electrons_MTW[iel]<100: continue
		smearedEl = TLorentzVector()
		smearedEl.SetPtEtaPhiE(0, 0, 0, 0)
		smear = 1.0 
		smearedEl.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedEl.Pt()>candPtCut and smearedEl.Pt()<candPtUpperCut): continue
		SmearedElectrons.append([smearedEl,c.Electrons_charge[iel],c.tracks_deDxHarmonic2pixel[matchedTrk[2]],c.tracks_deDxHarmonic2strips[matchedTrk[2]]])
		#print 'a lovely ele', ele.Pt(), smearedEle.Pt()


	SmearedMuons = []
	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_tightID[ilep]: continue
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: break
		if not drmin<0.01: continue
		#print ientry, 'found muon', lep.Pt() 
		
		if lep.Pt()>candPtCut: RecoMuons.append([lep,c.Muons_charge[ilep]])    
		if not c.Muons_MTW[ilep]<100: continue
		smear = 1
		smearedMu = TLorentzVector()
		smearedMu.SetPtEtaPhiE(0, 0, 0, 0)        
		smearedMu.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedMu.Pt()>candPtCut and smearedMu.Pt()<candPtUpperCut): continue
		SmearedMuons.append([smearedMu,c.Muons_charge[ilep],c.tracks_deDxHarmonic2pixel[matchedTrk[2]],c.tracks_deDxHarmonic2strips[matchedTrk[2]]])


	SmearedPions = []
	for ipi, pi in enumerate(c.TAPPionTracks):
		#if not c.isoPionTracks==1: continue
		isPromptPi = isMatched(pi, genpis, 0.02)		
		#if not isPromptPi: continue
		if verbose: print ientry, ipi,'pi with Pt' , pi.Pt()
		if (abs(pi.Eta()) < 1.566 and abs(pi.Eta()) > 1.4442): continue
		if not abs(pi.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.TAPPionTracks_trkiso[ipi]<0.01: continue
		
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:			
			if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
			if c.tracks_passPFCandVeto[trk[2]]: continue
			drTrk = trk[0].DeltaR(pi)
			if drTrk<drmin:			
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)):
		   drlep = lep.DeltaR(pi)
		   if drlep<0.01: 
			  passeslep = False
			  break
		if not passeslep: continue	  	   		
		smear = 1
		smearedPi = TLorentzVector()
		smearedPi.SetPtEtaPhiE(0, 0, 0, 0)        
		smearedPi.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].Pt()*TMath.CosH(matchedTrk[0].Eta()))
		if not (smearedPi.Pt()>candPtCut and smearedPi.Pt()<candPtUpperCut): continue
		if bool(isPromptPi): fillth1(hMtPionMatched,c.TAPPionTracks_mT[ipi])
		else: fillth1(hMtPionUnMatched,c.TAPPionTracks_mT[ipi])		
		if not c.TAPPionTracks_mT[ipi]<100: continue #this is kind of the one thing different about the control than the T&P		
		SmearedPions.append([smearedPi,c.TAPPionTracks_charge[ipi],c.tracks_deDxHarmonic2pixel[matchedTrk[2]],c.tracks_deDxHarmonic2strips[matchedTrk[2]]])
		
	
	singleElEvent_ = len(SmearedElectrons) >=1
	singleMuEvent_ = len(SmearedMuons) >=1    
	singlePiEvent_ = len(SmearedPions) >=1    
	presentDisTrkEvent = len(disappearingTracks) >=1# and len(SmearedElectrons) ==0 and len(SmearedMuons)==0 ##try commenting out last two

	if not (singleElEvent_ or presentDisTrkEvent or singleMuEvent_ or singlePiEvent_): continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	for elething in SmearedElectrons:
		elec, elcharge, eldedxPixel, eldedxStrips = elething
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = elec.DeltaR(genels[0])
			if verbose: print dr
			if not dr<0.02: continue

		#print ientry, 'found a tawdry se', elec.Pt()            
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(elec)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))

		if genMatchEverything:
				if RelaxGenKin:
						pt = elec.Pt()
						eta = abs(elec.Eta())
				else:
						pt = genels[0].Pt()
						eta = abs(genels[0].Eta())
		else:
				pt = elec.Pt()
				eta = abs(elec.Eta())    
		ptForKappa = pt
		
		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)
		log10dedxmass = TMath.Log10(TMath.Sqrt((eldedxPixel-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks), 1+nShort, nLong, mindphi, log10dedxmass,len(SmearedElectrons)-1, len(SmearedMuons), len(SmearedPions), pt,eta,eldedxPixel]
		fv.append(getBinNumber(fv))
		kPixOnly = fetchKappa(abs(eta),ptForKappa, kappadictElPixOnly, shortMaxKappaPt)
	
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight)
		
		#long        
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((eldedxStrips-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks), nShort, 1+nLong, mindphi, log10dedxmass,len(SmearedElectrons)-1, len(SmearedMuons), len(SmearedPions), pt,eta,eldedxStrips]
		fv.append(getBinNumber(fv))                    
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictElPixAndStrips)
		#kgen = fetchKappa(abs(eta),ptForKappa, fGenElProbePt_KappasPixAndStrips)
		#krec = fetchKappa(abs(eta),ptForKappa, fElProbePt_KappasPixAndStrips)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)# skip double counting 1-lep region
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight)                                        
		
		
	for muonthing in SmearedMuons:
		muon, mucharge, mudedxPixel, mudedxStrips = muonthing
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = muon.DeltaR(genmus[0])
			if verbose: print dr
			if not dr<0.02: continue           
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(muon)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))

		if genMatchEverything:
				if RelaxGenKin:
						pt = muon.Pt()
						eta = abs(muon.Eta())
				else:
						pt = genmus[0].Pt()
						eta = abs(genmus[0].Eta())
		else:
				pt = muon.Pt()
				eta = abs(muon.Eta())    
		ptForKappa = pt
		
		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		#smear *=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		#smear *=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)		
		log10dedxmass = TMath.Log10(TMath.Sqrt((mudedxPixel-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),1+nShort,nLong, mindphi, log10dedxmass,len(SmearedElectrons), len(SmearedMuons)-1, len(SmearedPions),pt,eta,mudedxPixel]
		fv.append(getBinNumber(fv))
		kPixOnly = fetchKappa(abs(eta),ptForKappa, kappadictMuPixOnly, shortMaxKappaPt)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Mu'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight)
					
		#long
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		#smear*=getSmearFactor(abs(eta),  min(pt,299.999), dResponseHist_mu_long)
		#smear*=getSmearFactor(abs(eta),  min(pt,299.999), dResponseHist_mu_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((mudedxStrips-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),nShort,nLong+1, mindphi,log10dedxmass, len(SmearedElectrons), len(SmearedMuons)-1, len(SmearedPions),pt,eta,mudedxStrips]
		fv.append(getBinNumber(fv))
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictMuPixAndStrips)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Mu'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight)                        
						
		
		
	for pithing in SmearedPions:
		pion, picharge, pidedxPixel, pidedxStrips = pithing
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = pion.DeltaR(genpis[0])
			if verbose: print dr
			if not dr<0.02: continue
		#print ientry, 'found a tawdry se', elec.Pt()            
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(pion)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))

		if genMatchEverything:
				if RelaxGenKin:
						pt = pion.Pt()
						eta = abs(pion.Eta())
				else:
						pt = genpis[0].Pt()
						eta = abs(genpis[0].Eta())
		else:
				pt = pion.Pt()
				eta = abs(pion.Eta()) 				
		ptForKappa = pt   
		
		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		log10dedxmass = TMath.Log10(TMath.Sqrt((pidedxPixel-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),1+nShort,nLong, mindphi, log10dedxmass,len(SmearedElectrons), len(SmearedMuons), len(SmearedPions)-1,pt,eta,pidedxPixel]
		fv.append(getBinNumber(fv))
		kPixOnly = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictPiPixOnly, shortMaxKappaPt)
		#print 'kPixOnly', kPixOnly, 'eta', eta, 'pt', ptForKappa
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Pi'+regionkey+'_'+varname
				#if 'TrkEta' in hname: print ientry, 'filling hname ', hname, fv
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight)
		#long
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		#smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((pidedxStrips-2.557)*pow(smear*pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),nShort,nLong+1, mindphi, log10dedxmass,len(SmearedElectrons), len(SmearedMuons), len(SmearedPions)-1,pt,eta,pidedxStrips]
		fv.append(getBinNumber(fv))
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictPiPixAndStrips)
		#print 'kPixAndStrips', kPixAndStrips, 'eta', eta, 'pt', ptForKappa
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Pi'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight)                        
									
	if presentDisTrkEvent:
		dt, status, dedxDT = disappearingTracks[0]
		print ientry, 'DT stuff dt, status, dedxDT ', dt, status, dedxDT 
		isPromptEl = isMatched(dt, genels, 0.02)
		isPromptMu = isMatched(dt, genmus, 0.02)
		isPromptPi = isMatched(dt, genpis, 0.02)
		if isdata: isPromptEl, isPromptMu, isPromptPi = True, True, True

		#if not (isPromptEl or isPromptMu or isPromptPi): continue

		#print ientry, 'found a nice dt', dt.Pt()   
		adjustedBTags = 0        
		adjustedJets = []
		adjustedHt = 0
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue			
			if not abs(jet.Eta())<5.0: continue###update to 2.4
			if not jet.DeltaR(dt)>0.4: continue###update to include second disappearing track
			adjustedMht-=jet		
			if not abs(jet.Eta())<2.4: continue###update to 2.4            
			adjustedJets.append(jet)			
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
			adjustedHt+=jet.Pt()
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))            
	#    if not adjustedNJets>0: continue                
		if genMatchEverything:
			if RelaxGenKin: 
				pt = dt.Pt()
				eta = abs(dt.Eta())
			else: 
				if isPromptEl: 
					pt = isPromptEl.Pt()
					eta = abs(isPromptEl.Eta())
				if isPromptMu:
					pt = isPromptMu.Pt()
					eta = abs(isPromptMu.Eta()) 
				if isPromptPi:
					pt = isPromptPi.Pt()
					eta = abs(isPromptPi.Eta()) 					               
		else: 
			pt = dt.Pt()
			eta = abs(dt.Eta()) 
		
		log10mass = TMath.Log10(TMath.Sqrt((dedxDT-2.557)*pow(pt*TMath.CosH(eta),2)/2.579))
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, log10mass, len(RecoElectrons), len(RecoMuons), len(SmearedPions), pt, eta,dedxDT]
		fv.append(getBinNumber(fv))
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				if selectionFeatureVector(fv,regionkey,varname):
					
						if isPromptEl: 
							fillth1(histoStructDict['El'+regionkey+'_'+varname].Truth,fv[ivar], weight)                
							if sayalot: print 'filling this el'
						elif isPromptMu: 
							fillth1(histoStructDict['Mu'+regionkey+'_'+varname].Truth,fv[ivar], weight)
							if sayalot: print 'filling this mu'
						elif isPromptPi: 
							fillth1(histoStructDict['Pi'+regionkey+'_'+varname].Truth,fv[ivar], weight)
							if sayalot: print 'filling this pi'							
						else: 	
							fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,fv[ivar], weight)
							if sayalot: print 'filling this fake'
			
		

fnew_.cd()
writeHistoStruct(histoStructDict)
hHt.Write()
hHtWeighted.Write()
hMtPionMatched.Write()
hMtPionUnMatched.Write()
print 'just created', fnew_.GetName()
fnew_.Close()
fKappaPixOnly.Close()
fsmear_short.Close()
fsmear_long.Close()

