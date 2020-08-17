from ROOT import *
import os, sys
from glob import glob
import time
import numpy as np
import random
gROOT.SetStyle('Plain')
import json
#gROOT.SetBatch(1)



'''#after simplest condor
hadd -f testWJ.root output/smallchunks/SimpleAnalyzer_WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8*.root
hadd -f testTT.root output/smallchunks/SimpleAnalyzer_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8*.root
hadd -f testDY.root output/smallchunks/SimpleAnalyzer_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_*.root
python tools/ahadd.py -f output/totalweightedbkgsDataDrivenDataNoSmear.root output/smallchunks/Simple*Run2016*MET*NoZSmear.root
'''


codeproduct = 'SimpleHists'

execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
specialTauPiValidation = False

#defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_3*_RA2AnalysisTree.root"
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
verbose = False
sayalot = False
candPtCut = 30
candPtUpperCut = 6499
if SmearLeps4Zed_: kappasmearlevellabel = 'YesZSmear'
else: kappasmearlevellabel = 'NoZSmear'


mZ = 91
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

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier



newfname = codeproduct+'_'+identifier+'.root'
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])
moreargs = moreargs.replace(' ','').replace('--','-')
newfname = newfname.replace('.root',moreargs+'.root')
fnew_ = TFile(newfname,'recreate')
print 'creating file', fnew_.GetName()

