import sys
import time
from ROOT import *
from utils import *
from glob import glob
from random import shuffle
trand = TRandom()

datamc = 'mc' 
mZ = 91

verbose = False 
ForceTopology = False
GenSwapTheThings = False

try: doGenVersion = bool(sys.argv[2])
except: doGenVersion = False
print 'doing gen version:', doGenVersion

UseSmearingTemplates_ = True 

matchingDeltaR = 0.02


try: fnames = sys.argv[1]
except: fnames = '/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root'

if UseSmearingTemplates_: fSmear = TFile('ScaleFactors/ResponseMC_allLengths2.root')
files = glob(fnames)
c = TChain('TreeMaker2/PreSelection')
if datamc == 'mc': 
        for fname in files:
                accessname = fname.replace('/eos/uscms','root://cmsxrootd.fnal.gov/')
                print 'adding', accessname
                c.Add(accessname)
if doGenVersion: addon = 'Truth'
else: addon = 'TagAndProbe'

shortinputname = (fnames.split('/')[-1]+'.root').replace('.root.root','.root')
fnew_ = TFile('KappaHists'+addon+'_'+shortinputname,'recreate')

hHt = makeHist('hHt','hHt',100,0,500, kBlack)
hHtWeighted = makeHist('hHtWeighted','hHtWeighted',100,0,500, kBlack)
hTagPt = makeHist('hTagPt','hTagPt',20,0,200, kBlack)
hTagEta = makeHist('hTagEta','hTagEta',25,0,2.5, kBlack)

ptbins = []
print binning['TrkPt']
for ibin, bin in enumerate(binning['TrkPt'][:-1]):
        ptbins.append((binning['TrkPt'][ibin],binning['TrkPt'][ibin+1]))
print 'ptbins', ptbins

etabins = []
print binning['TrkEta']
for ibin, bin in enumerate(binning['TrkEta'][:-1]):
        etabins.append((binning['TrkEta'][ibin],binning['TrkEta'][ibin+1]))
print etabins

lengthbins = [1,2]#pixel-only, pixel+tracker 


hInvMassElDict, hInvMassElGMDict, hInvMassDtDict, hInvMassDtGMDict = {}, {}, {}, {}

hPtResElDict, hPtResDtDict  = {}, {}
hPtElDict, hPtDtDict = {}, {}
hPtSmearDict  = {}

hPtChargeMisIdDict = {}
nbins, low, high = 40, 50, 130
for etabin_ in etabins:
        nBin = len(binning['TrkPt'])-1
        binArr = array('d',binning['TrkPt'])
        for trklen in lengthbins:        
                name = 'hPtEl_eta%dto%dlen%d' % (10*etabin_[0],10*etabin_[1],trklen)
                hPtElDict[(etabin_,trklen)] = TH1F(name,name,nBin,binArr)
                histoStyler(hPtElDict[(etabin_,trklen)],kGreen+2-trklen)
                name = name.replace('El','Dt')
                hPtDtDict[(etabin_,trklen)] = TH1F(name,name,nBin,binArr)
                histoStyler(hPtDtDict[(etabin_,trklen)],kAzure-trklen)
                name = 'hPtChargeMisId_eta%dto%dlen%d' % (10*etabin_[0],10*etabin_[1],trklen)
                hPtChargeMisIdDict[(etabin_,trklen)] = TH1F(name,name,nBin,binArr)        
                histoStyler(hPtChargeMisIdDict[(etabin_,trklen)],kAzure-trklen)
                for ptbin_ in ptbins:        
                        lenstr = 'len%d' % trklen
                        ider_ = 'eta%dto%d_pt%dto%d_%s' % (10*etabin_[0],10*etabin_[1],ptbin_[0],ptbin_[1], lenstr)
                        name = 'hInvMassEl_' + ider_
                        name = name.replace('9999','Inf')
                        hInvMassEl = makeHist(name,name, nbins, low, high, kGreen+2-trklen)
                        hInvMassElDict[(etabin_, ptbin_, trklen)] = hInvMassEl
                        name = name.replace('InvMass','PtRes').replace('_','_')
                        hPtResEl = makeHist(name,name, 350, -3.5, 3.5, kGreen+2-trklen)
                        hPtResElDict[(etabin_, ptbin_, trklen)] = hPtResEl        
                        name = 'hInvMassElGM_eta%dto%d_pt%dto%d_%s' % (10*etabin_[0],10*etabin_[1],ptbin_[0],ptbin_[1], trklen)
                        name = name.replace('9999','Inf')
                        hInvMassElGM = makeHist(name,name, nbins, low, high, kGreen+2-trklen)
                        hInvMassElGMDict[(etabin_, ptbin_, trklen)] = hInvMassElGM
                        name = 'hInvMassDt_' + ider_
                        name = name.replace('9999','Inf')
                        hInvMassDt = makeHist(name,name, nbins, low, high, kAzure-trklen)
                        hInvMassDtDict[(etabin_, ptbin_, trklen)] = hInvMassDt
                        name = name.replace('InvMass','PtRes').replace('_','_')
                        hPtResDt = makeHist(name,name, 350, -3.5, 3.5, kAzure-trklen)
                        hPtResDtDict[(etabin_, ptbin_, trklen)] = hPtResDt
                        if UseSmearingTemplates_:  hPtSmearDict[(etabin_, ptbin_, trklen)] = fSmear.Get(name)        
                        name = 'hInvMassDtGM_eta%dto%d_pt%dto%d_%s' % (10*etabin_[0],10*etabin_[1],ptbin_[0],ptbin_[1], trklen)
                        name = name.replace('9999','Inf')
                        hInvMassDtGM = makeHist(name,name, nbins, low, high, kGreen+2)
                        hInvMassDtGMDict[(etabin_, ptbin_, trklen)] = hInvMassDtGM                        

