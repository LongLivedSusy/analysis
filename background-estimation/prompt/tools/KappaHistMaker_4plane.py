
from ROOT import *
import sys
import numpy as np
import scipy.constants as scc
import math
from glob import glob
from random import shuffle
from utils import *
import random

GenOnly = True
RelaxGenKin = True

weight = 1 
gROOT.SetBatch()
gROOT.SetStyle('Plain')
verbose = False

hNTrackerLayersDT = TH1F('hNTrackerLayersDT','hNTrackerLayersDT',11,0,11)

try: inputFileNames = sys.argv[1]
except: 
    inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"
    inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_88_RA2AnalysisTree.root"
    print 'running on small default DYtoLL sample', inputFileNames
    
inputFiles = glob(inputFileNames)
x_ = len(inputFiles)

c = TChain("TreeMaker2/PreSelection")

#fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root'
fname = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_8_0_21/src/DataDrivenSmear_2016MC.root'
fSmear  = TFile(fname)

dResponseHist = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
    for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
        newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
        dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))
        
print 'dResponseHist', dResponseHist
def getSmearFactor(Eta, Pt, Draw = False):
    for histkey in  dResponseHist:
        if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
        	SF_trk = 10**(dResponseHist[histkey].GetRandom())
        	return SF_trk #/SF_ele
    print 'returning 1'
    return 1
    
dProbeTrkResponseHist_ = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
    for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
        newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
        dProbeTrkResponseHist_[newHistKey] = makeTh1("hProbeTrkresp"+str(newHistKey),"hProbeTrkresp"+str(newHistKey), 100,-2,2)
        histoStyler(dProbeTrkResponseHist_[newHistKey], 1)


dInvMassRECOHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
    for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
        newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
        dInvMassRECOHist[newHistKey] = makeTh1("hInvMass"+str(newHistKey)+"RECO_den"  , "hInvMass"+str(newHistKey)+"RECO_den", 40, 60, 120)
        histoStyler(dInvMassRECOHist[newHistKey], 1)

