from ROOT import *
import numpy as np
from glob import glob
from utils import *
gROOT.SetBatch()
gROOT.SetStyle('Plain')
zmass = 91
window = 15
metthresh = 100


debugmode = False
vetothebs_ = True ###hello...

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"
default2017 = '/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v2RunIIFall17MiniAODv*.root'
defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_3*_RA2AnalysisTree.root"
#python tools/TagNProbeHistMaker.py --fnamekeyword /pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_5_RA2AnalysisTree.root --dtmode PixAndStrips --SmearLeps4Zed=False
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-SmearLeps4Zed", "--SmearLeps4Zed", type=str, default='False')
parser.add_argument("-doPions", "--doPions", type=bool, default=True)        #false for the first round
parser.add_argument("-gk", "--useGenKappa", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
args = parser.parse_args()
nfpj = args.nfpj
useGenKappa = args.useGenKappa
SmearLeps4Zed = args.SmearLeps4Zed=='True'
inputFileNames = args.fnamekeyword
if ',' in inputFileNames: inputFiles = inputFileNames.split(',')
else: inputFiles = glob(inputFileNames)
dtmode = args.dtmode
analyzer = args.analyzer
JerUpDown = args.JerUpDown #79323846Pi!
pileup = args.pileup
doPions = args.doPions


GenOnly = False
RelaxGenKin = True
verbose = False
DoGenMatching = False
candPtCut = 25
candPtUpperCut = 6499
if SmearLeps4Zed: kappasmearlevellabel = 'YesZSmear'
else: kappasmearlevellabel = 'NoZSmear'

puwindows = {'Nom':[-inf, inf],'Low':[0, 14],'Med':[14, 27],'High':[27, inf]}
puwindow = puwindows[pileup]
if not pileup=='Nom': 
	PtBinEdges = [0,200]
	EtaBinEdges = [0, 1.4442,1.566, 2.4]

x_ = len(inputFiles)
print 'going to analyze events in', inputFileNames
isdata = 'Run20' in inputFileNames
if 'Run2016' in inputFileNames or 'Summer16' in inputFileNames or 'aksingh' in inputFileNames: 
	is2016, is2017, is2018 = True, False, False
elif 'Run2017' in inputFileNames or 'Fall17' in inputFileNames or 'somethingelse' in inputFileNames: 
	is2016, is2017, is2018 = False, True, False
elif 'Run2018' in inputFileNames or 'Autumn18' in inputFileNames or 'somthin or other' in inputFileNames: 
	is2016, is2017, is2018 = False, True, True

if is2016: phase = 0
else: phase = 1

verbose = False
candPtUpperCut = 6499
if is2016: BTAG_deepCSV = 0.6324
if is2017: BTAG_deepCSV = 0.4941
if is2018: BTAG_deepCSV = 2.55


if phase==0: mvathreshes=[.1,.25]#these mean nothing now
else: mvathreshes=[0.15,0.0]


print 'dtmode', dtmode
if dtmode == 'PixOnly': 
	PixMode = True
	PixStripsMode = False
	CombineMode = False
elif dtmode == 'PixAndStrips': 
	PixMode = False
	PixStripsMode = True
	CombineMode = False    
elif dtmode == 'PixOrStrips':
	PixMode = False
	PixStripsMode = False
	CombineMode = True    

if PixStripsMode: metthresh+=0


c = TChain("TreeMaker2/PreSelection")
if isdata: fsmearname = 'usefulthings/DataDrivenSmear_Run2016_'+dtmode+'.root'
else: fsmearname = 'usefulthings/DataDrivenSmear_DYJets_'+dtmode+'.root'

fSmear  = TFile(fsmearname)


hEtaVsPhiDT = TH2F('hEtaVsPhiDT','hEtaVsPhiDT',160,-3.2,3.2,250,-2.5,2.5)


hFakeCrBdtVsDxyIsShortEl = TH2F('hFakeCrBdtVsDxyIsShortEl','hFakeCrBdtVsDxyIsShortEl',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsLongEl  = TH2F('hFakeCrBdtVsDxyIsLongEl','hFakeCrBdtVsDxyIsLongEl',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsShortMu = TH2F('hFakeCrBdtVsDxyIsShortMu','hFakeCrBdtVsDxyIsShortMu',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsLongMu  = TH2F('hFakeCrBdtVsDxyIsLongMu','hFakeCrBdtVsDxyIsLongMu',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsShortPi = TH2F('hFakeCrBdtVsDxyIsShortPi','hFakeCrBdtVsDxyIsShortPi',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsLongPi  = TH2F('hFakeCrBdtVsDxyIsLongPi','hFakeCrBdtVsDxyIsLongPi',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsShortFake = TH2F('hFakeCrBdtVsDxyIsShortFake','hFakeCrBdtVsDxyIsShortFake',20,0,0.05,20,-.3,0.6)
hFakeCrBdtVsDxyIsLongFake  = TH2F('hFakeCrBdtVsDxyIsLongFake','hFakeCrBdtVsDxyIsLongFake',20,0,0.05,20,-.3,0.6)


fMask = TFile('usefulthings/Masks.root')
if 'Run2016' in inputFileNames: 
	fMask.ls()
	hMask = fMask.Get('hEtaVsPhiDT_maskData-2016Data-2016')
else: 
	#hMask = fMask.Get('hEtaVsPhiDT_maskRun2016')
	hMask = ''
#=====This sets up the smearing
dResponseHist_el = {}
dResponseHist_mu = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
	for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
	   newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
	   print 'attempting to get', "htrkresp"+str(newHistKey)
	   if '(1.4442,' in str(newHistKey): continue
	   dResponseHist_el[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey)+'El')
	   dResponseHist_mu[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey)+'Mu')       

print 'smearing factors', dResponseHist_el, dResponseHist_mu
def getSmearFactor(Eta, Pt, dResponseHist):
	for histkey in  dResponseHist:
	   if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
		   SF_trk = 10**(dResponseHist[histkey].GetRandom())
		   return SF_trk #/SF_ele
	print 'returning 1'
	return 1


shortMaxKappaPt = 1000
def fetchKappa(Eta, Pt_, KappaDict, maxpt = 2500):
	Pt = min(Pt_,maxpt)
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
		if abs(Eta) >= etakey[0] and abs(Eta) <= etakey[1]:
			return KappaDict[etakey].Eval(Pt)
			#ipt = KappaDict[etakey].GetXaxis().FindBin(Pt)
			#kappa = KappaDict[etakey].GetBinContent(ipt)
			return kappa
	print etakey, Eta
	print 'didnt get anything meaningful', Eta, Pt
	return 1



def fetchFakeRate(ht, npvtx, hFr):
	xax = hFr.GetXaxis()
	yax = hFr.GetYaxis()	
	xbin = xax.FindBin(npvtx)
	ybin = yax.FindBin(ht)	
	fr = hFr.GetBinContent(xbin,ybin)
	print 'found fr', fr
	return fr

def Mtautau(pt, l1, l2):
	xi1 = (pt.Px() * l2.Py() - pt.Py() * l2.Px()) / (l1.Px() * l2.Py() - l2.Px() * l1.Py())
	xi2 = (pt.Py() * l1.Px() - pt.Px() * l1.Py()) / (l1.Px() * l2.Py() - l2.Px() * l1.Py())
	nu1v = xi1 * l1.Vect()
	nu2v = xi2 * l2.Vect()
	nu1E = nu1v.Mag()
	nu2E = nu2v.Mag()
	nu1 = TLorentzVector(nu1v, nu1E)
	nu2 = TLorentzVector(nu2v, nu2E)	
	m = (l1 + l2 + nu1 + nu2).M()
	if m < 0:
		m = -1
	return m


def mttsam1(metvec, l1vec, l2vec):
				pxmiss, pymiss = metvec.Px(), metvec.Py()
				pxv1, pyv1 = l1vec.Px(), l1vec.Py()
				pxv2, pyv2 = l2vec.Px(), l2vec.Py()
				z1 = (-(pxv2*(pymiss + pyv1)) + (pxmiss + pxv1)*pyv2)/(-(pxv2*pyv1) + pxv1*pyv2)#(pxv2*pymiss-pyv2*pxmiss)/(pxv2*pyv1-pyv2*pxv1)+1
				z2 = 1 + (pxv1*pymiss - pxmiss*pyv1)/(-(pxv2*pyv1) + pxv1*pyv2)#(pxv1*pymiss-pyv1*pxmiss)/(pxv1*pyv2-pyv1*pxv2)+1
				#print z2, 'sam got visible, invisible px of', l2vec.Px(), (z2-1)*l2vec.Px()                
				tau1 = TLorentzVector()
				tau1.SetPtEtaPhiE(z1*l1vec.Pt(), l1vec.Eta(), l1vec.Phi(), z1*l1vec.E())
				tau2 = TLorentzVector()
				tau2.SetPtEtaPhiE(z2*l2vec.Pt(), l2vec.Eta(), l2vec.Phi(), z2*l2vec.E())
				#print 'sam tau mass 1', (tau1).M(), tau1.Pt()
				#print 'sam tau mass 2', (tau2).M(), tau2.Pt()        
				IMleplep = (tau1 + tau2).M()
				return IMleplep

hHt       = makeTh1("hHt","HT for number of events", 250,0,5000)
hHtWeighted       = makeTh1("hHtWeighted","HT for number of events", 250,0,5000)
hElTagPt        = makeTh1VB("hElTagPt"  , "pt of the ElTags", len(PtBinEdges)-1,PtBinEdges)
hElTagEta_       = makeTh1VB("hElTagEta_"  , "Eta of the ElTags", len(EtaBinEdges)-1,EtaBinEdges)

hMuTagPt        = makeTh1VB("hMuTagPt"  , "pt of the MuTags", len(PtBinEdges)-1,PtBinEdges)
hMuTagEta       = makeTh1VB("hMuTagEta"  , "Eta of the MuTags", len(EtaBinEdges)-1,EtaBinEdges)
hGenPtvsResp    = makeTh2("hGenPtvsResp","hGenPtvsResp",50, 10, 400, 20, -2 ,3)    

hNTrackerLayersDT_el = TH1F('hNTrackerLayersDT_el','hNTrackerLayersDT_el',11,0,11)
hNTrackerLayersDT_mu = TH1F('hNTrackerLayersDT_mu','hNTrackerLayersDT_mu',11,0,11)

hDPhiLepsPiDT = TH1F('hDPhiLepsPiDT','hDPhiLepsPiDT',10,0,3.2)
hBdtVsDxyPiDT    = makeTh2("hBdtVsDxyPiDT","hBdtVsDxyPiDT",20,-1,1, 20,0,0.2)    


#=====This sets up histograms for the pT response of the tracks
dProbeElTrkResponseDT_ = {}
dProbeElTrkResponseRECO_= {}
dProbeMuTrkResponseDT_ = {}
dProbeMuTrkResponseRECO_= {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	   newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))    
	   specialpart = '_eta'+str(newHistKey).replace('), (', '_pt').replace('(','').replace(')','').replace(', ','to')
	   dProbeElTrkResponseDT_[newHistKey] = makeTh1("hProbeElTrkrespDT"+specialpart,"hProbeElTrkrespDT"+specialpart, 100,-2,2)    
	   histoStyler(dProbeElTrkResponseDT_[newHistKey], 1)
	   dProbeElTrkResponseRECO_[newHistKey] = makeTh1("hProbeElTrkrespRECO"+specialpart,"hProbeElTrkrespRECO"+specialpart, 100,-2,2)    
	   histoStyler(dProbeElTrkResponseRECO_[newHistKey], 1)       

	   dProbeMuTrkResponseDT_[newHistKey] = makeTh1("hProbeMuTrkrespDT"+specialpart,"hProbeMuTrkrespDT"+specialpart, 100,-2,2)    
	   histoStyler(dProbeMuTrkResponseDT_[newHistKey], 1)
	   dProbeMuTrkResponseRECO_[newHistKey] = makeTh1("hProbeMuTrkrespRECO"+specialpart,"hProbeMuTrkrespRECO"+specialpart, 100,-2,2)    
	   histoStyler(dProbeMuTrkResponseRECO_[newHistKey], 1)             

#=====This sets up histograms for the invariant mass and kappas    
dInvMassElRECOHist = {}
dInvMassElDTHist = {}
hElProbePt_DTnums = {}
hElProbePt_RECOdens = {}
hGenElProbePt_DTnums = {}
hGenElProbePt_RECOdens = {}

dInvMassMuRECOHist = {}
dInvMassMuDTHist = {}
hMuProbePt_DTnums = {}
hMuProbePt_RECOdens = {}
hGenMuProbePt_DTnums = {}
hGenMuProbePt_RECOdens = {}

if doPions:
	dInvMassPiDTHist = {}
	dInvMassPiRECOHist = {}

	hGenPiProbePt_DTnums = {}
	hGenPiProbePt_RECOdens = {}

	dInvMassElFromTauRECOHist = {}
	dInvMassElFromTauWtdRECOHist = {}
	dInvMassMuFromTauRECOHist = {}
	dInvMassMuFromTauWtdRECOHist = {}
	#
	dInvMassFakeFromTauCRHist = {}
	dInvMassFakeFromTauWtdCRHist = {}
	#		
	hElFromTauProbePt_RECOdens = {}
	hElFromTauProbePtWtd_RECOdens = {}
	hElFromTauProbePt_DTnums = {}

	hMuFromTauProbePt_RECOdens = {}
	hMuFromTauProbePtWtd_RECOdens = {}
	hMuFromTauProbePt_DTnums = {}

	hPiProbePt_DTnums = {}
	hPiProbePt_RECOdens = {}
	hPiFromTauProbePt_DTnums = {}
	
	hFakeFromTauProbePt_CRdens = {}
	hFakeFromTauProbePtWtd_CRdens = {}	
	hFakeFromTauProbePt_DTnums = {}	



for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
	specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')
	hElProbePt_DTnums[etakey] = makeTh1VB("hElProbePtDT"+specialpart+"_num", "pt of the ElProbes", len(PtBinEdges)-1,PtBinEdges)
	hElProbePt_RECOdens[etakey]    = makeTh1VB("hElProbePtRECO"+specialpart+"_den", "pt of the ElProbes", len(PtBinEdges)-1,PtBinEdges)
	hMuProbePt_DTnums[etakey] = makeTh1VB("hMuProbePtDT"+specialpart+"_num", "pt of the MuProbes", len(PtBinEdges)-1,PtBinEdges)
	hMuProbePt_RECOdens[etakey]    = makeTh1VB("hMuProbePtRECO"+specialpart+"_den", "pt of the MuProbes", len(PtBinEdges)-1,PtBinEdges)
	hGenElProbePt_DTnums[etakey] = makeTh1VB("hGenElProbePtDT"+specialpart+"_num", "pt of the ElProbes", len(PtBinEdges)-1,PtBinEdges)
	hGenElProbePt_RECOdens[etakey]    = makeTh1VB("hGenElProbePtRECO"+specialpart+"_den", "pt of the ElProbes", len(PtBinEdges)-1,PtBinEdges)        
	hGenMuProbePt_DTnums[etakey] = makeTh1VB("hGenMuProbePtDT"+specialpart+"_num", "pt of the MuProbes", len(PtBinEdges)-1,PtBinEdges)    
	hGenMuProbePt_RECOdens[etakey]    = makeTh1VB("hGenMuProbePtRECO"+specialpart+"_den", "pt of the MuProbes", len(PtBinEdges)-1,PtBinEdges)    

	if doPions:

		hGenPiProbePt_DTnums[etakey] = makeTh1VB("hGenPiProbePtDT"+specialpart+"_num", "pt of the PiProbes", len(PtBinEdges)-1,PtBinEdges)
		hGenPiProbePt_RECOdens[etakey]    = makeTh1VB("hGenPiProbePtRECO"+specialpart+"_den", "pt of the PiProbes", len(PtBinEdges)-1,PtBinEdges)

		hPiProbePt_DTnums[etakey] = makeTh1VB("hPiProbePtDT"+specialpart+"_num", "pt of the PiProbes", len(PtBinEdges)-1,PtBinEdges)
		hPiProbePt_RECOdens[etakey]    = makeTh1VB("hPiProbePtRECO"+specialpart+"_den", "pt of the PiProbes", len(PtBinEdges)-1,PtBinEdges)
		hPiFromTauProbePt_DTnums[etakey]    = makeTh1VB("hPiFromTauProbePtDT"+specialpart+"_num", "pt of the DtPiFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		
		hElFromTauProbePt_RECOdens[etakey]    = makeTh1VB("hElFromTauProbePtRECO"+specialpart+"_den", "pt of the ElFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		hElFromTauProbePtWtd_RECOdens[etakey]    = makeTh1VB("hElFromTauProbePtWtdRECO"+specialpart+"_den", "pt of the ElFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		hElFromTauProbePt_DTnums[etakey]    = makeTh1VB("hElFromTauProbePtDT"+specialpart+"_num", "pt of the DtElFromTauProbes", len(PtBinEdges)-1,PtBinEdges)

		hMuFromTauProbePt_RECOdens[etakey]    = makeTh1VB("hMuFromTauProbePtRECO"+specialpart+"_den", "pt of the MuFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		hMuFromTauProbePtWtd_RECOdens[etakey]    = makeTh1VB("hMuFromTauProbePtWtdRECO"+specialpart+"_den", "pt of the MuFromTauProbes", len(PtBinEdges)-1,PtBinEdges)        
		hMuFromTauProbePt_DTnums[etakey]    = makeTh1VB("hMuFromTauProbePtDT"+specialpart+"_num", "pt of the DtMuFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		#
		hFakeFromTauProbePt_CRdens[etakey]    = makeTh1VB("hFakeFromTauProbePtCR"+specialpart+"_den", "pt of the FakeFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		hFakeFromTauProbePtWtd_CRdens[etakey]    = makeTh1VB("hFakeFromTauProbePtWtdCR"+specialpart+"_den", "pt of the FakeFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		hFakeFromTauProbePt_DTnums[etakey]    = makeTh1VB("hFakeFromTauProbePtDT"+specialpart+"_num", "pt of the DtFakeFromTauProbes", len(PtBinEdges)-1,PtBinEdges)
		#


	for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
	   newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
	   specialpart = '_eta'+str(newHistKey).replace('), (', '_pt').replace('(','').replace(')','').replace(', ','to')
	   dInvMassElRECOHist[newHistKey] = makeTh1("hInvMassEl"+specialpart+"_RECOden"  , "hInvMassEl"+specialpart+"_RECOden", 40, 60, 120)
	   histoStyler(dInvMassElRECOHist[newHistKey], 1)       
	   dInvMassElDTHist[newHistKey] = makeTh1("hInvMassEl"+specialpart+"_DTnum"  , "hInvMassEl"+specialpart+"_DTnum", 40, 60, 120)
	   histoStyler(dInvMassElDTHist[newHistKey], 1)
	   dInvMassMuRECOHist[newHistKey] = makeTh1("hInvMassMu"+specialpart+"_RECOden"  , "hInvMassMu"+specialpart+"_RECOden", 40, 60, 120)
	   histoStyler(dInvMassMuRECOHist[newHistKey], 1)
	   dInvMassMuDTHist[newHistKey] = makeTh1("hInvMassMu"+specialpart+"_DTnum"  , "hInvMassMu"+specialpart+"_DTnum", 40, 60, 120)
	   histoStyler(dInvMassMuDTHist[newHistKey], 1)
	   if doPions:
		   dInvMassPiRECOHist[newHistKey] = makeTh1("hInvMassPi"+specialpart+"_RECOden"  , "hInvMassPi"+specialpart+"_RECOden", 100, 0, 200)
		   histoStyler(dInvMassPiRECOHist[newHistKey], 1)
		   dInvMassPiDTHist[newHistKey] = makeTh1("hInvMassPi"+specialpart+"_DTnum"  , "hInvMassPi"+specialpart+"_DTnum", 100, 0, 200)
		   histoStyler(dInvMassPiDTHist[newHistKey], 1)
		   dInvMassElFromTauRECOHist[newHistKey] = makeTh1("hInvMassElFromTau"+specialpart+"_RECOden"  , "hInvMassElFromTau"+specialpart+"_RECOden", 100, 0, 200)
		   histoStyler(dInvMassElFromTauRECOHist[newHistKey], 1)       
		   dInvMassElFromTauWtdRECOHist[newHistKey] = makeTh1("hInvMassElFromTauWtd"+specialpart+"_RECOden"  , "hInvMassElFromTauWtd"+specialpart+"_RECOden", 100, 0, 200)
		   histoStyler(dInvMassElFromTauWtdRECOHist[newHistKey], 1)       
		   dInvMassMuFromTauRECOHist[newHistKey] = makeTh1("hInvMassMuFromTau"+specialpart+"_RECOden"  , "hInvMassMuFromTau"+specialpart+"_RECOden", 100, 0, 200)
		   histoStyler(dInvMassMuFromTauRECOHist[newHistKey], 1)
		   dInvMassMuFromTauWtdRECOHist[newHistKey] = makeTh1("hInvMassMuFromTauWtd"+specialpart+"_RECOden"  , "hInvMassMuFromTauWtd"+specialpart+"_RECOden", 100, 0, 200)
		   histoStyler(dInvMassMuFromTauWtdRECOHist[newHistKey], 1)
   
		   #
		   dInvMassFakeFromTauCRHist[newHistKey] = makeTh1("hInvMassFakeFromTau"+specialpart+"_CRden"  , "hInvMassFakeFromTau"+specialpart+"_CRden", 100, 0, 200)
		   histoStyler(dInvMassFakeFromTauCRHist[newHistKey], kRed-1)
		   dInvMassFakeFromTauWtdCRHist[newHistKey] = makeTh1("hInvMassFakeFromTauWtd"+specialpart+"_CRden"  , "hInvMassFakeFromTauWtd"+specialpart+"_CRden", 100, 0, 200)
		   histoStyler(dInvMassFakeFromTauWtdCRHist[newHistKey], kRed+2)
		   #
   
   

import os, sys
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



if doPions: ###load in prediction for electron and muon tracks for subtraction
	fakeratefilename = 'usefulthings/fakerate.root'
	frfile = TFile(fakeratefilename)
	frversion = '7'
	if isdata: 
		if phase==0:
			fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly_'+kappasmearlevellabel+'.root'
			fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips_'+kappasmearlevellabel+'.root' 
			fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly_'+kappasmearlevellabel+'.root'
			fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips_'+kappasmearlevellabel+'.root'
			frhistnamePixAndStrips = 'qcd_lowMHT_loose'+frversion+'_long/Run2016/fakerate_HT_n_allvertices'
			frhistnamePixOnly = 'qcd_lowMHT_loose'+frversion+'_short/Run2016/fakerate_HT_n_allvertices'			
		else:
			fileKappaPixOnly = 'usefulthings/KappaRun2016_PixOnly_'+kappasmearlevellabel+'.root'
			#fileKappaPixAndStrips = 'usefulthings/KappaRun2016_PixAndStrips'+kappasmearlevellabel+'.root' 
			#fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly'+kappasmearlevellabel+'.root'
			#fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips'+kappasmearlevellabel+'.root'		
			frhistnamePixAndStrips = 'qcd_lowMHT_loose'+frversion+'_long/Run2017/fakerate_HT_n_allvertices'
			frhistnamePixOnly = 'qcd_lowMHT_loose'+frversion+'_short/Run2017/fakerate_HT_n_allvertices'						

	else: 
		if phase==0:
			fileKappaPixOnly = 'usefulthings/KappaSummer16.AllMC_PixOnly_'+kappasmearlevellabel+'.root'#should be updated to All
			fileKappaPixAndStrips = 'usefulthings/KappaSummer16.AllMC_PixAndStrips_'+kappasmearlevellabel+'.root'
			fileKappaPixOnlyGen = 'usefulthings/KappaSummer16.WJets_PixOnly_'+kappasmearlevellabel+'.root'
			fileKappaPixAndStripsGen = 'usefulthings/KappaSummer16.WJets_PixAndStrips_'+kappasmearlevellabel+'.root' 
			frhistnamePixAndStrips = 'qcd_lowMHT_loose'+frversion+'_long/Summer16/fakerate_HT_n_allvertices'
			frhistnamePixOnly = 'qcd_lowMHT_loose'+frversion+'_short/Summer16/fakerate_HT_n_allvertices'
		else:
			fileKappaPixOnly = 'usefulthings/KappaFall17.AllMC_PixOnly_'+kappasmearlevellabel+'.root'#should be updated to All
			fileKappaPixAndStrips = 'usefulthings/KappaFall17.AllMC_PixAndStrips_'+kappasmearlevellabel+'.root'
			fileKappaPixOnlyGen = 'usefulthings/KappaFall17.WJets_PixOnly_'+kappasmearlevellabel+'.root'
			fileKappaPixAndStripsGen = 'usefulthings/KappaFall17.WJets_PixAndStrips_'+kappasmearlevellabel+'.root' 
			frhistnamePixAndStrips = 'qcd_lowMHT_loose'+frversion+'_long/Fall17/fakerate_HT_n_allvertices'
			frhistnamePixOnly = 'qcd_lowMHT_loose'+frversion+'_short/Fall17/fakerate_HT_n_allvertices'			


	hFrPixOnly = frfile.Get(frhistnamePixOnly)
	hFrPixAndStrips = frfile.Get(frhistnamePixAndStrips)

	fKappaPixOnly  = TFile(fileKappaPixOnly)
	fKappaPixAndStrips  = TFile(fileKappaPixAndStrips)
	fKappaPixOnlyGen  = TFile(fileKappaPixOnlyGen)
	fKappaPixAndStripsGen  = TFile(fileKappaPixAndStripsGen)


	fElProbePt_KappasPixOnly = {}
	fGenElProbePt_KappasPixOnly = {}
	fMuProbePt_KappasPixOnly = {}
	fGenMuProbePt_KappasPixOnly = {}

	fElProbePt_KappasPixAndStrips = {}
	fGenElProbePt_KappasPixAndStrips = {}
	fMuProbePt_KappasPixAndStrips = {}
	fGenMuProbePt_KappasPixAndStrips = {}

	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
		if etakey == (1.4442, 1.566): continue
		specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')
		oldNumName = "hElProbePtDT"+specialpart+"_num"
		newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
		newKappaFuncName = 'f1'+newKappaName.replace('.','p')
		print 'trying to get', newKappaFuncName, 'from', fKappaPixOnly.GetName()
		fElProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
		fElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
		oldGenNumName = "hGenElProbePtDT"+specialpart+"_num"
		newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
		newGenKappaFuncName = 'f1'+newGenKappaName.replace('.','p')
		fGenElProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
		fGenElProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long')
		oldNumName = "hMuProbePtDT"+specialpart+"_num"
		newKappaName = oldNumName.replace('_num','').replace('DT','Kappa')
		newKappaFuncName = 'f1'+newKappaName.replace('.','p')
		fMuProbePt_KappasPixOnly[etakey] = fKappaPixOnly.Get(newKappaFuncName).Clone()
		fMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStrips.Get(newKappaFuncName).Clone()    
		oldGenNumName = "hGenMuProbePtDT"+specialpart+"_num"
		newGenKappaName = oldGenNumName.replace('_num','').replace('DT','Kappa')
		newGenKappaFuncName = 'f1'+newGenKappaName.replace('.','p')
		fGenMuProbePt_KappasPixOnly[etakey] = fKappaPixOnlyGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Short')
		fGenMuProbePt_KappasPixAndStrips[etakey] = fKappaPixAndStripsGen.Get(newGenKappaFuncName).Clone(newGenKappaFuncName+'Long') 


	if useGenKappa: 
		kappadictElPixOnly = fGenElProbePt_KappasPixOnly
		kappadictMuPixOnly = fGenMuProbePt_KappasPixOnly    
		kappadictElPixAndStrips = fGenElProbePt_KappasPixAndStrips
		kappadictMuPixAndStrips = fGenMuProbePt_KappasPixAndStrips        
	else: 
		kappadictElPixOnly = fElProbePt_KappasPixOnly
		kappadictMuPixOnly = fMuProbePt_KappasPixOnly  
		kappadictElPixAndStrips = fElProbePt_KappasPixAndStrips
		kappadictMuPixAndStrips = fMuProbePt_KappasPixAndStrips	

	if dtmode=='PixOnly': 
		kappadictEl = kappadictElPixOnly	
		kappadictMu = kappadictMuPixOnly
		hFr = hFrPixOnly
		maxKappaPt = 1000
	else:
		kappadictEl = kappadictElPixAndStrips	
		kappadictMu = kappadictMuPixAndStrips
		hFr = hFrPixAndStrips		
		maxKappaPt = 3000



def isGenMatched(lep, pdgid):
	for igenm, genm in enumerate(c.GenParticles):
	   if not genm.Pt() > 5: continue
	   #if not abs(c.GenParticles_ParentId[igenm]) == 23: continue
	   if not (abs(c.GenParticles_PdgId[igenm]) == pdgid and c.GenParticles_Status[igenm] == 1):continue
	   drm = genm.DeltaR(lep)
	   if drm < .01: return genm.Pt()
	return 0

for ifile, f in enumerate(inputFiles):
	if ifile>=nfpj: break
	print 'adding file:', f
	c.Add(f)
nentries = c.GetEntries()
c.Show(0)
print nentries, ' events to be analyzed (nentries)'
verbosity = 10000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))

newfname = 'TagnProbeHists_'+identifier+'.root'
if PixMode: newfname = newfname.replace('.root','_PixOnly.root')
if PixStripsMode: newfname = newfname.replace('.root','_PixAndStrips.root')
if CombineMode: newfname = newfname.replace('.root','_PixOrStrips.root')

if pileup!='Nom':
	newfname = newfname.replace('.root', 'PU'+str(puwindow[0])+'to'+str(puwindow[1])+'.root')
if SmearLeps4Zed: newfname = newfname.replace('.root', '_YesZSmear.root')
else: newfname = newfname.replace('.root', '_NoZSmear.root')

fnew = TFile(newfname,'recreate')
print 'making', fnew.GetName()

triggerIndecesV2 = {}
#triggerIndecesV2['SingleEl'] = [36,39]
triggerIndecesV2['SingleElCocktail'] = [14, 15, 16, 17, 18, 19, 20, 21]
triggerIndecesV2['MhtMet6pack'] = [109,110,111,112,113,114,115,116,117,118,119,120,124,125,126,127,128,129,130,131,132,133,134,135,136]
#triggerIndecesV2["SingleMu"] = [48,50,52,55,63]
triggerIndecesV2["SingleMuCocktail"] = [24,25,26,27,28,30,31,32]

triggerIndeces = triggerIndecesV2

def PassTrig(c,trigname):
	for trigidx in triggerIndeces[trigname]: 
		if c.TriggerPass[trigidx]==1: 
			return True
	return False


for ientry in range(nentries):
	if verbose:
		if not ientry > 75210: continue
	if debugmode:
		if not ientry in [175,193]: continue
	if ientry%verbosity==0: print 'now processing event number', ientry, 'of', nentries
	c.GetEntry(ientry)
	if isdata: weight = 1
	else: 
		#weight = c.CrossSection
		#weight = 1.0#*c.puWeight#c.CrossSection
		weight = 1
	fillth1(hHt, c.HT, 1)
	fillth1(hHtWeighted, c.HT, weight)
	TagPt  =  0
	TagEta  =  0
	ProbePt  =  0
	ProbeEta = 0
	probeTlv = TLorentzVector()
	probeTlv.SetPxPyPzE(0, 0, 0, 0)
	if vetothebs_: 
		if not c.BTags==0: continue
	if ientry==0:
		for itrig in range(len(c.TriggerPass)):
			print itrig, c.TriggerNames[itrig], c.TriggerPrescales[itrig], c.HT
		print '='*20
	genels, genmus, genpis = [], [], []
	if not isdata:     
		for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue       
			if not (abs(c.GenParticles_PdgId[igp])==11 or abs(c.GenParticles_PdgId[igp])==13) : continue
			if not c.GenParticles_Status[igp]==1 : continue          
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue                    
			if abs(c.GenParticles_PdgId[igp])==11: genels.append([gp,igp])
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append([gp,igp])          
		for igp, gphadhobject in enumerate(c.GenTaus):
			if not c.GenTaus_LeadTrk[igp].Pt()>5: continue
			if not abs(c.GenTaus_LeadTrk[igp].Eta())<2.4: continue
			if not (abs(c.GenTaus_LeadTrk[igp].Eta())<1.445 or abs(c.GenTaus_LeadTrk[igp].Eta())>1.56): continue
			if not bool(c.GenTaus_had[igp]): continue
			if not doPions: continue
			genpis.append([c.GenTaus_LeadTrk[igp], igp])

	if isdata:
		if not (PassTrig(c, 'SingleElCocktail') or PassTrig(c, 'SingleMuCocktail') or PassTrig(c, 'MhtMet6pack')): continue

	if not (c.nAllVertices >= puwindow[0] and c.nAllVertices < puwindow[1]): continue

	basicTracks = []
	disappearingTracks = []
	disappearingCRTracks = []
	for itrack, track in enumerate(c.tracks):
		if not track.Pt() > 15 : continue
		if not abs(track.Eta()) < 2.4: continue
		if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
		if not isBaselineTrack(track, itrack, c, hMask): continue
		basicTracks.append([track,c.tracks_charge[itrack], itrack])
		if not (track.Pt()>candPtCut and track.Pt()<candPtUpperCut): continue
		dtstatus, mva_ = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips, mvathreshes)
		if dtstatus==0: continue
		if PixMode:
			if not abs(dtstatus)==1: continue
		if PixStripsMode:
			if not abs(dtstatus)==2: continue          
		passeslep = True
		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)):
		   drlep = lep.DeltaR(track)
		   if drlep<0.01: 
			  passeslep = False
			  break         
		if not passeslep: continue
		fillth2(hEtaVsPhiDT, track.Phi(), track.Eta())
		print ientry, 'found disappearing track w pT =', track.Pt(), dtstatus
		if dtstatus>0: disappearingTracks.append([track,itrack])
		else: disappearingCRTracks.append([track,itrack])
		if dtstatus<0:
			if isMatched_([track], genels, 0.02): 
				if abs(dtstatus)==1: fillth2(hFakeCrBdtVsDxyIsShortEl, c.tracks_dxyVtx[itrack], mva_)
				else: fillth2(hFakeCrBdtVsDxyIsLongEl, c.tracks_dxyVtx[itrack], mva_)
				print ientry, 'fakeCR.........is electron'
			elif isMatched_([track], genmus, 0.02):
				if abs(dtstatus)==1: fillth2(hFakeCrBdtVsDxyIsShortMu, c.tracks_dxyVtx[itrack], mva_)
				else: fillth2(hFakeCrBdtVsDxyIsLongMu, c.tracks_dxyVtx[itrack], mva_)
				print ientry, 'fakeCR.........is muon'			
			elif isMatched_([track], genpis, 0.02):
				if abs(dtstatus)==1: fillth2(hFakeCrBdtVsDxyIsShortPi, c.tracks_dxyVtx[itrack], mva_)
				else: fillth2(hFakeCrBdtVsDxyIsLongPi, c.tracks_dxyVtx[itrack], mva_)
				print ientry, 'fakeCR.........is pion'
			else:
				if abs(dtstatus)==1: fillth2(hFakeCrBdtVsDxyIsShortFake, c.tracks_dxyVtx[itrack], mva_)
				else: fillth2(hFakeCrBdtVsDxyIsLongFake, c.tracks_dxyVtx[itrack], mva_)
				print ientry, 'fakeCR.........is an actual fake'			


	SmearedElectrons = []
	TightElectrons = []       
	for ilep, lep in enumerate(c.Electrons):
	   #if not lep.Pt()>10: continue               
	   if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
	   if not abs(lep.Eta())<2.4: continue     
	   if not c.Electrons_passIso[ilep]: continue      
	   if not c.Electrons_tightID[ilep]: continue    
	   if lep.Pt() > 30:
		  TightElectrons.append([lep,c.Electrons_charge[ilep]])
	   matchedTrack = TLorentzVector()           
	   drmin = 9999
	   itrk_ = -1
	   for trk in basicTracks:
			 if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
			 drTrk = trk[0].DeltaR(lep)
			 if drTrk<drmin:
				drmin = drTrk
				matchedTrack = trk[0]
				itrk_ = trk[2]
				if drTrk<0.02: break
	   if not drmin<0.02: continue
	   #print ientry, 'found electron', lep.Pt() 
	   smear = 1# getSmearFactor(abs(matchedTrack.Eta()), min(matchedTrack.Pt(),299.999), dResponseHist_el)
	   smearedEl = TLorentzVector()          
	   if SmearLeps4Zed: smearedEl.SetPtEtaPhiE(smear*matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),smear*matchedTrack.E())
	   else: smearedEl.SetPtEtaPhiE(matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),matchedTrack.E())
	   #smearedEl.SetPtEtaPhiE(smear*lep.Pt(),lep.Eta(),lep.Phi(),smear*lep.E())
	   if not (smearedEl.Pt()>candPtCut and smearedEl.Pt()<candPtUpperCut): continue
	   if PixMode:
	   	if c.tracks_nValidTrackerHits[itrk_]==c.tracks_nValidPixelHits[itrk_]:
	   		SmearedElectrons.append([smearedEl, c.Electrons_charge[ilep], lep.Clone()])
	   if PixStripsMode:
	   	if (c.tracks_nMissingOuterHits[itrk_]>=2 and c.tracks_nValidTrackerHits[itrk_]>c.tracks_nValidPixelHits[itrk_]):
	   		SmearedElectrons.append([smearedEl, c.Electrons_charge[ilep], lep.Clone()])	   		

	SmearedMuons = []
	TightMuons = []
	for ilep, lep in enumerate(c.Muons):
	   if not lep.Pt()>10: continue               
	   if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
	   if not abs(lep.Eta())<2.4: continue     
	   if not c.Muons_passIso[ilep]: continue  
	   if not c.Muons_tightID[ilep]: continue        
	   if lep.Pt() > 30:
		  TightMuons.append([lep,c.Muons_charge[ilep]])
	   matchedTrack = TLorentzVector()           
	   drmin = 9999
	   for trk in basicTracks:
			 if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			 if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
			 drTrk = trk[0].DeltaR(lep)
			 if drTrk<drmin:
				drmin = drTrk
				matchedTrack = trk[0]
				if drTrk<0.01: break
	   if not drmin<0.01: continue
	   smear = getSmearFactor(abs(matchedTrack.Eta()), min(matchedTrack.Pt(),299.999), dResponseHist_mu)
	   smearedMu = TLorentzVector()          
	   if SmearLeps4Zed: smearedMu.SetPtEtaPhiE(smear*matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),smear*matchedTrack.E())
	   else: smearedMu.SetPtEtaPhiE(matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),matchedTrack.E())
	   #smearedMu.SetPtEtaPhiE(smear*lep.Pt(),lep.Eta(),lep.Phi(),smear*lep.E())
	   if not (smearedMu.Pt()>candPtCut and smearedMu.Pt()<candPtUpperCut): continue
	   SmearedMuons.append([smearedMu, c.Muons_charge[ilep], lep.Clone()])# matchedTrack])       

	SmearedPions = []  
	for ipi, pion in enumerate(c.TAPPionTracks):	   
	   if not pion.Pt()>25: continue               
	   if (abs(pion.Eta()) < 1.566 and abs(pion.Eta()) > 1.4442): continue
	   if not abs(pion.Eta())<2.4: continue  
	   if not c.TAPPionTracks_trkiso[ipi]<0.01: continue
	   matchedTrack = TLorentzVector()   
	   drmin = 9999
	   for trk in basicTracks:
			 if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
			 if not c.tracks_trkRelIso[trk[2]] < 0.01: continue
			 if c.tracks_passPFCandVeto[trk[2]]: continue
			 drTrk = trk[0].DeltaR(pion)
			 if drTrk<drmin:
				drmin = drTrk
				matchedTrack = trk[0]
				if drTrk<0.01: break
	   if not drmin<0.01: continue 
	   passeslep = True
	   for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)):
		   drlep = lep.DeltaR(pion)
		   if drlep<0.01: 
			  passeslep = False
			  break
	   if not passeslep: continue

	   
	   smear = getSmearFactor(abs(matchedTrack.Eta()), min(matchedTrack.Pt(),299.999), dResponseHist_mu)
	   smearedPi = TLorentzVector()    
	   if SmearLeps4Zed: smearedPi.SetPtEtaPhiE(smear*matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),smear*matchedTrack.Pt()*TMath.CosH(matchedTrack.Eta()))
	   else: smearedPi.SetPtEtaPhiE(matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),matchedTrack.Pt()*TMath.CosH(matchedTrack.Eta()))
	   #smearedPi.SetPtEtaPhiE(smear*pion.Pt(),pion.Eta(),pion.Phi(),smear*pion.E())
	   if not (smearedPi.Pt()>candPtCut and smearedPi.Pt()<candPtUpperCut): continue
	   SmearedPions.append([smearedPi, c.TAPPionTracks_charge[ipi], pion.Clone()])# matchedTrack])

	TightLeptons = TightMuons+TightElectrons
	if not len(SmearedPions)==c.isoPionTracks: continue
	for igen, genlep in enumerate(genels):
		for idistrk, distrk in enumerate(disappearingTracks):
			dr = genlep[0].DeltaR(distrk[0])
			if not dr < 0.02: continue
			if RelaxGenKin: pt, eta = distrk[0].Pt(),abs(distrk[0].Eta())
			else: pt, eta = genlep[0].Pt(), abs(genlep[0].Eta())
			for histkey in  hGenElProbePt_DTnums:
				if abs(eta) > histkey[0] and abs(eta) <= histkey[1]:
					fillth1(hGenElProbePt_DTnums[histkey], pt, weight)
			#print ientry, 'found a nice dt', distrk[0].Pt()
			break       
		drminSmearedlepGenlep = 9999
		gotthematch = False      
		for ie, lep in enumerate(SmearedElectrons):
			dr = genlep[0].DeltaR(lep[0])
			if not dr < 0.02: continue #here we have a probe dt
			pt = lep[2].Pt() 
			for histkey in  hGenElProbePt_RECOdens:
				if abs(lep[0].Eta()) > histkey[0] and abs(lep[0].Eta()) < histkey[1]:
					#fillth1(hGenElProbePt_RECOdens[histkey], lep[0].Pt(), weight)
					fillth1(hGenElProbePt_RECOdens[histkey], pt, weight)
					gotthematch = True
					break
			if gotthematch: break

	for igen, genlep in enumerate(genmus):
		for idistrk, distrk in enumerate(disappearingTracks):
			dr = genlep[0].DeltaR(distrk[0])
			if not dr < 0.02: continue
			if RelaxGenKin: pt, eta = distrk[0].Pt(),abs(distrk[0].Eta())
			else: pt, eta = genlep[0].Pt(), abs(genlep[0].Eta())
			for histkey in  hGenMuProbePt_DTnums:
				if abs(eta) > histkey[0] and abs(eta) <= histkey[1]:
					fillth1(hGenMuProbePt_DTnums[histkey], pt, weight)
			print ientry, 'found a nice dt', distrk[0].Pt()
			break       

		drminSmearedlepGenlep = 9999
		gotthematch = False      
		for imu, lep in enumerate(SmearedMuons):
			dr = genlep[0].DeltaR(lep[0])
			if not dr < 0.02: continue #here we have a probe dt
			pt = lep[2].Pt() 
			for histkey in  hGenMuProbePt_RECOdens:
				if abs(lep[0].Eta()) > histkey[0] and abs(lep[0].Eta()) <= histkey[1]:
					#fillth1(hGenMuProbePt_RECOdens[histkey], lep[0].Pt(), weight)
					fillth1(hGenMuProbePt_RECOdens[histkey], pt, weight)
					gotthematch = True
					break
			if gotthematch: break  

	for igen, gencand in enumerate(genpis):
		for idistrk, distrk in enumerate(disappearingTracks):
			dr = gencand[0].DeltaR(distrk[0])
			if not dr < 0.02: continue
			if RelaxGenKin: pt, eta = distrk[0].Pt(),abs(distrk[0].Eta())
			else: pt, eta = gencand[0].Pt(), abs(gencand[0].Eta())
			for histkey in  hGenPiProbePt_DTnums:
				if abs(eta) > histkey[0] and abs(eta) <= histkey[1]:
					fillth1(hGenPiProbePt_DTnums[histkey], pt, weight)
			print ientry, 'found a nice dt', distrk[0].Pt()
			break       
		drminSmearedcandGencand = 9999
		gotthematch = False      
		for ipi, cand in enumerate(SmearedPions):
			dr = gencand[0].DeltaR(cand[0])
			if not dr < 0.02: continue 
			pt = cand[2].Pt() 
			for histkey in  hGenPiProbePt_RECOdens:
				if abs(cand[0].Eta()) > histkey[0] and abs(cand[0].Eta()) <= histkey[1]:
					#fillth1(hGenPiProbePt_RECOdens[histkey], cand[0].Pt(), weight)
					fillth1(hGenPiProbePt_RECOdens[histkey], pt, weight)
					gotthematch = True
					break
			if gotthematch: break                        

	if GenOnly: continue
	tagTlv = TLorentzVector()
	tagTlv.SetPxPyPzE(0,0,0,0)

	metvec = TLorentzVector()
	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET)


	for charge in range(-1,2,2):

		#electrons
		for itag, tag in enumerate(TightElectrons):    
			if not tag[1]==charge: continue
			IM  =  0 
			TagPt, TagEta = tag[0].Pt(), tag[0].Eta()
			probeIsReco, probeIsDt = False, False
			dmMin = 999
			dtindex  =-1
	
		
			for idt, dt in enumerate(disappearingTracks):
				if not (tag[1] + c.tracks_charge[dt[1]] == 0): continue
				if dt[0].DeltaR(tag[0])<0.01: continue  
				correctedMet = metvec.Clone()
				dphimet = abs(dt[0].DeltaPhi(correctedMet))
				#if not dphimet<3.1415/2: continue
							 
				IMleplep = (tag[0] + dt[0]).M()
				if (IMleplep < 0): 
					print 'something horribly wrong, space-like event a', IMleplep
					continue
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep
					probeTlv =  dt[0]
					dtindex = dt[1]
					probeIsDt = True                    
					probeIsReco = False          
			for iSmearedEl, smearedEl in enumerate(SmearedElectrons):
				if not (tag[1] + smearedEl[1] == 0): continue
				if smearedEl[0].DeltaR(tag[0])<0.02: continue
				correctedMet = metvec.Clone()
				correctedMet+=smearedEl[2]
				dphimet = abs(smearedEl[0].DeltaPhi(correctedMet))
				#if not dphimet<3.1415/2: continue
					
				IMleplep = (tag[0] + smearedEl[0]).M()
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep
					probeTlv = smearedEl[0]
					probeIsReco = True
					probeIsDt = False                    

			if dmMin<100:
				fillth1(hElTagPt, TagPt, weight)
				fillth1(hElTagEta_, TagEta, weight)
				ProbePt = probeTlv.Pt()
				ProbeEta = abs(probeTlv.Eta())
				if probeIsDt:					
					fillth1(hNTrackerLayersDT_el, c.tracks_trackerLayersWithMeasurement[dtindex], weight)
					print 'just filled the el thing with layers ',c.tracks_trackerLayersWithMeasurement[dtindex]					
					if not isdata: isgenmatched  = isGenMatched(probeTlv, 11)
					else: isgenmatched = 1
					if DoGenMatching:
						if isgenmatched == 0: continue #uncomment to skip isGenMatcheding of Probes
					for histkey in  dInvMassElDTHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassElDTHist[histkey],IM,weight)
					if (PixMode and IM>zmass-15 and IM<zmass+30) or (PixStripsMode and dmMin<15):
					  for histkey in  hElProbePt_DTnums:
						if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
							fillth1(hElProbePt_DTnums[histkey], ProbePt, weight)                    
					  for histkey in  dProbeElTrkResponseDT_:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and isgenmatched > histkey[1][0] and isgenmatched < histkey[1][1]:
							fillth1(dProbeElTrkResponseDT_[histkey],TMath.Log10(ProbePt/isgenmatched),weight)
		
				if probeIsReco:
					if not isdata: isgenmatched  = isGenMatched(probeTlv, 11)
					else: isgenmatched = 1    
					if DoGenMatching:                
						if isgenmatched == 0: continue #uncomment to skip isGenMatcheding of Probes
					for histkey in  dInvMassElRECOHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassElRECOHist[histkey],IM, weight)       
					if (PixMode and IM>zmass-15 and IM<zmass+30) or (PixStripsMode and dmMin<15):
					  for histkey in  hElProbePt_RECOdens:
						if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
							fillth1(hElProbePt_RECOdens[histkey], ProbePt, weight)   
					  for histkey in  dProbeElTrkResponseRECO_:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and isgenmatched > histkey[1][0] and isgenmatched < histkey[1][1]:
							fillth1(dProbeElTrkResponseRECO_[histkey],TMath.Log10(ProbePt/isgenmatched),weight) 

		#muons
		for itag, tag in enumerate(TightMuons):    
			if not tag[1]==charge: continue
			IM  =  0 
			TagPt, TagEta = tag[0].Pt(), tag[0].Eta()
			probeIsReco, probeIsDt = False, False
			dmMin = 999
			dtindex = -1
			for idt, dt in enumerate(disappearingTracks):
				if not (tag[1] + c.tracks_charge[dt[1]] == 0): continue
				if dt[0].DeltaR(tag[0])<0.01: continue 
				correctedMet = metvec.Clone()
				dphimet = abs(dt[0].DeltaPhi(correctedMet))
				if not dphimet<3.1415/2: continue				
				IMleplep = (tag[0] + dt[0]).M()
				if (IMleplep < 0): 
					print 'something horribly wrong, space-like event b'
					continue
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					IM = IMleplep
					dmMin = dIM
					probeTlv =  dt[0]
					dtindex = dt[1]
					probeIsDt = True
					#fill layers hist here
					probeIsReco = False          
			for iSmearedMu, smearedMu in enumerate(SmearedMuons):
				if not (tag[1] + smearedMu[1] == 0): continue
				if smearedMu[0].DeltaR(tag[0])<0.02: continue   
				correctedMet = metvec.Clone()
				correctedMet+=smearedMu[2]
				dphimet = abs(smearedMu[0].DeltaPhi(correctedMet))
				if not dphimet<3.1415/2: continue
									 
				IMleplep = (tag[0] + smearedMu[0]).M()
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep                    
					probeTlv = smearedMu[0]
					probeIsReco = True
					probeIsDt = False                    

			if dmMin<100:
				fillth1(hMuTagPt, TagPt, weight)
				fillth1(hMuTagEta, TagEta, weight)
				ProbePt = probeTlv.Pt()
				ProbeEta = abs(probeTlv.Eta())
				if probeIsDt:
					fillth1(hNTrackerLayersDT_mu, c.tracks_trackerLayersWithMeasurement[dtindex], weight)
					print 'just filled the mu thing with layers ',c.tracks_trackerLayersWithMeasurement[dtindex]					
					if not isdata: isgenmatched  = isGenMatched(probeTlv, 13)
					else: isgenmatched = 1
					if DoGenMatching:
						if isgenmatched == 0: continue #uncomment to skip isGenMatcheding of Probes
					print 'here at the muon threshold', ProbePt, ProbeEta
					for histkey in  dInvMassMuDTHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassMuDTHist[histkey],IM,weight)                    
					if dmMin<15:
					#if IMleplep>zmass-20:
					  for histkey in  hMuProbePt_DTnums:						
						if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]: 
							fillth1(hMuProbePt_DTnums[histkey], ProbePt, weight)                    
					  for histkey in  dProbeMuTrkResponseDT_:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and isgenmatched > histkey[1][0] and isgenmatched < histkey[1][1]:
							fillth1(dProbeMuTrkResponseDT_[histkey],TMath.Log10(ProbePt/isgenmatched),weight)

				if probeIsReco:
					if not isdata: isgenmatched  = isGenMatched(probeTlv, 13)
					else: isgenmatched = 1 
					if DoGenMatching:               
						if isgenmatched == 0: continue #uncomment to skip isGenMatcheding of Probes
					for histkey in  dInvMassMuRECOHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassMuRECOHist[histkey],IM, weight)       
					if dmMin<15:
					  for histkey in  hMuProbePt_RECOdens:
						if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
							fillth1(hMuProbePt_RECOdens[histkey], ProbePt, weight)   
					  for histkey in  dProbeMuTrkResponseRECO_:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and isgenmatched > histkey[1][0] and isgenmatched < histkey[1][1]:
							fillth1(dProbeMuTrkResponseRECO_[histkey],TMath.Log10(ProbePt/isgenmatched),weight) 
			
		#taus
		if doPions:
		 for itag, tag in enumerate(TightLeptons):
			if not tag[1]==charge: continue
			IM  =  0 
			TagPt, TagEta = tag[0].Pt(), tag[0].Eta()
			probeIsDt, probeIsCrDt, probeIsRecoEl,probeIsRecoMu,probeIsRecoPi   = False, False, False, False, False
			dmMin = 999
			dtindex = -1
			for idt, dt in enumerate(disappearingTracks):
				if not (tag[1] + c.tracks_charge[dt[1]] == 0): continue
				if dt[0].DeltaR(tag[0])<0.01: continue   
				#if not metvec.Pt()>metthresh: continue# can try also including this before correction				
				correctedMet = metvec.Clone()
				correctedMet-=dt[0]###
				if not correctedMet.Pt()>metthresh: continue
		
				hDPhiLepsPiDT.Fill(correctedMet.DeltaPhi(dt[0]))
		
				#if not abs(correctedMet.DeltaPhi(dt[0]))<3.14159/2: continue
				#if not abs(correctedMet.DeltaPhi(tag[0]))<3.14159/2: continue
				#if PixStripsMode:
		
		
		
		
				#hello!!!
				#if not isMatched_([dt[0]], genpis, 0.02): continue ######################################### Note this is matched
		
				dphileps = abs(dt[0].DeltaPhi(tag[0]))
				#hDPhiLepsPiDT.Fill(correctedMet.DeltaPhi(dt[0]))
				if not dphileps<2.8: continue
				if not dphileps<2.8: continue#3.14159: continue
		
				IMleplep = mttsam1(correctedMet, tag[0], dt[0])
				#IMleplep = PreciseMtautau(correctedMet.Pt(), correctedMet.Phi(),  tag[0], dt[0])#basil

				if (IMleplep < 0): 
					print 'something horribly wrong, space-like event c'
					continue
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					IM = IMleplep
					dmMin = dIM
					probeTlv =  dt[0]
					dtindex = dt[1]
					#fill layers hist here					
					probeIsDt = True
					probeIsCrDt = False
					probeIsRecoEl = False
					probeIsRecoMu = False
					probeIsRecoPi = False
			
					dtIsGenEl, dtIsGenMu, dtIsGenPi, dtIsGenFake = False, False, False, False
					if isMatched_(dt, genels, 0.02): dtIsGenEl = True
					elif isMatched_(dt, genmus, 0.02): dtIsGenMu = True
					elif isMatched_(dt, genpis, 0.02): dtIsGenPi = True					
					else: dtIsGenFake = True																				
			
			
			for idt, dt in enumerate(disappearingCRTracks):
				if not (tag[1] + c.tracks_charge[dt[1]] == 0): continue
				if dt[0].DeltaR(tag[0])<0.01: continue   
				#if not metvec.Pt()>metthresh: continue# can try also including this before correction				
				correctedMet = metvec.Clone()
				correctedMet-=dt[0]###
				if not correctedMet.Pt()>metthresh: continue
		
				hDPhiLepsPiDT.Fill(correctedMet.DeltaPhi(dt[0]))
		
				#if not abs(correctedMet.DeltaPhi(dt[0]))<3.14159/2: continue
				#if not abs(correctedMet.DeltaPhi(tag[0]))<3.14159/2: continue
				#if PixStripsMode:
				#if not isMatched_([dt[0]], genpis, 0.02): continue
		
				dphileps = abs(dt[0].DeltaPhi(tag[0]))
				#hDPhiLepsPiDT.Fill(correctedMet.DeltaPhi(dt[0]))
				if not dphileps<2.8: continue
				if not dphileps<2.8: continue#3.14159: continue
		
				IMleplep = mttsam1(correctedMet, tag[0], dt[0])
				#IMleplep = PreciseMtautau(correctedMet.Pt(), correctedMet.Phi(),  tag[0], dt[0])#basil

				if (IMleplep < 0): 
					print 'mtt grumpy', IMleplep
					continue
				print 'IMleplep', IMleplep
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					IM = IMleplep
					dmMin = dIM
					probeTlv =  dt[0]
					dtindex = dt[1]
					probeIsDt = False
					probeIsCrDt = True					
					probeIsRecoEl = False
					probeIsRecoMu = False
					probeIsRecoPi = False					
	
			#pions in tau
			for ismearedPi, smearedPi in enumerate(SmearedPions):
				if not (tag[1] + smearedPi[1] == 0): continue
				if smearedPi[2].DeltaR(tag[0])<0.01: continue
				correctedMet = metvec.Clone()
				#can also put a "funny alternate MET cut here to make the two cases equivalent"
				if not correctedMet.Pt()>metthresh: continue
				dphileps = abs(smearedPi[2].DeltaPhi(tag[0]))
				if not dphileps<2.8: continue
				if not dphileps<2.8: continue#3.14159: continue
						
				IMleplep = mttsam1(correctedMet, tag[0], smearedPi[2]) 
				#if not isMatched_([smearedPi[0]], genpis, 0.02): continue
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep                    
					probeTlv = smearedPi[0]
					probeIsRecoEl = False
					probeIsRecoMu = False
					probeIsRecoPi = True
					probeIsDt = False
					probeIsCrDt = False					
		
			#electrons in tau 
			for ismearedEl, smearedEl in enumerate(SmearedElectrons):
				if not (tag[1] + smearedEl[1] == 0): continue
				if smearedEl[0].DeltaR(tag[0])<0.01: continue
				correctedMet = metvec.Clone()
		
				if not correctedMet.Pt()>metthresh: continue
				#if not abs(correctedMet.DeltaPhi(smearedEl[0]))<3.14159/2: continue
				#if not abs(correctedMet.DeltaPhi(tag[0]))<3.14159/2: continue
		
				dphileps = abs(smearedEl[2].DeltaPhi(tag[0]))
				if not dphileps<2.8: continue
				if not dphileps<2.8: continue#3.14159: continue
						
				IMleplep = mttsam1(correctedMet, tag[0], smearedEl[2]) 
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep                    
					probeTlv = smearedEl[0]
					probeIsRecoEl = True
					probeIsRecoMu = False
					probeIsRecoPi = False
					probeIsDt = False
					probeIsCrDt = False					
			#muons in tau
			for ismearedMu, smearedMu in enumerate(SmearedMuons):
				if not (tag[1] + smearedMu[1] == 0): continue
				if smearedMu[0].DeltaR(tag[0])<0.01: continue
				correctedMet = metvec.Clone()
		
				if not correctedMet.Pt()>metthresh: continue
				#if not abs(correctedMet.DeltaPhi(smearedMu[0]))<3.14159/2: continue
				#if not abs(correctedMet.DeltaPhi(tag[0]))<3.14159/2: continue
		
				dphileps = abs(smearedMu[2].DeltaPhi(tag[0]))
				if not dphileps<2.8: continue
				if not dphileps<2.8: continue
						
				IMleplep = mttsam1(correctedMet, tag[0], smearedMu[2]) 
				dIM = abs(IMleplep - zmass)
				if(dIM < dmMin):
					dmMin = dIM
					IM = IMleplep                    
					probeTlv = smearedMu[0]
					probeIsRecoEl = False
					probeIsRecoMu = True
					probeIsRecoPi = False
					probeIsDt = False 
					probeIsCrDt = False					                
						
			if dmMin<100:
	
				ProbePt   = probeTlv.Pt()
				ProbeEta = abs(probeTlv.Eta())
					
				if probeIsDt:
					fillth1(hNTrackerLayersDT_mu, c.tracks_trackerLayersWithMeasurement[dtindex], weight)
					#if DoGenMatching:
					#	if isgenmatched == 0: continue #uncomment to skip isGenMatcheding of Probes
					#if not isMatched_([probeTlv], genpis, 0.2): continue
					for histkey in  dInvMassPiDTHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassPiDTHist[histkey],IM,weight)                    
					if dmMin<window:
					  for histkey in  hPiProbePt_DTnums:
						if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]: 
							fillth1(hPiProbePt_DTnums[histkey], ProbePt, weight)
							if dtIsGenEl: fillth1(hElFromTauProbePt_DTnums[histkey], ProbePt, weight)
							if dtIsGenMu: fillth1(hMuFromTauProbePt_DTnums[histkey], ProbePt, weight)
							if dtIsGenPi: fillth1(hPiFromTauProbePt_DTnums[histkey], ProbePt, weight)							
							if dtIsGenFake: fillth1(hFakeFromTauProbePt_DTnums[histkey], ProbePt, weight)														
							
				if probeIsRecoPi:
					for histkey in  dInvMassPiRECOHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassPiRECOHist[histkey],IM, weight)
					if dmMin<window:
						for histkey in  hPiProbePt_RECOdens:
							if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
								fillth1(hPiProbePt_RECOdens[histkey], ProbePt, weight)
				if probeIsRecoMu:
					kappa = fetchKappa(abs(ProbeEta),min(ProbePt,9999.99), kappadictMu, maxKappaPt)
					for histkey in  dInvMassMuFromTauRECOHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassMuFromTauRECOHist[histkey],IM, weight)
							fillth1(dInvMassMuFromTauWtdRECOHist[histkey],IM, kappa*weight)
					if dmMin<window:
						for histkey in  hMuFromTauProbePt_RECOdens:
							if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
								fillth1(hMuFromTauProbePt_RECOdens[histkey], ProbePt, weight)
								fillth1(hMuFromTauProbePtWtd_RECOdens[histkey], ProbePt, kappa*weight)
				if probeIsRecoEl:
					kappa = fetchKappa(abs(ProbeEta),min(ProbePt,9999.99), kappadictEl, maxKappaPt)
					for histkey in  dInvMassElFromTauRECOHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassElFromTauRECOHist[histkey],IM, weight)
							fillth1(dInvMassElFromTauWtdRECOHist[histkey],IM, kappa*weight)
					if dmMin<window:
						for histkey in  hElFromTauProbePt_RECOdens:
							if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
								fillth1(hElFromTauProbePt_RECOdens[histkey], ProbePt, weight)
								fillth1(hElFromTauProbePtWtd_RECOdens[histkey], ProbePt, kappa*weight)
						
				if probeIsCrDt:
					fakerate = fetchFakeRate(c.HT, c.NVtx, hFr)
					for histkey in  dInvMassFakeFromTauCRHist:
						if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
							fillth1(dInvMassFakeFromTauCRHist[histkey],IM, weight)
							fillth1(dInvMassFakeFromTauWtdCRHist[histkey],IM, fakerate*weight)
					if dmMin<window:
						for histkey in  hFakeFromTauProbePt_CRdens:
							if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
								fillth1(hFakeFromTauProbePt_CRdens[histkey], ProbePt, weight)
								fillth1(hFakeFromTauProbePtWtd_CRdens[histkey], ProbePt, fakerate*weight)								

						   



