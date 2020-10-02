import DataFormats.FWLite as fwlite
import ROOT 
import math
import numpy as np
from commons import *
import os,sys
from glob import glob
from shared_utils import *

ROOT.TH1.SetDefaultSumw2(True)

try: 
    inputfiles = glob(sys.argv[1])
except: 
#    inputfiles = glob("/afs/desy.de/user/s/spak/dust/DisappearingTracks/FastSim/output/smallchunks/SUS-RunIISummer15GS-00734_T2btLLFastSim_*.root")
    inputfiles = [
	    "root://xrootd-cms.infn.it//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/DED79FC2-74A5-E911-8BA3-002590E39D90.root",
	    "root://xrootd-cms.infn.it//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/32262683-5EA5-E911-BFC3-3C4A92F8DC66.root",
	    "root://xrootd-cms.infn.it//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/08D82DA4-5DA5-E911-8F9A-A0369FE2C22E.root",
	    "root://xrootd-cms.infn.it//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/B64B10BA-6BA5-E911-B5B2-AC1F6B0DE348.root",
	    "root://xrootd-cms.infn.it//store/mc/RunIISummer16DR80Premix/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_longlived_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/0AABDACD-7AA5-E911-8B31-AC1F6B0DE33E.root",
	    ]

events = fwlite.Events(inputfiles)


primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
genParticles = fwlite.Handle("std::vector<reco::GenParticle>")
tracks_handle = fwlite.Handle("std::vector<reco::Track>")

dEdxPixelTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
dEdxStripsTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
#label_dEdXtrack = 'dedxPixelHarmonic2'
#label_dEdXtrack = 'dedxHarmonic2'


tlegend = ROOT.TLegend(0.17, 0.77, 0.51, 0.88)

outDir = './LLchargino'
if not os.path.exists(outDir):
    os.system('mkdir -p '+outDir)

outputName = inputfiles[-1].split('/')[-1]
if 'FastSim' in outputName : output = outDir+'/SUS-RunIISummer15GS-00734_T2btLLFastSim.root'
else : output = outDir+'/SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'

print 'output : ',output

fnew = ROOT.TFile(output,'recreate')

# Histograms
P_chargino = ROOT.TH1F("P_chargino","chargino total momentum [GeV]", 200, 0, 2000)
pt_chargino = ROOT.TH1F("pt_chargino","chargino transverse momentum [GeV]", 200, 0, 2000)
eta_chargino = ROOT.TH1F("eta_chargino","chargino pseudo-rapidity", 50, -2.5, 2.5)
phi_chargino = ROOT.TH1F("phi_chargino","chargino phi", 50, -3.14, 3.14)

P_chargino_trackmatch = ROOT.TH1F("P_chargino_trackmatch","chargino after track matching, total momentum [GeV]", 200, 0, 2000)
P_chargino_trackmatch_pt1200 = ROOT.TH1F("P_chargino_trackmatch_pt1200","chargino after track matching, total momentum [GeV]", 500, 0, 5000)
pt_chargino_trackmatch = ROOT.TH1F("pt_chargino_trackmatch","chargino after track matching, transverse momentum [GeV]", 200, 0, 2000)
pt_chargino_trackmatch_pt1200 = ROOT.TH1F("pt_chargino_trackmatch_pt1200","chargino after track matching, transverse momentum [GeV]", 500, 0, 5000)
eta_chargino_trackmatch = ROOT.TH1F("eta_chargino_trackmatch","chargino after track matching, pseudo-rapidity", 50, -2.5, 2.5)
eta_chargino_trackmatch_pt1200 = ROOT.TH1F("eta_chargino_trackmatch_pt1200","chargino after track matching, pseudo-rapidity", 50, -2.5, 2.5)
phi_chargino_trackmatch = ROOT.TH1F("phi_chargino_trackmatch","chargino phi after track matching,", 50, -3.14, 3.14)
phi_chargino_trackmatch_pt1200 = ROOT.TH1F("phi_chargino_trackmatch_pt1200","chargino phi after track matching,", 50, -3.14, 3.14)