hHt = TH1F('hHt','hHt',100,0,3000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',100,0,3000)
hHtWeighted.Sumw2()

hMtPionMatched = TH1F('hMtPionMatched','hMtPionMatched',50,0,200)
histoStyler(hMtPionMatched,kOrange+1)
hMtPionUnMatched = TH1F('hMtPionUnMatched','hMtPionUnMatched',50,0,200)
histoStyler(hMtPionUnMatched,kRed+1)



inf = 999999

regionCuts = {}
varlist_                     = ['Ht',     'Mht',     'NJets', 'BTags','MinDPhiMhtJets','NElectrons','NMuons', 'InvMass', 'LepMT', 'ElPt',     'ElEta',   'MuPt',      'MuEta']
#regionCuts['NoMetBaseline']  = [(0,inf),  (0,inf),   (1,inf), (0,inf),(0.4,inf),        (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
regionCuts['NoLBaseline']    = [(200,inf),(250,inf),   (1,inf), (0,inf),(0.4,inf),        (0,0),     (0,0),    (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
regionCuts['SElBaseline']    = [(200,inf),(0,inf),     (1,inf), (0,inf),(-inf,inf),       (1,1),     (0,inf),  (-inf,inf),(-inf,inf),(30,inf),  (-inf,inf),(-inf,inf),(-inf,inf)]
regionCuts['SMuBaseline']    = [(200,inf),(0,inf),     (1,inf), (0,inf),(-inf,inf),       (0,inf),   (1,1),    (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf),(30,inf),  (-inf,inf)]
regionCuts['DiElBaseline']   = [(200,inf),(0,inf),     (1,inf), (0,inf),(-inf,inf),       (2,2),     (0,inf),  (50,inf),(-inf,inf),(30,inf),  (-inf,inf),(-inf,inf),(-inf,inf)]
regionCuts['DiMuBaseline']   = [(200,inf),(0,inf),     (1,inf), (0,inf),(-inf,inf),       (0,inf),   (2,2),    (50,inf),(-inf,inf),(-inf,inf),(-inf,inf),(30,inf),  (-inf,inf)]

#regionCuts['SElHighNJetsBaseline']=[(0,inf),(280,inf), (3,inf), (0,inf),(0.4,inf),        (1,inf),   (0,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
#regionCuts['SMuHighNJetsBaseline']=[(0,inf),(280,inf), (3,inf), (0,inf),(0.4,inf),        (0,inf),   (1,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
#regionCuts['SElHighHTBaseline']=[(300,inf),(280,inf), (1,inf), (0,inf),(0.4,inf),        (1,inf),   (0,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
#regionCuts['SMuHighHTBaseline']=[(300,inf),(280,inf), (1,inf), (0,inf),(0.4,inf),        (0,inf),   (1,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
#regionCuts['SElRa2bBaseline']=[(300,inf),(280,inf), (3,inf), (0,inf),(0.4,inf),        (1,inf),   (0,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]
#regionCuts['SMuRa2bBaseline']=[(300,inf),(280,inf), (3,inf), (0,inf),(0.4,inf),        (0,inf),   (1,inf),  (-inf,inf),(-inf,inf),(-inf,inf),(-inf,inf)]





ncuts = 12

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
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
#nentries = 1000

c.Show(0)
#nentries = 5

def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
	iomits = []
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i>=ncuts: break
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
			return False
	return True


if 'TTJets_TuneCUET' in inputFileNames:  madranges = [(0,600)]
elif 'TTJets_HT' in inputFileNames: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneCUET' in inputFileNames: madranges = [(0, 100)]
elif 'WJetsToLNu_HT' in inputFileNames: madranges = [(100, inf)]
else: madranges = [(0, inf)]

if 'MET' in inputFileNames: trigkey = 'MhtMet6pack'
elif 'SingleMu' in inputFileNames: trigkey = 'SingleMuon'
elif 'SingleEl' in inputFileNames or 'SingleEG' in inputFileNames: trigkey = 'SingleElectron'


#madranges = [(0, inf)]
#print 'madranges', madranges
#exit(0)

import time
t1 = time.time()
i0=0

runs = {}
lastlumi = -1
lastrun = -1

print nentries, 'events to be analyzed'
for ientry in range(nentries):
	if verbose:
		if not ientry in [17681]: continue
	if ientry%verbosity==0:
		print 'now processing event number', ientry, 'of', nentries

	if verbose: print 'getting entry', ientry
	c.GetEntry(ientry) 
	if isdata: 
	
		runnum = c.RunNum
		lumisec = c.LumiBlockNum
		if runnum!=lastrun:
			if runnum not in runs:
				runs[runnum] = []
		if lumisec!=lastlumi:
			if lumisec not in runs[runnum]:
				runs[runnum].append(lumisec)
                                	
		weight = 1	
		fillth1(hHt,c.HTOnline)
	else: 
		weight = c.CrossSection#*c.puWeight#*gtrig.Eval(max(c.MHT,96.))
		#print 'gtrig.Eval(',str(c.MHT)+') =', gtrig.Eval(max(c.MHT,96.))
		fillth1(hHt, c.madHT)				

	if ientry==0:
		for itrig in range(len(c.TriggerPass)):
			print itrig, c.TriggerNames[itrig], c.TriggerPrescales[itrig], 'offline mht=', c.MHT
		c.Show(0)
		print '='*20
	


	#if not c.MHT>150: continue
	if isdata:
		if not passesUniversalDataSelection(c): continue
	else:
		if not passesUniversalSelection(c): continue
	
	if isdata:
		fillth1(hHtWeighted,c.HTOnline,weight)	
		#print ientry, c.MHT, PassTrig(c, 'MhtMet6pack')	
		if not PassTrig(c, trigkey): continue
	else:
	  isValidHtRange = False
	  for madrange in madranges:
		if (c.madHT>=madrange[0] and c.madHT<madrange[1]):
			isValidHtRange = True
			break 
	  if not isValidHtRange: continue#####this should be changed/fixed in Prompt code
	  
	  fillth1(hHtWeighted,c.madHT,weight)
	  

	RecoElectrons = []
	for ilep, lep in enumerate(c.Electrons):
		#if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not lep.Pt()>10: continue		
		if not abs(lep.Eta())<2.4: continue
		if (abs(lep.Eta()) > 1.4442 and abs(lep.Eta()) < 1.566): continue
		if not c.Electrons_passIso[ilep]: continue
		if not c.Electrons_tightID[ilep]: continue
		RecoElectrons.append([lep,ilep])

	RecoMuons = []
	for ilep, lep in enumerate(c.Muons):
		#if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
		if not lep.Pt()>10: continue			
		if not abs(lep.Eta())<2.4: continue	
		if (abs(lep.Eta()) > 1.4442 and abs(lep.Eta()) < 1.566): continue
		if not c.Muons_passIso[ilep]: continue
		if not c.Muons_tightID[ilep]: continue
		RecoMuons.append([lep,ilep])
		
	#if len(RecoMuons)>0 and RecoMuons[0][0].Pt()>30:
	#	print ientry, 'found nice muon', RecoMuons[0][0].Pt(), RecoMuons[0][0].Eta()
	

	if len(RecoElectrons)>0: elpt, eleta = RecoElectrons[0][0].Pt(), RecoElectrons[0][0].Eta()		
	else: elpt, eleta = -11, -11
	
	if len(RecoMuons)>0: mupt, mueta = RecoMuons[0][0].Pt(), RecoMuons[0][0].Eta()	
	else: mupt, mueta = -11, -11	

	adjustedMht = TLorentzVector()
	adjustedMht.SetPxPyPzE(0,0,0,0)
	adjustedJets = []
	for ijet, jet in enumerate(c.Jets):
		if not jet.Pt()>30: continue
		if not abs(jet.Eta())<5.0: continue####update to 2.4
		adjustedMht-=jet
		if not abs(jet.Eta())<2.4: continue####update to 2.4
		adjustedJets.append(jet)            

	adjustedNJets = len(adjustedJets)
	mindphi = 4
	for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht)))
	
	
	#if not abs(c.MHT-c.MET)<70: continue
	#if not c.HT>c.MHT: continue
		
	###if not isdata: weight*=max(0, gtrig.Eval(c.MHT))
	#if adjustedMht.Pt()<80:
	#	print 'mht', adjustedMht.Pt(), 'weight', weight
	if len(RecoElectrons)>0: mT = c.Electrons_MTW[RecoElectrons[0][1]]
	elif len(RecoMuons)>0: mT = c.Muons_MTW[RecoMuons[0][1]]
	else: mT = 999
	
	if len(RecoMuons)>1:
		if c.Muons_charge[RecoMuons[0][1]]*c.Muons_charge[RecoMuons[1][1]]==-1:invmass = (RecoMuons[0][0]+RecoMuons[1][0]).M()
		else: invmass = 999
	elif len(RecoElectrons)>1:
		if c.Electrons_charge[RecoElectrons[0][1]]*c.Electrons_charge[RecoElectrons[1][1]]==-1: invmass = (RecoElectrons[0][0]+RecoElectrons[1][0]).M()
		else: invmass = 999		
	else: invmass = 999
	
	fv = [c.HT,   c.MHT   ,c.NJets, c.BTags, mindphi, len(RecoElectrons), len(RecoMuons), invmass, mT, elpt, eleta, mupt, mueta]
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist_):
			if selectionFeatureVector(fv,regionkey,varname):
				#if 'SElBaseline' in regionkey and 'Mht' in varname: print ientry, 'filling this mht hist while HT=', fv[0], 'pt=', elpt
				fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar], weight)                
	


fnew_.cd()
writeHistoStruct(histoStructDict)
hHt.Write()
hHtWeighted.Write()
hMtPionMatched.Write()
hMtPionUnMatched.Write()
print 'just created', fnew_.GetName()

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
