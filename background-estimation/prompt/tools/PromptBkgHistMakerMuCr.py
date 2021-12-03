from ROOT import *
import os, sys
from glob import glob
from random import shuffle
import time
import numpy as np
import random
import math
import json
gROOT.SetStyle('Plain')
##gROOT.SetBatch(1)
from code import interact
import collections


execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False 

'''
python tools/PromptBkgHistMakerFullyInformed.py --fnamekeyword /nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_10_1_0/src/analysis/background-estimation/prompt/output/mediumchunks/Summer16TTJets_SingleLeptFromT_Prompt.root --smearvar Nom --analyzeskims True
'''

turnoffpred = False
maketree = False

flythrough4tf = False
exomode = False
deriveMask = False #also turn this to true when skimming

varname_kappaBinning = 'TrkEta'
varname_kappaBinning = 'TrkPt'
varname_thetaBinning = 'TrkPt'
varname_thetaBinning = 'TrkEta'

#smearvar = 'Drop1st'
codeproduct = sys.argv[0].split('/')[-1].split('With')[0].split('Maker')[0]
defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_50000-3*.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_78_RA2AnalysisTree.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-smearvar", "--smearvar", type=str, default='Nom',help="use gen-kappa")
parser.add_argument("-ps", "--analyzeskims", type=str, default='False',help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
args = parser.parse_args()
nfpj = args.nfpj
analyzeskims = bool(args.analyzeskims=='True')
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
analyzer = args.analyzer
pileup = args.pileup
smearvar = args.smearvar
verbosity = args.verbosity

maketree = bool(not analyzeskims)


genMatchEverything = False
RelaxGenKin = True
ClosureMode = True #false means run as if real data
UseFits = False
UseJets_bJetTagDeepCSVBvsAll = True
sayalot = False
candPtCut = 25
hiptcut = 40
leppt = 40





verbose = False

isSkimRun2017DSingleMu = False

blockhem = False
partiallyblockhem = False

isdata = 'Run201' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames: 
	is2016, is2017, is2018, year = True, False, False, '2016'
elif 'Run2017' in inputFileNames: 
	#is2016, is2017, is2018, year = False, True, False, '2017'
	is2016, is2017, is2018, year = False, True, False, 'Phase1'	
	if 'skimRun2017D-SingleMu.root' in inputFileNames: isSkimRun2017DSingleMu=True
elif  'Fall17' in inputFileNames:
	is2016, is2017, is2018, year = False, True, False, '2017'
elif 'Run2018' in inputFileNames or 'Autumn18' in inputFileNames or 'somthin or other' in inputFileNames: 
	#is2016, is2017, is2018, year = False, True, True, '2018'
	is2016, is2017, is2018, year = False, False, True, 'Phase1'	
	if 'Run2018B' in inputFileNames:
		partiallyblockhem = True
	if 'Run2018C' in inputFileNames or 'Run2018D' in inputFileNames:
		blockhem = True

ismc = not isdata
if is2016: phase = 0
else: phase = 1



if ismc: hiptcut = 30

if 'SMS' in inputFileNames: issignal = True
else: issignal = False


if is2016: BTAG_deepCSV = 0.6321###hello!!
if is2017: BTAG_deepCSV = 0.4941
if is2018: BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV

print 'phase', phase

if isdata: ClosureMode = False


if not turnoffpred:
	if isdata:  ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'_data.root')
	else: ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'_mc.root')


	hfrlong = ffakerate.Get('hfrlong')
	hfrshort = ffakerate.Get('hfrshort')	

	if isdata:  fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'_data.root')
	else: fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'_mc.root')

	print 'trying to get hprshort from', fpromptrate.GetName() 
	hprshort = fpromptrate.Get('hprshort')
	hprlong = fpromptrate.Get('hprlong')

	if isdata:  fmurate = TFile('usefulthings/murateInfo_year'+year+'_data.root')
	else: fmurate = TFile('usefulthings/murateInfo_year'+year+'_mc.root')	
	hmrshort = fmurate.Get('hprshort')
	hmrlong = fmurate.Get('hprlong')	


def getfakerate(ht, hfr):
	#return 2.0
	xax = hfr.GetXaxis()
	thebin = max(1, min(xax.FindBin(ht), xax.GetNbins()))
	return hfr.GetBinContent(thebin)

def getpromptrate(obs, hpr):
	return hpr.GetBinContent(hpr.GetXaxis().FindBin(abs(obs)))

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
print 'Identifier', identifier



calib_version = '-SingleMuon'
calib_version = ''# Sang-Il's new key names
if 'Run20' in identifier: 
	keyforcalibs = identifier.split('-')[0].replace('skims','').replace('skim','')+calib_version
	keyforcalibs = keyforcalibs.replace('PromptBkgTree_','').replace('PromptBkgHist_','')
	print 'keyforcalibs', keyforcalibs
	#exit(0)
	dedxcalib_barrel = DedxCorr_Pixel_barrel[keyforcalibs]
	dedxcalib_endcap = DedxCorr_Pixel_endcap[keyforcalibs]
elif 'Summer16' in identifier: 
	dedxcalib_barrel = DedxCorr_Pixel_barrel['Summer16']
	dedxcalib_endcap = DedxCorr_Pixel_endcap['Summer16']
elif 'Fall17' in identifier or 'Autumn18' in identifier: 
	dedxcalib_barrel = DedxCorr_Pixel_barrel['Fall17']
	dedxcalib_endcap = DedxCorr_Pixel_endcap['Fall17']
else: 
	dedxcalib_barrel = 1.0
	dedxcalib_endcap = 1.0	


#######Sang-Il new
doDedxSmear = False
if ismc:
	doDedxSmear = True
	if smearvar=='Nom': fsmear_barrel, fsmear_endcap = Load_DedxSmear(1)
	if smearvar=='Drop1st': fsmear_barrel, fsmear_endcap = Load_DedxSmear_MIH(1)


f_dxydzcalibration = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/dxydzcalibration.root')
if 'Fall17' in identifier or 'Autumn18' in identifier:
		vtx_calibs = [f_dxydzcalibration.Get('g_calibratedxy'), f_dxydzcalibration.Get('g_calibratedz')]
else:
	vtx_calibs = []