fnew.cd()
hHt.Write()
hHtWeighted.Write()
hElTagPt.Write()
hElTagEta_.Write()
hMuTagPt.Write()
hMuTagEta.Write()
hEtaVsPhiDT.Write()
hDPhiLepsPiDT.Write()

#Dictionaries:
for histkey in hElProbePt_DTnums: 
	hElProbePt_DTnums[histkey].Write()    
	hElProbePt_RECOdens[histkey].Write()
	hGenElProbePt_DTnums[histkey].Write()    
	hGenElProbePt_RECOdens[histkey].Write() 
	hMuProbePt_DTnums[histkey].Write()    
	hMuProbePt_RECOdens[histkey].Write()
	hGenMuProbePt_DTnums[histkey].Write()    
	hGenMuProbePt_RECOdens[histkey].Write() 
	if not doPions: continue
	hPiProbePt_DTnums[histkey].Write()    
	hPiProbePt_RECOdens[histkey].Write()
	hGenPiProbePt_DTnums[histkey].Write()    
	hGenPiProbePt_RECOdens[histkey].Write()
	hElFromTauProbePt_RECOdens[histkey].Write()
	hMuFromTauProbePt_RECOdens[histkey].Write()
	hFakeFromTauProbePt_CRdens[histkey].Write()
	hElFromTauProbePtWtd_RECOdens[histkey].Write()
	hMuFromTauProbePtWtd_RECOdens[histkey].Write()    
	hFakeFromTauProbePtWtd_CRdens[histkey].Write()
  
  
	hElFromTauProbePt_DTnums[histkey].Write()
	hMuFromTauProbePt_DTnums[histkey].Write()
	hPiFromTauProbePt_DTnums[histkey].Write()
	hFakeFromTauProbePt_DTnums[histkey].Write()			

  
