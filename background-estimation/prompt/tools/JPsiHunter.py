from ROOT import *
import os, sys
from glob import glob
from random import shuffle
import time
import numpy as np
import random
import math
gROOT.SetStyle('Plain')
gROOT.SetBatch(1)


#a next thing to try would be removing the track matching criteria on the electrons - but let's wait until after the singleMuon stuff runs. Funny i would have thought the electron stuff was ok, based on the results from before. Do I have something funny with the luminosity?

execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False

codeproduct = sys.argv[0].split('/')[-1].split('With')[0].split('Maker')[0]

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_80000*.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_78_RA2AnalysisTree.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
args = parser.parse_args()
nfpj = args.nfpj
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
analyzer = args.analyzer
verbosity = args.verbosity

verbose = False


isdata = 'Run201' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames or 'aksingh' in inputFileNames: 
	is2016, is2017, is2018 = True, False, False
elif 'Run2017' in inputFileNames or 'Fall17' in inputFileNames or 'Run2017' in inputFileNames: 
	is2016, is2017, is2018 = False, True, False
elif 'Run2018' in inputFileNames or 'Autumn18' in inputFileNames or 'somthin or other' in inputFileNames: 
	is2016, is2017, is2018 = False, True, True

if is2016: phase = 0
else: phase = 1

if is2016: BTAG_deepCSV = 0.6324
if is2017: BTAG_deepCSV = 0.4941
if is2018: BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
print 'Identifier', identifier


#dedxcalib = 1.0

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


binning['MiniInvMass'] = [100,0,20]
binning['NIsoTracks'] = [5,0,5]
binning['Sign1Sign2'] = [10,-1.1,1.1]


inf = 999999

regionCuts = {}
varlist_                             = ['Ht',    'Mht',     'NJets',   'NElectrons', 'InvMass',   'NMuons', 'MuPt', 'NIsoTracks', 'TrkPt', 'MiniInvMass', 'Sign1Sign2']
regionCuts['SimpleOS']               = [(0,inf), (0,inf),    (0,inf),  (2,2),          (75,105),  (0,inf),     (-inf,inf), (0,inf), (-inf,inf),    (-inf,inf), (-3,3)]
regionCuts['BaselineOS']               = [(0,inf), (0,inf),    (0,inf),  (2,2),          (75,105),  (1,1),     (-inf,inf), (1,1),   (-inf,inf),    (0,15), (1,1)]
regionCuts['BaselineSS']               = [(0,inf), (0,inf),    (0,inf),  (2,2),          (75,105),  (1,1),     (-inf,inf), (1,1),   (-inf,inf),    (0,15), (-1,-1)]



indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
hEtaVsPhiDT = {}

def getBinNumber(fv, binnumberdict=binnumbers, omitidx=-1):
	for binkey in binnumberdict:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if iwindow==omitidx: continue
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumberdict[binkey]
	return -10

for region in regionCuts:
	for var in varlist_:
		histname = region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)

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
c.GetEntry(0)
thisfile = ''
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


if 'MET' in inputFileNames: 
	trigkey = 'MhtMet6pack'
	ismu = False
	isel = False
	ismet= True	
elif 'SingleMu' in inputFileNames: 
	trigkey = 'SingleMuon'
	ismu = True
	isel = False
	ismet= False	
elif 'SingleEl' in inputFileNames or 'SingleEG' in inputFileNames: 
	trigkey = 'SingleElectron'
	ismu = False
	isel = True
	ismet= False	

fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: 
	hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
	hMask = ''
else: 
	#hMask = fMask.Get('hEtaVsPhiDTRun2016')
	hMask = ''




import os

import time
t1 = time.time()
i0=0

runs = {}
lastlumi = -1
lastrun = -1


