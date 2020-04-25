from ROOT import *
import os, sys
from glob import glob
from random import shuffle
import numpy as np
import random
import math
gROOT.SetStyle('Plain')
gROOT.SetBatch(1)



execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
debugmode = False

codeproduct = sys.argv[0].split('/')[-1].split('With')[0].split('Maker')[0]

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_50000-3*.root"
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
verbosity = args.verbosity


genMatchEverything = False
RelaxGenKin = True
ClosureMode = True #false means run as if real data
SmearLeps = False
UseFits = False
UseJets_bJetTagDeepCSVBvsAll = False
sayalot = False
candPtCut = 30
candPtUpperCut = 6499



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


if 'Run201' in identifier: dedxcalib = datacalibdict[identifier.split('-')[0]]
elif 'Summer16' in identifier: dedxcalib = datacalibdict['Summer16']
else: dedxcalib = 1.0

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

hMtPionMatched = TH1F('hMtPionMatched','hMtPionMatched',50,0,200)
histoStyler(hMtPionMatched,kOrange+1)
hMtPionUnMatched = TH1F('hMtPionUnMatched','hMtPionUnMatched',50,0,200)
histoStyler(hMtPionUnMatched,kRed+1)



inf = 999999

regionCuts = {}
varlist_                             = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'Moh',     'MinDPhiMhtJets', 'DeDxAverage', 'NElectrons',   'NMuons', 'InvMass',  'LepMT',   'TrkPt',        'TrkEta', 'Log10DedxMass','BinNumber', 'Met']
regionCuts['NoCuts']               =   [(0,inf), (0,inf),      (0,inf), (0,inf), (1,inf), (0,inf),     (0.0,inf),       (-inf,inf),         (0,inf),     (0,inf),  (0,inf),  (0,inf), (candPtCut,inf),(0,2.4),   (-inf,inf),  (-inf,inf)]