newfname = codeproduct+'_'+identifier+'.root'
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])
moreargs = moreargs.replace(' ','').replace('--','-')
newfname = newfname.replace('.root',moreargs+'.root')
if exomode:
	newfname = newfname.replace('.root','ExoMode.root')
if maketree:
	newfname = newfname.replace('Hist', 'Tree')
	try:
		l= c.GetLeaf("HLTElectronObjects")
		c.GetListOfLeaves().Remove(l)
	except: 
		pass

fnew = TFile(newfname,'recreate')
print 'making', fnew.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 999999999999


callShort = 13
callShort = 15
callShort = 15 
callShort = 12 ##  tighten for normal version #works kinda fine with hybrid
callShort = 15 ##  loosen for frac version

#callShort = 20 ##  loosen for frac version
callLong = 20

lowht = 0
#lowht = 60

if is2016: 

	mvaPromptLongLoose = 0.1#<==0.1 ##this is good May21
	mvaPromptShortLoose = 0.05#<==#-0.05

	mvaFakeShortLoose = -0.1	
	mvaFakeShortMedium = -0.05#could try this next 4.08.21
	
	mvaFakeLongLoose = -0.1
	mvaFakeLongMedium = 0.0
	mvaShortTight = 0.1
	mvaLongTight = 0.12

	calmShort, calhShort = 30, 300 #works well in data		
	calmLong, calhLong = 30, 120
else:

	mvaPromptShortLoose = 0.05
	mvaPromptLongLoose = 0.08
	
	mvaFakeShortLoose = -0.1#==-0.1#-0.1#-0.3
	mvaFakeShortMedium = 0.05
		
	mvaFakeLongLoose = -0.1#<==-0.05#<==-0.15 #tuesday earlymorning	
	mvaFakeLongMedium = 0.0	
	
	
	mvaShortTight = 0.15#was feeling good about this after shower, but it was a bit loose########
	mvaLongTight = 0.08#Tuesday earlymorning
	
	calmShort, calhShort = 30, 300 #works well in data		
	calmLong, calhLong = 30, 120


mdp= 0.3
print 'calhLong, calmLong', calhLong, calmLong
mvaminShort = min([mvaPromptShortLoose, mvaFakeShortLoose])
mvaminLong  = min([mvaPromptLongLoose,  mvaFakeLongLoose] )

mvaminLong, mvaminShort = -1, -1 #one more try to expand prompt short CR
if deriveMask: 
	mvaLongTight, mvaShortTight = -0.2, -0.2

