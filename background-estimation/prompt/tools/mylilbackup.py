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
from code import interact


execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False 


binning['MatchedCalo'] = [100,0,100]

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
UseFits = False
UseJets_bJetTagDeepCSVBvsAll = False
sayalot = False
candPtCut = 30
candPtUpperCut = 6499
if SmearLeps4Zed_: kappasmearlevellabel = 'SmearLeps4ZedTrue'
else: kappasmearlevellabel = 'SmearLeps4ZedFalse'



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


if phase==0: mvathreshes=[.1,.25]
else: mvathreshes=[0.15,0.0]

print 'phase', phase

if isdata: ClosureMode = False

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
print 'Identifier', identifier


if 'Run201' in identifier: 
	dedxcalib_barrel = datacalibdict_SingleElectron_barrel[identifier.split('-')[0]]
	dedxcalib_endcap = datacalibdict_SingleElectron_endcap[identifier.split('-')[0]]	
elif 'Summer16' in identifier: 
	dedxcalib_barrel = datacalibdict_SingleElectron_barrel['Summer16']	
	dedxcalib_endcap = datacalibdict_SingleElectron_endcap['Summer16']
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

fnew = TFile(newfname,'recreate')
print 'making', fnew.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)

inf = 999999

regionCuts = {}
varlist_                                   = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons',   'NMuons', 'InvMass', 'LepMT', 'NPions',   'TrkPt',        'TrkEta',    'MatchedCalo', 'Log10DedxMass','BinNumber', 'Met']
regionCuts['Baseline']                     = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,inf),      (0,inf),    (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4), (0,10),     (-inf,inf),  (-inf,inf)]
regionCuts['BaselineCaloSideband']         = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,inf),      (0,inf),    (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4), (30,9999),     (-inf,inf),  (-inf,inf)]
regionCuts['HadBaseline']                  = [(150,inf), (150,inf),(1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (0,0),    (0,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),       (0,10),    (-inf,inf),  (-inf,inf)]
regionCuts['HadBaselineCaloSideband']      = [(150,inf), (150,inf),(1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (0,0),    (0,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),      (30,9999),     (-inf,inf),  (-inf,inf)]
regionCuts['SMuBaseline']                  = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),    (0,10),     (-inf,inf),  (-inf,inf)]
regionCuts['SMuBaselineCaloSideband']      = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),    (30,9999),     (-inf,inf),  (-inf,inf)]
regionCuts['SElBaseline']                  = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),     (0,inf), (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),    (0,10),    (-inf,inf),  (-inf,inf)]
regionCuts['SElBaselineCaloSideband']      = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),     (0,inf), (110,inf), (90,inf),   (0,inf),    (candPtCut,inf), (0,2.4),    (30,9999),    (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationZLL']             = [(0,inf),   (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),    (0,0),     (65,110), (0,inf),   (0,inf),    (candPtCut,inf), (0,2.4),       (0,10), (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationZLLCaloSideband'] = [(0,inf),   (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,inf ),    (0,0),     (65,110), (0,inf),   (0,inf),    (candPtCut,inf), (0,2.4),       (30,9999), (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationMT']              = [(0,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,1 ),      (0,0),     (0,inf),  (0,70),   (0,inf),    (candPtCut,inf), (0,2.4),        (0,10),   (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationMTCaloSideband']  = [(0,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (1,1 ),      (0,0),     (0,inf),  (0,70),   (0,inf),    (candPtCut,inf), (0,2.4),        (30,9999),   (-inf,inf),  (-inf,inf)]
regionCuts['SMuValidationMT']              = [(0,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0),       (1,1),     (0,inf),  (0,70),   (0,inf),    (candPtCut,inf), (0,2.4),        (0,10),    (-inf,inf),  (-inf,inf)]
regionCuts['SMuValidationMTCaloSideband']  = [(0,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,0),       (1,1),     (0,inf),  (0,70),   (0,inf),    (candPtCut,inf), (0,2.4),        (30,9999),    (-inf,inf),  (-inf,inf)]



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
	hEtaVsPhiDT[region] = TH2F(histname,histname,160,-3.2,3.2,250,-2.5,2.5)# need to try this
	for var in varlist_:
		histname = 'El'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Mu'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Pi'+region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname)
		histname = 'Fake'+region+'_'+var
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
#nentries = 100

c.Show(0)
c.GetEntry(0)
thisfile = ''
#nentries = 5

ncuts = 17
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
readerPixelOnly.SetName('Reader1')
readerPixelStrips = TMVA.Reader()
readerPixelStrips.SetName('Reader2')
prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
prepareReaderPixel_loose(readerPixelOnly, pixelXml)

#prepareReaderPixelStrips(readerPixelStrips, pixelstripsXml)
#prepareReaderPixel(readerPixelOnly, pixelXml)


import time
t1 = time.time()
i0=0

runs = {}
lastlumi = -1
lastrun = -1


matchedpinum = 0.0001
unmatchedpinum = 0.0001
print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if debugmode:
		if not ientry in [29168]: continue
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
	
	if not c.JetID: continue

	if isdata: 
		if not passesUniversalDataSelection(c): continue
	else: 
		if not passesUniversalSelection(c): continue

	
	
	basicTracks = []
	disappearingTracks = []    
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if verbose: print itrack, 'no selection at all', track.Pt(), 'eta', track.Eta()        
		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue    #I kind of want to drop this eventually
		if verbose: print itrack, 'before baseline pt', track.Pt(), 'eta', track.Eta()        
		if not isBaselineTrack(track, itrack, c, hMask): continue
				
		if verbose: print itrack, 'pt', track.Pt(), 'eta', track.Eta()
		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     
		if verbose: print ientry, itrack, 'basic track!', track.Pt()
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
		
		if abs(track.Eta())<1.4: dedxcalib = dedxcalib_barrel
		else: dedxcalib = dedxcalib_endcap
		if dtstatus==1: disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], itrack])
		if dtstatus==2: disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], itrack])			


	if not len(disappearingTracks)>=1: continue
	
			
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
			
			
	for dt in disappearingTracks:
		track = dt[0]
		print ientry, itrack, 'disappearing track! pt', track.Pt(), 'eta', track.Eta(), 'status', dtstatus, mva
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


	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		if (abs(lep.Eta()) > 1.4442 and abs(lep.Eta()) < 1.566): continue
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
		if ismu: 
			if not (len(RecoMuons)>0 and len(RecoElectrons)==0): continue			
		if isel: 
			if not (len(RecoElectrons)>0): continue
						
	elif len(RecoElectrons)+len(RecoMuons)>0: 
		weight = c.CrossSection#*c.puWeight
	else: 
		weight = c.CrossSection*gtrig.Eval(c.MHT)#*c.puWeight

	if isdata: hHtWeighted.Fill(c.HTOnline,weight)
	else: hHtWeighted.Fill(c.madHT,weight)	

					

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
		phi = dt.Phi()
						
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
	
				
	matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]
	fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, 0, pt, eta,matchedcalo, log10dedxmass]
	fv.append(getBinNumber(fv))
	fv.extend([c.MET])		
	for regionkey in regionCuts:
	
		if selectionFeatureVector(fv,regionkey,'Mht'): fillth2(hEtaVsPhiDT[regionkey], phi, eta)
		
		for ivar, varname in enumerate(varlist_):
				if selectionFeatureVector(fv,regionkey,varname):
						if isPromptEl: 
							print 'filling', histoStructDict['El'+regionkey+'_'+varname].Truth
							fillth1(histoStructDict['El'+regionkey+'_'+varname].Truth,fv[ivar], weight)								
						elif isPromptMu: 
							fillth1(histoStructDict['Mu'+regionkey+'_'+varname].Truth,fv[ivar], weight)
						elif isPromptPi: 
							fillth1(histoStructDict['Pi'+regionkey+'_'+varname].Truth,fv[ivar], weight)
						else:
							fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,fv[ivar], weight)



fnew.cd()
writeHistoStruct(histoStructDict, 'truth')
for key_ in hEtaVsPhiDT: hEtaVsPhiDT[key_].Write()
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

