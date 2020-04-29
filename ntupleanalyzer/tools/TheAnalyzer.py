'''
---------------------BR: 100%-----------------------
/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_10cm/*/*.root
python tools/TheAnalyzerWithDeDx.py --fnamekeyword "/nfs/dust/cms/user/singha/FullSim/final_ext/NtupleProduction20June/Signal200cm_aug/g2100_chi400_27_200970_step4_50miniAODSIM_112_RA2AnalysisTree.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root
#python tools/TheAnalyzerWithDeDxLowMht.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_40000-*.root"
'''
import os, sys
import time
import numpy as np
from ROOT import *
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
from random import shuffle
import random
from array import array
gROOT.SetStyle('Plain')
#gROOT.SetBatch(1)



thebinning = binning
thebinning['MatchedCalo'] = [100,0,100]
binning['FakeCrNr'] = [6,-3,3]
debugmode = False

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_230000-FCD9083D-3E88-E911-B3D1-0CC47A7EEE76_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_50cm/July5-SUMMER19sig/g1700_chi1550_27_200970_step4_50miniAODSIM_*_RA2AnalysisTree.root"
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


is2016, is2017, is2018 = True, False, False
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
if is2018: BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV




from CrossSectionDictionary import *
if 'Lifetime_' in inputFileNames or 'Signal' in inputFileNames or 'T1' in inputFileNames: model = 'T1'
elif 'iggsino' in inputFileNames:  model = 'PureHiggsino'
elif 'T2bt' in inputFileNames: model = 'T2tt'
else: model = 'Other'
print 'were considering model', model
loadCrossSections(model)
hard_coded_higgsino_events_per_file = 20000# shoot, can't get this info from the ntuple
newfileEachsignal = True
if model=='PureHiggsino': newfileEachsignal = False


#counter histogram:
holdingbay = 'bay_'+model

	

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier



calib_version = '-SingleElectron'
if 'Run201' in identifier: 
	keyforcalibs = identifier.split('-')[0].replace('skims','').replace('skim','')+calib_version
	dedxcalib_barrel = datacalibdict_Run2016_barrel[keyforcalibs]/datacalibdict_Run2016_barrel['Summer16']
	dedxcalib_endcap = datacalibdict_Run2016_endcap[keyforcalibs]/datacalibdict_Run2016_barrel['Summer16']
elif 'Summer16' in identifier: 
	dedxcalib_barrel = 1.
	dedxcalib_endcap = datacalibdict_Run2016_endcap['Summer16']/datacalibdict_Run2016_barrel['Summer16']
else: 
	dedxcalib_barrel = 1.0
	dedxcalib_endcap = 1.0	
	
thejet = TLorentzVector()
	
'''
if 'Run201' in identifier: 
	dedxcalib_barrel = datacalibdict_SingleElectron_barrel[identifier.split('-')[0]]/datacalibdict_SingleElectron_barrel['Summer16']
	dedxcalib_endcap = datacalibdict_SingleElectron_endcap[identifier.split('-')[0]]/datacalibdict_SingleElectron_barrel['Summer16']
elif 'Summer16' in identifier: 
	dedxcalib_barrel = 1.
	dedxcalib_endcap = datacalibdict_SingleElectron_endcap['Summer16']/datacalibdict_SingleElectron_barrel['Summer16']
else: 
	dedxcalib_barrel = 1.0
	dedxcalib_endcap = 1.0	
'''

ftrig = TFile(os.environ['CMSSW_BASE']+'/src/analysis/triggerefficiency/susy-trig-plots_amag.root')#triggersRa2bRun2_v4_withTEffs.root')
ttrig = ftrig.Get('tEffhMetMhtRealXMht_run2;1')
hpass = ttrig.GetPassedHistogram().Clone('hpass')
htotal = ttrig.GetTotalHistogram().Clone('htotal')
gtrig = TGraphAsymmErrors(hpass, htotal)