pi = TMath.Pi()
#                                                   1        2          3        4       5         6       7               8           9                    10          11       12        13           14           15          16              17             18             19           20             21             22                23        24
regionCuts = {}
varlist_                                       = ['Ht',     'Mht',  'NJets', 'BTags', 'NTags', 'NPix','NPixStrips','MinDPhiMhtJets','DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',    'MatchedCalo', 'IsMuMatched', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',  'MissingOuterHits',  'LepPt',  'DrJetDt', 'BinNumber','MinDPhiMhtHemJet','MTauTau','Log10DedxMass']#]#'Log10DedxMass'
if analyzeskims:
	regionCuts['ShortSElValidZLL']             = [(0,inf), (0,inf), (0,inf), (0,inf), (1,inf), (1,1),   (0,0),   (mdp,inf),          (0,inf),        (1,1 ),      (0,0),     (70,105),   (0,100),  (candPtCut,inf), (0,2.4),  (0,callShort),   (0,0),   (-inf,inf),    (0,pi/4), (mvaShortTight,inf), (-inf,inf),     (-inf,inf),     (-inf,inf),   (0.2,inf)]
	regionCuts['ShortSMuValidZLL']             = [(0,inf), (0,inf), (0,inf), (0,inf), (1,inf), (1,1),   (0,0),   (mdp,inf),          (0,inf),        (0,0 ),      (1,1),     (70,105),   (0,100),  (candPtCut,inf), (0,2.4),  (0,callShort),   (0,0),   (-inf,inf),    (0,pi/4), (mvaShortTight,inf), (-inf,inf),     (-inf,inf),     (-inf,inf),   (0.2,inf)]	
	regionCuts['LongSElValidZLL']              = [(0,inf), (30,inf), (0,inf), (0,inf), (1,inf), (0,0),   (1,1),   (mdp,inf),          (0,inf),         (1,1 ),     (0,0),      (75,100),  (0,100),  (hiptcut,inf),    (0,2.4),  (0,callLong),   (0,0),  (-inf,inf),      (0,pi/2),  (mvaLongTight,inf), (-inf,inf),    (2,inf),        (-inf,inf),   (0.2,inf)]
	regionCuts['LongSMuValidZLL']              = [(0,inf), (30,inf), (0,inf), (0,inf), (1,inf), (0,0),   (1,1),   (mdp,inf),          (0,inf),         (0,0 ),     (1,1),      (75,100),  (0,100),  (hiptcut,inf),    (0,2.4),  (0,callLong),   (0,0),  (-inf,inf),      (0, pi/2),   (mvaLongTight,inf), (-inf,inf),  (2,inf),        (-inf,inf),   (0.2,inf)]	
	#regionCuts['ShortSMuLowMTLowMet']         = [(0,inf),(30,100), (1,inf), (0,inf), (1,inf), (1,1),  (0,0),     (-inf,inf),          (0,inf),         (0,0),     (1,1),      (140,inf), (30,100),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),   (-inf,inf),      (0,inf), (mvaLongTight,inf), (-inf,inf),    (-inf,inf),       (-inf,inf), (0.2,inf)]	
	#regionCuts['LongSMuLowMTLowMet']          = [(0,inf),(30,100), (1,inf), (0,inf), (1,inf), (0,0),  (1,inf),   (-inf,inf),          (0,inf),         (0,0),     (1,1),      (140,inf), (30,100),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),   (-inf,inf),      (0,inf), (mvaLongTight,inf), (-inf,inf),    (-inf,inf),      (-inf,inf),   (0.2,inf)]
	regionCuts['ShortHadMhtSideband']          = [(0,inf), (30,60),    (1,inf), (0,0), (1,inf), (1,1),(0,0),       (mdp,inf),       (0,inf),        (0,0),       (0,0),       (140,inf),  (0,inf),  (candPtCut,inf), (0,2.4), (0,callShort),   (0,0),   (-inf,inf),    (0,inf), (mvaShortTight,inf), (20,inf),       (-inf,inf),      (-inf,inf),   (0.2,inf)]
	regionCuts['LongHadMhtSideband']           = [(0,inf), (30,60),    (1,inf), (0,0), (1,inf), (0,0),(1,1),       (mdp,inf),       (0,inf),         (0,0),      (0,0),      (140,inf), (0,inf),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),    (-inf,inf),      (0,inf), (mvaLongTight,inf), (20,inf),      (2,inf),        (-inf,inf),    (0.2,inf)]
	if not flythrough4tf:    
    
    
		regionCuts['Long1bHadMhtSideband']     = [(0,inf), (30,60),    (1,inf), (1,1), (1,inf), (0,0),(1,1),       (mdp,inf),       (0,inf),         (0,0),      (0,0),      (140,inf), (0,inf),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),    (-inf,inf),      (0,inf), (mvaLongTight,inf), (20,inf),      (2,inf),        (-inf,inf),    (0.2,inf)]
		regionCuts['LongBaseline']             = [(0,inf), (30,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),   (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (hiptcut,inf),   (0,2.4),  (0,callLong),   (0,0),   (-inf,inf),   (0,inf), (mvaLongTight,inf),   (20,inf),         (2,inf),        (20,inf),    (0.2,inf)]
		#regionCuts['Long1bBaseline']           = [(0,inf), (30,inf), (1,inf), (1,inf), (1,inf), (0,inf), (1,inf),   (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (hiptcut,inf),   (0,2.4),  (0,callLong),   (0,0),   (-inf,inf),   (0,inf), (mvaLongTight,inf),   (40,inf),         (2,inf),        (20,inf),    (0.2,inf)]		
		regionCuts['LongHighMetBaseline']      = [(0,inf), (300,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),  (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (hiptcut,inf),   (0,2.4),  (0,callLong),   (0,0),   (-inf,inf),   (0,inf), (mvaLongTight,inf),   (20,inf),         (2,inf),        (20,inf),    (0.2,inf)]		
		#regionCuts['LongBin23']               = [(0,inf), (300,inf),(3,inf),  (0,inf),  (1,1),  (0,inf), (1,inf),    (mdp,inf),(0,dedxcutMid),  (0,0),     (0,0),      (140,inf),  (110,inf), (hiptcut,inf),    (0,2.4),  (0,callLong),   (-inf,inf),   (0,inf), (mvaLongTight,inf), (10,inf),      (-inf,inf),  (-inf,inf)]

		regionCuts['LongSElValidZLLHighMT']    = [(0,inf),  (30,inf),  (0,inf), (0,inf), (1,inf), (0,0),   (1,inf),  (mdp,inf),      (0,inf),         (1,1 ),    (0,0),      (70,110),  (100,inf),  (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),  (-inf,inf),      (0,inf), (mvaLongTight,inf),(-inf,inf),       (2,inf),        (20,inf),    (0.2,inf)]
		regionCuts['LongSElValidMT']           = [(0,inf),  (30,inf),  (0,inf), (0,inf), (1,inf), (0,0),   (1,inf),  (mdp,inf),      (0,inf),         (1,1 ),    (0,0),      (140,inf), (0,100),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),   (-inf,inf),      (0,inf), (mvaLongTight,inf),(-inf,inf),       (2,inf),        (20,inf),    (0.2,inf)]
		regionCuts['LongSMuValidMT']           = [(0,inf),  (30,inf),  (0,inf), (0,inf), (1,inf), (0,0),   (1,inf),    (mdp,inf),      (0,inf),         (0,0),     (1,1),      (140,inf), (0,100),   (hiptcut,inf),    (0,2.4), (0,callLong),   (0,0),   (-inf,inf),      (0,inf), (mvaLongTight,inf),(-inf,inf),     (2,inf),        (20,inf),    (0.2,inf)]
#varlist_                                      = ['Ht',           'Mht',  'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',    'MatchedCalo', 'IsMuMatched', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',      'MissingOuterHits',  'LepPt',  'BinNumber','DrJetDt','MinDPhiMhtHemJet','MTauTau','Log10DedxMass']#]#'Log10DedxMass'
		regionCuts['Short1bHadMhtSideband']    = [(0,inf), (30,60),    (1,inf), (1,1), (1,inf), (1,1),(0,0),       (mdp,inf),       (0,inf),        (0,0),       (0,0),       (140,inf),  (0,inf),  (candPtCut,inf), (0,2.4), (0,callShort),   (0,0),   (-inf,inf),    (0,inf), (mvaShortTight,inf), (20,inf),       (-inf,inf),      (-inf,inf),   (0.2,inf)]
		regionCuts['ShortBaseline']            = [(0,inf), (30,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,0),     (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (candPtCut,inf),    (0,2.4),  (0,callShort),   (0,0),      (-inf,inf),   (0,inf), (mvaShortTight,inf),(20,inf),    (-inf,inf),     (40,inf),    (0.2,inf)]
		#regionCuts['Short1bBaseline']          = [(0,inf), (30,inf), (1,inf), (1,inf), (1,inf), (1,inf), (0,0),     (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (candPtCut,inf),    (0,2.4),  (0,callShort),   (0,0),      (-inf,inf),   (0,inf), (mvaShortTight,inf),(40,inf),    (-inf,inf),     (40,inf),    (0.2,inf)]		
		regionCuts['ShortHighMetBaseline']     = [(0,inf), (300,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,0),    (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (candPtCut,inf),    (0,2.4),  (0,callShort),   (0,0),      (-inf,inf),   (0,inf), (mvaShortTight,inf),(20,inf),    (-inf,inf),     (40,inf),    (0.2,inf)]		
		#regionCuts['Short1bBaseline']         = [(0,inf), (30,inf), (1,inf),(1,inf), (1,inf), (1,inf), (0,0),     (0.3,inf),   (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (candPtCut,inf),    (0,2.4),  (0,callShort),       (0,0),   (0,1),      (-inf,inf),   (0,inf), (mvaShortTight,inf),(10,inf),  (-inf,inf), (-inf,inf)]		
		#regionCuts['ShortBin23']                = [(0,inf),  (300,inf),(3,inf),  (0,inf),  (1,1),  (1,1), (0,0),    (mdp,inf),      (0,dedxcutMid),  (0,0),   (0,0),     (140,inf), (110,inf), (candPtCut,inf),       (0,2.4),  (0,callShort),   (0,0),   (-inf,inf),   (0,inf), (mvaShortTight,inf),(10,inf), (-inf,inf), (-inf,inf)]
		##regionCuts['ShortLowMhtBaseline']    = [(0,inf), (100,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (0,inf),         (0,inf),     (0,inf),  (110,inf), (100,inf), (candPtCut,inf),   (0,2.4), (0,callLong),       (0,0),      (1,1),    (0,inf), (mvaLongTight,inf)]
		#varlist_                              = ['Ht',          'Mht',  'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',         'TrkEta',    'MatchedCalo', 'IsMuMatched',   (0,1), 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',     'MTauTau',    'LepPt',      'BinNumber','DrJetDt','MinDPhiMhtHemJet','Log10DedxMass']
		regionCuts['ShortSElValidZLLHighMT']   = [(0,inf), (30,inf),  (0,inf), (0,inf), (1,inf), (1,inf), (0,0),      (mdp,inf),     (0,inf),        (1,1 ),     (0,0),     (70,110),   (100,inf),  (candPtCut,inf), (0,2.4), (0,callShort),   (0,0),  (-inf,inf),      (0,inf), (mvaShortTight,inf),(20,inf),        (-inf,inf),     (20,inf),    (0.2,inf)]	
		regionCuts['ShortSElValidMT']          = [(0,inf), (30,inf),  (0,inf), (0,inf), (1,inf), (1,inf), (0,0),      (mdp,inf),     (0,inf),        (1,1 ),     (0,0),     (140,inf),  (0,100),   (candPtCut,inf), (0,2.4), (0,callShort),   (0,0),   (-inf,inf),      (0,inf), (mvaShortTight,inf),(20,inf),        (-inf,inf),     (20,inf),    (0.2,inf)]
		regionCuts['ShortSMuValidMT']          = [(0,inf), (30,inf),  (0,inf), (0,inf), (1,inf), (1,inf), (0,0),      (mdp,inf),     (0,inf),        (0,0),      (1,1),     (140,inf),  (0,100),   (candPtCut,inf), (0,2.4), (0,callShort),   (0,0),   (-inf,inf),      (0,inf), (mvaShortTight,inf),(20,inf),        (-inf,inf),     (20,inf),    (0.2,inf)]
#varlist_                                      = ['Ht',           'Mht',  'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',    'MatchedCalo', 'IsMuMatched', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',      'MissingOuterHits',  'LepPt',  'BinNumber','DrJetDt','MinDPhiMhtHemJet','MTauTau','Log10DedxMass']#]#'Log10DedxMass'



#varlist_                                       = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo',      'DtStatus',    'inf', 'Met']

dedxidx = varlist_.index('DeDxAverage')
srindex = varlist_.index('BinNumber')
mcalidx = varlist_.index('MatchedCalo')
statidx = varlist_.index('DtStatus')
dphiidx = varlist_.index('DPhiMhtDt')
mvaidx  = varlist_.index('LeadTrkMva')
ismuidx = varlist_.index('IsMuMatched')
drjidx = varlist_.index('DrJetDt')

kappabinIdx = varlist_.index(varname_kappaBinning)
thetabinIdx = varlist_.index(varname_thetaBinning)


regionkeys = regionCuts.keys()
for key in regionkeys:

	#for prompt measurement
	newlist2 = list(regionCuts[key])
	newlist2[drjidx] = (0.1,inf)
	if 'Short' in key: 
		newlist2[mvaidx] = (mvaPromptShortLoose,inf)
		newlist2[mcalidx] = (calmShort,calhShort)
	else: 
		newlist2[mvaidx] = (mvaPromptLongLoose,inf)
		newlist2[mcalidx] = (calmLong,calhLong)
	newkey = key+'CaloSideband'
	regionCuts[newkey] = newlist2

	newlist1 = list(regionCuts[key])
	#newlist1[dphiidx] = (TMath.Pi()*1./2,3.2)
	#newlist1[dphiidx] = (TMath.Pi()*1./3,inf)
	#newlist1[dphiidx] = (-inf,inf)	
	if 'Short' in key: 
		#newlist1[mcalidx] = (0,10)
		newlist1[mvaidx] = (mvaFakeShortLoose,mvaFakeShortMedium)#using prompt cut here
	else: 	
		newlist1[mvaidx] = (mvaFakeLongLoose,mvaFakeLongMedium)	
		#newlist1[mcalidx] = (0,10)
	newkey = key+'FakeCr'
	regionCuts[newkey] = newlist1

	newlist0 = list(regionCuts[key])
	#newlist0[dphiidx] = (TMath.Pi()*1./2,3.2)
	newlist0[ismuidx] = (1,1)
	newlist0[drjidx] = (0,inf)
	newkey = key+'RecoMuMatched'
	regionCuts[newkey] = newlist0	



#zonebinning = [0.0,99]

print 'dedxidx, srindex', dedxidx, srindex

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
hEtaVsPhiDT = {}
for region in regionCuts:
	histname = 'Track'+region+'_'+'EtaVsPhiDT'
	hEtaVsPhiDT[region] = TH2F(histname,histname,180,-3.2,3.2,170,-2.5,2.5)# need to try this
	for var in varlist_:
		histname = 'Prompt'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Fake'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)


print 'regionCuts', regionCuts


def getBinNumber(fv, binnumberdict=binnumbers, omitidx=-1):
	for binkey in binnumberdict:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if iwindow==omitidx: continue
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumberdict[binkey]
	return -10



ftrig = TFile(os.environ['CMSSW_BASE']+'/src/analysis/triggerefficiency/susy-trig-plots.root')#triggersRa2bRun2_v4_withTEffs.root')
ttrig = ftrig.Get('tEffhMetMhtRealXMht;1')
#tEffhMetMhtRealXMht_run2;1
#susy-trig-plots_amag.root
hpass = ttrig.GetPassedHistogram().Clone('hpass')
htotal = ttrig.GetTotalHistogram().Clone('htotal')
gtrig = TGraphAsymmErrors(hpass, htotal)

c = TChain("TreeMaker2/PreSelection")
for ifile, f in enumerate(inputFiles):
	if ifile>nfpj: break
	print 'adding file:', f
	c.Add(f)

nentries = c.GetEntries()

if maketree:
	fnew.mkdir('TreeMaker2')
	fnew.cd('TreeMaker2/')
	try: 
		c.SetBranchStatus('HLTElectronObjects', 0)

	except:
		pass
	tree_out = c.CloneTree(0)	

#c.Show(0)

c.GetEntry(0)


thisfile = ''

ncuts = 24
def selectionFeatureVector(fvector, regionkey='', omitcuts='', verbose=False):
	if not fvector[0]>=fvector[1]: 
		if verbose: print 'first thing screwed it up'
		return False
	iomits = []
	if not omitcuts=='':
		for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i>=ncuts: continue
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
			if verbose: print 'this is what screwed it up', i, regionkey, feature
			return False
	return True


if 'TTJets_TuneC' in inputFileNames:  madranges = [(0,600)]
elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneC' in inputFileNames: madranges = [(0, 100)]
elif 'WJetsToLNu_HT' in inputFileNames: madranges = [(100, inf)]
elif 'DYJetsToLL_M-50_Tune' in inputFileNames: madranges = [(0, 100)]
elif 'DYJetsToLL_M-50_HT' in inputFileNames: madranges = [(100, inf)]
else: madranges = [(0, inf)]



#madranges = [(0, inf)]


if 'MET' in inputFileNames: 
	trigkey = 'MhtMet6pack'
	ismu = False
	isel = False
	ismet= True	
	isjetht = False	
elif 'SingleMu' in inputFileNames: 
	trigkey = 'SingleMuon'
	ismu = True
	isel = False
	ismet= False	
	isjetht = False	
elif 'SingleEl' in inputFileNames or 'EGamma' in inputFileNames: 
	trigkey = 'SingleElectron'
	ismu = False
	isel = True
	ismet= False	
	isjetht = False	
elif 'JetHT' in inputFileNames: 
	trigkey = 'HtTrain'
	ismu = False
	isel = False
	ismet= False
	isjetht = True

#fMask = TFile('usefulthings/Masks.root')
#fMask = TFile('usefulthings/Masks_mcal25to40.root')


#fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to13.root')
#hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')

####should be this## if isdata:  fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal13to30_Data2016.root')
if isdata:  fMask = TFile('usefulthings/Masks_mcal13to30_Data2016.root')
else: fMask = TFile('usefulthings/Masks_mcal13to30_MC2016.root')	

hMask = fMask.Get('h_Mask_allyearsLongBaseline_EtaVsPhiDT')#this is the sum of long and short mht sideband

if exomode: hMask = ''
if deriveMask: hMask = ''



print 'using mask', hMask
#safe for FS report:
#nov20-noEdep

import os
if phase==0:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'	
else:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'	

readerPixelOnly = TMVA.Reader("")
readerPixelOnly.SetName('Reader1')
readerPixelStrips = TMVA.Reader("")
readerPixelStrips.SetName('Reader2')

print 'going to process', pixelXml
prepareReaderPixel_fullyinformed(readerPixelOnly, pixelXml)

print 'going to process', pixelstripsXml
prepareReaderPixelStrips_fullyinformed(readerPixelStrips, pixelstripsXml)



#prepareReaderPixelStrips(readerPixelStrips, pixelstripsXml)
#prepareReaderPixel(readerPixelOnly, pixelXml)


import time
t1 = time.time()
i0=0

runs = {}
lastlumi = -1
lastrun = -1



print nentries, 'events to be analyzed'
for ientry in range(nentries):

	#print 'now processing event number', ientry, 'of', nentries
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]
			print 'going to process', nentries, 'events'


	#if not ientry>7200: continue

	#print 'here we are', ientry
	if isSkimRun2017DSingleMu:
		if ientry in [1663,1664,1665,1666,1667]: continue
		#if ientry> 1663 and ientry<1700: continue
	c.GetEntry(ientry) 
	#waters = 0
	if debugmode:
		if not ientry in [566]: continue
		print 'taking a close look at event', ientry
	if ientry%1000==0:
		if not (thisfile==c.GetFile().GetName()):
			thisfile = c.GetFile().GetName()
			print 'starting new file', thisfile

	if isdata:
		runnum = c.RunNum
		lumisec = c.LumiBlockNum
		if runnum!=lastrun:
			if runnum not in runs:
				runs[runnum] = []
		if lumisec!=lastlumi:
			if lumisec not in runs[runnum]:
				runs[runnum].append(lumisec)	
		hHt.Fill(c.HTOnline)
		if not PassTrig(c, trigkey): continue
	else:	
	  hHt.Fill(c.madHT)
	  isValidHtRange = False
	  for madrange in madranges:
		if (c.madHT>=madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	  if not isValidHtRange: continue#####this should be changed/fixed in Prompt code	

	#if not c.JetID: continue

	if isdata: 
		if not passesUniversalDataSelection(c): continue
	else: 
		if not passesUniversalSelection(c): continue


	disappearingTracks = []    
	fakecrTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if verbose: print itrack, 'no selection at all', track.Pt(), 'eta', track.Eta()        
		if not track.Pt() > 10 : continue
		#if not abs(track.Eta()) < 2.4: continue
		#if not abs(track.Eta()) < 2.2: continue
		#if not abs(track.Eta()) < 2.1: continue####what has been lookin' good
		if not abs(track.Eta()) < 2.0: continue	
		#if not abs(track.Eta()) < 1.8: continuew		
		##if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue    #I kind of want to drop this eventually
		if verbose: print itrack, 'before baseline pt', track.Pt(), 'eta', track.Eta()        

		

		if not isBaselineTrackLoosetag(track, itrack, c, hMask): continue		
	
		if verbose: print itrack, 'pt', track.Pt(), 'eta', track.Eta()


		if not (track.Pt() > candPtCut): continue    
		if verbose: print ientry, itrack, 'basic track!', track.Pt()
		dtstatus, mva = isDisappearingTrack_FullyInformed(track, itrack, c, readerPixelOnly, readerPixelStrips, [mvaminShort,mvaminLong], vtx_calibs)
		if verbose: print ientry, itrack, 'mva results were:', dtstatus, mva
		if exomode:
			if not passesExtraExoCuts(track, itrack, c): continue
	
		if dtstatus==0: continue
		

		if verbose: print ientry, itrack, 'still got this', track.Pt()


		drlep = 99
		islep = False
		for ilep, lep in enumerate(list(c.Electrons)+list(c.TAPPionTracks)): #+list(c.Muons)
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.1: 
				islep = True
				break            
		if islep: continue 
		dtisrecomu = False	
		for ilep, lep in enumerate(list(c.Muons)):
			dr = lep.DeltaR(track)
			if dr<0.1: 
				dtisrecomu = True
				break
			
	
		#if dtisrecomu: print ientry, itrack, 'we do in fact happen to have a muon situation'
		dtisrecomu = dtisrecomu and not (bool(c.tracks_passPFCandVeto[itrack]))
			

		isjet = False
		if dtstatus==1: ##short track
			jt = 30
			drcut=0.4
		else: 
			jt = 30
			drcut=0.4
		for jet in c.Jets:
			if (jet.Pt()>jt and jet.DeltaR(track)<drcut):
				isjet = True
				break
			#elif jet.Pt()>10 and jet.DeltaR(track)<0.05:
			#	isjet = True
			#	break
		#if isjet: 
		#	continue
		#if not c.tracks_trackJetIso[itrack]>0.3: continue###this is the new temp jet iso, huh?
		#if abs(dtstatus)==1: isjet = bool(c.tracks_trackJetIso[itrack]<0.5)
		#if abs(dtstatus)==2: isjet = bool(c.tracks_trackJetIso[itrack]<0.4)		
		
		dtisrecomu = dtisrecomu and isjet
		if isjet and not dtisrecomu: continue
		if not (c.tracks_passPFCandVeto[itrack] or dtisrecomu): continue
		
		if blockhem: 
			if -3.2<track.Eta() and track.Eta()<-1.2 and -1.77<track.Phi() and track.Phi()<-0.67: continue
		if partiallyblockhem:
			if c.RunNum>=319077:
				if -3.2<track.Eta() and track.Eta()<-1.2 and -1.77<track.Phi() and track.Phi()<-0.67: 
					continue		
									
		if abs(dtstatus)==1: nShort+=1
		if abs(dtstatus)==2: nLong+=1         
		if verbose: print ientry, itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta(), dtstatus   

		if abs(track.Eta())<1.5: dedxcalib = dedxcalib_barrel
		else: dedxcalib = dedxcalib_endcap

		if exomode:
			if not track.Pt()>55: continue
			if not abs(track.Eta())<2.1: continue
			if not (abs(track.Eta())<0.15 or abs(track.Eta())>0.35): continue
			if not (abs(track.Eta())<1.42 or abs(track.Eta())>0.65): continue
			if not (abs(track.Eta())<1.55 or abs(track.Eta())>1.85): continue        	
		#print 'ientry', ientry, 'found disappearing track w mva =', mva, dtstatus, 'c.RunNum', c.RunNum, 'c.LumiBlockNum',c.LumiBlockNum
		dedx = dedxcalib*c.tracks_deDxHarmonic2pixel[itrack]
	
		if not isdata and doDedxSmear:
			if abs(track.Eta())< 1.5: smearfactor = fsmear_barrel.GetRandom()
			else: smearfactor = fsmear_endcap.GetRandom()
			dedx = dedx + smearfactor
			
	
		#if track.Eta()>-0.94 and track.Eta()<-0.88 and track.Phi()>2.95 and track.Phi()<3.06: continue
		#if track.Eta()>1.7 and track.Eta()<1.77 and track.Phi()>0.71 and track.Phi()<0.82: continue		
	
		disappearingTracks.append([track,dtstatus,dedx, mva, dtisrecomu, c.tracks_nMissingOuterHits[itrack], itrack])


	if not len(disappearingTracks)>=1: continue

	if maketree:
		#print 'filling tree', ientry
		tree_out.Fill()


	genels = []
	genmus = []
	genpis = []		
	if ClosureMode:
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not c.GenParticles_Status[igp] == 1: continue        
			#if not abs(c.GenParticles_ParentId[igp]) == 24: continue
			if abs(c.GenParticles_PdgId[igp])==11: genels.append(gp)
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append(gp)            
		for igp, gp in enumerate(c.GenTaus_LeadTrk):
			if not gp.Pt()>5: continue
			if not abs(gp.Eta())<2.4: continue
			if not bool(c.GenTaus_had[igp]): continue
			##if not c.GenTaus_NProngs[igp]==1: continue###
			#print igp, 'found tau', bool(c.GenTaus_had[igp])==True, 'nprongs', c.GenTaus_NProngs[igp]
			#print 'isoPionTracks', c.isoPionTracks
			genpis.append(gp)

	'''		
	for dt in disappearingTracks:
		track = dt[0]
		itrack = dt[-1]
		if isMatched2(track, genels, 0.02):
			print ientry, '---->is electron'
		elif isMatched2(track, genmus, 0.02):
			print ientry, '---->is muon'		
		elif isMatched2(track, genpis , 0.02):
			print ientry, '---->is pi'
			for igp, gp in enumerate(c.GenTaus_LeadTrk):
				print igp, bool(c.GenTaus_had[igp]==True), c.GenTaus_NProngs[igp] 
		else:
			print 'is fake'			
	'''
	RecoElectrons = []
	for ilep, lep in enumerate(c.Electrons):
		if not lep.Pt()>30: continue
		if debugmode: print ientry, ilep, 'ele with Pt' , lep.Pt()
		if not lep.DeltaR(disappearingTracks[0][0])>0.03: continue
		#if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_tightID[ilep]: continue
		if debugmode: print ilep, 'passed that nice tight id'
		if blockhem: 
			if -3.2<lep.Eta() and lep.Eta()<-1.2 and -1.77<lep.Phi() and lep.Phi()<-0.67: continue
		if partiallyblockhem:
			if c.RunNum>=319077:
				if -3.2<lep.Eta() and lep.Eta()<-1.2 and -1.77<lep.Phi() and lep.Phi()<-0.67: 
					continue
		RecoElectrons.append([lep, ilep])


	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if not lep.Pt()>30: continue
		if not lep.DeltaR(disappearingTracks[0][0])>0.1: continue
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		#if (abs(lep.Eta()) > 1.4442 and abs(lep.Eta()) < 1.566): continue
		if not abs(lep.Eta())<2.4: continue
		if debugmode: print ientry, ilep, 'mu with Pt testing' , lep.Pt(), bool(c.Muons_passIso[ilep]), bool(c.Muons_mediumID[ilep]), lep.Eta()
		if not bool(c.Muons_passIso[ilep]): continue
		if debugmode: print ientry, ilep, 'mu with Pt' , lep.Pt(), c.Muons_MiniIso[ilep]
		if not bool(c.Muons_mediumID[ilep]): continue
		if debugmode: print ientry, ilep, 'mu with Pt' , lep.Pt()
		#if not lep.Pt()>40: continue
			#print 'promoted!'
		RecoMuons.append([lep,ilep])
		

	#if not len(RecoMuons)==c.NMuons: continue
	#if not len(RecoElectrons)==c.NElectrons: continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region

	if isdata: 
		weight = 1   
		if ismet: 
			if not (len(RecoElectrons)+len(RecoMuons)==0): continue
			if not c.MHT>150: continue
		if ismu: 
			if not (len(RecoMuons)>0 and len(RecoElectrons)==0): 
				continue
		if isel: 
			if not (len(RecoElectrons)>0): continue
		if isjetht:
			if not (c.MHT<150): continue
			if not (len(RecoMuons)==0 and len(RecoElectrons)==0): continue
	else:
		if analyzeskims: 
			#wof = c.weight
			wof = c.puWeight
		else: wof = c.CrossSection
		if len(RecoElectrons)+len(RecoMuons)>0: 
			weight = 0.9*wof#*c.puWeight
		else: 
			weight = wof#*gtrig.Eval(c.MHT)#*c.puWeight

	if isdata: hHtWeighted.Fill(c.HTOnline,weight)
	else: hHtWeighted.Fill(c.madHT,weight)	



	dt, status, dedxPixel, mvascore, dtisrecomu, MOH, itrack = disappearingTracks[0]
	#print ientry, 'DT stuff dt, status, dedxPixel ', dt, status, dedxPixel 
	isPromptEl = isMatched2(dt, genels, 0.1)
	isPromptMu = isMatched2(dt, genmus, 0.1)
	isPromptPi = isMatched2(dt, genpis, 0.1)
	if isdata or issignal: isPromptEl, isPromptMu, isPromptPi, isfake = True, True, True, True
	else: isfake = not (isPromptEl or isPromptMu or isPromptPi)


	##if isPromptPi: continue
	#if not isfake: continue
	##if isPromptEl: continue
	#if (isPromptEl or isPromptMu or isPromptPi): continue
	#if isPromptMu: continue
	#if not isPromptPi: continue

	#if not isdata:
		#if isPromptPi: continue
		#if isPromptMu: continue
	#	if isPromptEl: continue

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
		if not abs(jet.Eta())<2.5: continue###update to 2.4            
		adjustedJets.append(jet)			
		if c.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1
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
		phi = dt.Phi()
			
	log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74))
	if log10dedxmass!=log10dedxmass: log10dedxmass = -10	

	newmetvec = metvec.Clone()
	newmetvec-=dt
	if len(RecoElectrons)>0: 
		#mT = c.Electrons_MTW[RecoElectrons[0][1]]
		mT = TMath.Sqrt(2*RecoElectrons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoElectrons[0][0].DeltaPhi(adjustedMht))))
		dt__ = dt.Clone()
		#dt__*=adjustedMht.Pt()/dt.Pt()*TMath.Cos(dt.DeltaPhi(adjustedMht))
		DrJetDt = abs(RecoElectrons[0][0].DeltaR(dt__))
		mtautau = mttsam1(newmetvec, RecoElectrons[0][0], dt__)
		if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt__).M()
		else: invmass = 999		
		leppt = RecoElectrons[0][0].Pt()
	elif len(RecoMuons)>0: 
		#mT = c.Muons_MTW[RecoMuons[0][1]]
		mT = TMath.Sqrt(2*RecoMuons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoMuons[0][0].DeltaPhi(adjustedMht))))
		dt__ = dt.Clone()
		DrJetDt = abs(RecoMuons[0][0].DeltaR(dt__))
		mtautau = mttsam1(newmetvec, RecoMuons[0][0], dt__)
		#dt__*=adjustedMht.Pt()/dt.Pt()*TMath.Cos(dt.DeltaPhi(adjustedMht))		
		if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoMuons[0][0]+dt__).M()
		else: invmass = 999
		leppt = RecoMuons[0][0].Pt()
	else: 
		mT = 999
		invmass = 999
		DrJetDt = 999
		mtautau = 999
		leppt = 999


	DrJetDt = c.tracks_trackJetIso[itrack]

	#DrJetDt = 999	
	#for ijet, jet in enumerate(c.Jets):
	#		if not jet.Pt()>15: continue			
	#		if not abs(jet.Eta())<2.5: continue###update to 2.4	
	#		#if not c.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: continue
	#		DrJetDt = min(DrJetDt,jet.DeltaR(dt))

	matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#/TMath.CosH(c.tracks[disappearingTracks[0][-1]].Eta())
	#matchedcalo = c.tracks_matchedCaloEnergyJets[disappearingTracks[0][-1]]

	#if abs(disappearingTracks[0][1])==1: matchedcalofrac = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#only do it for long tracks
	##matchedcalofrac = 100*matchedcalo/(dt.P())
	#matchedcalofrac = 100*c.tracks_chargedPtSum[disappearingTracks[0][-1]]/(dt.Pt())


	if abs(disappearingTracks[0][1])==1: 
		matchedcalofrac = matchedcalo # max(matchedcalo,100*matchedcalo/(dt.P()))#100*matchedcalo/(dt.P())#test same as long# matchedcalo #short
	else: matchedcalofrac = 100*matchedcalo/(dt.P())#long

	dphiMhtDt = abs(adjustedMht.DeltaPhi(dt))
	mhtWithTrack = adjustedMht.Clone()
	mhtWithTrack-=dt
	mtDtMht = TMath.Sqrt(2*dt.Pt()*mhtWithTrack.Pt()*(1-TMath.Cos(mhtWithTrack.DeltaPhi(dt))))
	#to do: could try to do overlap removal between jets and leptons