P_track = ROOT.TH1F("P_track","track total momentum [GeV]", 200, 0, 2000)
pt_track = ROOT.TH1F("pt_track","track transverse momentum [GeV]", 200, 0, 2000)
eta_track = ROOT.TH1F("eta_track","track pseudo-rapidity", 50, -2.5, 2.5)
phi_track = ROOT.TH1F("phi_track","track phi", 50, -3.14, 3.14)
pixeldedx_track = ROOT.TH1F("pixeldedx_track","pixel dedx",150,0,15)
stripsdedx_track = ROOT.TH1F("stripsdedx_track","strips dedx",150,0,15)


events.toBegin()
findMatch = 0
for i, event in enumerate(events):

    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("genParticles", genParticles)
    event.getByLabel("generalTracks", tracks_handle)
    event.getByLabel("dedxPixelHarmonic2", dEdxPixelTrackHandle)
    event.getByLabel("dedxHarmonic2", dEdxStripsTrackHandle)
    
    if i > 30000: break
    #if i > 100: break
    if i%1000==0:print 'passing {}th event'.format(i)
    
    genparticles = genParticles.product()
    tracks = tracks_handle.product()
    dEdxPixelTrack = dEdxPixelTrackHandle.product()
    dEdxStripsTrack = dEdxStripsTrackHandle.product()

    for j, gp in enumerate(genparticles):
	#if abs(gp.pdgId()) == 1000024 : print i,' th event ',j,'th genparticle pdgid:', gp.pdgId()
	if not abs(gp.pdgId()) == 1000024 : continue
	if not gp.isLastCopy() : continue
	if not gp.pt() > 20 : continue
	
	fillth1(P_chargino,gp.p())
	fillth1(pt_chargino,gp.pt())
	fillth1(eta_chargino,gp.eta())
	fillth1(phi_chargino,gp.phi())

	
	drmin = 10
	idx = -1
	matchingTrack = None
	match = False
	threshold = 0.01
	
	for itrack, track in enumerate(tracks) :
	    #if not passesPreselection_basic_track(track) : continue
	    if not track.numberOfValidHits() > 0: continue
	    if not track.ndof() > 0: continue
	    if not abs(track.charge()) > 0: continue
	    #if not track.quality(2) : continue # 2: high-purity track quality
	    if not track.pt()>10 : continue
	    
	    if not track.charge() * gp.charge() > 0: continue
	    #if not abs(track.pt() - gp.pt()) / gp.pt() < 0.2: continue
	    
	    gpTlv = TLorentzVector()
	    gpTlv.SetPxPyPzE(gp.px(),gp.py(),gp.pz(),gp.energy())	
	    trkTlv = TLorentzVector()
	    trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt()*np.cosh(track.eta()))
	    
	    dr = trkTlv.DeltaR(gpTlv)

	    if dr < drmin:
	    		
	    	drmin = dr
	    	idx = itrack
	    	matchingTrack = track
	
	if drmin < threshold: 
	    match = True
	    dedxpixel = dEdxPixelTrack.get(idx).dEdx()
	    dedxstrips = dEdxStripsTrack.get(idx).dEdx()
	    #print ('{}th event {}th gp {}th track dR:{} pixeldedx:{} stripsdedx:{}'.format(i,j,itrack,drmin,dedxpixel,dedxstrips))
		
	    fillth1(P_chargino_trackmatch,gp.p())
	    fillth1(pt_chargino_trackmatch,gp.pt())
	    fillth1(eta_chargino_trackmatch,gp.eta())
	    fillth1(phi_chargino_trackmatch,gp.phi())

	    fillth1(P_track,matchingTrack.p())
	    fillth1(pt_track,matchingTrack.pt())
	    fillth1(eta_track,matchingTrack.eta())
	    fillth1(phi_track,matchingTrack.phi())
	    fillth1(pixeldedx_track,dedxpixel)
	    fillth1(stripsdedx_track,dedxstrips)

	    if gp.pt() > 1200 : 
		fillth1(P_chargino_trackmatch_pt1200,gp.p())
	    	fillth1(pt_chargino_trackmatch_pt1200,gp.pt())
	    	fillth1(eta_chargino_trackmatch_pt1200,gp.eta())
	    	fillth1(phi_chargino_trackmatch_pt1200,gp.phi())

fnew.cd()
fnew.Write()
print 'just created', fnew.GetName()
fnew.Close()