nEvents = c.GetEntries()
verbosity = round(10000)



t1 = time.time()
i0=0
for ientry_ in range(0,c.GetEntries()):
    if verbose and (not ientry_ in [2404, 15471]): continue ##skip
    if verbose: print '\n',ientry_,'==='*10
    if ientry_<i0+2: t0 = time.time()    
    if ientry_%verbosity==0:
            t1 = time.time()
            rtime1 = (time.time()-t0)*nEvents/(ientry_+1)*(1-1.0*ientry_/nEvents), 'sec'
            print 'processing', ientry_,'/',nEvents, ' = ', 1.0*ientry_/nEvents,'remaining time estimate: ', rtime1                 
    
    c.GetEntry(ientry_) 
    hHt.Fill(c.HT) #hHtWeighted.Fill(c.HT,c.CrossSection)
    weight = 1#c.CrossSection 
    
    genels = []
    for igp, gp in enumerate(c.GenParticles):
                if not gp.Pt()>5: continue                
                if not abs(c.GenParticles_PdgId[igp])==11: continue                                        
                if not c.GenParticles_Status[igp] == 1: continue           
                if not abs(gp.Eta())<2.4: continue
                if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue                                                
                genel_ = [gp,-int(abs(c.GenParticles_PdgId[igp])/c.GenParticles_PdgId[igp])]
                genels.append(genel_)

    for charge in [-1,1]:

        RecoElectrons = []
        HighPtElectrons = []
        for iel, electron in enumerate(c.Electrons):
                if not electron.Pt()>5: continue
                if not abs(electron.Eta())<2.4: continue
                if not (abs(electron.Eta())<1.4442 or abs(electron.Eta())>1.566): continue                                
                if not c.Electrons_passIso[iel]: continue
                elevec = TLorentzVector()
                elevec.SetPtEtaPhiE(electron.Pt(),electron.Eta(),electron.Phi(),electron.Energy())
                condition = c.Electrons_charge[iel]==-charge
                if condition: RecoElectrons.append([elevec,c.Electrons_charge[iel]])                
                if not electron.Pt()>30: continue
                condition = c.Electrons_charge[iel]==charge
                if condition: HighPtElectrons.append([elevec,c.Electrons_charge[iel]])

        muons = []
        for imu, muon in enumerate(c.Muons):
                if not muon.Pt()>10: continue
                if not abs(muon.Eta())<2.4: continue        
                muons.append([muon,c.Muons_charge[imu]])
        if not len(muons)==0: continue                



        if doGenVersion and (not ForceTopology):# and False:# false is for comparison reasons
                tag = [TLorentzVector(),-2]
                tag[0].SetPtEtaPhiE(0,0,0,0)
        else:
                if not len(HighPtElectrons)>0: continue
                tag = [HighPtElectrons[0][0].Clone(),HighPtElectrons[0][1]]
        
        nonTagElectrons = {}
        tagProbeMasses = {}
        disappearingTracks = {}
        dmMin = {}
        iprobe = {}
        for trklen in lengthbins: 
                nonTagElectrons[trklen] = []
                tagProbeMasses[trklen] = []
                dmMin[trklen] = 9999
                iprobe[trklen] = -1
                disappearingTracks[trklen] = []
        
        for itrack, track in enumerate(c.tracks):
                if not track.Pt()>5: continue
                if not isBasicTrack(c,itrack): continue                                        
                if isMatched_([track,c.tracks_charge[itrack]], [tag], matchingDeltaR, verbose): continue
                if int(c.tracks_charge[itrack]*tag[1])==1: continue 
                if not c.tracks_charge[itrack]==-charge: continue                        
                matchedEle = isMatched_([track, c.tracks_charge[itrack]], RecoElectrons, matchingDeltaR, verbose)                        
                if matchedEle:
                        #print ientry_, 'the matched electron had charge', matchedEle[1]
                        pterr = c.tracks_ptError[itrack]/(track.Pt()*track.Pt())
                        if not (pterr<0.005): continue
                        etaBin = findbin(etabins, abs(matchedEle[0].Eta()))
                        ptBin = findbin(ptbins, matchedEle[0].Pt())
                        for trklen in lengthbins:
                                if UseSmearingTemplates_: smear = pow(10,hPtSmearDict[(etaBin, ptBin, trklen)].GetRandom())
                                else: smear = 1.0
                                singleEleVec = TLorentzVector()
                                singleEleVec.SetPtEtaPhiE(smear*matchedEle[0].Pt(), matchedEle[0].Eta(), matchedEle[0].Phi(), smear*matchedEle[0].Energy())                                
                                if not singleEleVec.Pt()>15: continue                        
                                if not singleEleVec.Pt()<600: continue        
                                nonTagElectrons[trklen].append([singleEleVec.Clone(), matchedEle[1]])
                                m = (nonTagElectrons[trklen][-1][0]+tag[0]).M()
                                dm = abs(mZ-m)
                                if dm<dmMin[trklen]: dmMin[trklen], iprobe[trklen] = dm, itrack                                        
                        continue
                trklen = isDisappearingTrack(c, itrack)
                if trklen==-1: continue #not a disappearing track
                disappearingTracks[trklen].append([c.tracks[itrack], c.tracks_charge[itrack]])
                m = (track+tag[0]).M()
                dm = abs(mZ-m)
                if dm<dmMin[trklen]: dmMin[trklen], iprobe[trklen] = dm, itrack

        #print ientry_, 'nonTagElectrons', nonTagElectrons

        if verbose: print 'disappearingTracks', disappearingTracks, 'nonTagElectrons', nonTagElectrons
        if doGenVersion:
                for trklen in lengthbins:
                        if verbose: print 'we got iprobe', iprobe[trklen]        
                        if not (len(nonTagElectrons[trklen])>0 or len(disappearingTracks[trklen])>0): continue
                        if (len(nonTagElectrons[trklen])>0 and len(disappearingTracks[trklen])>0): continue                
                        for genel in genels:
                                genEtaBin = findbin(etabins,abs(genel[0].Eta()))                                
                                genPtBin = findbin(ptbins, genel[0].Pt())        
                                dt_ = isMatched_(genel, disappearingTracks[trklen], matchingDeltaR, verbose)        
                                genElIsDt = bool(dt_)        
                                el_ = isMatched_(genel, nonTagElectrons[trklen], matchingDeltaR, verbose)        
                                genElIsEl = bool(el_)        
                                if not (genElIsEl or genElIsDt): continue
                                if (genElIsEl and genElIsDt):  continue        
                                if genElIsEl:                                         
                                        fillth1(hPtResElDict[(genEtaBin,genPtBin,trklen)], TMath.Log10(el_[0].Pt()/genel[0].Pt()))
                                        if not GenSwapTheThings:                                
                                                etaBin, ptBin = findbin(etabins,abs(el_[0].Eta())), findbin(ptbins,el_[0].Pt())
                                        else: etaBin, ptBin = genEtaBin, genPtBin
                                        fillth1(hPtElDict[(etaBin,trklen)], el_[0].Pt(),weight)                                        
                                        fillth1(hInvMassElDict[(etaBin,ptBin,trklen)], mZ, weight)
                                if genElIsDt:  
                                        fillth1(hPtResDtDict[(genEtaBin,genPtBin,trklen)], TMath.Log10(dt_[0].Pt()/genel[0].Pt()))                                
                                        if dt_[1]*genel[1]==-1: fillth1(hPtChargeMisIdDict[(genEtaBin,trklen)], genel[0].Pt())
                                        if not GenSwapTheThings:                                                                        
                                                etaBin, ptBin = findbin(etabins,abs(dt_[0].Eta())), findbin(ptbins,dt_[0].Pt())
                                        else: etaBin, ptBin = genEtaBin, genPtBin                                                
                                        fillth1(hPtDtDict[(etaBin,trklen)], dt_[0].Pt(),weight)                                        
                                        fillth1(hInvMassDtDict[(etaBin,ptBin,trklen)], mZ, weight)
                                        print ientry_, 'found disappearing track, pt=', dt_[0].Pt(),dt_[1]
        else:
                for trklen in lengthbins:        
                        if not iprobe[trklen]>-1: continue
                        if verbose: print 'we got iprobe', iprobe[trklen]
                        doubleEleEvent_  = bool(len(HighPtElectrons)>0 and len(nonTagElectrons[trklen])==1) 
                        oneDtOneEleEvent = bool(len(HighPtElectrons)>0 and len(disappearingTracks[trklen])==1)
                        if not (doubleEleEvent_ or oneDtOneEleEvent): continue        
                        if (doubleEleEvent_ and oneDtOneEleEvent): continue
                        probe = [c.tracks[iprobe[trklen]], c.tracks_charge[iprobe[trklen]]]
                        if not isMatched_(probe, genels, matchingDeltaR, verbose): continue        #######        ############                        
                        dt_ = isMatched_(probe, disappearingTracks[trklen], matchingDeltaR, verbose)
                        probeIsDt = bool(dt_)
                        el_ = isMatched_(probe, nonTagElectrons[trklen], matchingDeltaR, verbose)
                        probeIsEl = bool(el_)
                        if not (probeIsEl or probeIsDt): continue
                        if (probeIsEl and probeIsDt): continue                        
                        if probeIsDt: reco_obj = dt_
                        elif probeIsEl: reco_obj = el_        
                        mZ_ = (reco_obj[0]+tag[0]).M()
                        genmatched = isMatched_(reco_obj, genels, matchingDeltaR, verbose) #if not bool(genmatched): continue
                        ptBin, etaBin = findbin(ptbins, reco_obj[0].Pt()), findbin(etabins,abs(reco_obj[0].Eta()))
                        if GenSwapTheThings:
                                if not bool(genmatched): continue
                                ptBin, etaBin = findbin(ptbins, genmatched[0].Pt()), findbin(etabins,abs(genmatched[0].Eta()))
                        if probeIsEl:                                         
                                fillth1(hPtElDict[(etaBin,trklen)], reco_obj[0].Pt(),weight)                                        
                                if isMatched_(el_, HighPtElectrons, matchingDeltaR, verbose): correction = 1.0
                                else: correction = 1.0
                                fillth1(hInvMassElDict[(etaBin,ptBin,trklen)],mZ_, correction*weight)
                                if genmatched: fillth1(hInvMassElGMDict[(etaBin,ptBin,trklen)], mZ_, correction*weight)
                        if probeIsDt: 
                                fillth1(hInvMassDtDict[(etaBin,ptBin,trklen)],mZ_, weight)
                                if genmatched: fillth1(hInvMassDtGMDict[(etaBin,ptBin,trklen)], mZ_, weight)                                        
                                fillth1(hPtDtDict[(etaBin,trklen)], reco_obj[0].Pt(),weight)                        
                                print ientry_, 'found disappearing track, pt=', reco_obj[0].Pt()
                
hHt.Write()#hHtWeighted.Write()
hTagPt.Write()
hTagEta.Write()
for key in hInvMassElDict:
        hInvMassElDict[key].Write()
        hInvMassDtDict[key].Write()        
        hPtResElDict[key].Write()
        hPtResDtDict[key].Write()        
        if not doGenVersion: 
                hInvMassDtGMDict[key].Write()        
                hInvMassElGMDict[key].Write()                        
for key in hPtChargeMisIdDict:
        hPtChargeMisIdDict[key].Write()
        hPtElDict[key].Write()        
        hPtDtDict[key].Write()                
print 'just created', fnew_.GetName()
fnew_.Close()
