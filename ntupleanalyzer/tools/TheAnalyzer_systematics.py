'''
---------------------BR: 100%-----------------------
/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_10cm/*/*.root
python tools/TheAnalyzerWithDeDx.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIAutumn18FSv2.SMS-T2tbv2-LLChipm-ctau10to200*.root"
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root
#python tools/TheAnalyzerWithDeDxLowMht.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_40000-*.root"

#higgsino file
compare fast and full for higgsinos

/nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Full/ntuple_sidecar/higgsino94xfull_susyall_mChipm115GeV_dm0p268GeV_pu35_part27of100_RA2AnalysisTree.root 
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

#for q quick higgsino test run:
#python tools/TheAnalyzer_systematics.py --fnamekeyword "/nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Fast/ntuple_sidecar/higgsino94x_susyall_mChipm200GeV_dm0p3GeV_pu35_part*.root" --nfpj 999 --outdir bay_PureHiggsino
#python tools/TheAnalyzer_systematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3*/RunIIAutumn18FSv2.SMS-T2tbv2-LLChipm-ctau10to200*.root" --nfpj 10 --outdir bay_T2tb_2018

#python tools/TheAnalyzer_systematics.py --fnamekeyword  "/nfs/dust/cms/user/singha/FullSim/final_ext/NtupleProduction20June/Signal200cm_aug/g2100_chi400_27_200970_step4_50miniAODSIM_112_RA2AnalysisTree.root"
#set up systematics
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/lib_systematics.py')
readerBtag = prepareReaderBtagSF()


doControlRegions = True

thebinning = binning
thebinning['MatchedCalo'] = [100,0,100]
binning['FakeCrNr'] = [6,-3,3]
debugmode = False
exomode = False
fnameprefire = 'usefulthings/Map_Jet_L1IsoEG30eff_bxm1_looseJet_SingleMuon_Run2017F.root'

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_230000-FCD9083D-3E88-E911-B3D1-0CC47A7EEE76_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_50cm/July5-SUMMER19sig/g1700_chi1550_27_200970_step4_50miniAODSIM_*_RA2AnalysisTree.root"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--updateevery", type=int, default=1000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-jecvar", "--jecvar", type=str, default='Nom',help="")
parser.add_argument("-numberOfFilesPerJob", "--nfpj", type=int, default=100)
parser.add_argument("-outdir", "--outdir", type=str, default='testout')
args = parser.parse_args()
nfpj = args.nfpj
filenames = args.fnamekeyword
if ',' in filenames: inputFiles = filenames.split(',')
else: inputFiles = glob(filenames)
analyzer = args.analyzer
updateevery = args.updateevery
verbose = False
outdir = args.outdir

is2016, is2017, is2018 = True, False, False
isdata = 'Run20' in filenames
if 'Run2016' in filenames or 'Summer16' in filenames or 'aksingh' in filenames: 
	is2016, is2017, is2018 = True, False, False
elif 'Run2017' in filenames or 'Fall17' in filenames or 'somethingelse' in filenames: 
	is2016, is2017, is2018 = False, True, False
elif 'Run2018' in filenames or 'Autumn18' in filenames or 'somthin or other' in filenames: 
	is2016, is2017, is2018 = False, True, True

if is2016: phase = 0
else: phase = 1

candPtCut = 25
candPtUpperCut = 6499
hiptcut = 40

if is2016: 
	BTAG_deepCSV = 0.6321
if is2017: 
	BTAG_deepCSV = 0.4941
if is2018: 
	BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV

####scale factors needed for actual interpretation with 17, 18 data
#usefulthings/signal_scalefactor.root



from CrossSectionDictionary import *
if 'Lifetime_' in filenames or 'Signal' in filenames or 'T1' in filenames: model = 'T1'
elif 'iggsino' in filenames:  model = 'PureHiggsino'
elif 'T2bt' in filenames or 'T2tb' in filenames: model = 'T2tt'
else: model = 'Other'
print 'were considering model', model
loadCrossSections(model)
hard_coded_higgsino_events_per_file = 20000# shoot, can't get this info from the ntuple
newfileEachSignal = True
if model=='PureHiggsino': newfileEachSignal = False


#counter histogram:
if outdir=='': outdir = 'bay_'+model



identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier


calib_version = '-SingleMuon'
calib_version = ''# Sang-Il's new key names
if 'Run20' in identifier: 
	keyforcalibs = identifier.split('-')[0].replace('skims','').replace('skim','')+calib_version
	dedxcalib_barrel = DedxCorr_Pixel_barrel[keyforcalibs]
	dedxcalib_endcap = DedxCorr_Pixel_endcap[keyforcalibs]
elif 'Summer16' in identifier: 
	dedxcalib_barrel = DedxCorr_Pixel_barrel['Summer16']
	dedxcalib_endcap = DedxCorr_Pixel_endcap['Summer16']
elif 'Fall17' in identifier: 
	dedxcalib_barrel = DedxCorr_Pixel_barrel['Fall17']
	dedxcalib_endcap = DedxCorr_Pixel_endcap['Fall17']
else: 
	dedxcalib_barrel = 1.0
	dedxcalib_endcap = 1.0	


doDedxSmear = False
if not isdata :
	doDedxSmear = True
	fsmear_barrel, fsmear_endcap = Load_DedxSmear(1)
	
	
f_dxydzcalibration = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/dxydzcalibration.root')
if 'Fall17' in identifier or 'Autumn18' in identifier:
		vtx_calibs = [f_dxydzcalibration.Get('g_calibratedxy'), f_dxydzcalibration.Get('g_calibratedz')]
else:
	vtx_calibs = []
	





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


if not newfileEachSignal:
	newfname = 'Hists_'+identifier+'.root'
	if not os.path.isdir(outdir): 	
		os.system('mkdir '+outdir)
	fnew_ = TFile(outdir+'/'+newfname,'recreate')
	print 'creating file', fnew_.GetName()


mdp= 0.3
inf = 9999999
lowht = 0

callShort = 15 
callLong = 20



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
	
	
	
print 'calhLong, calmLong', calhLong, calmLong
mvaminShort = min([mvaPromptShortLoose, mvaFakeShortLoose])
mvaminLong  = min([mvaPromptLongLoose,  mvaFakeLongLoose] )
	

	
#varlist_                              = ['Ht',     'Mht',  'NJets', 'BTags', 'NTags', 'NPix', 'NPixStrips', 'MinDPhiMhtJets', 'DeDxAverage', 'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',    'MatchedCalo', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',  'MTauTau',     'LepPt', 'BinNumber','DrJetDt','MinDPhiMhtHemJet','Log10DedxMass']
regionCuts = {}
varlist_                               = ['Ht',     'Mht',  'NJets', 'BTags', 'NTags', 'NPix','NPixStrips','MinDPhiMhtJets','DeDxAverage',    'NElectrons', 'NMuons', 'InvMass', 'LepMT',   'TrkPt',     'TrkEta',    'MatchedCalo', 'IsMuMatched', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'MtDtMht',  'MissingOuterHits',  'LepPt',  'DrJetDt', 'BinNumber','MinDPhiMhtHemJet','MTauTau','Log10DedxMass']#]#'Log10DedxMass'


regionCuts['ShortBaselineSystNom']     = [(0,inf), (30,inf), (1,inf), (0,inf), (1,inf), (1,inf), (0,0),     (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (candPtCut,inf), (0,2.4),  (0,callShort),   (0,0),     (-inf,inf),   (0,inf), (mvaShortTight,inf),    (20,inf),         (-inf,inf),     (40,inf),    (0.2,inf)]
regionCuts['LongBaselineSystNom']      = [(0,inf), (30,inf), (1,inf), (0,inf), (1,inf), (0,inf), (1,inf),   (mdp,inf),       (0,inf),         (0,inf),     (0,inf),  (140,inf), (110,inf), (hiptcut,inf),   (0,2.4),  (0,callLong),   (0,0),      (-inf,inf),   (0,inf), (mvaLongTight,inf),     (20,inf),         (2,inf),        (40,inf),    (0.2,inf)]
	
dedxidx = varlist_.index('DeDxAverage')
srindex = varlist_.index('BinNumber')
mcalidx = varlist_.index('MatchedCalo')
statidx = varlist_.index('DtStatus')
dphiidx = varlist_.index('DPhiMhtDt')
mvaidx = varlist_.index('LeadTrkMva')

regionkeys = regionCuts.keys()
for key in regionkeys:
	break

	#for bkg control regions
	'''
	newlist2 = list(regionCuts[key])
	newlist2[mcalidx] = (calm,calh)
	newlist2[mvaidx] = (mvaLoose,inf)		
	newkey = key.replace('SystNom','CaloSidebandSystNom')
	regionCuts[newkey] = newlist2
	'''


#collectionsysts = ['JecNom','JecUp','JecDown']
weightsysts = ['BTagUp','BTagDown','IsrUp','IsrDown','JecUp','Prefire']

regionkeys = regionCuts.keys()
for key in regionkeys:
	for syst in weightsysts: 
		newkey = key.replace('Nom',syst)
		regionCuts[newkey] = list(regionCuts[key])



ncuts = 22
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
		print 'histname', histname
	
print 'histoStructDict', histoStructDict.keys()

	
if model=='PureHiggsino':

	print 'filenames', inputFiles[0]
	print 'next thing', inputFiles[0].split('/')[-1]	
	print 'big thing', inputFiles[0].split('/')[-1].split('mChipm')[-1].split('GeV')[0]
	print 'last thing', inputFiles[0].split('/')[-1].split('mChipm')[-1]	
	mothermass = float(inputFiles[0].split('/')[-1].split('mChipm')[-1].split('GeV')[0])
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
print 'inputFiles', inputFiles
for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)

nentries = c.GetEntries()
#nentries = 100

c.Show(0)


fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal13to30_Data2016.root')	
hMask = fMask.Get('h_Mask_allyearsLongBaseline_EtaVsPhiDT')

if exomode: hMask = ''


fprefiring = TFile(fnameprefire)
hprefiring = fprefiring.Get('prefireEfficiencyMap')
hprefireDerived = hprefiring.GetPassedHistogram()
xaxprefiring = hprefireDerived.GetXaxis()
yaxprefiring = hprefireDerived.GetYaxis()
	

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


import time
t1 = time.time()
i0=0

nnotjet, totdt, totmt, passmt, passdt = 0, 0, 0, 0, 0

mcpass, mctot = 0, 0

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


	if newfileEachSignal:
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
				exit(0)
			print 'creating new file based on', orderedmasses
			newfname = 'Hists'
			for ip, susypid in enumerate(orderedmasses):
				print susybypdg[orderedmasses[ip][0]], orderedmasses[ip][1]
				newfname+='_'+susybypdg[orderedmasses[ip][0]]+str(orderedmasses[ip][1]).split('.')[0]
			newfname+='_time'+str(round(time.time(),6)).replace('.','p').replace('Chi1pm','Chi1ne')+'.root'
			if not os.path.isdir(outdir): os.system('mkdir '+outdir)
			fnew_ = TFile(outdir+'/'+newfname,'recreate')
			print 'creating file', fnew_.GetName()		
			print 'from', susymasses
			exit(0)		
			hHt = TH1F('hHt','hHt',200,0,10000)
			hHtWeighted = TH1F('hHtWeighted','hHtWeighted',200,0,10000)
			indexVar = {}
			for ivar, var in enumerate(varlist_): indexVar[var] = ivar
			#histoStructDict = {}
			for region in regionCuts:
				for var in varlist_:
					histname = region+'_'+var
					histoStructDict[histname] = mkHistoStruct(histname, thebinning)
								
			if 'T1' in model or 'T2tt' in model:
				mothermass = orderedmasses[0][1]#filenames.split('/')[-1].split('_')[0].replace('Higgsino','PLACEHOLDER').replace('g','').replace('*','').replace('PLACEHOLDER','Higgsino')
				xsecpb = CrossSectionsPb[model][str(int(5*round(mothermass/5)))]
				
				print 'got xsec', xsecpb, 'for mothermass', str(int(5*round(mothermass/5)))
			else:
				xsecpb = 1
				
			
			
					
	if not (model=='PureHiggsino'): hHt.Fill(c.HT)
			
	
	#can't we just put a loop here?
	for jecup in [False, True]:
				
		disappearingTracks = []    
		nShort, nLong = 0, 0
		for itrack, track in enumerate(c.tracks):
			if not track.Pt() > 15 : continue		
			#if not abs(track.Eta()) < 2.4: continue
			#if not abs(track.Eta()) < 2.2: continue
			if not abs(track.Eta()) < 2.0: continue		
		
		
			ischargino = False
			for igp, gp in enumerate(c.GenParticles):
				if not abs(c.GenParticles_PdgId[igp])==1000024: continue	
				if not abs(c.GenParticles_LabXYmm[igp]>25): continue
				dr = gp.DeltaR(track)			
				if dr<0.04:
					ischargino = True
					print 'got chargino', c.GenParticles_LabXYmm[igp]
					break
			if not ischargino: continue	
		
			totdt+=1
				
									
			if not isBaselineTrackLoosetag(track, itrack, c, hMask):  continue
			if not (track.Pt() > candPtCut): continue     	# and track.Pt()<candPtUpperCut
	
			dtstatus, mva = isDisappearingTrack_FullyInformed(track, itrack, c, readerPixelOnly, readerPixelStrips, [mvaminShort,mvaminLong], vtx_calibs)
			if dtstatus==0: continue
		
	
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
				
			isjet = False
			if dtstatus==1: ##short track
				jt = 30
				drcut=0.4
			else: 
				jt = 30
				drcut=0.4
			for ijet, jet_ in enumerate(c.Jets):
				jet = jet_.Clone()
				if jecup: jet*=1.0/(1-c.Jets_jecUnc[ijet])
				if (jet.Pt()>jt and jet.DeltaR(track)<drcut):
					isjet = True
					break	
		
			dtisrecomu = dtisrecomu and isjet
			if isjet and not dtisrecomu: continue
			if not (c.tracks_passPFCandVeto[itrack] or dtisrecomu): continue
		
			#if c.tracks_trackJetIso[itrack]<0.2: 
			#	continue		
		
			dedx = -1
			if dtstatus==1: 
				nShort+=1
				dedx = c.tracks_deDxHarmonic2pixel[itrack]
			if dtstatus==2: 
				nLong+=1			
				dedx = c.tracks_deDxHarmonic2pixel[itrack]
			if abs(track.Eta())<1.5: dedxcalib = dedxcalib_barrel
			else: dedxcalib = dedxcalib_endcap
	
			if exomode:
				print 'here we are'
				if not passesExtraExoCuts(track, itrack, c): continue
				print 'we made it'
		  
		
			dedx = dedxcalib*c.tracks_deDxHarmonic2pixel[itrack]
			if not isdata and doDedxSmear:
				smearfactor = fsmear_barrel.GetRandom()
				dedx = dedx + smearfactor
		
			passdt+=1
		
			#print 'got one! bringing the total up to', 1.0*passdt/totdt			
			disappearingTracks.append([track,dtstatus,dedx, mva, dtisrecomu, c.tracks_nMissingOuterHits[itrack], itrack])		


		if not len(disappearingTracks)>0: continue

		RecoElectrons = []
		for iel, ele in enumerate(c.Electrons):
			if debugmode: print ientry, iel,'ele with Pt' , ele.Pt()
			if not abs(ele.Eta())<2.4: continue
			if debugmode: print 'passed eta and Pt'
			if not c.Electrons_passIso[iel]: continue
			if not c.Electrons_tightID[iel]: continue
			if ele.Pt()>40: RecoElectrons.append([ele, iel])


		RecoMuons = []
		for ilep, lep in enumerate(c.Muons):
			if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
			if not abs(lep.Eta())<2.4: continue
			if verbose: print 'passed eta and Pt'
			if not c.Muons_passIso[ilep]: continue
			if not c.Muons_mediumID[ilep]: continue
			if lep.Pt()>40: RecoMuons.append([lep,ilep])    


		metvec = TLorentzVector()
		metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
			  
			  
		dt, status, dedxPixel, mvascore, dtisrecomu, MOH, itrack = disappearingTracks[0]

		pt = dt.Pt()
		eta = abs(dt.Eta()) 
		log10dedxmass = TMath.Log10(TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74))
	
	
	
	
	

		adjustedBTags = 0        
		adjustedJets = []
		adjustedHt = 0
		adjustedMht = TLorentzVector()
		adjustedMht.SetPxPyPzE(0,0,0,0)
		for ijet, jet_ in enumerate(c.Jets):
			jet = jet_.Clone()
			if jecup: jet*=1.0/(1-c.Jets_jecUnc[ijet])
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

		newmetvec = metvec.Clone()
		newmetvec-=dt
		if len(RecoElectrons)>0: 
			#mT = c.Electrons_MTW[RecoElectrons[0][1]]
			mT = TMath.Sqrt(2*RecoElectrons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoElectrons[0][0].DeltaPhi(adjustedMht))))
			dt__ = dt.Clone()
			mtautau = mttsam1(newmetvec, RecoElectrons[0][0], dt__)
			if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt__).M()
			else: invmass = 999		
			leppt = RecoElectrons[0][0].Pt()
		elif len(RecoMuons)>0: 
			#mT = c.Muons_MTW[RecoMuons[0][1]]
			mT = TMath.Sqrt(2*RecoMuons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoMuons[0][0].DeltaPhi(adjustedMht))))
			dt__ = dt.Clone()
			mtautau = mttsam1(newmetvec, RecoMuons[0][0], dt__)
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
		matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#/TMath.CosH(c.tracks[disappearingTracks[0][-1]].Eta())
		#matchedcalofrac = 100*c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]/(dt.P())
	
		if abs(disappearingTracks[0][1])==1: matchedcalofrac = max(matchedcalo,100*matchedcalo/(dt.P()))
		else: matchedcalofrac = 100*matchedcalo/(dt.P())

		dphiMhtDt = abs(adjustedMht.DeltaPhi(dt))
		mhtWithTrack = adjustedMht.Clone()
		mhtWithTrack-=dt
		mtDtMht = TMath.Sqrt(2*dt.Pt()*mhtWithTrack.Pt()*(1-TMath.Cos(mhtWithTrack.DeltaPhi(dt))))
	
		if adjustedMht.Pt()>100:
			totmt+=1
			#if dphiMhtDt>0.05: passmt+=1
			#if c.tracks_trackJetIso[itrack]>0.3: passmt+=1
			if bool(c.tracks_trackJetIso[itrack]>0.2): passmt+=1
	
	
		#new
		fv = [adjustedHt,   adjustedMht.Pt()   ,adjustedNJets-len(RecoElectrons)-len(RecoMuons),adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta, matchedcalofrac,          dtisrecomu, status, dphiMhtDt,             mvascore,    mtDtMht,         MOH,          leppt, DrJetDt]#'''*TMath.CosH(eta)
		fv.append(getBinNumber(fv))
		fv.extend([GetMinDeltaPhiMhtHemJets(adjustedJets,adjustedMht),mtautau,log10dedxmass])
	
	
		##old	
		#fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets-len(RecoElectrons)-len(RecoMuons),adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi,dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta, matchedcalofrac, status, dphiMhtDt, mvascore, mtDtMht, mtautau, leppt]
		#fv.append(getBinNumber(fv))
		#fv.extend([DrJetDt, GetMinDeltaPhiMhtHemJets(adjustedJets,adjustedMht),log10dedxmass])


		if abs(disappearingTracks[0][1])==1:
			mctot+=1
			if matchedcalofrac<15: mcpass+=1
			#print 'mc eff', 1.0*mcpass/mctot
			#for ifv in range(len(fv)): print varlist_[ifv], fv[ifv]
	
	
		if isdata: weight = 1
		elif len(RecoElectrons)+len(RecoMuons)>0: 
			weight = 0.9*xsecpb#*c.puWeight
		else: 
			weight = xsecpb*gtrig.Eval(c.MHT)#*c.puWeight
			#weight = 1.0
		
		weight*=1.25####only for estimating everything with 2016!
	
	
		pfweight = 1.0
		for jet in c.Jets:
			pt, eta = xaxprefiring.FindBin(jet.Pt()), yaxprefiring.FindBin(abs(jet.Eta()))
			gbin = hprefireDerived.GetBin(pt, eta, -1)
			pfweight*=(1-hprefiring.GetEfficiency(gbin))
	
		hHtWeighted.Fill(c.HT,weight)
	
		#print fv
		#for ifv in range(len(fv)): print ifv, varlist_[ifv], fv[ifv]	
		sfbtagnom = get_btag_weight(c,nSigmaBtagSF=0,nSigmaBtagFastSimSF=0,isFastSim=0,readerBtag=readerBtag)
		sfbtagup = get_btag_weight(c,nSigmaBtagSF=1,nSigmaBtagFastSimSF=0,isFastSim=0,readerBtag=readerBtag)
		sfbtagdown = get_btag_weight(c,nSigmaBtagSF=-1,nSigmaBtagFastSimSF=0,isFastSim=0,readerBtag=readerBtag)

	
		isrnom = get_isr_weight(c,0)
		isrup = get_isr_weight(c,1)
		isrdown = get_isr_weight(c,-1)

		#if c.MHT>150: print 'njetsISR', c.NJetsISR, c.NJets, 'the noms', sfbtagnom, isrnom, sfbtagnom*isrnom
		for regionkey in regionCuts:
			if not 'Nom' in regionkey: continue
			for ivar, varname in enumerate(varlist_):
				if selectionFeatureVector(fv,regionkey,varname):
					#weightsysts = ['Nom','BTagUp','BTagDown','IsrUp','IsrDown']			
					if jecup: 
						print 'we are in uppyland'
						fillth1(histoStructDict[regionkey.replace('Nom','JecUp')+'_'+varname].Truth,fv[ivar], sfbtagnom*isrnom*weight)
						continue
					fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar], sfbtagnom*isrnom*weight)						
					fillth1(histoStructDict[regionkey.replace('Nom','BTagUp')+'_'+varname].Truth,fv[ivar], sfbtagup*isrnom*weight)
					fillth1(histoStructDict[regionkey.replace('Nom','BTagDown')+'_'+varname].Truth,fv[ivar], sfbtagdown*isrnom*weight)
					fillth1(histoStructDict[regionkey.replace('Nom','IsrUp')+'_'+varname].Truth,fv[ivar], sfbtagnom*isrup*weight)
					#print 'going for', regionkey.replace('Nom','IsrDown')+'_'+varname
					fillth1(histoStructDict[regionkey.replace('Nom','IsrDown')+'_'+varname].Truth,fv[ivar], sfbtagnom*isrdown*weight)
					fillth1(histoStructDict[regionkey.replace('Nom','Prefire')+'_'+varname].Truth,fv[ivar], pfweight*sfbtagnom*isrnom*weight)
			



fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict, 'truth')
print 'just created', fnew_.GetName()
fnew_.Close()	
fMask.Close()
os.abort()