if not newfileEachsignal:
	newfname = 'Hists_'+identifier+'.root'
	if not os.path.isdir(holdingbay): os.system('mkdir '+holdingbay)
	fnew_ = TFile(holdingbay+'/'+newfname,'recreate')
	print 'creating file', fnew_.GetName()


lowht = 0
inf = 999999
regionCuts = {}
#varlist_                        = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage','NElectrons', 'NMuons', 'InvMass', 'LepMT', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
regionCuts = {}
varlist_                                   = ['Ht',    'Mht',     'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage',  'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo', 'FakeCrNr', 'Log10DedxMass','BinNumber', 'Met']
#regionCuts['Baseline']                     = [(100,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),    (0.0,inf),       (-inf,inf),         (0,inf),   (0,inf),  (110,inf), (110,inf), (candPtCut,inf), (-2.4,2.4), (0,10),       (0,inf),    (-inf,inf),  (-inf,inf)]
regionCuts['Baseline']                     = [(lowht,inf), (0,inf),    (1,inf), (0,inf), (1,inf), (0,inf), (0,inf),  (0.0,inf),   (dedxcutLow,inf),         (0,inf),   (0,inf),  (110,inf), (100,inf), (candPtCut,inf), (0,2.4), (0,10),     (0,inf),    (-inf,inf),  (-inf,inf)]


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


def getBinNumber(fv):
	for binkey in binnumbers:
		foundbin = True
		for iwindow, window in enumerate(binkey):
			if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
		if foundbin: return binnumbers[binkey]
	return -1
		

#counter histogram:
hHt = TH1F('hHt','hHt',200,0,10000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',200,0,10000)
indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
	for var in varlist_:
		histname = region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname, thebinning)
		
if model=='PureHiggsino':
	mothermass = float(inputFileNames.split('/')[-1].split('mChipm')[-1].split('GeV')[0])
	higgsinoxsecfile = TFile('usefulthings/CN_hino_13TeV.root')
	if mothermass<150:
		xsecpb = 0.001*higgsinoxsecfile.Get('fit_nom_0').Eval(max(100,mothermass))
	elif mothermass>=150 and mothermass<200:
		xsecpb = 0.001*higgsinoxsecfile.Get('fit_nom_1').Eval(mothermass)
	elif mothermass>=200 and mothermass<300:
		xsecpb = 0.001*higgsinoxsecfile.Get('fit_nom_2').Eval(mothermass)	
	elif mothermass>=300 and mothermass<400:
		xsecpb = 0.001*higgsinoxsecfile.Get('fit_nom_3').Eval(mothermass)	
	elif mothermass>=400:
		xsecpb = 0.001*higgsinoxsecfile.Get('fit_nom_4').Eval(mothermass)					
	print 'xsec was', xsecpb
	for i in range(hard_coded_higgsino_events_per_file): hHt.Fill(555)
	higgsinoxsecfile.Close()

c = TChain("TreeMaker2/PreSelection")
for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)

nentries = c.GetEntries()
#nentries = 100



c.Show(0)


'''
fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
else: 
	#hMask = fMask.Get('hEtaVsPhiDTRun2016')
	hMask = ''
'''

fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to15.root')
hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')

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