#varlist_   = ['Ht',     'Mht',           'NJets',                                           'BTags',         'NTags',      'NPix','NPixStrips','MinDPhiMhtJets','DeDxAverage','NElectrons', 'NMuons','InvMass', 'LepMT','TrkPt','TrkEta','MatchedCalo','IsMuMatched', 'DtStatus', 'DPhiMhtDt',   'LeadTrkMva', 'MtDtMht',  'MissingOuterHits',  'LepPt',  'DrJetDt', 'BinNumber','MinDPhiMhtHemJet','MTauTau','Log10DedxMass']#]#'Log10DedxMass'
	fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets-len(RecoElectrons)-len(RecoMuons),adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta, matchedcalofrac,          dtisrecomu, status, dphiMhtDt,             mvascore,    mtDtMht,         MOH,          leppt, DrJetDt]#'''*TMath.CosH(eta)
	fv.append(getBinNumber(fv))
	fv.extend([GetMinDeltaPhiMhtHemJets(adjustedJets,adjustedMht),mtautau,log10dedxmass])

	#print 'invmass', invmass
	#print fv
	if isPromptMu:
		br = getBinNumber(fv)
		if br==21 or br==23: 
			print ientry, "got ourselves a muon thingy", fv, c.GetFile().GetName()
	if turnoffpred:
		FR, PR = 1.0, 1.0
	else:
		if abs(disappearingTracks[0][1])==1: 
			FR = getfakerate(fv[thetabinIdx], hfrshort)
			PR = getpromptrate(fv[kappabinIdx], hprshort)/2.0
			MR = getpromptrate(fv[kappabinIdx], hmrshort)
			#PR = getpromptrate(fv[kappabinIdx], hprshort)/2.0		
			PRfcr = getpromptrate(fv[kappabinIdx], hprshort)
			FRpcr = 1.0
		if abs(disappearingTracks[0][1])==2: 
			FR = getfakerate(fv[thetabinIdx], hfrlong)
			PR = getpromptrate(fv[kappabinIdx], hprlong)
			MR = getpromptrate(fv[kappabinIdx], hmrlong)			
			PRfcr = getpromptrate(fv[kappabinIdx], hprlong)
			FRpcr = 1.0
		
	for regionkey in regionCuts:
		###if 'MhtSideband' in regionkey and (not isdata): weight_ = weight/gtrig.Eval(c.MHT)
		#turning off trigger december 22##else: weight_ = weight
		weight_ = weight
		if selectionFeatureVector(fv,regionkey):  
			fillth2(hEtaVsPhiDT[regionkey], phi, dt.Eta())
		if deriveMask: continue
		for ivar, varname in enumerate(varlist_):
			if selectionFeatureVector(fv,regionkey,varname):
				if True:
				   #if 'ShortBin23' in regionkey and not ('Sideband' in regionkey or 'FakeCr' in regionkey) and getBinNumber(fv)==23 and varname=='BinNumber':
				   if 'ShortHighMetBaseline' in regionkey and not ('Sideband' in regionkey or 'FakeCr' in regionkey) and adjustedMht.Pt()>450 and mvascore>0.1: 
						print 'precious!'
						c.Show(ientry)
						print 'dump out gen particles'
						if not isdata:
						  for igen, gp in enumerate(c.GenParticles):
							if not gp.Pt()>10: continue
							print igen, c.GenParticles_PdgId[igen], 'dr =', dt.DeltaR(gp), 'pt =', gp.Pt()
						for ifv in range(len(fv)): print varlist_[ifv], fv[ifv]
						print c.GetFile()
						print ientry, 'got something suspicious', 'Fake'+regionkey
						print 'isPromptEl, isPromptMu, isPromptPi', isPromptEl, isPromptMu, isPromptPi
						ntrks = len(c.tracks)
						for br in c.GetListOfBranches():
							bname = br.GetName()
							if not ("tracks_" in bname or 'Quality' in bname): continue
							if 'pass' in bname or 'Quality' in bname:
								print 'bname', bname, bool(getattr(c,bname)[itrack])
							else:
								print 'bname', bname, getattr(c,bname)[itrack]
									
				if (isPromptEl or isPromptMu or isPromptPi): 
				
					fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Truth, fv[ivar], weight_)####
					if not turnoffpred: 
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method1,fv[ivar], FR*weight_)
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method2,fv[ivar], PR*weight_)
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method3,fv[ivar], MR*weight_)
						#fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method3,fv[ivar], PRfcr*FR*weight_)						
				if isfake:
					#print 'filling something with weight', weight_, 'Fake'+regionkey+'_'+varname
					fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,   fv[ivar], weight_)
					if not turnoffpred: 
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method1,  fv[ivar], FR*weight_)							
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method2,  fv[ivar], PR*weight_)
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method3,  fv[ivar], MR*weight_)						
						#fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method3,  fv[ivar], PR*FR*weight_)								



fnew.cd()
hHt.Write()
hHtWeighted.Write()

writeHistoStruct(histoStructDict, 'truthmethod1method2method3')
for key_ in hEtaVsPhiDT: hEtaVsPhiDT[key_].Write()

if maketree and not analyzeskims:
	fnew.cd('TreeMaker2/')
	tree_out.Write()


if isdata:
	if len(runs) > 0:
		runs_compacted = {}
		for run in runs:
			if run not in runs_compacted:
				runs_compacted[run] = []
			for lumisec in runs[run]:
				if len(runs_compacted[run]) > 0 and lumisec == runs_compacted[run][-1][-1]+1:
					runs_compacted[run][-1][-1] = lumisec
				else:
					runs_compacted[run].append([lumisec, lumisec])

		json_content = json.dumps(runs_compacted)
		with open(fnew.GetName().replace(".root", ".json"), "w") as fo:
			fo.write(json_content)


print 'just created', fnew.GetName()
fnew.Close()
