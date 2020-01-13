from ROOT import *
import os, sys
from glob import glob
from random import shuffle
import time
import numpy as np
import random
import math
gROOT.SetStyle('Plain')
#gROOT.SetBatch(1)

execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False

specialTauPiValidation = False
simplifyControlRegion = False

codeproduct = sys.argv[0].split('/')[-1].split('With')[0].split('Maker')[0]

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_50000-3*.root"
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
sayalot = False
candPtCut = 30
candPtUpperCut = 6499
if SmearLeps4Zed_: kappasmearlevellabel = 'SmearLeps4ZedTrue'
else: kappasmearlevellabel = 'SmearLeps4ZedFalse'



verbose = False


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

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
print 'Identifier', identifier

datacalibdict = {'Run2016H': 1.0, 'Run2016D': 0.9061080624374195, 'Run2016E': 0.9080677535191167, 'Run2016F': 0.9722403102882298, 'Run2016G': 0.980409154652915, 'Run2016B': 0.8985872543754646, 'Run2016C': 0.8993061999613786}

if 'Run2016' in identifier: dedxcalib = datacalibdict[identifier.split('-')[0]]
else: dedxcalib = 1.0


newfname = codeproduct+'_'+identifier+'.root'
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])
moreargs = moreargs.replace(' ','').replace('--','-')
newfname = newfname.replace('.root',moreargs+'.root')

fnew = TFile(newfname,'recreate')
print 'making', fnew.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

hMtPionMatched = TH1F('hMtPionMatched','hMtPionMatched',50,0,200)
histoStyler(hMtPionMatched,kOrange+1)
hMtPionUnMatched = TH1F('hMtPionUnMatched','hMtPionUnMatched',50,0,200)
histoStyler(hMtPionUnMatched,kRed+1)



inf = 999999

regionCuts = {}
varlist_                             = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons',   'NMuons', 'InvMass', 'LepMT', 'NPions',   'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber', 'Met']
regionCuts['Baseline']               = [(0,inf), (0,inf),    (0,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,inf),     (0,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),     (-inf,inf),  (-inf,inf)]
regionCuts['HadBaseline']            = [(150,inf), (150,inf),(1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (0,0),    (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),     (-inf,inf),  (-inf,inf)]
#regionCuts['HighMetBaseline']       = [(0,inf), (250,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,inf ),    (0,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),  (-inf,inf),  (-inf,inf)]
regionCuts['SMuBaseline']            = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SMuZLL']                 = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (65,110), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SElBaseline']            = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),    (0,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SElZLL']                  = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),    (0,inf),  (65,110), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]



zoneOfDedx = {}
zonebinning = binning['DeDxZones']
dedxidx = varlist_.index('DeDxAverage')
srindex = varlist_.index('BinNumber')


#zonebinning = [0.0,99]

print 'dedxidx, srindex', dedxidx, srindex

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
hEtaVsPhiDT = {}
for region in regionCuts:
  histname = 'Track'+region+'_'+'EtaVsPhiDT'
  hEtaVsPhiDT[histname] = TH2F(histname,histname,160,-3.2,3.2,250,-2.5,2.5)# need to try this
  for izone in range(len(zonebinning)-1):
	dedx_zone = str(zonebinning[izone]).replace('.','p')+'To'+str(zonebinning[izone+1]).replace('.','p')
	zoneOfDedx[izone] = dedx_zone
	for var in varlist_:
		histname = 'El'+region+'Zone'+dedx_zone+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Mu'+region+'Zone'+dedx_zone+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)        
		histname = 'Pi'+region+'Zone'+dedx_zone+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)        		
		histname = 'Fake'+region+'Zone'+dedx_zone+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)  




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
hpass = ttrig.GetPassedHistogram().Clone('hpass')
htotal = ttrig.GetTotalHistogram().Clone('htotal')
gtrig = TGraphAsymmErrors(hpass, htotal)

c = TChain("TreeMaker2/PreSelection")
for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)

nentries = c.GetEntries()
#nentries = 100

