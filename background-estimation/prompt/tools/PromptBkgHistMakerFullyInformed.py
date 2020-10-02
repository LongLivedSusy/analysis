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
####gROOT.SetBatch(1)
from code import interact
import collections

execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False 


listOfEventNumbers = []

turnoffpred = True

maketree = True

codeproduct = sys.argv[0].split('/')[-1].split('With')[0].split('Maker')[0]
defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_50000-3*.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_78_RA2AnalysisTree.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-gk", "--useGenKappa", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-ps", "--processskims", type=str, default='False',help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
args = parser.parse_args()
nfpj = args.nfpj
processskims = bool(args.processskims=='True')
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
analyzer = args.analyzer
pileup = args.pileup
useGenKappa = args.useGenKappa
verbosity = args.verbosity
print 'useGenKappa =', useGenKappa

maketree = bool(not processskims)

if inputFileNames=='skimRun2017B-SingleElectron.root':
	need2skip =-1#that didn't work1102
else: need2skip = -1


genMatchEverything = False
RelaxGenKin = True
ClosureMode = True #false means run as if real data
UseFits = False
UseJets_bJetTagDeepCSVBvsAll = True
sayalot = False
candPtCut = 30
candPtUpperCut = 6499




verbose = False


isdata = 'Run201' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames or 'aksingh' in inputFileNames: 
	is2016, is2017, is2018, year = True, False, False, '2016'
elif 'Run2017' in inputFileNames or 'Fall17' in inputFileNames: 
	is2016, is2017, is2018, year = False, True, False, '2017'
elif 'Run2018' in inputFileNames or 'Autumn18' in inputFileNames or 'somthin or other' in inputFileNames: 
	is2016, is2017, is2018, year = False, True, True, '2018'

if is2016: phase = 0
else: phase = 1

if is2016: BTAG_deepCSV = 0.6324
if is2017: BTAG_deepCSV = 0.4941
if is2018: BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV


if phase==0: mvathreshes=[.1,.25]
else: mvathreshes=[0.15,0.0]

print 'phase', phase

if isdata: ClosureMode = False


if not turnoffpred:
	if isdata:  ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'_cute.root')
	else: ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'.root')
	hfrlong = ffakerate.Get('hfrlong')
	hfrshort = ffakerate.Get('hfrshort')	

	if isdata:  fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'_cute.root')
	else: fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'.root')

	hprshort = fpromptrate.Get('hprshort')
	hprlong = fpromptrate.Get('hprlong')

	fakeax = hfrlong.GetXaxis()
	promptax = hprlong.GetXaxis()


def getfakerate(ht, hfr):
	#return 2.0
	return hfr.GetBinContent(fakeax.FindBin(ht))

def getpromptrate(obs, hpr):
	return hpr.GetBinContent(promptax.FindBin(abs(obs)))

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
print 'Identifier', identifier


calib_version = '-SingleMuon'
calib_version = ''# Sang-Il's new key names
if 'Run20' in identifier: 
	keyforcalibs = identifier.split('-')[0].replace('skims','').replace('skim','')+calib_version
	dedxcalib_barrel = Dedxcalibdict_Muon_barrel[keyforcalibs]
	dedxcalib_endcap = Dedxcalibdict_Muon_endcap[keyforcalibs]
elif 'Summer16' in identifier: 
	dedxcalib_barrel = Dedxcalibdict_Muon_barrel['Summer16']
	dedxcalib_endcap = Dedxcalibdict_Muon_endcap['Summer16']
elif 'Fall17' in identifier: 
	dedxcalib_barrel = Dedxcalibdict_Muon_barrel['Fall17']
	dedxcalib_endcap = Dedxcalibdict_Muon_endcap['Fall17']
else: 
	dedxcalib_barrel = 1.0
	dedxcalib_endcap = 1.0	

#dedxcalib = 1.0

newfname = codeproduct+'_'+identifier+'.root'
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])
moreargs = moreargs.replace(' ','').replace('--','-')
newfname = newfname.replace('.root',moreargs+'.root')
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