for histkey in  dProbeElTrkResponseDT_: 
	dProbeElTrkResponseDT_[histkey].Write()
	dProbeElTrkResponseRECO_[histkey].Write()
	dProbeMuTrkResponseDT_[histkey].Write()
	dProbeMuTrkResponseRECO_[histkey].Write()    
for histkey in  dInvMassElRECOHist:
	dInvMassElRECOHist[histkey].Write()
	dInvMassElDTHist[histkey].Write()
	dInvMassMuRECOHist[histkey].Write()
	dInvMassMuDTHist[histkey].Write()
	if not doPions: continue
	dInvMassPiRECOHist[histkey].Write()
	dInvMassPiDTHist[histkey].Write()
	dInvMassElFromTauRECOHist[histkey].Write()
	dInvMassElFromTauWtdRECOHist[histkey].Write()    
	dInvMassMuFromTauRECOHist[histkey].Write()
	dInvMassMuFromTauWtdRECOHist[histkey].Write()	
	dInvMassFakeFromTauCRHist[histkey].Write()
	dInvMassFakeFromTauWtdCRHist[histkey].Write()

hGenPtvsResp.Write()


hFakeCrBdtVsDxyIsShortEl.Write()
hFakeCrBdtVsDxyIsLongEl.Write()
hFakeCrBdtVsDxyIsShortMu.Write()
hFakeCrBdtVsDxyIsLongMu.Write()
hFakeCrBdtVsDxyIsShortPi.Write()
hFakeCrBdtVsDxyIsLongPi.Write()
hFakeCrBdtVsDxyIsShortFake.Write()
hFakeCrBdtVsDxyIsLongFake.Write()

print "just created file:", fnew.GetName()
hNTrackerLayersDT_el.Write()
hNTrackerLayersDT_mu.Write()
fnew.Close()