c.Show(0)
#nentries = 5

ncuts = 13
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
else: madranges = [(0, inf)]

trigkey = 'SingleMuon'
trigkey = 'MhtMet6pack'

fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: 
	hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
	hMask = ''
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
	if SmearLeps4Zed_: return 1
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


matchedpinum = 0.0001
unmatchedpinum = 0.0001
print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if verbose:
		if not ientry in [432005,446869,768376]: continue
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]
			print 'going to process', nentries, 'events'
	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
	
		
		
	if isdata:
		#if not PassTrig(c, 'MhtMet6pack'): continue
		if not PassTrig(c, trigkey): continue
		#print ientry, c.MHT, PassTrig(c, 'MhtMet6pack')		
	else:	
	  isValidHtRange = False
	  for madrange in madranges:
		if (c.madHT>=madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	  if not isValidHtRange: continue#####this should be changed/fixed in Prompt code	
	
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

	#if not c.JetID: continue

	#if not passesUniversalSelection(c): continue

	#print 'here we are after stuff'
	#print 'c.MHT-c.MET', c.MHT, c.MET
	#if not abs(c.MHT-c.MET)<70: continue
	#if not c.HT>c.MHT: continue


	basicTracks = []
	disappearingTracks = []    
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if verbose: print itrack, 'no selection at all', track.Pt(), 'eta', track.Eta()        
		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if verbose: print itrack, 'before baseline pt', track.Pt(), 'eta', track.Eta()        
		if not isBaselineTrack(track, itrack, c, hMask): continue
				
		if verbose: print itrack, 'pt', track.Pt(), 'eta', track.Eta()
		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     
		if verbose: print ientry, itrack, 'basic bitch!', track.Pt()
		dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips)
		if verbose: print ientry, itrack, 'mva results were:', dtstatus, mva
		if not dtstatus>0: continue
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
			if jet.DeltaR(track)<0.4: 
				isjet = True
				break
		if isjet: continue
		print ientry, 'found disappearing track w pT =', track.Pt(), dtstatus
		print 'track has pixel layers', c.tracks_pixelLayersWithMeasurement[itrack]		
		
		if dtstatus==1: nShort+=1
		if dtstatus==2: nLong+=1         
		if verbose: print ientry, itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta()     
		'''
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
		if dtstatus==1: disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], itrack])
		if dtstatus==2: disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], itrack])		


	SmearedElectrons = []
	RecoElectrons = []
	for ilep, lep in enumerate(c.Electrons):
		if debugmode: print ientry, ilep, 'ele with Pt' , lep.Pt()
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if debugmode: print ilep, 'passed eta and Pt'
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_tightID[ilep]: continue
		if debugmode: print ilep, 'passed that nice tight id'
		drmin = inf
		matchedTrk = TLorentzVector()
		if lep.Pt()>candPtCut: RecoElectrons.append([lep, ilep])
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				if not simplifyControlRegion:
					if not c.tracks_nMissingOuterHits[trk[2]]>1: continue
					#if not c.tracks_trackerLayersWithMeasurement[trk[2]]==c.tracks_pixelLayersWithMeasurement[trk[2]]: continue
					if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if debugmode: print ilep, 'matched to a nice basic track', 	c.Electrons_MTW[ilep]
	
		#print ientry, 'found electron', lep.Pt()

		'''
		if isMatched2(ele, genels, 0.02):
			print ientry, 'this CR electron determined to be an electron'
		else:
			print ientry, 'this CR electron AINT no electron', c.Electrons_MTW[ilep]		
		'''
	
		###if not c.Electrons_MTW[ilep]<100: continue
		if debugmode: print ilep, 'el passed the mtw!'
		smearedEl = TLorentzVector()
		smearedEl.SetPtEtaPhiE(0, 0, 0, 0)
		smear = 1.0 
		smearedEl.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedEl.Pt()>candPtCut and smearedEl.Pt()<candPtUpperCut): continue
		SmearedElectrons.append([smearedEl,ilep,dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]],dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]]])
		#print ientry, 'a lovely ele', lep.Pt(), smearedEl.Pt()


	SmearedMuons = []
	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_tightID[ilep]: continue
		if lep.Pt()>candPtCut: RecoMuons.append([lep,ilep])
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				if not simplifyControlRegion:
					if not c.tracks_nMissingOuterHits[trk[2]]>1: continue
					#if not c.tracks_trackerLayersWithMeasurement[trk[2]]==c.tracks_pixelLayersWithMeasurement[trk[2]]: continue
					if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		#print ientry, 'found muon', lep.Pt() 


		#if not c.Muons_MTW[ilep]<100: continue
		smear = 1
		smearedMu = TLorentzVector()
		smearedMu.SetPtEtaPhiE(0, 0, 0, 0)        
		smearedMu.SetPtEtaPhiE(smear*matchedTrk[0].Pt(),matchedTrk[0].Eta(),matchedTrk[0].Phi(),smear*matchedTrk[0].E())
		if not (smearedMu.Pt()>candPtCut and smearedMu.Pt()<candPtUpperCut): continue
		SmearedMuons.append([smearedMu,ilep,dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]],dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]]])


	SmearedPions = []
	for ipi, pi in enumerate(c.TAPPionTracks):
		#if not c.isoPionTracks==1: continue
		isPromptPi = isMatched2(pi, genpis, 0.02)		
		#if not isPromptPi: continue
		if (abs(pi.Eta()) < 1.566 and abs(pi.Eta()) > 1.4442): continue
		if not abs(pi.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.TAPPionTracks_trkiso[ipi]<0.01: continue

		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(pi)
			if drTrk<drmin:
				if not simplifyControlRegion:
					if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
					#if not c.tracks_trackerLayersWithMeasurement[trk[2]]==c.tracks_pixelLayersWithMeasurement[trk[2]]: continue
					if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
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
		SmearedPions.append([smearedPi,ipi,dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]],dedxcalib*c.tracks_deDxHarmonic2pixel[matchedTrk[2]]])


	singleElEvent_ = len(SmearedElectrons) >=1  or  len(RecoElectrons) >=1 
	singleMuEvent_ = len(SmearedMuons) >=1 or  len(RecoMuons) >=1 
	singlePiEvent_ = len(SmearedPions) >=1
	presentDisTrkEvent = len(disappearingTracks) >=1# and len(RecoElectrons) ==0 and len(RecoMuons)==0 ##try commenting out last two

	if not (singleElEvent_ or presentDisTrkEvent or singleMuEvent_ or singlePiEvent_): continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
	
	if isdata: weight = 1                    ###this needs some help
	elif len(RecoElectrons)+len(RecoMuons)>0: 
		weight = c.CrossSection*c.puWeight
	else: 
		weight = c.CrossSection*c.puWeight*gtrig.Eval(c.MHT)
	hHtWeighted.Fill(c.HT,weight)	

	for elething in SmearedElectrons:
		dtproxy, elidx, dedxPixel, dedxPixel = elething
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = dtproxy.DeltaR(genels[0])
			if verbose: print dr
			if not dr<0.02: continue

		#print ientry, 'found a tawdry se', dtproxy.Pt()            
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(dtproxy)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))

		analysisElectrons = []
		for el in RecoElectrons:
			if el[0].DeltaR(dtproxy)>0.01: analysisElectrons.append(el)
		analysisMuons = RecoMuons

		pt = dtproxy.Pt()
		eta = abs(dtproxy.Eta())    
		ptForKappa = pt

		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_short)		
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10
		
		
		if len(analysisElectrons)>0: 
			mT = c.Electrons_MTW[analysisElectrons[0][1]]
			if c.Electrons_charge[analysisElectrons[0][1]]*c.Electrons_charge[elidx]==-1: invmass = (analysisElectrons[0][0]+dtproxy).M()
			else: invmass = 999			
		elif len(analysisMuons)>0: 
			mT = c.Muons_MTW[analysisMuons[0][1]]
			if c.Muons_charge[analysisMuons[0][1]]*c.Electrons_charge[elidx]==-1: invmass = (analysisMuons[0][0]+dtproxy).M()
			else: invmass = 999			
		else: 
			invmass = 999
			mT = 999
		
			
		#           ['Ht', 'Mht',           'NJets',      'BTags',        'NTags',         'NPix', 'NPixStrips','MinDPhiMhtJets','DeDxAverage','NElectrons', 'NMuons', 'NPions', 'TrkPt', 'TrkEta', 'Log10DedxMass','BinNumber']
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks), 1+nShort, nLong, mindphi, dedxPixel,len(RecoElectrons)-1, len(RecoMuons), invmass, mT, len(SmearedPions), pt,eta,log10dedxmass]		
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])
		kPixOnly = fetchKappa(abs(eta),ptForKappa, kappadictElPixOnly, shortMaxKappaPt)
		trigcor = 1#gtrig.Eval(adjustedMht.Pt())/gtrig.Eval(c.MHT)

		#print ientry, 'before filling', dedxPixel, fv
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue									
					if izone==0: fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)											
					hname = 'El'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname
					if selectionFeatureVector(fv,regionkey,varname):
						fillth1(histoStructDict[hname].Control,fv[ivar], weight)
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight*trigcor)					
						if izone==0 and ivar==srindex:
							#print 'izone', izone, 'trying to fill this thing with', fv[ivar], fv[ivar]-1, fv
							fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixOnly*weight*trigcor)
							

		#long        
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_el_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10
		
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks), nShort, 1+nLong, mindphi, dedxPixel,len(RecoElectrons)-1, len(RecoMuons), invmass, mT, len(SmearedPions), pt,eta,log10dedxmass]
		fv.append(getBinNumber(fv))                    
		fv.extend([c.MET])		
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictElPixAndStrips)
		#kgen = fetchKappa(abs(eta),ptForKappa, fGenElProbePt_KappasPixAndStrips)
		#krec = fetchKappa(abs(eta),ptForKappa, fElProbePt_KappasPixAndStrips)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue
					
					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)	
										
					hname = 'El'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname			
					if selectionFeatureVector(fv,regionkey,varname):
						if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)# skip double counting 1-lep region
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight*trigcor)					
						if izone==0 and ivar==srindex:					
							if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)# skip double counting 1-lep region
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixAndStrips*weight*trigcor)


	for muonthing in SmearedMuons:
		dtproxy, muidx, dedxPixel, dedxPixel = muonthing
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = dtproxy.DeltaR(genmus[0])
			if verbose: print dr
			if not dr<0.02: continue           
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(dtproxy)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))


		analysisElectrons = RecoElectrons
		analysisMuons = []
		for mu in RecoMuons:
			if mu[0].DeltaR(dtproxy)>0.01: analysisMuons.append(mu)
		
		
		pt = dtproxy.Pt()
		eta = abs(dtproxy.Eta())    
		ptForKappa = pt

		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		smear *=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)		
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10		
		
		
		if len(analysisElectrons)>0: 
			mT = c.Electrons_MTW[analysisElectrons[0][1]]
			if c.Electrons_charge[analysisElectrons[0][1]]*c.Muons_charge[muidx]==-1: invmass = (analysisElectrons[0][0]+dtproxy).M()
			else: invmass = 999			
		elif len(analysisMuons)>0: 
			mT = c.Muons_MTW[analysisMuons[0][1]]
			if c.Muons_charge[analysisMuons[0][1]]*c.Muons_charge[muidx]==-1: invmass = (analysisMuons[0][0]+dtproxy).M()
			else: invmass = 999			
		else: 
			invmass = 999
			mT = 999
			
					
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks),1+nShort,nLong, mindphi, dedxPixel,len(RecoElectrons), len(RecoMuons)-1, invmass, mT, len(SmearedPions),pt,eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		

		trigcor = 1#gtrig.Eval(adjustedMht.Pt())/gtrig.Eval(c.MHT)
	
		kPixOnly = fetchKappa(abs(eta),ptForKappa, kappadictMuPixOnly, shortMaxKappaPt)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue

					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)	
										
					hname = 'Mu'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname			
					if selectionFeatureVector(fv,regionkey,varname):					
						fillth1(histoStructDict[hname].Control,fv[ivar], weight)
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight*trigcor)
						if izone==0 and ivar==srindex:				
							fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixOnly*weight*trigcor)						
		
		#long
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		smear*=getSmearFactor(abs(eta),  min(pt,299.999), dResponseHist_mu_long)
		smear*=getSmearFactor(abs(eta),  min(pt,299.999), dResponseHist_mu_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10		
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks),nShort,nLong+1, mindphi,dedxPixel, len(RecoElectrons), len(RecoMuons)-1, invmass, mT, len(SmearedPions),pt,eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictMuPixAndStrips)
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
				
					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)	
									
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue
					hname = 'Mu'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname			
					if selectionFeatureVector(fv,regionkey,varname):
						if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight*trigcor)
						if izone==0 and ivar==srindex:
							if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixOnly*weight*trigcor)

	for pithing in SmearedPions:
		dtproxy, pidx, dedxPixel, dedxPixel = pithing
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		adjustedJets = []
		adjustedHt = 0
		adjustedBTags = 0
		if genMatchEverything:
			dr = dtproxy.DeltaR(genpis[0])
			if verbose: print dr
			if not dr<0.02: continue
		#print ientry, 'found a tawdry se', elec.Pt()            
		for ijet, jet in enumerate(c.Jets):
			if not jet.Pt()>30: continue
			if not jet.DeltaR(dtproxy)>0.4: continue####update 
			if not abs(jet.Eta())<5.0: continue####update to 2.4
			adjustedMht-=jet
			if not abs(jet.Eta())<2.4: continue####update to 2.4
			adjustedJets.append(jet)            
			adjustedHt+=jet.Pt()
			if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedNJets = len(adjustedJets)
		mindphi = 4
		for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))

		analysisElectrons = RecoElectrons
		analysisMuons = RecoMuons
				
		if len(analysisElectrons)>0: 
			mT = c.Electrons_MTW[analysisElectrons[0][1]]
			if c.Electrons_charge[analysisElectrons[0][1]]*c.TAPPionTracks_trkiso[pidx]==-1: invmass = (analysisElectrons[0][0]+dtproxy).M()
			else: invmass = 999			
		elif len(analysisMuons)>0: 
			mT = c.Muons_MTW[analysisMuons[0][1]]
			if c.Muons_charge[analysisMuons[0][1]]*c.TAPPionTracks_trkiso[pidx]==-1: invmass = (analysisMuons[0][0]+dtproxy).M()
			else: invmass = 999
		else: 
			invmass = 999
			mT = 999
			
		pt = dtproxy.Pt()
		eta = abs(dtproxy.Eta()) 				
		ptForKappa = pt   

		#short
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_short)
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))		
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10		
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks),1+nShort,nLong, mindphi, dedxPixel,len(RecoElectrons), len(RecoMuons), invmass, mT, len(SmearedPions)-1,pt,eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		
		trigcor = 1#gtrig.Eval(adjustedMht.Pt())/gtrig.Eval(c.MHT)
		kPixOnly = fetchKappa(abs(eta),min(ptForKappa,9999.99), kappadictPiPixOnly, shortMaxKappaPt)
		#print 'kPixOnly', kPixOnly, 'eta', eta, 'pt', ptForKappa
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue
					
					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)	
										
					hname = 'Pi'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname
					if selectionFeatureVector(fv,regionkey,varname):
						fillth1(histoStructDict[hname].Control,fv[ivar], weight)
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixOnly*weight*trigcor)
						if izone==0 and ivar==srindex:						
							fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixOnly*weight*trigcor)						
		#long
		smear = getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		smear*=getSmearFactor(abs(eta), min(pt,299.999), dResponseHist_mu_long)
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(smear*pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10		
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks),nShort,nLong+1, mindphi, dedxPixel,len(RecoElectrons), len(RecoMuons), invmass, mT, len(SmearedPions)-1,pt,eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		
		kPixAndStrips = fetchKappa(abs(eta),ptForKappa, kappadictPiPixAndStrips)
		#print 'kPixAndStrips', kPixAndStrips, 'eta', eta, 'pt', ptForKappa
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue
					
					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)	
										
					hname = 'Pi'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname	
					if selectionFeatureVector(fv,regionkey,varname):			
						if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar], weight)
						fillth1(histoStructDict[hname].Method,fv[ivar], kPixAndStrips*weight*trigcor)
						if izone==0 and ivar==srindex:				
							if 'Pix' in regionkey or 'Bin' in varname: fillth1(histoStructDict[hname].Control,fv[ivar]-1, weight)
							fillth1(histoStructDict[hname].Method,fv[ivar]-1, kPixAndStrips*weight*trigcor)						
	if presentDisTrkEvent:
		dt, status, dedxPixel, itrack = disappearingTracks[0]
		#print ientry, 'DT stuff dt, status, dedxPixel ', dt, status, dedxPixel 
		isPromptEl = isMatched2(dt, genels, 0.02)
		isPromptMu = isMatched2(dt, genmus, 0.02)
		isPromptPi = isMatched2(dt, genpis, 0.02)
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
			phi = dt.phi()
							
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10	
		
		
		if len(RecoElectrons)>0: 
			mT = c.Electrons_MTW[RecoElectrons[0][1]]
			if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt).M()
			else: invmass = 999			
		elif len(RecoMuons)>0: 
			mT = c.Muons_MTW[RecoMuons[0][1]]
			if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoMuons[0][0]+dt).M()
			else: invmass = 999			
		else: 
			mT = 999
			invmass = 999
		
					
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, len(SmearedPions), pt, eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		
		for regionkey in regionCuts:
		
			if selectionFeatureVector(fv,regionkey,''): fillth2(hEtaVsPhiDT[regionkey], phi, eta)
			for ivar, varname in enumerate(varlist_):
				for izone in range(len(zonebinning)-1):
					if not (dedxPixel>zonebinning[izone] and dedxPixel<zonebinning[izone+1]): continue
					
					if izone==0: 
						fv[srindex] = 2*math.ceil(1.0*getBinNumber(fv,binnumbers,dedxidx)/2)
					else: fv[srindex] = getBinNumber(fv)
					
										
					if selectionFeatureVector(fv,regionkey,varname):
							if isPromptEl: 
								fillth1(histoStructDict['El'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar], weight)								
								if izone==0 and ivar==srindex: fillth1(histoStructDict['El'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar]-1, weight)							
								if sayalot: print 'filling this el'
							elif isPromptMu: 
								fillth1(histoStructDict['Mu'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar], weight)
								if izone==0 and ivar==srindex: fillth1(histoStructDict['Mu'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar]-1, weight)
								if sayalot: print 'filling this mu'
							elif isPromptPi: 
								fillth1(histoStructDict['Pi'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar], weight)
								if izone==0 and ivar==srindex: fillth1(histoStructDict['Pi'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar]-1, weight)
								if sayalot: print 'filling this pi'							
							else:
								fillth1(histoStructDict['Fake'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar], weight)
								if izone==0 and ivar==srindex: fillth1(histoStructDict['Fake'+regionkey+'Zone'+zoneOfDedx[izone]+'_'+varname].Truth,fv[ivar]-1, weight)
								if sayalot: print 'filling this fake'



fnew.cd()
writeHistoStruct(histoStructDict)
for keys in hEtaVsPhiDT: hEtaVsPhiDT[key].Write()
hHt.Write()
hHtWeighted.Write()
hMtPionMatched.Write()
hMtPionUnMatched.Write()
print 'just created', fnew.GetName()
fnew.Close()
fKappaPixOnly.Close()
fsmear_short.Close()
fsmear_long.Close()