dInvMassDTHist = {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
    for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
        newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
        dInvMassDTHist[newHistKey] = makeTh1("hInvMass"+str(newHistKey)+"DT_num"  , "hInvMass"+str(newHistKey)+"DT_num", 40, 60, 120)
        histoStyler(dInvMassDTHist[newHistKey], 1)

##adapt script for BDT disappearing track
readerPixelOnly = TMVA.Reader()
pixelXml = '/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel3-200-4-short/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelOnly, pixelXml)
readerPixelStrips = TMVA.Reader()
trackerXml = '/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel2-200-4-medium/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelStrips, trackerXml)

def main():
    for f in inputFiles:
        print 'adding file:', f
        c.Add(f)
        
    nentries = c.GetEntries()
    print nentries, ' events to be analyzed'
    verbosity = 10000
    identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
    identifier+='nFiles'+str(len(inputFiles))

    hHTnum        = makeTh1("hHTnum","HT for number of events", 150,40,2500)
    hne          = makeTh1("hne", "number of electrons", 4, 0, 4)
    hIMcheck          = makeTh1("hIMcheck"  , "IM  ", 60, 20, 180)
    hEleGenPt         = makeTh1VB("hEleGenPt", ";m [GeV] ;pt of the gen Ele;;", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtRECO_den      = makeTh1VB("hEleGenPtRECO_den", ";m [GeV] ;pt of the RECO Ele;;", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtDT_num    = makeTh1VB("hEleGenPtDT_num", "pt of the DT Ele", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtbarrelRECO_den      = makeTh1VB("hEleGenPtbarrelRECO_den", ";m [GeV] ;pt of the RECO Ele;;", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtbarrelDT_num    = makeTh1VB("hEleGenPtbarrelDT_num", "pt of the DT Ele", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtECRECO_den      = makeTh1VB("hEleGenPtECRECO_den", ";m [GeV] ;pt of the RECO Ele;;", len(PtBinEdges)-1,PtBinEdges)
    hEleGenPtECDT_num    = makeTh1VB("hEleGenPtECDT_num", "pt of the DT Ele", len(PtBinEdges)-1,PtBinEdges)
    hEleGenEta        = makeTh1VB("hEleGenEta", "Eta of the gen Ele", len(EtaBinEdges)-1,EtaBinEdges)
    hEleGenEtaRECO_den     = makeTh1VB("hEleGenEtaRECO_den", "Eta of the gen Ele", len(EtaBinEdges)-1,EtaBinEdges)
    hEleGenEtaDT_num       = makeTh1VB("hEleGenEtaDT_num", "Eta of the reco Ele", len(EtaBinEdges)-1,EtaBinEdges)
    hEleProbePt       = makeTh1VB("hEleProbePt", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtDT_num      = makeTh1VB("hEleProbePtDT_num", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtbarrelDT_num      = makeTh1VB("hEleProbePtbarrelDT_num", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtECDT_num      = makeTh1VB("hEleProbePtECDT_num", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtRECO_den    = makeTh1VB("hEleProbePtRECO_den", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtbarrelRECO_den    = makeTh1VB("hEleProbePtbarrelRECO_den", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbePtECRECO_den    = makeTh1VB("hEleProbePtECRECO_den", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    #hEleProbePtDTmeff      = makeTh1VB("hEleProbePtDTmeff", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
    hEleProbeEta      = makeTh1VB("hEleProbeEta", "Eta of the EleProbes", len(EtaBinEdges)-1,EtaBinEdges)
    hEleProbeEtaDT_num     = makeTh1VB("hEleProbeEtaDT_num", "Eta of the EleProbes", len(EtaBinEdges)-1,EtaBinEdges)
    hEleProbeEtaDTmeff     = makeTh1VB("hEleProbeEtaDTmeff", "Eta of the EleProbes", len(EtaBinEdges)-1,EtaBinEdges)
    hEleProbeEtaRECO_den   = makeTh1VB("hEleProbeEtaRECO_den", "Eta of the EleProbes", len(EtaBinEdges)-1,EtaBinEdges)
    hEleTagPt         = makeTh1VB("hEleTagPt"  , "pt of the EleTags", len(PtBinEdges)-1,PtBinEdges)
    hEleTagEta        = makeTh1VB("hEleTagEta"  , "Eta of the EleTags", len(EtaBinEdges)-1,EtaBinEdges)
    hbkgID              = makeTh1("hbkgID", "background pdgID", 100, -25, 25)
    hEleControlPt         = makeTh1VB("hEleControlPt"  , "hEleControlPt", len(PtBinEdges)-1,PtBinEdges)
    hEleSmearedControlPt         = makeTh1VB("hEleSmearedControlPt"  , "hEleSmearedControlPt", len(PtBinEdges)-1,PtBinEdges)
    hprobe        = makeTh1("hprobe"  , "probe status", 2, 0, 2)
    hIMmuZ        = makeTh1("hIMmuZ"  , "IM z ", 60, 20, 150)
    hIMmuZsmear       = makeTh1("hIMmuZsmear"  , "IM z smeared ", 60, 20, 150)
    hIMZ          = makeTh1("hIMZ"  , "IM z ", 40, 60, 120)
    hIMZRECO_den       = makeTh1("hIMZRECO_den"  , "IM tag + RECOing probe ", 40, 60, 120)
    hIMZDT_num         = makeTh1("hIMZDT_num"  , "IM tag + DTing probe ", 40, 60, 120)
    hIMZDTmeff        = makeTh1("hIMZDTmeff"  , "IM tag + DTing probe ", 40, 60, 120)
    heleresp         =makeTh1("heleresp","electron response", 50,-3,3.2)
    hRelErrPtvsptMu    = makeTh2("hRelErrPtvsptMu","hRelErrPtvsptMu",50, 10, 400, 20, 0 ,2)
    hRelErrPtvsptTrk       = makeTh2("hRelErrPtvsptTrk","hRelErrPtvsptTrk",50, 10, 400, 20, 0 ,2)
    hGenPtvsResp    = makeTh2("hGenPtvsResp","hGenPtvsResp",50, 10, 400, 20, -2 ,3)     
    hGenPtvsRespS    = makeTh2("hGenPtvsRespS","hGenPtvsRespS",50, 10, 400, 20, -2 ,3)
    hGenPtvsRespM    = makeTh2("hGenPtvsRespM","hGenPtvsRespM",50, 10, 400, 20, -2 ,3)
    hGenPtvsRespL    = makeTh2("hGenPtvsRespL","hGenPtvsRespL",50, 10, 400, 20, -2 ,3)
    hPtvsEtaRECO_den    = makeTh2VB("hPtvsEtaRECO_den","hPtvsEtaRECO_den",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
    hPtvsEtaDT_num    = makeTh2VB("hPtvsEtaDT_num","hPtvsEtaDT_num",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
    hGenPtvsEtaRECO_den    = makeTh2VB("hGenPtvsEtaRECO_den","hGenPtvsEtaRECO_den",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
    hGenPtvsEtaDT_num    = makeTh2VB("hGenPtvsEtaDT_num","hGenPtvsEtaDT_num",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
    hEleProbePtDTmeff      = makeTh1VB("hEleProbePtDTmeff", "pt of the EleProbes", len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'))
    
    jentry=0
    n = 0
    f = 0
    rand = 1
    e1 = 0
    e2 = 0
    e3 = 0
    etaMax = 2.4
        
    for ientry in range(nentries):
        if verbose:
            if not ientry in [8841]: continue
        if ientry%verbosity==0:
            print 'now processing event number', ientry, 'of', nentries
        c.GetEntry(ientry)
        full = 2.4 
        weight = 1 #(c.CrossSection*35.9)/(1*.001)
        SmearedelePt = 0
        fillth1(hHTnum, c.madHT)
        flag_DT = -1
        recof = 0
        nmu = -1
        TagPt  =  0
        TagEta  =  0
        TagCharge = 0
        ProbePt  =  0
        ProbeEta = 0
        ProbeCharge = 0
        dumTlvsum = TLorentzVector()
        dumTlvsum.SetPxPyPzE(0, 0, 0, 0)
        tagTlv = TLorentzVector()
        tagTlv.SetPxPyPzE(0, 0, 0, 0)
        tagProbeTlvSum = TLorentzVector()
        tagProbeTlvSum.SetPxPyPzE(0, 0, 0, 0)
        smearedEleProbe = TLorentzVector()
        smearedEleProbe.SetPtEtaPhiE(0, 0, 0, 0)
        probeTlv = TLorentzVector()
        probeTlv.SetPxPyPzE(0, 0, 0, 0)
        dtTlvsum = TLorentzVector()
        dtTlvsum.SetPxPyPzE(0, 0, 0, 0)
        checkTlvsum = TLorentzVector()
        checkTlvsum.SetPxPyPzE(0, 0, 0, 0)
        ne = 0
        muons = []		
        for imu, muon in enumerate(c.Muons):
        	if not muon.Pt()>10: continue
        	#if abs(muon.Eta()) < 1.566 and abs(muon.Eta()) > 1.4442: continue
        	if not abs(muon.Eta())<2.4: continue	
        	muons.append([muon,c.Muons_charge[imu]])
        if not len(muons)==0: continue	
        if verbose: print 'test no muons'
        
        genels = []
        for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue		
			if not (abs(c.GenParticles_PdgId[igp])==11 and c.GenParticles_Status[igp] == 1) : continue			
			if not c.GenParticles_Status[igp] == 1: continue		
			if not abs(gp.Eta())<2.4: continue
			#if not abs(gp.Eta())<1.445: continue			
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue						
			genels.append([gp,igp])
        if not len(genels)==1: continue
        if verbose: print 'test genels'
        		
        basicTracks = []
        disappearingTracks = []        
        for itrack, track in enumerate(c.tracks):
            if not track.Pt() > 20 : continue
            if not abs(track.Eta()) < 2.4: continue
            if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
            if not isBaselineTrack(track, itrack, c): continue
            basicTracks.append([track,c.tracks_charge[itrack], itrack])
            if not track.Pt()<600: continue
            if not isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips): continue
            #print 'found disappearing track w pT =', track.Pt()
            drlep = 99
            passeslep = True
            for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)): 
            	drlep = min(drlep, lep.DeltaR(track))
            	if drlep<0.01: 
            		passeslep = False
            		break
            if not passeslep: continue
            disappearingTracks.append([track,c.tracks_charge[itrack]])
                        
                        
        mva, dedx, trkpt, trketa, trkp = -999, -999, -999, -999, -999
        nprompt = 0
        moh = -1
        pt = -1


        RecoElectrons = []        
        SmearedElectrons = []
        TightElectrons = []        
        for iel, ele in enumerate(c.Electrons):
            if not ele.Pt()>5: continue                  
            if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
            if not abs(ele.Eta())<2.4: continue      
            if not c.Electrons_passIso[iel]: continue
            if (ele.Pt() > 30 and c.Electrons_passIso[iel] and bool(c.Electrons_tightID[iel])):
            	TightElectrons.append([ele,c.Electrons_charge[iel]])
            matchedTrack = TLorentzVector()             
            drmin = 9999
            for trk in basicTracks:
            		if not c.tracks_nMissingOuterHits[trk[2]]==0: continue
            		drTrk = trk[0].DeltaR(ele)
            		if drTrk<drmin:
						drmin = drTrk
						matchedTrack = trk[0]
						if drTrk<0.01: break
            if not drmin<0.01: continue
            RecoElectrons.append([ele,iel])
            smear = getSmearFactor(abs(matchedTrack.Eta()), min(matchedTrack.Pt(),299.999))
            smearedEle = TLorentzVector()            
            smearedEle.SetPtEtaPhiE(smear*matchedTrack.Pt(),matchedTrack.Eta(),matchedTrack.Phi(),smear*matchedTrack.E())
            if not (smearedEle.Pt()>20 and smearedEle.Pt()<600): continue
            SmearedElectrons.append([smearedEle, c.Electrons_charge[iel]])
            #print 'a lovely ele', ele.Pt(), smearedEle.Pt()                     

        for igen, genel in enumerate(genels):
            drminDtGenel  = 9999                
            iddt = -1
            for idistrk, distrk in enumerate(disappearingTracks):
                dr = genel[0].DeltaR(distrk[0])
                if dr < drminDtGenel:
                    drminDtGenel = dr
                    iddt = idistrk
                    if verbose: print dr
            if drminDtGenel < .02:
            	dt = disappearingTracks[iddt][0]
            	if RelaxGenKin: pt, eta = dt.Pt(),abs(dt.Eta())
            	else: pt, eta = genel[0].Pt(), abs(genel[0].Eta())
                fillth2(hGenPtvsEtaDT_num, pt, eta, weight)
                fillth1(hEleGenPtDT_num, pt, weight)
                fillth1(hbkgID, c.GenParticles_PdgId[genel[1]], weight)
                fillth1(hEleGenEtaDT_num, abs(eta), weight)
                fillth2(hGenPtvsResp, math.log10(dt.Pt()/genel[0].Pt()),genel[0].Pt(),weight)
                print ientry, 'found a nice dt', dt.Pt()
                continue        
            idlep   = -1
            fillth1(hEleGenPt, genel[0].Pt(), weight)
            fillth1(hEleGenEta, abs(genel[0].Eta()), weight)
            drminSmearedelGenel = 9999            
            for ie, ele in enumerate(SmearedElectrons):
                dr = genel[0].DeltaR(ele[0])
                if dr < drminSmearedelGenel:
                    drminSmearedelGenel = dr
                    idlep   = ie
            if drminSmearedelGenel < .02:
            	se = SmearedElectrons[idlep][0]
                fillth2(hGenPtvsEtaRECO_den, se.Pt(), abs(se.Eta()), weight )#This seemed to be calling the last iterated electron
                fillth1(hEleGenPtRECO_den, se.Pt(), weight)
                fillth1(hEleGenEtaRECO_den, abs(se.Eta()), weight)
                fillth1(heleresp, math.log10(se.Pt()/genel[0].Pt()),weight)
                #print ientry, 'found a tawdry se', se.Pt()
  
        if GenOnly: continue
        tagTlv = TLorentzVector()
        tagTlv.SetPxPyPzE(0,0,0,0)
        for charge in range(-1,2,2):
            for itag, tag in enumerate(TightElectrons):	
                if not tag[1]==charge: continue
                IM  =  0 
                dIM =  0                
                TagPt, TagEta = tag[0].Pt(), tag[0].Eta()
                probeIsEl, probeIsDt = False, False
                dmMin = 999
                for idt, dt in enumerate(disappearingTracks):
                    if not (tag[1] + dt[1] == 0): continue
                    if dt[0].DeltaR(tag[0])<0.01: continue        
                    IMleplep = (tag[0] + dt[0]).M()
                    if (IMleplep < 0): 
                    	print 'something horribly wrong, space-like event'
                    	continue
                    dIM = abs(IMleplep - 91)
                    if(dIM < dmMin):
                        dmMin = dIM
                        IM = IMleplep
                        probeTlv =  dt[0]
                        ProbeCharge = dt[1]
                        probeIsDt = True
                        probeIsEl = False            
                for iSmearedEl, smearedEl in enumerate(SmearedElectrons):
                    if not (tag[1] + smearedEl[1] == 0): continue
                    if smearedEl[0].DeltaR(tag[0])<0.01: continue                    
                    IMleplep = (tag[0] + smearedEl[0]).M()
                    fillth1(hIMmuZ, IMleplep, weight)
                    fillth1(hIMmuZsmear, IMleplep, weight)
                    dIM = abs(IMleplep - 91)
                    if(dIM < dmMin):
                        dmMin = dIM
                        IM     = IMleplep
                        probeTlv  = smearedEl[0]
                        ControlPt = RecoElectrons[iSmearedEl][0].Pt() # should be same as deemedgen_elePt
                        ProbeCharge = smearedEl[1]
                        probeIsEl = True
                        probeIsDt = False                        


                if (IM > 60 and IM < 120):
                    gm = 0
                    if probeIsDt:
                        ProbePt = probeTlv.Pt()
                        ProbeEta = abs(probeTlv.Eta())
                        fillth1(hEleTagPt, TagPt, weight)
                        fillth1(hEleProbePt, ProbePt, weight)
                        fillth1(hEleTagEta, TagEta, weight)
                        fillth1(hEleProbeEta, ProbeEta, weight)
                        #print ientry, 'inside disappearing track', IM, ProbePt   
                        fillth1(hIMZ, IM, weight)
                        fillth1(hIMZDTmeff, IM, weight)
                        fillth1(hEleProbePtDTmeff, ProbePt, weight)
                        fillth1(hEleProbeEtaDTmeff, ProbeEta, weight)
                        gm  = genMatch(probeTlv)
#                        if gm == 0: continue #uncomment to skip genMatching of Probes
                        fillth2(hPtvsEtaDT_num, ProbePt, ProbeEta, weight)
                        fillth1(hIMZDT_num, IM, weight)
                        fillIMdt(ProbeEta, ProbePt,IM)
                        fillth1(hEleProbePtDT_num, ProbePt, weight)
                        fillResponse(ProbeEta, ProbePt, gm,min(gm, 299.99), dProbeTrkResponseHist_)
                        if ProbeEta < 1.4442: fillth1(hEleProbePtbarrelDT_num, ProbePt, weight)
                        if ProbeEta > 1.4442: fillth1(hEleProbePtECDT_num, ProbePt, weight)
                        fillth1(hEleProbeEtaDT_num, ProbeEta, weight)
                    if probeIsEl:
                        gm  = genMatch(probeTlv)
                        fillth1(hEleControlPt, ControlPt, weight)
                        fillth1(hEleSmearedControlPt, ProbePt, weight)
#                        if gm == 0: continue #uncomment to skip genMatching of Probes
                        fillth1(hIMZ, IM, weight)  ##try to use this to get counts
                        ProbePt   = probeTlv.Pt()
                        ProbeEta = abs(probeTlv.Eta())
                        fillth2(hPtvsEtaRECO_den, ProbePt, ProbeEta, weight)    
                        fillth1(hEleTagPt, TagPt, weight)
                        #print ientry, 'inside smeared el', IM, ProbePt                           
                        #fillth1(hEleProbePt, ProbePt, weight)
                        fillth1(hEleTagEta, TagEta, weight)
                        fillth1(hEleProbeEta, ProbeEta, weight)
                        fillth1(hIMZRECO_den, IM, weight)
                        fillIMreco(ProbeEta, ProbePt, IM)
                        fillth1(hEleProbePtRECO_den, ProbePt, weight)
                        if ProbeEta < 1.4442 : fillth1(hEleProbePtbarrelRECO_den, ProbePt, weight)
                        if ProbeEta > 1.4442 : fillth1(hEleProbePtECRECO_den, ProbePt, weight)
                        fillth1(hEleProbeEtaRECO_den, ProbeEta, weight)
                        recof = 1                

    print "RECOing probe", f , "DTing probes", n

    fnew = TFile('TagnProbeEleHists_'+identifier+'.root','recreate')
    print 'making', 'TagnProbeEleHists_'+identifier+'.root'
    fnew.cd()
    hbkgID.Write()
    hEleSmearedControlPt.Write()
    hEleControlPt.Write()
    hGenPtvsEtaRECO_den.Write()
    hGenPtvsEtaDT_num.Write()
    hPtvsEtaRECO_den.Write()
    hPtvsEtaDT_num.Write()

    hIMcheck.Write()
    hHTnum.Write()

    hEleGenPt.Write()
    hEleGenEta.Write()

    hEleGenPtRECO_den.Write()
    hEleGenPtbarrelRECO_den.Write()
    hEleGenPtECRECO_den.Write()
    hEleGenEtaRECO_den.Write()

    hEleGenPtDT_num.Write()
    hEleGenPtbarrelDT_num.Write()
    hEleGenPtECDT_num.Write()
    hEleGenEtaDT_num.Write()
    hEleTagPt.Write()
    hEleTagEta.Write()

    hEleProbePt.Write()
    hEleProbeEta.Write()
    hIMZ.Write()
    hIMmuZsmear.Write()
    hIMmuZ.Write()
    hprobe.Write()

    hIMZRECO_den.Write()
    hEleProbePtRECO_den.Write()
    hEleProbePtbarrelRECO_den.Write()
    hEleProbePtECRECO_den.Write()
    hEleProbeEtaRECO_den.Write()
    hIMZDT_num.Write()
    hEleProbePtDT_num.Write()
    hEleProbePtbarrelDT_num.Write()
    hEleProbePtECDT_num.Write()
    hEleProbeEtaDT_num.Write()

    #InvMassRECO
    for histkey in  dProbeTrkResponseHist_: dProbeTrkResponseHist_[histkey].Write()
    for histkey in  dInvMassRECOHist: dInvMassRECOHist[histkey].Write()
    for histkey in  dInvMassDTHist: dInvMassDTHist[histkey].Write()
    #response
    heleresp.Write()
    hRelErrPtvsptTrk.Write()

    hGenPtvsResp.Write()
    hGenPtvsRespS.Write()
    hGenPtvsRespM.Write()
    hGenPtvsRespL.Write()
    hne.Write()
    print "just created file:", fnew.GetName()
    fnew.Close()


def genMatch(lep):
    for igenm, genm in enumerate(c.GenParticles):
        if not genm.Pt() > 10: continue
        if not abs(c.GenParticles_ParentId[igenm]) == 23: continue
        if not (abs(c.GenParticles_PdgId[igenm]) == 11 and c.GenParticles_Status[igenm] == 1):continue
        drm = genm.DeltaR(lep)
        if drm < .01:
            return genm.Pt()
    return 0



def fillIMreco(Eta, Pt, InvM):
    for histkey in  dInvMassRECOHist:
        if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
            fillth1(dInvMassRECOHist[histkey],InvM,weight)
            return 1
    return 1

def fillIMdt(Eta, Pt, InvM):
    for histkey in  dInvMassDTHist:
        if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
            fillth1(dInvMassDTHist[histkey],InvM,weight)
            return 1
    return 1

def fillResponse(Eta, SmearedPt, GenPt, decisionPt, dictionary):
    for histkey in  dictionary:
        if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and decisionPt > histkey[1][0] and decisionPt < histkey[1][1]:
            fillth1(dictionary[histkey],math.log10(SmearedPt/GenPt),weight)
            return 1
    return 1

main()
