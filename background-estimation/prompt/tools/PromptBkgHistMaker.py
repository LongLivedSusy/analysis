import os, sys
import time
import numpy as np
from ROOT import *
from utils import *
from glob import glob
from random import shuffle
import random

#gROOT.SetBatch(1)
gROOT.SetStyle('Plain')


defaultInfile_ = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_285_RA2AnalysisTree.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_78_RA2AnalysisTree.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-gk", "--useGenKappa", type=bool, default=False,help="use gen-kappa")
args = parser.parse_args()
inputFileNames = args.fnamekeyword
inputFiles = glob(inputFileNames)
analyzer = args.analyzer
pileup = args.pileup
useGenKappa = args.useGenKappa
print 'useGenKappa =', useGenKappa


genMatchEverything = False
RelaxGenKin = True
ClosureMode = True #false means run as if real data
SmearLeps = False
UseFits = False
UseDeep = False
verbose = False

c = TChain("TreeMaker2/PreSelection")
mZ = 91

isdata = 'Run20' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames: phase = 0
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
identifier+='nFiles'+str(len(inputFiles))
print 'Identifier', identifier


newfname = 'PromptBkgHists_'+identifier+'.root'

if useGenKappa: newfname = newfname.replace('.root','Truth.root')
fnew_ = TFile(newfname,'recreate')
print 'creating file', fnew_.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)


lepPtCut = 30
lepPtUpperCut = 6499

inf = 999999

