'''
---------------------BR: 100%-----------------------
/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_10cm/*/*.root
'''

import os, sys
import time
import numpy as np
from ROOT import *
from shared_utils import *
from glob import glob
from random import shuffle
import random
gROOT.SetStyle('Plain')
gROOT.SetBatch(1)

debugmode = False

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_50cm/*/*g1400_chi750_27*.root"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--updateevery", type=int, default=1000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-numberOfFilesPerJob", "--nfpj", type=int, default=100)
args = parser.parse_args()
nfpj = args.nfpj
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
analyzer = args.analyzer
updateevery = args.updateevery
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

candPtCut = 30
candPtUpperCut = 6499
if is2016: BTAG_deepCSV = 0.6324
if is2017: BTAG_deepCSV = 0.4941
if is2018: BTAG_deepCSV = 2.55
btag_cut = BTAG_deepCSV

from CrossSectionDictionary import *
if 'Lifetime_50cm' in inputFileNames: model = 'T1'
loadCrossSections(model)
mothermass = inputFileNames.split('/')[-1].split('_')[0].replace('g','').replace('*','')
xsecpb = CrossSectionsPb[model][mothermass]
print 'got xsec', xsecpb, 'for mothermass', mothermass




if phase==0: mvathreshes=[.1,.25] #these are not used currently
else: mvathreshes=[0.15,0.0] #these are not used currently

print 'phase', phase
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier


newfname = 'AnalysisHistsDedx_'+identifier+'.root'
fnew_ = TFile(newfname,'recreate')
print 'creating file', fnew_.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)
hBdtVsDxyIsLong = TH2F('hBdtVsDxyIsLong','hBdtVsDxyIsLong',20,0,0.2,24,-.6,0.6)
hBdtVsDxyIsShort = TH2F('hBdtVsDxyIsShort','hBdtVsDxyIsShort',20,0,0.2,24,-.6,0.6)

#hHt = TH1F('hHt','hHt',100,0,3000)

inf = 999999

regionCuts = {}
varlist_                         = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'Log10DedxMass','NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'DeDxAverage','BinNumber']
regionCuts['Baseline']           = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (-inf,inf),         (0,0 ),      (0,inf),  (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf),  (-1,inf)]
regionCuts['BaselineMuVeto']     = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),     (0.3,inf),        (-inf,inf),         (0,0 ),      (0,0),    (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf),  (-1,inf)]
regionCuts['BaselinePixOnly']    = [(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,inf),     (0.3,inf),        (-inf,inf),         (0,0),       (0,inf),   (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
regionCuts['BaselinePixAndStrips']=[(0,inf), (250,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),     (0.3,inf),        (-inf,inf),         (0,0),       (0,inf),   (0,0),    (candPtCut,inf), (0,2.4),      (-inf,inf), (-1,inf)]
def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
	iomits = []
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
			return False
	return True
	
indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
	for var in varlist_:
		histname = region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)	   

lmasscutLlow = TMath.Log10(100)
lmasscutLmid = TMath.Log10(450)
lmasscutSlow = TMath.Log10(60)
lmasscutSmid = TMath.Log10(150)
binnumbers = {}
listagain = ['Ht',  'Mht',    'NJets','BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets','Log10DedxMass',                  'NElectrons', 'NMuons', 'NPions', 'TrkPt','TrkEta','BinNumber']
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutLlow,lmasscutLmid))] = 1
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutLmid,inf))] = 2
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutSlow,lmasscutSmid))] = 3
binnumbers[((0,inf),(250,400),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutSmid,inf))] = 4
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLlow,lmasscutLmid))] = 5
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLmid,inf))] = 6
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSlow,lmasscutSmid))] = 7
binnumbers[((0,inf),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSmid,inf))] = 8
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLlow,lmasscutLmid))] = 9
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLmid,inf))] = 10
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSlow,lmasscutSmid))] = 11
binnumbers[((0,inf),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSmid,inf))] = 12
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLlow,lmasscutLmid))] = 13
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLmid,inf))] = 14
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSlow,lmasscutSmid))] = 15
binnumbers[((0,inf),(250,400),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSmid,inf))] = 16
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLlow,lmasscutLmid))] = 17
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.5,inf),          (lmasscutLmid,inf))] = 18
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSlow,lmasscutSmid))] = 19
binnumbers[((0,inf),(250,400),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSmid,inf))] = 20
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutLlow,lmasscutLmid))] = 21
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutLmid,inf))] = 22
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutSlow,lmasscutSmid))] = 23
binnumbers[((0,inf),(400,700),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutSmid,inf))] = 24
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 25
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutLmid,inf))] = 26
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSlow,lmasscutSmid))] = 27
binnumbers[((0,inf),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,inf),          (lmasscutSmid,inf))] = 28
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 29
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 30
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 31
binnumbers[((0,inf),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 32
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 33
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 34
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 35
binnumbers[((0,inf),(400,700),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 36
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 37
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 38
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 39
binnumbers[((0,inf),(400,700),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 40
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutSlow,lmasscutSmid))] = 41
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (lmasscutSmid,inf))] = 42
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutLlow,lmasscutLmid))] = 43
binnumbers[((0,inf),(700,inf),(1,1),  (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (lmasscutLmid,inf))] = 44
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 45
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 46
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 47
binnumbers[((0,inf),(700,inf),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 48
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 49
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 50
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 51
binnumbers[((0,inf),(700,inf),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 52
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 53
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 54
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 55
binnumbers[((0,inf),(700,inf),(6,inf),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 56
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSlow,lmasscutSmid))] = 57
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (lmasscutSmid,inf))] = 58
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLlow,lmasscutLmid))] = 59
binnumbers[((0,inf),(700,inf),(6,inf),(1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (lmasscutLmid,inf))] = 60
binnumbers[((0,inf),(0,400),  (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=61
binnumbers[((0,inf),(400,inf),(0,inf),(0,inf),(2,inf),(0,inf),(0,inf),    (0.0,inf))]=62





def getBinNumber(fv):
	for binkey in binnumbers:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumbers[binkey]
	return -1
		

c = TChain("TreeMaker2/PreSelection")
for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)

nentries = c.GetEntries()
#nentries = 100


signalweight = xsecpb*1.0/nentries
c.Show(0)



fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
else: 
	#hMask = fMask.Get('hEtaVsPhiDTRun2016')
	hMask = ''


import os
if phase==0:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
else:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'	

readerPixelOnly = TMVA.Reader()
readerPixelStrips = TMVA.Reader()
prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
prepareReaderPixel_loose(readerPixelOnly, pixelXml)
#prepareReaderPixelStrips(readerPixelStrips, pixelstripsXml)
#prepareReaderPixel(readerPixelOnly, pixelXml)


import time
t1 = time.time()
i0=0

triggerIndecesV2 = {}
triggerIndecesV2['MhtMet6pack'] = [108,110,114,123,124,125,126,128,129,130,131,132,133,122,134]
triggerIndeces = triggerIndecesV2

def PassTrig(c,trigname):
	for trigidx in triggerIndeces[trigname]: 
		if c.TriggerPass[trigidx]==1: 
			return True
	return False


print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if ientry%updateevery==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]

	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	hHt.Fill(c.HT)
	if isdata: weight = 1
	else: 
		weight = signalweight*c.puWeight
		#weight = 1.0
	hHtWeighted.Fill(c.HT,weight)

	if c.MET>100:
		if not c.CaloMET/c.MET<5.0: continue

	'''
	print ientry, '='*10
	for igp, gp in enumerate(c.GenParticles):
		if not gp.Pt()>5: continue
		if not abs(c.GenParticles_PdgId[igp])>1000000: continue
		print igp, 'we got ', c.GenParticles_PdgId[igp], 'with pT=', gp.Pt(), gp.Eta()
	'''
	
	basicTracks = []
	disappearingTracks = []    
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isBaselineTrack(track, itrack, c, hMask): continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     
		dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips, mvathreshes)
		
		if c.tracks_nValidPixelHits[itrack]==c.tracks_nValidTrackerHits[itrack]: fillth2(hBdtVsDxyIsShort, c.tracks_dxyVtx[itrack], mva)
		else: fillth2(hBdtVsDxyIsLong, c.tracks_dxyVtx[itrack], mva)
		if not dtstatus>0: continue
		drlep = 99
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.01: 
				passeslep = False
				break            
		if not passeslep: continue 
		dedx = -1
		if dtstatus==1: 
			nShort+=1
			dedx = c.tracks_deDxHarmonic2strips[itrack]
		if dtstatus==2: 
			nLong+=1			
			dedx = c.tracks_deDxHarmonic2strips[itrack]
	
		disappearingTracks.append([track,dtstatus,dedx])

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
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: 
					break
		if not drmin<0.01: continue
		if ele.Pt()>candPtCut: RecoElectrons.append([ele, c.Electrons_charge[iel]])


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
			drTrk = trk[0].DeltaR(lep)
			if drTrk<drmin:
				drmin = drTrk
				matchedTrk = trk
				if drTrk<0.01: break
		if not drmin<0.01: continue
		if lep.Pt()>candPtCut: RecoMuons.append([lep,c.Muons_charge[ilep]])    


	SmearedPions = []
	for ipi, pi in enumerate(c.TAPPionTracks):
		if (abs(pi.Eta()) < 1.566 and abs(pi.Eta()) > 1.4442): continue
		if not abs(pi.Eta())<2.4: continue
		if not c.TAPPionTracks_trkiso[ipi]<0.2: continue
		drmin = inf
		matchedTrk = TLorentzVector()
		for trk in basicTracks:
			drTrk = trk[0].DeltaR(pi)
			if drTrk<drmin:
				if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
				if c.tracks_passPFCandVeto[trk[2]]: continue
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
		
		
	#print 'len(disappearingTracks)', len(disappearingTracks)
	presentDisTrkEvent = len(disappearingTracks) >=1

	if not presentDisTrkEvent: continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
				  
	if len(disappearingTracks)>0: 
		dt = disappearingTracks[0][0]
		pt = dt.Pt()
		eta = abs(dt.Eta()) 
		dedx = disappearingTracks[0][2] 
		Log10DedxMass = TMath.Log10(TMath.Sqrt((dedx-3.01)*pow(c.tracks[itrack].P(),2)/1.74))
	else: 
		dt = TLorentzVector()
		pt = -1
		eta = -1
		dedx = -1
		Log10DedxMass = 0.01
	adjustedBTags = 0        
	adjustedJets = []
	adjustedHt = 0
	adjustedMht = TLorentzVector()
	adjustedMht.SetPxPyPzE(0,0,0,0)
	for ijet, jet in enumerate(c.Jets):
		if not jet.Pt()>30: continue			
		if not abs(jet.Eta())<5.0: continue###update to 2.4
		someoverlap = False
		for dt_ in disappearingTracks: 
			if jet.DeltaR(dt_[0])<0.4: 
				someoverlap = True
				break
		if someoverlap: continue
		adjustedMht-=jet		
		if not abs(jet.Eta())<2.4: continue###update to 2.4            
		adjustedJets.append(jet)			
		if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedHt+=jet.Pt()
	adjustedNJets = len(adjustedJets)
	mindphi = 4
	for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 
	
	fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi,Log10DedxMass, len(RecoElectrons), len(RecoMuons), len(SmearedPions), pt, eta, dedx]
	fv.append(getBinNumber(fv))
	#print fv
	#for ifv in range(len(fv)): print ifv, varlist_[ifv], fv[ifv]	
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist_):
			if selectionFeatureVector(fv,regionkey,varname):
				fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar], weight)
		
	

fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict, 'truth')
hBdtVsDxyIsShort.Write()
hBdtVsDxyIsLong.Write()
print 'just created', fnew_.GetName()
fnew_.Close()
fMask.Close()