regionCuts['HadBaseline']            = [(150,inf), (150,inf),(1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (0,0 ),      (0,0),    (110,inf),(90,inf),(candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SMuBaseline']            = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (110,inf),(90,inf),(candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SMuValidationZLL']       = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (0,0 ),      (1,inf),  (65,110), (0,inf), (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SElBaseline']            = [(150,inf), (0,inf),  (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (1,inf ),    (0,inf),  (110,inf),(90,inf),(candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationZLL']       = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (1,inf ),    (0,0),    (65,110), (0,inf), (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SElValidationMT']        = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (1,1 ),      (0,0),    (0,inf),  (0,70),  (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]
regionCuts['SMuValidationMT']        = [(0,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (2,11),     (0.0,inf),       (-inf,inf),         (0,0),       (1,1),    (0,inf),  (0,70),  (candPtCut,inf), (0,2.4),   (-inf,inf),  (-inf,inf)]

regionkeys = regionCuts.keys()
for key in regionkeys:
	regionCuts[key+'MohSB'] = list(regionCuts[key])
	regionCuts[key+'MohSB'][varlist_.index('Moh')] = (0,0)
	regionCuts[key+'MohST'] = list(regionCuts[key])
	regionCuts[key+'MohST'][varlist_.index('Moh')] = (12,12)	

for key in regionCuts:
	print key, regionCuts[key][:5]

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
if phase==0:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
else:
	pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
	pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'	
readerPixelOnly = TMVA.Reader()
print 'test a'
readerPixelStrips = TMVA.Reader()
print 'test b'
prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
print 'test c'
prepareReaderPixel_loose(readerPixelOnly, pixelXml)


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
		hHt.Fill(c.HTOnline)
		#if not PassTrig(c, 'MhtMet6pack'): continue
		if not PassTrig(c, trigkey): continue
		#print ientry, c.MHT, PassTrig(c, 'MhtMet6pack')		
	else:	
	  hHt.Fill(c.madHT)
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


	#if not c.JetID: continue

	if isdata: 
		if not passesUniversalDataSelection(c): continue
	else:
		if not passesUniversalSelection(c): continue
                

	#basicTracks = []
	disappearingTracks = []
	promptCRTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):

		if not track.Pt() > 10 : continue
		if not abs(track.Eta()) < 2.4: continue
		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isBaselineTrack(track, itrack, c, hMask): continue
				
		#basicTracks.append([track,c.tracks_charge[itrack], itrack])		
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue   
		
		
		pixelOnly = bool(c.tracks_nValidPixelHits[itrack]>0 and c.tracks_nValidTrackerHits[itrack]==c.tracks_nValidPixelHits[itrack])
		if pixelOnly: moh = 12
		else: moh = min(11,c.tracks_nMissingOuterHits[itrack])
				  
		dtstatus, mva = isPenultimateTrack(track, itrack, c, readerPixelStrips,moh)# could use mva
		if not dtstatus>0: continue
		
		drlep = 99
		ismu = False
		for ilep, lep in enumerate(c.Muons): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.1: 
				ismu = True
				break            
		if ismu: continue 
				
	
		
		istightest = isTightestTrack(c,track, itrack)
		ispromptcr = not istightest

		if istightest: disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], moh, itrack])
		if ispromptcr: promptCRTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], moh, itrack])		
		
		if istightest: print ientry, 'found disappearing track w pT =', track.Pt(), dtstatus
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
		#pixelOnly = bool(c.tracks_nValidPixelHits[itrack]>0 and c.tracks_nValidTrackerHits[itrack]==c.tracks_nValidPixelHits[itrack])


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
		drmin = 999
		for crel in promptCRTracks:
			dr_ = crel[0].DeltaR(lep)
			if dr_<drmin:
				drmin = dr_
				if drmin<0.01: 
					break
		if drmin<0.01: continue #non-orthogonal set of CR electrons from good electrons
		if lep.Pt()>candPtCut: RecoElectrons.append([lep, ilep])	
		
		'''
		if isMatched2(ele, genels, 0.02):
			print ientry, 'this CR electron determined to be an electron'
		else:
			print ientry, 'this CR electron AINT no electron', c.Electrons_MTW[ilep]		
		'''
		
	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if debugmode: print ientry, ilep, 'ele with Pt' , lep.Pt()
		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not abs(lep.Eta())<2.4: continue
		if debugmode: print ilep, 'passed eta and Pt'
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_tightID[ilep]: continue
		if debugmode: print ilep, 'passed that nice tight id'
		drmin = inf
		matchedTrk = TLorentzVector()
		drmin = 999
		for crel in promptCRTracks:
			dr_ = crel[0].DeltaR(lep)
			if dr_<drmin:
				drmin = dr_
				if drmin<0.01: 
					break
		if drmin<0.01: continue #non-orthogonal set of CR Muons from good Muons
		if lep.Pt()>candPtCut: RecoMuons.append([lep, ilep])	



	singlePromptCREvent_ = len(promptCRTracks) >=1
	presentDisTrkEvent = len(disappearingTracks) >=1# and len(RecoElectrons) ==0 and len(RecoMuons)==0 ##try commenting out last two

	if not (singlePromptCREvent_ or presentDisTrkEvent): continue

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) 
		
	if isdata: #set for big hadd of all data, but *assumes all datasets have the same lumi*
		weight = 1       
		if ismet: 
			if not (len(RecoElectrons)+len(RecoMuons)==0): continue
		if ismu: 
			if not (len(RecoMuons)>0 and len(RecoElectrons)==0): continue			
		if isel: 
			if not (len(RecoElectrons)>0): continue
						
	elif len(RecoElectrons)+len(RecoMuons)>0: 
		weight = c.CrossSection*c.puWeight
	else: 
		weight = c.CrossSection*c.puWeight*gtrig.Eval(c.MHT)

	if isdata: hHtWeighted.Fill(c.HTOnline,weight)
	else: hHtWeighted.Fill(c.madHT,weight)	


	for promptcrthing in promptCRTracks:
		dtproxy, dtstatus, dedxPixel, moh, pcridx = promptcrthing
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

		analysisElectrons = RecoElectrons
		analysisMuons = RecoMuons

		pt = dtproxy.Pt()
		eta = abs(dtproxy.Eta())    

	
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74))
		if log10dedxmass!=log10dedxmass: log10dedxmass = -10
		
		
		if len(analysisElectrons)>0: 
			mT = c.Electrons_MTW[analysisElectrons[0][1]]
			if c.Electrons_charge[analysisElectrons[0][1]]*c.tracks_charge[pcridx]==-1: invmass = (analysisElectrons[0][0]+dtproxy).M()
			else: invmass = 999			
		elif len(analysisMuons)>0: 
			mT = c.Muons_MTW[analysisMuons[0][1]]
			print 'hello, c.tracks_charge[pcridx]', pcridx, c.tracks_charge[pcridx]
			if c.Muons_charge[analysisMuons[0][1]]*c.tracks_charge[pcridx]==-1: invmass = (analysisMuons[0][0]+dtproxy).M()
			else: invmass = 999			
		else: 
			invmass = 999
			mT = 999
		
			
		#           ['Ht',    'Mht',              'NJets',       'BTags',            'NTags',     'Moh','MinDPhiMhtJets','DeDxAverage','NElectrons', 'NMuons', 'InvMass', 'LepMT','TrkPt','TrkEta', 'Log10DedxMass','BinNumber', 'Met']
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags, 1+len(disappearingTracks), moh, mindphi, dedxPixel,len(RecoElectrons), len(RecoMuons), invmass, mT, pt,eta,log10dedxmass]		
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])
		trigcor = 1#gtrig.Eval(adjustedMht.Pt())/gtrig.Eval(c.MHT)

		#print ientry, 'before filling', dedxPixel, fv
		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist_):
				hname = 'El'+regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname):
					fillth1(histoStructDict[hname].Control,fv[ivar], weight)
							

						
	if presentDisTrkEvent:
		dt, status, dedxPixel, moh, itrack = disappearingTracks[0]
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
		
		#           ['Ht',    'Mht',              'NJets',       'BTags',            'NTags',   'Moh','MinDPhiMhtJets','DeDxAverage','NElectrons', 'NMuons', 'InvMass', 'LepMT','TrkPt','TrkEta','Log10DedxMass','BinNumber', 'Met']			
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets,adjustedBTags,len(disappearingTracks), moh, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta,log10dedxmass]
		fv.append(getBinNumber(fv))
		fv.extend([c.MET])		
		for regionkey in regionCuts:
		
			if selectionFeatureVector(fv,regionkey,'Mht'): fillth2(hEtaVsPhiDT[regionkey], phi, eta)
			for ivar, varname in enumerate(varlist_):
					if selectionFeatureVector(fv,regionkey,varname):
							if isPromptEl: 
								fillth1(histoStructDict['El'+regionkey+'_'+varname].Truth,fv[ivar], weight)								
							elif isPromptMu: 
								fillth1(histoStructDict['Mu'+regionkey+'_'+varname].Truth,fv[ivar], weight)
							elif isPromptPi: 
								fillth1(histoStructDict['Pi'+regionkey+'_'+varname].Truth,fv[ivar], weight)
							else:
								fillth1(histoStructDict['Fake'+regionkey+'_'+varname].Truth,fv[ivar], weight)


fnew.cd()
writeHistoStruct(histoStructDict)
for key_ in hEtaVsPhiDT: hEtaVsPhiDT[key_].Write()
hHt.Write()
hHtWeighted.Write()
hMtPionMatched.Write()
hMtPionUnMatched.Write()
print 'just created', fnew.GetName()
fnew.Close()