regionCuts = {}
varlist_                         = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'NElectrons', 'NMuons', 'TrkPt',       'TrkEta','BinNumber']
regionCuts['NoCuts']             = [(0,inf), (0.0,inf), (0,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.0,inf),        (0,inf),     (0,inf),  (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['LowMhtBaseline']     = [(0,inf), (150,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (0,0  ),     (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
regionCuts['Baseline']           = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (0,0  ),     (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrEl']         = [(0,inf), (100,300), (2,inf), (1,5),   (1,1),   (0,inf), (0,inf),     (0.3,inf),        (1,1),       (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrMu']         = [(0,inf), (100,300), (2,inf), (1,5),   (1,1),   (0,inf), (0,inf),     (0.3,inf),        (0,0),       (1,1),    (lepPtCut,inf), (0,2.4), (-1,inf)]


regionCuts['BaselinePixOnly']    = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,inf),     (0.3,inf),        (0,0  ),     (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
regionCuts['BaselinePixAndStrips']  =[(0,inf),(250,inf),(1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (0,0  ),     (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrElPixOnly']  = [(100,inf), (100,300), (2,inf), (1,5),   (1,1),   (1,inf), (0,inf),     (0.3,inf),        (1,1),       (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrMuPixOnly']  = [(100,inf), (100,300), (2,inf), (1,5),   (1,1),   (1,inf), (0,inf),     (0.3,inf),        (0,0),       (1,1),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrElPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),   (1,1),   (0,inf), (1,inf),     (0.3,inf),        (1,1),       (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]
#regionCuts['TtbarCtrMuPixAndStrips']=[(100,inf),(100,300),(2,inf), (1,5),   (1,1),   (0,inf), (1,inf),     (0.3,inf),        (0,0),       (1,1),    (lepPtCut,inf), (0,2.4), (-1,inf)]

#regionCuts['LowMhtBasePixAndStrips']=[(0,inf),(150,inf),(1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (0,0  ),     (0,0),    (lepPtCut,inf), (0,2.4), (-1,inf)]


indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
	for var in varlist_:
		histname = 'El'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Mu'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)        
		histname = 'Fake'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)  
		   
		
binnumbers = {}
listagain = ['Ht',  'Mht',    'NJets','BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets', 'NElectrons', 'NMuons', 'TrkPt','TrkEta','BinNumber']
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.2,inf))] = 1
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.2,inf))] = 2
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.2,inf))] = 3
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.2,inf))] = 4
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.2,inf))] = 5
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.3,inf))] = 6
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 7
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 8
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 9
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf))] = 10
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.3,inf))] = 11
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 12
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 13
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf))] = 14
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf))] = 15
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.2,inf))] = 16
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.2,inf))] = 17
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.2,inf))] = 18
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.2,inf))] = 19
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.2,inf))] = 20
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.3,inf))] = 21
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 22
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 23
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 24
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf))] = 25
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.3,inf))] = 26
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 27
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 28
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf))] = 29
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf))] = 30
binnumbers[((0,inf),(250,400),(1,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=31
binnumbers[((0,inf),(400,inf),(1,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=32

def getBinNumber(fv):
	for binkey in binnumbers:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumbers[binkey]
	return -1

for f in inputFiles:
	print 'adding file:', f
	c.Add(f)
	break
nentries = c.GetEntries()
#nentries = 100

c.Show(0)
#nentries = 5

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


#pause()
#fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root'
if isdata: fsmearname = 'usefulthings/DataDrivenSmear_2016Data.root'
else: fsmearname = 'usefulthings/DataDrivenSmear_2016MC.root' ##this is different from tag/probe
fSmear  = TFile(fsmearname)
fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
else: 
	#hMask = fMask.Get('hEtaVsPhiDTRun2016')
	hMask = ''

dResponseHist = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
	for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
		newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
		dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))

print 'dResponseHist', dResponseHist
def getSmearFactor(Eta, Pt, Draw = False):
	if SmearLeps:
	  for histkey in  dResponseHist:
		if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
			return 10**(dResponseHist[histkey].GetRandom())
	else: return 1.0
	print 'returning 1', Eta, Pt, dResponseHist
	return 1

import os
if phase==0:
	pixelXml =       '/nfs/dust/cms/user/kutznerv/disapptrks/track-tag/cmssw8-newpresel3-200-4-short-updated/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = '/nfs/dust/cms/user/kutznerv/disapptrks/track-tag/cmssw8-newpresel2-200-4-medium-updated/weights/TMVAClassification_BDT.weights.xml'
else:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks/weights/TMVAClassification_BDT.weights.xml'
readerPixelOnly = TMVA.Reader()
readerPixelStrips = TMVA.Reader()
prepareReaderPixel(readerPixelOnly, pixelXml)
prepareReaderPixelStrips(readerPixelStrips, pixelstripsXml)


if isdata: 
	if phase==0:
		fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly.root'
		fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips.root' 
		fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips.root'
	else:
		fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly.root'
		#fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips.root' 
		#fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly.root'
		#fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips.root'		
   
else: 
	if phase==0:
		fileKappaPixOnly = 'usefulthings/KappaSummer16.DYJets_PixOnly.root'#should be updated to All
		fileKappaPixAndStrips = 'usefulthings/KappaSummer16.DYJets_PixAndStrips.root'
		fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips.root' 
	else:
		fileKappaPixOnly = 'usefulthings/KappaFall17.DYJets_PixOnly.root'#should be updated to All
		fileKappaPixAndStrips = 'usefulthings/KappaFall17.DYJets_PixAndStrips.root'
		fileKappaPixOnlyGen = 'usefulthings/KappaFall17.WJets_PixOnly.root'
		fileKappaPixAndStripsGen = 'usefulthings/KappaFall17.WJets_PixAndStrips.root' 


fKappaPixOnly  = TFile(fileKappaPixOnly)
fKappaPixAndStrips  = TFile(fileKappaPixAndStrips)
fKappaPixOnlyGen  = TFile(fileKappaPixOnlyGen)
fKappaPixAndStripsGen  = TFile(fileKappaPixAndStripsGen)


fElProbePt_KappasPixOnly = {}
fGenElProbePt_KappasPixOnly = {}
fMuProbePt_KappasPixOnly = {}
fGenMuProbePt_KappasPixOnly = {}

fElProbePt_KappasPixAndStrips = {}
fGenElProbePt_KappasPixAndStrips = {}
fMuProbePt_KappasPixAndStrips = {}
fGenMuProbePt_KappasPixAndStrips = {}


for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
	if etakey == (1.4442, 1.566): continue
	specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')
	oldNumName = "hElProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
	newKappaFuncName = UseFits*'f1'+newKappaName
	fElProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
	fElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
	oldGenNumName = "hGenElProbePtDT"+specialpart+"_num"
	newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
	newGenKappaFuncName = UseFits*'f1'+newGenKappaName
	fGenElProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
	fGenElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long')
	
	oldNumName = "hMuProbePtDT"+specialpart+"_num"
	newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
	newKappaFuncName = UseFits*'f1'+newKappaName
	fMuProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
	fMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
	oldGenNumName = "hGenMuProbePtDT"+specialpart+"_num"
	newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
	newGenKappaFuncName = UseFits*'f1'+newGenKappaName
	fGenMuProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
	fGenMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long') 
	 

if useGenKappa: 
	kappadictElPixOnly = fGenElProbePt_KappasPixOnly
	kappadictMuPixOnly = fGenMuProbePt_KappasPixOnly    

	kappadictElPixAndStrips = fGenElProbePt_KappasPixAndStrips
	kappadictMuPixAndStrips = fGenMuProbePt_KappasPixAndStrips        
else: 
	kappadictElPixOnly = fElProbePt_KappasPixOnly
	kappadictMuPixOnly = fMuProbePt_KappasPixOnly  

	kappadictElPixAndStrips = fElProbePt_KappasPixAndStrips
	kappadictMuPixAndStrips = fMuProbePt_KappasPixAndStrips        


dKappaBinList = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdges[:-1]):
		for iEtaBinEdge, EtaBinEdge in enumerate(EtaBinEdges[:-1]):
				newHistKey = ((EtaBinEdge,EtaBinEdges[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdges[iPtBinEdge + 1]))
				dKappaBinList[newHistKey] = [iPtBinEdge+1,iEtaBinEdge+1]
		
		
shortMaxKappaPt = 1000
def fetchKappa(Eta, Pt_, KappaDict=fGenElProbePt_KappasPixOnly, maxpt = 1000):
	Pt = min(Pt_,maxpt)
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
		if abs(Eta) >= etakey[0] and abs(Eta) <= etakey[1]:
			#return 1
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
#triggerIndecesV2['SingleEl'] = [36,39]
#triggerIndecesV2['SingleEl45'] = [41]
triggerIndecesV2['SingleElCocktail'] = [14, 15, 16, 17, 18, 19, 20, 21]
#triggerIndecesV2['MhtMet6pack'] = [108,110,114,123,124,125,126,128,129,130,131,132,133,122,134]#123
#triggerIndecesV2["SingleMu"] = [48,50,52,55,63]
triggerIndecesV2["SingleMuCocktail"] = [24,25,26,27,28,30,31,32]
#triggerIndecesV2["SinglePho"] = [139]
#triggerIndecesV2["SinglePhoWithHt"] = [138, 139,141,142,143]
#triggerIndecesV2['HtTrain'] = [67,68,69,72,73,74,80,84,88,91,92,93,95,96,99,102,103,104]

triggerIndeces = triggerIndecesV2

def PassTrig(c,trigname):
	for trigidx in triggerIndeces[trigname]: 
		if c.TriggerPass[trigidx]==1: 
			return True
	return False

verbosity = 10000
print nentries, 'evets to be analyzed'
for ientry in range(nentries):
	if verbose:
		if not ientry in [17681]: continue
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
	hHtWeighted.Fill(c.HT,weight)


	if not isdata:
	  isValidHtRange = False
	  for madrange in madranges:
		if (c.madHT>madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	  if not isValidHtRange: continue

	if ClosureMode:
		genels = []
		genmus = []
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue    
			if not c.GenParticles_Status[igp] == 1: continue        
			#if not abs(c.GenParticles_ParentId[igp]) == 24: continue
			if abs(c.GenParticles_PdgId[igp])==11: genels.append(gp)
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append(gp)            
		#if genMatchEverything:
		#    if not len(genels)==1: continue
	else: genels, genmus = [], []

	#if isdata:################################################################################# this is probably something you want to change
	#    if not (PassTrig(c, 'SingleElCocktail') or PassTrig(c, 'SingleMuCocktail')): continue

	if not c.CaloMET/c.MET<5.0: continue
	#if not c.JetID: continue

	muons = []        
	for imu, muon in enumerate(c.Muons):
		if not muon.Pt()>10: continue
		#if abs(muon.Eta()) < 1.566 and abs(muon.Eta()) > 1.4442: continue
		if not abs(muon.Eta())<2.4: continue    
		muons.append([muon,c.Muons_charge[imu]])
	#if not len(muons)==0: continue    
	if verbose: print "test muon"
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
		basicTracks.append([track,c.tracks_charge[itrack], itrack])
		if not (track.Pt() > lepPtCut and track.Pt()<lepPtUpperCut): continue     
		if verbose: print 'still in the woods', itrack, 'pt', track.Pt(), 'eta', track.Eta()           
		dtstatus = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips, mvathreshes)
		if dtstatus==0: continue
		drlep = 99
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break            
		if not passeslep: continue        
		#print 'found disappearing track w pT =', track.Pt() 
		if dtstatus==1: nShort+=1
		if dtstatus==2: nLong+=1         
		if verbose: print itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta()        
		disappearingTracks.append([track,dtstatus])

	if len(disappearingTracks)>0:
		print ientry, 'got disappearing track!', disappearingTracks[0]

	SmearedElectrons = []
	RecoElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if verbose: print ientry, iel,'ele with Pt' , ele.Pt()
		if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
		if not abs(ele.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Electrons_passIso[iel]: continue
		if not c.Electrons_mediumID[iel]: continue
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(ele)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if ele.Pt()>lepPtCut: RecoElectrons.append([ele, c.Electrons_charge[iel]])
		smear = getSmearFactor(abs(matchedTrk[0].Eta()), min(matchedTrk[0].Pt(),299.999))
		smearedEl = TLorentzVector()
		smearedEl.SetPtEtaPhiE(0, 0, 0, 0)        
		smearedEl.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedEl.Pt()>lepPtCut and smearedEl.Pt()<lepPtUpperCut): continue
		SmearedElectrons.append([smearedEl,c.Electrons_charge[iel]])
		#print 'a lovely ele', ele.Pt(), smearedEle.Pt()


	SmearedMuons = []
	RecoMuons = []
	for ilep, mu in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , mu.Pt()
		if (abs(mu.Eta()) < 1.566 and abs(mu.Eta()) > 1.4442): continue
		if not abs(mu.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Muons_passIso[ilep]: continue
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(mu)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if mu.Pt()>lepPtCut: RecoMuons.append([mu,c.Muons_charge[ilep]])    
		smear = getSmearFactor(abs(matchedTrk[0].Eta()), min(matchedTrk[0].Pt(),299.999))
		smearedMu = TLorentzVector()
		smearedMu.SetPtEtaPhiE(0, 0, 0, 0)        
		smearedMu.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedMu.Pt()>lepPtCut and smearedMu.Pt()<lepPtUpperCut): continue
		SmearedMuons.append([smearedMu,c.Muons_charge[ilep]])    


	singleElEvent_ = len(SmearedElectrons) >=1
	singleMuEvent_ = len(SmearedMuons) >=1    
	presentDisTrkEvent = len(disappearingTracks) >=1# and len(SmearedElectrons) ==0 and len(SmearedMuons)==0 ##try commenting out last two

	if not (singleElEvent_ or presentDisTrkEvent or singleMuEvent_): continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	if singleElEvent_:
		elec = random.sample(SmearedElectrons,1)[0][0]
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
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1
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
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks), 1+nShort, nLong, mindphi, len(SmearedElectrons)-1, len(SmearedMuons), pt,eta]
		fv.append(getBinNumber(fv))
		kPixOnly = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictElPixOnly, shortMaxKappaPt)
		
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight)
			
		#long        
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks), nShort, 1+nLong, mindphi, len(SmearedElectrons)-1, len(SmearedMuons), pt,eta]
		fv.append(getBinNumber(fv))                    
		kPixAndStrips = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictElPixAndStrips)
		
		kgen = fetchKappa(abs(eta),min(ptForKappa,9999.99), fGenElProbePt_KappasPixAndStrips)
		krec = fetchKappa(abs(eta),min(ptForKappa,9999.99), fElProbePt_KappasPixAndStrips)
			
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)# skip double counting 1-lep region
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight)                                        
			
			
	if singleMuEvent_:
		muon = random.sample(SmearedMuons,1)[0][0]
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = muon.DeltaR(genmus[0])
			if verbose: print dr
			if not dr<0.02: continue
		#print ientry, 'found a tawdry se', elec.Pt()            
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(muon)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1
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
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),1+nShort,nLong, mindphi, len(SmearedElectrons), len(SmearedMuons)-1,pt,eta]
		fv.append(getBinNumber(fv))
		kPixOnly = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictMuPixOnly, shortMaxKappaPt)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Mu'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight)
			
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, 1+len(disappearingTracks),nShort,nLong+1, mindphi, len(SmearedElectrons), len(SmearedMuons)-1,pt,eta]
		fv.append(getBinNumber(fv))
		kPixAndStrips = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictMuPixAndStrips)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'Mu'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)
					fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight)                        
							
			
			
								
	if presentDisTrkEvent:
		dt = disappearingTracks[0][0]
		isPromptEl = isMatched(dt, genels, 0.02)
		isPromptMu = isMatched(dt, genmus, 0.02)    
		if isdata:     isPromptEl, isPromptMu = True, True

		#if not (isPromptEl or isPromptMu): continue

		print ientry, 'found a nice dt', dt.Pt()
		adjustedNJets = 0        
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
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1
			adjustedJets.append(jet)
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
		else: 
			pt = dt.Pt()
			eta = abs(dt.Eta())    
		fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi,len(RecoElectrons), len(RecoMuons), pt, eta]
		fv.append(getBinNumber(fv))
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				if selectionFeatureVector(fv,regionkey,varname):
						if isPromptEl: fillth1(histoStructDict['El'+regionkey+'_'+varname].Truth,fv[ivar], weight)                
						elif isPromptMu: fillth1(histoStructDict['Mu'+regionkey+'_'+varname].Truth,fv[ivar], weight)
						else: fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,fv[ivar], weight)
				
			

fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict)
print 'just created', fnew_.GetName()
fnew_.Close()
fKappaPixOnly.Close()
fSmear.Close()