inf = 999999

calm = 20
calh = 25

calm = 25
calh = 40

calm = 10
calh = 15

calm = 10
calh = 13

calm = 13
calh = 27

calm = 13
calh = 35

calm = 15
calh = 25

calm = 15
calh = 25

calm = 15
calh = 22

calm = 17
calh = 27

call = 12
calm = 12
calh = 80


lowht = 0
lowdphi, hidphi = 0.0,3.2
#lowdphi, hidphi = 0.0,1.0
#hihidphi = hidphi#hihidphi = 3.14159-1
hihidphi = 3.14159*2/3


#lowlowmva = 0.0
lowlowmva = -0.1
lowmva, himva = 0.13, inf

regionCuts = {}
varlist_                                           = ['Ht',       'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',  'MatchedCalo', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'BinNumber', 'MinDPhiMhtHemJet','Met','Log10DedxMass']
regionCuts['Baseline']                            = [(lowht,inf),   (30,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),   (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf),  (120,inf), (110,inf), (candPtCut,inf), (0,2.4),     (0,call),   (0,inf),   (lowdphi,hidphi), (lowmva,himva)]
if processskims:
	##regionCuts['ShortLowMhtBaseline']              = [(lowht,inf), (100,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),      (1,1),    (lowdphi,hidphi), (lowmva,himva)]
	#varlist_                                     = ['Ht',         'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo', 'DtStatus',  'BinNumber', 'Met']
	##regionCuts['ShortBaseline']                    = [(lowht,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf), (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (1,1),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['ShortHadBaseline']                 = [(lowht,inf),(150,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0 ),    (0,0),   (0,inf),   (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (1,1),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['ShortSMuBaseline']                 = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0 ),    (1,inf), (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (1,1),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['ShortSElBaseline']                 = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,inf ),  (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (1,1),    (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['ShortSElValidationZLL']            = [(0,inf),     (0,inf),  (0,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,inf ),  (0,0),     (70,110),   (0,inf),  (candPtCut,inf), (0,2.4), (0,call),      (1,1),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['ShortSElValidationMT']             = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,1 ),    (0,0),     (110,inf),  (0,95),   (candPtCut,inf), (0,2.4), (0,call),    (1,1),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['ShortSElValidationMTLowMass']      = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,1 ),    (0,0),     (0,60),     (0,95),   (candPtCut,inf), (0,2.4), (0,call),       (1,1),      (lowdphi,hidphi), (lowmva,himva)]	
	regionCuts['ShortSMuValidationMT']             = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0),     (1,1),     (110,inf),  (0,95),   (candPtCut,inf), (0,2.4), (0,call),      (1,1),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['ShortHadMhtSideband']              = [(lowht,inf), (0,50),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (dedxcutLow,inf),         (0,0),   (0,0),       (110,inf),  (0,inf),  (candPtCut,inf), (0,2.4), (0,call),      (1,1),     (lowdphi,hidphi), (lowmva,himva)]
	#varlist_                                       = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons', 'NMuons',    'InvMass', 'LepMT',       'TrkPt',  'TrkEta',  'MatchedCalo', 'DtStatus',     'BinNumber', 'Met']
	##regionCuts['LongBaseline']                     = [(lowht,inf), (30,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (2,2),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['LongLowMhtBaseline']               = [(lowht,inf), (100,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (2,2),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['LongHadBaseline']                  = [(lowht,inf),(150,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0 ),    (0,0),    (0,inf),   (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (2,2),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['LongSMuBaseline']                  = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0 ),    (1,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (2,2),    (lowdphi,hidphi), (lowmva,himva)]
	##regionCuts['LongSElBaseline']                  = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,inf ),  (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,call),     (2,2),    (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['LongSElValidationZLL']             = [(0,inf),     (0,inf),  (0,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,inf ),  (0,0),      (70,110),  (0,inf),  (candPtCut,inf), (0,2.4), (0,call),      (2,2),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['LongSElValidationMT']              = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,1 ),    (0,0),      (110,inf), (0,95),   (candPtCut,inf), (0,2.4), (0,call),      (2,2),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['LongSElValidationMTLowMass']       = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (1,1 ),    (0,0),      (0,60),    (0,95),   (candPtCut,inf), (0,2.4), (0,call),      (2,2),        (lowdphi,hidphi), (lowmva,himva)]	
	regionCuts['LongSMuValidationMT']              = [(lowht,inf), (30,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0),     (1,1),      (110,inf), (0,95),   (candPtCut,inf), (0,2.4), (0,call),      (2,2),      (lowdphi,hidphi), (lowmva,himva)]
	regionCuts['LongHadMhtSideband']               = [(lowht,inf), (0,50),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),   (dedxcutLow,inf),         (0,0),     (0,0),      (110,inf), (0,inf), (candPtCut,inf), (0,2.4), (0,call),      (2,2),     (lowdphi,hidphi), (lowmva,himva)]