print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if debugmode:
		if not ientry in [12]: continue
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries
		os.system('echo "now processing '+str(ientry)+'of'+str(nentries)+'" > funnylog'+str(ientry)+'.log')
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]
			print 'going to process', nentries, 'events'
	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	
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
	            
	

	RecoElectrons = []
	for ilep, lep in enumerate(c.Electrons):
		if not abs(lep.Eta())<2.4: continue
		if debugmode: print ilep, 'passed eta and Pt'
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_mediumID[ilep]: continue
		if debugmode: print ilep, 'passed that nice tight id'
		drmin = inf
		matchedTrk = TLorentzVector()
		if lep.Pt()>10: RecoElectrons.append([lep, ilep])
		
	if not len(RecoElectrons) >1: continue


	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt'
		if not abs(lep.Eta())<2.4: continue
		#if not c.Muons_passIso[ilep]: continue
		if not c.Muons_mediumID[ilep]: continue
		if lep.Pt()<20: RecoMuons.append([lep,ilep])
	
	
	basicTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() < 20 : continue
		if not abs(track.Eta()) < 2.4: continue	
		if not isBaselineTrack(track, itrack, c): continue			
		basicTracks.append([track,c.tracks_charge[itrack], itrack])	
	
	
	
	
	
	
	if len(basicTracks)>0: trackpt = basicTracks[0][0].Pt()
	else: trackpt = -1
	
	if len(basicTracks)>0 and len(RecoMuons)>0: 
		minimass = (basicTracks[0][0]+RecoMuons[0][0]).M()
		sign1sign2 = basicTracks[0][1]*c.Muons_charge[RecoMuons[0][1]]
	else: 
		minimass = 99
		sign1sign2 = 0
	
	if len(RecoMuons)>0: mupt = RecoMuons[0][0].Pt()
	else: mupt = -1
		
				
	if isdata: 
		weight = 1
						
	elif len(RecoElectrons)+len(RecoMuons)>0: 
		weight = 1# c.CrossSection*c.puWeight
	else: 
		weight = c.CrossSection*c.puWeight*gtrig.Eval(c.MHT)

	if isdata: hHtWeighted.Fill(c.HTOnline,weight)
	else: hHtWeighted.Fill(c.madHT,weight)	
					

	adjustedJets = []
	adjustedHt = 0
	adjustedMht = TLorentzVector()
	adjustedMht.SetPxPyPzE(0,0,0,0)
	for ijet, jet in enumerate(c.Jets):
		if not jet.Pt()>30: continue			
		if not abs(jet.Eta())<5.0: continue###update to 2.4
		adjustedMht-=jet		
		if not abs(jet.Eta())<2.4: continue###update to 2.4            
		adjustedJets.append(jet)
		adjustedHt+=jet.Pt()
	adjustedNJets = len(adjustedJets)
	mindphi = 4
	for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))            

	if len(RecoElectrons)==2: 
		if c.Electrons_charge[RecoElectrons[0][1]]*c.Electrons_charge[RecoElectrons[1][1]]==-1: 
			invmass = (RecoElectrons[0][0]+RecoElectrons[1][0]).M()
		else: invmass = 999			
	else: 
		mT = 999
		invmass = 999
		

	

				
#varlist_  = ['Ht',    'Mht',                  'NJets',   'NElectrons',     'InvMass',   'NMuons', 'MuPt', 'NIsoTracks', 'TrkPt', 'MiniInvMass', 'Sign1Sign2']

	fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,len(RecoElectrons), invmass, len(RecoMuons), mupt,len(basicTracks), trackpt, minimass, sign1sign2]

	
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist_):								
			if selectionFeatureVector(fv,regionkey,varname):
				fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar]-1, weight)



fnew.cd()
writeHistoStruct(histoStructDict, 'truth')
hHt.Write()
hHtWeighted.Write()


print 'just created', fnew.GetName()
fnew.Close()

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
		with open(fnew_.GetName().replace(".root", ".json"), "w") as fo:
			fo.write(json_content)

	fnew_.Close()