orderedmasses = []
newfname = ''
print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if ientry%updateevery==0:
		print 'now processing event number', ientry, 'of', nentries
		if ientry==0: 
			for itrig, trigname in enumerate(c.TriggerNames):
				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]

	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	
	if newfileEachsignal:
		susymasses = []
		susies = []
		for igp, gp in enumerate(c.GenParticles):		
			if not abs(c.GenParticles_PdgId[igp])>1000000: continue
			#if c.GenParticles_Status[igp]==23: continue
			pid = abs(c.GenParticles_PdgId[igp])
			if not pid in susies:				
				susies.append(pid)
				susymasses.append([pid,round(gp.M(),2)])
						
		orderedmasses_ = sorted(susymasses, key=lambda x: x[1], reverse=True)
		orderedmasses_ = [orderedmasses_[0], orderedmasses_[-1]]
		
		if not orderedmasses==orderedmasses_:
			print 'looks like a model transition from', orderedmasses, 'to', orderedmasses_
			orderedmasses = orderedmasses_
			if not newfname=='':
				fnew_.cd()
				hHt.Write()
				hHtWeighted.Write()
				writeHistoStruct(histoStructDict, 'truth')
				print 'just created', fnew_.GetName()
				fnew_.Close()
			print 'creating new file based on', orderedmasses
			newfname = 'Hists'
			for ip, susypid in enumerate(orderedmasses):
				print susybypdg[orderedmasses[ip][0]], orderedmasses[ip][1]
				newfname+='_'+susybypdg[orderedmasses[ip][0]]+str(orderedmasses[ip][1]).split('.')[0]
			newfname+='_time'+str(round(time.time(),4)).replace('.','p')+'.root'
			if not os.path.isdir(holdingbay): os.system('mkdir '+holdingbay)
			fnew_ = TFile(holdingbay+'/'+newfname,'recreate')
			print 'creating file', fnew_.GetName()				
			hHt = TH1F('hHt','hHt',200,0,10000)
			hHtWeighted = TH1F('hHtWeighted','hHtWeighted',200,0,10000)
			indexVar = {}
			for ivar, var in enumerate(varlist_): indexVar[var] = ivar
			histoStructDict = {}
			for region in regionCuts:
				for var in varlist_:
					histname = region+'_'+var
					histoStructDict[histname] = mkHistoStruct(histname, thebinning)
									
			if 'T1' in model or 'T2tt' in model:
				mothermass = orderedmasses[0][1]#inputFileNames.split('/')[-1].split('_')[0].replace('Higgsino','PLACEHOLDER').replace('g','').replace('*','').replace('PLACEHOLDER','Higgsino')
				xsecpb = CrossSectionsPb[model][str(int(5*round(mothermass/5)))]
					
				print 'got xsec', xsecpb, 'for mothermass', str(int(5*round(mothermass/5)))
			else:
				xsecpb = 1
				
	signalweight = xsecpb
						
	if not (model=='PureHiggsino'): hHt.Fill(c.HT)
				
	'''
	#genchis = []
	#for igp, gp in enumerate(c.GenParticles):
	#	if not gp.Pt()>5: continue
	#	if not abs(c.GenParticles_PdgId[igp])==1000024: continue
	#	print igp, 'we got ', c.GenParticles_PdgId[igp], 'with pT=', gp.Pt(), gp.Eta()	
	#	genchis.append(gp)
	
	'''	
	basicTracks = []
	disappearingTracks = []    
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 10 : continue		
		if not abs(track.Eta()) < 2.4: continue
		#if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442):  continue
		if not isBaselineTrack(track, itrack, c, hMask): 
			continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack])
		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     	
		
		
		dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips)
		if dtstatus==0: continue
			
		drlep = 99
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
			drlep = min(drlep, lep.DeltaR(track))
			if drlep<0.1: 
				passeslep = False
				break            
		if not passeslep: 
			print 'losing this thing to a lepton', c.tracks_nMissingOuterHits[itrack]	
			continue
		isjet = False
		for jet in c.Jets:
			if not jet.Pt()>30: continue
			if jet.DeltaR(track)<0.4: 
				isjet = True
				thejet = jet
				break
		if isjet: 
			print 'losing to a jet', thejet.Pt()
			continue
			
		ischargino = False
		for igp, gp in enumerate(c.GenParticles):
			if not abs(c.GenParticles_PdgId[igp])==1000024: continue			
			dr = gp.DeltaR(track)			
			if dr<0.04:
				ischargino = True
				break
		if not ischargino: continue	
		
	
		'''
		print '=============charging at it with a particle with pdgid, pt =', c.GenParticles_PdgId[igp], c.GenParticles[igp].Pt(), c.GenParticles[igp].Eta()
		print 'while mother mass=', mothermass, 'dr', thegp.DeltaR(track)
		print 'parent id:', c.GenParticles_ParentId[igp]
		print 'this track had status', dtstatus
		'''
		#print '-------->>>>keeping this through thick', mothermass
		dedx = -1
		if dtstatus==1: 
			nShort+=1
			dedx = c.tracks_deDxHarmonic2pixel[itrack]
		if dtstatus==2: 
			nLong+=1			
			dedx = c.tracks_deDxHarmonic2pixel[itrack]
		if abs(track.Eta())<1.5: dedxcalib = dedxcalib_barrel
		else: dedxcalib = dedxcalib_endcap
		disappearingTracks.append([track,dtstatus,dedxcalib*c.tracks_deDxHarmonic2pixel[itrack], itrack])


	if not len(disappearingTracks)>0: continue
	
	
	RecoElectrons = []
	for iel, ele in enumerate(c.Electrons):
		if debugmode: print ientry, iel,'ele with Pt' , ele.Pt()
		if not abs(ele.Eta())<2.4: continue
		if debugmode: print 'passed eta and Pt'
		if not c.Electrons_passIso[iel]: continue
		if not c.Electrons_mediumID[iel]: continue
		if ele.Pt()>candPtCut: RecoElectrons.append([ele, iel])


	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
		if not abs(lep.Eta())<2.4: continue
		if verbose: print 'passed eta and Pt'
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_mediumID[ilep]: continue
		if lep.Pt()>candPtCut: RecoMuons.append([lep,ilep])    


	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
				  
	if len(disappearingTracks)>0: 
		dt = disappearingTracks[0][0]
		pt = dt.Pt()
		eta = abs(dt.Eta()) 
		dedx = disappearingTracks[0][2] 
		Log10DedxMass = TMath.Log10(TMath.Sqrt((dedx-3.01)*pow(c.tracks[disappearingTracks[0][3]].P(),2)/1.74))
	else: 
		print 'should never see this'
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
		if not abs(jet.Eta())<5.0: continue
		someoverlap = False
		for dt_ in disappearingTracks: 
			if jet.DeltaR(dt_[0])<0.4: 
				someoverlap = True
				break
		if someoverlap: continue
		adjustedMht-=jet		
		if not abs(jet.Eta())<2.4: continue
		adjustedJets.append(jet)			
		if c.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
		adjustedHt+=jet.Pt()
	adjustedNJets = len(adjustedJets)
	mindphi = 4
	for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 
	
	if len(RecoElectrons)>0: 
		mT = c.Electrons_MTW[RecoElectrons[0][1]]
		if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[disappearingTracks[0][-1]]==-1: invmass = (RecoElectrons[0][0]+dt).M()
		else: invmass = 999			
	elif len(RecoMuons)>0: 
		mT = c.Muons_MTW[RecoMuons[0][1]]
		if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[disappearingTracks[0][-1]]==-1: invmass = (RecoMuons[0][0]+dt).M()
		else: invmass = 999			
	else: 
		mT = 999
		invmass = 999	
	
	matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#/TMath.CosH(c.tracks[disappearingTracks[0][-1]].Eta())

	fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi,dedx, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta, matchedcalo, disappearingTracks[0][1],Log10DedxMass]
	fv.append(getBinNumber(fv))
	fv.append(c.MET)
	
	if isdata: weight = 1
	elif len(RecoElectrons)+len(RecoMuons)>0: 
		weight = 0.9*signalweight#*c.puWeight
	else: 
		weight = signalweight*gtrig.Eval(c.MHT)#*c.puWeight
		#weight = 1.0
	hHtWeighted.Fill(c.HT,signalweight)
		
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
print 'just created', fnew_.GetName()
fnew_.Close()	
fMask.Close()
os.abort()