#varlist_                                       = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo',      'DtStatus',    'BinNumber', 'Met']

dedxidx = varlist_.index('DeDxAverage')
srindex = varlist_.index('BinNumber')
mcalidx = varlist_.index('MatchedCalo')
statidx = varlist_.index('DtStatus')
dphiidx = varlist_.index('DPhiMhtDt')
mvaidx = varlist_.index('LeadTrkMva')

regionkeys = regionCuts.keys()
for key in regionkeys:

	newlist1 = list(regionCuts[key])
	###newlist1[statidx] = (-regionCuts[key][statidx][1],-regionCuts[key][statidx][0])#commenting this says ditch old fake CR
	newlist1[dphiidx] = (hihidphi,3.2)
	newlist1[mvaidx] = (lowlowmva,lowmva)	
	newkey = key+'FakeCr'
	regionCuts[newkey] = newlist1


	newlist2 = list(regionCuts[key])
	newlist2[mcalidx] = (calm,calh)
	newlist2[dphiidx] = (0,3.2)
	newlist2[mvaidx] = (lowmva,99)		
	newkey = key+'CaloSideband'
	regionCuts[newkey] = newlist2

	newlist3 = list(regionCuts[key])
	newlist3[mcalidx] = (calm,calh)
	###newlist3[statidx] = (-regionCuts[key][statidx][1],-regionCuts[key][statidx][0])#commenting this says ditch old fake CR
	newlist3[dphiidx] = (hihidphi,3.2)
	newlist3[mvaidx] = (lowlowmva,lowmva)	
	newkey = key+'CaloSidebandFakeCr'
	regionCuts[newkey] = newlist3	



#zonebinning = [0.0,99]

print 'dedxidx, srindex', dedxidx, srindex

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
hEtaVsPhiDT = {}
for region in regionCuts:
	histname = 'Track'+region+'_'+'EtaVsPhiDT'
	hEtaVsPhiDT[region] = TH2F(histname,histname,180,-3.2,3.2,170,-2.5,2.5)# need to try this
	hEtaVsPhiDT[region+'_tel'] = TH2F(histname+'_tel',histname+'_tel',180,-3.2,3.2,170,-2.5,2.5)# need to try this	
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
	if ifile>=nfpj: break
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
	#tree_out.SetBranchStatus('tracks', 0)

	tracksAUX = ROOT.std.vector('TLorentzVector')()
	#tree_out.Branch('thingies', tracksAUX)
	print 'test done'

c.Show(0)

c.GetEntry(0)


thisfile = ''
nentries = 10000

ncuts = 19
def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
	if not fvector[0]>=fvector[1]: return False
	iomits = []
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i>=ncuts: continue
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
			return False
	return True


if 'TTJets_TuneCUET' in inputFileNames:  madranges = [(0,600)]
elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneCUET' in inputFileNames: madranges = [(0, 100)]
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



fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to13.root')
hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')

hMask = ''

import os
if phase==0:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml'	

else:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml'	

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


	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]
			print 'going to process', nentries, 'events'

	c.GetEntry(ientry) 

	if debugmode:
		if not c.EvtNum in [108101]: continue
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



	basicTracks = []
	disappearingTracks = []    
	fakecrTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if verbose: print itrack, 'no selection at all', track.Pt(), 'eta', track.Eta()        
		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		##if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue    #I kind of want to drop this eventually
		if verbose: print itrack, 'before baseline pt', track.Pt(), 'eta', track.Eta()        
		#if not isBaselineTrack(track, itrack, c, hMask): continue
	
	
	
		if not isBaselineTrackLoosetag(track, itrack, c, hMask): continue		
	
	
	
			
		if verbose: print itrack, 'pt', track.Pt(), 'eta', track.Eta()
		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut): continue     # and track.Pt()<candPtUpperCut
		if verbose: print ientry, itrack, 'basic track!', track.Pt()
		dtstatus, mva = isDisappearingTrack_FullyInformed(track, itrack, c, readerPixelOnly, readerPixelStrips)
		if verbose: print ientry, itrack, 'mva results were:', dtstatus, mva
		if dtstatus==0: continue
		if verbose: print ientry, itrack, 'still got this', track.Pt()
		
	
		drlep = 99
		islep = False
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.1: 
				islep = True
				break            
		if islep: continue 
		if verbose: print ientry, 'passeslepton'
		isjet = False
		for jet in c.Jets:
			if not jet.Pt()>25: continue
			if jet.DeltaR(track)<0.4: 
				isjet = True
				break
		if isjet: 
			continue
		#print ientry, 'found disappearing track w pT =', track.Pt(), dtstatus
		listOfEventNumbers.append(c.EvtNum)
	
		if abs(dtstatus)==1: nShort+=1
		if abs(dtstatus)==2: nLong+=1         
		if verbose: print ientry, itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta(), dtstatus   
	
		if abs(track.Eta())<1.5: dedxcalib = dedxcalib_barrel
		else: dedxcalib = dedxcalib_endcap
	
		disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], mva, itrack])


	if not len(disappearingTracks)>=1: continue

	if maketree:
		tracksAUX.clear()
		for track in c.tracks:
			tracksAUX.push_back(track)
		tree_out.Fill()

		
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
		if not lep.Pt()>candPtCut: continue
		if debugmode: print ientry, ilep, 'ele with Pt' , lep.Pt()
		#if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if debugmode: print ilep, 'passed eta and Pt'
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_tightID[ilep]: continue
		if debugmode: print ilep, 'passed that nice tight id'
		matchedTrk = TLorentzVector()
		RecoElectrons.append([lep, ilep])
	
	if len(RecoElectrons)>0: fillth2(hEtaVsPhiDT['Baseline'+'_tel'], RecoElectrons[0][0].Phi(), RecoElectrons[0][0].Eta())


	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		#if (abs(lep.Eta()) > 1.4442 and abs(lep.Eta()) < 1.566): continue
		if not abs(lep.Eta())<2.4: continue
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_tightID[ilep]: continue
		if lep.Pt()>candPtCut: RecoMuons.append([lep,ilep])

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
	
	if isdata: 
		weight = 1                    ###this needs some help
		if ismet: 
			if not (len(RecoElectrons)+len(RecoMuons)==0): continue
			if not c.MHT>150: continue
		if ismu: 
			if not (len(RecoMuons)>0 and len(RecoElectrons)==0): continue			
		if isel: 
			if not (len(RecoElectrons)>0): continue
		if isjetht:
			if not (c.MHT<150): continue
			if not (len(RecoMuons)==0 and len(RecoElectrons)==0): continue
	else:
		if processskims: wof = c.weight
		else: wof = c.CrossSection
		if len(RecoElectrons)+len(RecoMuons)>0: 
			weight = 0.9*wof*c.puWeight
		else: 
			weight = wof*gtrig.Eval(c.MHT)*c.puWeight


	if isdata: hHtWeighted.Fill(c.HTOnline,weight)
	else: hHtWeighted.Fill(c.madHT,weight)	

				

	dt, status, dedxPixel, mvascore, itrack = disappearingTracks[0]
	#print ientry, 'DT stuff dt, status, dedxPixel ', dt, status, dedxPixel 
	isPromptEl = isMatched2(dt, genels, 0.02)
	isPromptMu = isMatched2(dt, genmus, 0.02)
	isPromptPi = isMatched2(dt, genpis, 0.02)
	if isdata: isPromptEl, isPromptMu, isPromptPi, isfake = True, True, True, True
	else: isfake = not (isPromptEl or isPromptMu or isPromptPi)

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
		if c.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
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


	if len(RecoElectrons)>0: 
		mT = c.Electrons_MTW[RecoElectrons[0][1]]
		dt__ = dt.Clone()
		#dt__*=adjustedMht.Pt()/dt.Pt()*TMath.Cos(dt.DeltaPhi(adjustedMht))
		if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt__).M()
		else: invmass = 999		
	elif len(RecoMuons)>0: 
		mT = c.Muons_MTW[RecoMuons[0][1]]
		dt__ = dt.Clone()
		#dt__*=adjustedMht.Pt()/dt.Pt()*TMath.Cos(dt.DeltaPhi(adjustedMht))		
		if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoMuons[0][0]+dt__).M()
		else: invmass = 999				
	else: 
		mT = 999
		invmass = 999

			
	matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#/TMath.CosH(c.tracks[disappearingTracks[0][-1]].Eta())
	matchedcalofrac = 100*c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]/(dt.Pt()*TMath.CosH(dt.Eta()))
	dphiMhtDt = abs(adjustedMht.DeltaPhi(dt))
	fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets-len(RecoElectrons)-len(RecoMuons),adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta,matchedcalofrac, disappearingTracks[0][1], dphiMhtDt, mvascore]
	fv.append(getBinNumber(fv))
	fv.extend([c.MET, GetMinDeltaPhiMhtHemJets(adjustedJets,adjustedMht),log10dedxmass])
	if turnoffpred:
		FR, PR = 1.0, 1.0
	else:
		if abs(disappearingTracks[0][1])==1: 
			FR = getfakerate(fv[0], hfrshort)
			PR = getpromptrate(fv[13], hprshort)
		if abs(disappearingTracks[0][1])==2: 
			FR = getfakerate(fv[0], hfrlong)
			PR = getpromptrate(fv[13], hprlong)
	
	for regionkey in regionCuts:
		if 'MhtSideband' in regionkey and (not isdata): weight_ = weight/gtrig.Eval(c.MHT)
		else: weight_ = weight
		if selectionFeatureVector(fv,regionkey,'Mht'):  fillth2(hEtaVsPhiDT[regionkey], phi, dt.Eta())
		for ivar, varname in enumerate(varlist_):
			if selectionFeatureVector(fv,regionkey,varname):
				if (isPromptEl or isPromptMu or isPromptPi): 
					fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Truth, fv[ivar], weight_)
					if not turnoffpred: 
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method1,fv[ivar], FR*weight_)
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method2,fv[ivar], PR*weight_)
						fillth1(histoStructDict['Prompt'+regionkey+'_'+varname].Method3,fv[ivar], PR*FR*weight_)								
				if isfake:
					#print 'filling something with weight', weight_, 'Fake'+regionkey+'_'+varname
					fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,   fv[ivar], weight_)
					if not turnoffpred: 
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method1,  fv[ivar], FR*weight_)							
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method2,  fv[ivar], PR*weight_)
						fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Method3,  fv[ivar], PR*FR*weight_)								



fnew.cd()
hHt.Write()
hHtWeighted.Write()

writeHistoStruct(histoStructDict, 'truthmethod1method2method3')
for key_ in hEtaVsPhiDT: hEtaVsPhiDT[key_].Write()

if maketree and not processskims:
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


print 'listOfEventNumbers', listOfEventNumbers
print 'just created', fnew.GetName()
fnew.Close()
