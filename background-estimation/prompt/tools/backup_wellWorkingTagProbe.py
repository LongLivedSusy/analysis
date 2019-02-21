from ROOT import *
import sys
import numpy as np
from glob import glob
from utils import *
gROOT.SetBatch()
gROOT.SetStyle('Plain')

GenOnly = False
RelaxGenKin = True
verbose = False

try: inputFileNames = sys.argv[1]
except: 
    inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_88_RA2AnalysisTree.root"
    inputFileNames = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_391_RA2AnalysisTree.root"
inputFiles = glob(inputFileNames)
x_ = len(inputFiles)
print 'going to analyze events in', inputFileNames

c = TChain("TreeMaker2/PreSelection")
#fname = '/nfs/dust/cms/user/singha/LLCh/BACKGROUNDII/CMSSW_8_0_20/src/MCTemplatesBinned/BinnedTemplatesIIDY_WJ_TT.root'
fname = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_8_0_21/src/DataDrivenSmear_2016MC.root'
fSmear  = TFile(fname)


#=====This sets up the smearing
dResponseHist = {}
for iPtBinEdge, PtBinEdge in enumerate(PtBinEdgesForSmearing[:-1]):
    for iEtaBinEdge, EtaBinEdge_ in enumerate(EtaBinEdgesForSmearing[:-1]):
        newHistKey = ((EtaBinEdge_,EtaBinEdgesForSmearing[iEtaBinEdge + 1]),(PtBinEdge,PtBinEdgesForSmearing[iPtBinEdge + 1]))
        dResponseHist[newHistKey] = fSmear.Get("htrkresp"+str(newHistKey))     
print 'smearing factors', dResponseHist
def getSmearFactor(Eta, Pt, Draw = False):
    for histkey in  dResponseHist:
        if abs(Eta) > histkey[0][0] and abs(Eta) < histkey[0][1] and Pt > histkey[1][0] and Pt < histkey[1][1]:
        	SF_trk = 10**(dResponseHist[histkey].GetRandom())
        	return SF_trk #/SF_ele
    print 'returning 1'
    return 1

hHt        = makeTh1("hHt","HT for number of events", 250,0,5000)
hHtWeighted        = makeTh1("hHtWeighted","HT for number of events", 250,0,5000)
hEleTagPt         = makeTh1VB("hEleTagPt"  , "pt of the EleTags", len(PtBinEdges)-1,PtBinEdges)
hEleTagEta        = makeTh1VB("hEleTagEta"  , "Eta of the EleTags", len(EtaBinEdges)-1,EtaBinEdges)
hGenPtvsResp    = makeTh2("hGenPtvsResp","hGenPtvsResp",50, 10, 400, 20, -2 ,3)     
hPtvsEta_RECOden    = makeTh2VB("hPtvsEta_RECOden","hPtvsEta_RECOden",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
hPtvsEta_DTnum    = makeTh2VB("hPtvsEta_DTnum","hPtvsEta_DTnum",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
hGenPtvsEta_RECOden    = makeTh2VB("hGenPtvsEta_RECOden","hGenPtvsEta_RECOden",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))
hGenPtvsEta_DTnum    = makeTh2VB("hGenPtvsEta_DTnum","hGenPtvsEta_DTnum",len(PtBinEdges)-1,np.asarray(PtBinEdges, 'd'), len(EtaBinEdges)-1,np.asarray(EtaBinEdges, 'd'))

#=====This sets up histograms for the pT response of the tracks
dProbeTrkResponseDT_ = {}
dProbeTrkResponseRECO_= {}
for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
	for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
		newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))	
		specialpart = '_eta'+str(newHistKey).replace('), (', '_pt').replace('(','').replace(')','').replace(', ','to')
		dProbeTrkResponseDT_[newHistKey] = makeTh1("hProbeTrkrespDT"+specialpart,"hProbeTrkrespDT"+specialpart, 100,-2,2)	
		histoStyler(dProbeTrkResponseDT_[newHistKey], 1)
		dProbeTrkResponseRECO_[newHistKey] = makeTh1("hProbeTrkrespRECO"+specialpart,"hProbeTrkrespRECO"+specialpart, 100,-2,2)	
		histoStyler(dProbeTrkResponseRECO_[newHistKey], 1)		

#=====This sets up histograms for the invariant mass and kappas    
dInvMassRECOHist = {}
dInvMassDTHist = {}
hEleProbePt_DTnums = {}
hEleProbePt_RECOdens = {}
hGenEleProbePt_DTnums = {}
hGenEleProbePt_RECOdens = {}

for iEtaBin, EtaBin in enumerate(EtaBinEdges[:-1]):
	etakey = (EtaBin,EtaBinEdges[iEtaBin + 1])
	specialpart = '_eta'+str(etakey).replace('(','').replace(')','').replace(', ','to')
	hEleProbePt_DTnums[etakey] = makeTh1VB("hEleProbePtDT"+specialpart+"_num", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
	hEleProbePt_RECOdens[etakey]    = makeTh1VB("hEleProbePtRECO"+specialpart+"_den", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
	hGenEleProbePt_DTnums[etakey] = makeTh1VB("hGenEleProbePtDT"+specialpart+"_num", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)
	hGenEleProbePt_RECOdens[etakey]    = makeTh1VB("hGenEleProbePtRECO"+specialpart+"_den", "pt of the EleProbes", len(PtBinEdges)-1,PtBinEdges)	
	for iPtBin, PtBin in enumerate(PtBinEdges[:-1]):
		newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
		specialpart = '_eta'+str(newHistKey).replace('), (', '_pt').replace('(','').replace(')','').replace(', ','to')
		dInvMassRECOHist[newHistKey] = makeTh1("hInvMass"+specialpart+"_RECOden"  , "hInvMass"+specialpart+"_RECOden", 40, 60, 120)
		histoStyler(dInvMassRECOHist[newHistKey], 1)
		newHistKey = ((EtaBin,EtaBinEdges[iEtaBin + 1]),(PtBin,PtBinEdges[iPtBin + 1]))
		dInvMassDTHist[newHistKey] = makeTh1("hInvMass"+specialpart+"_DTnum"  , "hInvMass"+specialpart+"_DTnum", 40, 60, 120)
		histoStyler(dInvMassDTHist[newHistKey], 1)

##adapt script for BDT disappearing track
readerPixelOnly = TMVA.Reader()
pixelXml = '/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel3-200-4-short/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelOnly, pixelXml)
readerPixelStrips = TMVA.Reader()
pixelstripsXml = '/nfs/dust/cms/user/kutznerv/shorttrack/fake-tracks/newpresel2-200-4-medium/weights/TMVAClassification_BDT.weights.xml'
prepareReader(readerPixelStrips, pixelstripsXml)

def genMatch(lep):
    for igenm, genm in enumerate(c.GenParticles):
        if not genm.Pt() > 5: continue
        if not abs(c.GenParticles_ParentId[igenm]) == 23: continue
        if not (abs(c.GenParticles_PdgId[igenm]) == 11 and c.GenParticles_Status[igenm] == 1):continue
        drm = genm.DeltaR(lep)
        if drm < .01: return genm.Pt()
    return 0

for f in inputFiles:
	print 'adding file:', f
	c.Add(f)
nentries = c.GetEntries()
print nentries, ' events to be analyzed'
verbosity = 10000
identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
identifier+='nFiles'+str(len(inputFiles))


for ientry in range(nentries):
        if verbose:
            if not ientry in [8841]: continue
        if ientry%verbosity==0: print 'now processing event number', ientry, 'of', nentries
        c.GetEntry(ientry)
        weight = 1 #(c.CrossSection*35.9)
        fillth1(hHt, c.HT, 1)
        fillth1(hHtWeighted, c.HT, c.CrossSection)
        TagPt  =  0
        TagEta  =  0
        ProbePt  =  0
        ProbeEta = 0
        probeTlv = TLorentzVector()
        probeTlv.SetPxPyPzE(0, 0, 0, 0)
        
        muons = []		
        for imu, muon in enumerate(c.Muons):
        	if not muon.Pt()>10: continue
        	#if abs(muon.Eta()) < 1.566 and abs(muon.Eta()) > 1.4442: continue
        	if not abs(muon.Eta())<2.4: continue	
        	muons.append([muon,c.Muons_charge[imu]])
        #if not len(muons)==0: continue	
        if verbose: print 'test no muons'
        
        genels = []
        genmus = []        
        for igp, gp in enumerate(c.GenParticles):
			if not gp.Pt()>5: continue		
			if not (abs(c.GenParticles_PdgId[igp])==11 or abs(c.GenParticles_PdgId[igp])==13) : continue
			if not c.GenParticles_Status[igp]==1 : continue			
			if not abs(gp.Eta())<2.4: continue
			if not (abs(gp.Eta())<1.445 or abs(gp.Eta())>1.56): continue						
			if abs(c.GenParticles_PdgId[igp])==11: genels.append([gp,igp])
			if abs(c.GenParticles_PdgId[igp])==13: genmus.append([gp,igp])			
			
			        		
        basicTracks = []
        disappearingTracks = []        
        for itrack, track in enumerate(c.tracks):
            if not track.Pt() > 20 : continue
            if not abs(track.Eta()) < 2.4: continue
            if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
            if not isBaselineTrack(track, itrack, c): continue
            basicTracks.append([track,c.tracks_charge[itrack], itrack])
            if not track.Pt()<1999: continue
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
                
        RecoElectrons = []        
        SmearedElectrons = []
        TightElectrons = []        
        for iel, ele in enumerate(c.Electrons):
            if not ele.Pt()>5: continue                  
            if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
            if not abs(ele.Eta())<2.4: continue      
            if not c.Electrons_passIso[iel]: continue            
            if (ele.Pt() > 30 and c.Electrons_passIso[iel] and bool(c.Electrons_mediumID[iel])):
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
            if not (smearedEle.Pt()>20 and smearedEle.Pt()<1999): continue
            SmearedElectrons.append([smearedEle, c.Electrons_charge[iel]])
            #print 'a lovely ele', ele.Pt(), smearedEle.Pt()
	adjustedHt = 0
	adjustedMht = TLorentzVector()
	adjustedMht.SetPxPyPzE(0,0,0,0)
	for jet in c.Jets:
		if not jet.Pt()>30: continue
		if not abs(jet.Eta())<5: continue
		if len(SmearedElectrons)>0:
			if not jet.DeltaR(SmearedElectrons[0][0])>0.5: continue####update 
		if len(disappearingTracks)>0:
			if not jet.DeltaR(disappearingTracks[0][0])>0.5: continue####update 			
		adjustedMht-=jet
		if not abs(jet.Eta())<2.4: continue####update to 2.4		
		adjustedHt+=jet.Pt()
			
        for igen, genel in enumerate(genels):
            drminDtGenel  = 9999                
            for idistrk, distrk in enumerate(disappearingTracks):
                dr = genel[0].DeltaR(distrk[0])
                if not dr < 0.02: continue

            	if RelaxGenKin: pt, eta = distrk[0].Pt(),abs(distrk[0].Eta())
            	else: pt, eta = genel[0].Pt(), abs(genel[0].Eta())
            	
            	energyvar = pt
            	
                fillth2(hGenPtvsEta_DTnum, pt, eta, weight)
                fillth2(hGenPtvsResp, TMath.Log10(distrk[0].Pt()/genel[0].Pt()),genel[0].Pt(),weight)                
                for histkey in  hGenEleProbePt_DTnums:
                	if abs(eta) > histkey[0] and abs(eta) < histkey[1]:
                		fillth1(hGenEleProbePt_DTnums[histkey], energyvar, weight)
                print ientry, 'found a nice dt', distrk[0].Pt()
                break        
            idlep   = -1
            drminSmearedelGenel = 9999
            gotthematch = False       
            for ie, ele in enumerate(SmearedElectrons):
                dr = genel[0].DeltaR(ele[0])
                if not dr < 0.02: continue #here we have a probe dt
                pt = ele[0].Pt()
                energyvar = pt
                fillth2(hGenPtvsEta_RECOden, energyvar, abs(ele[0].Eta()), weight )#This seemed to be calling the last iterated electron
                for histkey in  hGenEleProbePt_RECOdens:
                	if abs(ele[0].Eta()) > histkey[0] and abs(ele[0].Eta()) < histkey[1]:
                		#fillth1(hGenEleProbePt_RECOdens[histkey], ele[0].Pt(), weight)
                		fillth1(hGenEleProbePt_RECOdens[histkey], energyvar, weight)
                		gotthematch = True
                		break
                if gotthematch: break
  
        if GenOnly: continue
        tagTlv = TLorentzVector()
        tagTlv.SetPxPyPzE(0,0,0,0)
        
        
        for charge in range(-1,2,2):
            for itag, tag in enumerate(TightElectrons):	
                if not tag[1]==charge: continue
                IM  =  0 
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
                        probeIsDt = True
                        probeIsEl = False            
                for iSmearedEl, smearedEl in enumerate(SmearedElectrons):
                    if not (tag[1] + smearedEl[1] == 0): continue
                    if smearedEl[0].DeltaR(tag[0])<0.01: continue                    
                    IMleplep = (tag[0] + smearedEl[0]).M()
                    dIM = abs(IMleplep - 91)
                    if(dIM < dmMin):
                        dmMin = dIM
                        IM     = IMleplep
                        probeTlv  = smearedEl[0]
                        probeIsEl = True
                        probeIsDt = False                        

                if (IM > 60 and IM < 120):
			fillth1(hEleTagPt, TagPt, weight)
			fillth1(hEleTagEta, TagEta, weight)
			if probeIsDt:
				ProbePt = probeTlv.Pt()
				ProbeEta = abs(probeTlv.Eta())
				genmatched  = genMatch(probeTlv)
				#if genmatched == 0: continue #uncomment to skip genMatching of Probes
				fillth2(hPtvsEta_DTnum, ProbePt, ProbeEta, weight)

				for histkey in  dInvMassDTHist:
					if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
						fillth1(dInvMassDTHist[histkey],IM,weight)                        
				for histkey in  hEleProbePt_DTnums:
					if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
						fillth1(hEleProbePt_DTnums[histkey], ProbePt, weight)                        
				cappedPt = min(genmatched, 99999)#299.99)
				for histkey in  dProbeTrkResponseDT_:
					if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and cappedPt > histkey[1][0] and cappedPt < histkey[1][1]:
						fillth1(dProbeTrkResponseDT_[histkey],TMath.Log10(ProbePt/genmatched),weight)
		
			if probeIsEl:
				genmatched  = genMatch(probeTlv)
				#if genmatched == 0: continue #uncomment to skip genMatching of Probes
				ProbePt   = probeTlv.Pt()
				ProbeEta = abs(probeTlv.Eta())
				fillth2(hPtvsEta_RECOden, ProbePt, ProbeEta, weight)      
				for histkey in  dInvMassRECOHist:
					if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and ProbePt > histkey[1][0] and ProbePt < histkey[1][1]:
						fillth1(dInvMassRECOHist[histkey],IM, weight)		
				for histkey in  hEleProbePt_RECOdens:
					if abs(ProbeEta) > histkey[0] and abs(ProbeEta) < histkey[1]:
						fillth1(hEleProbePt_RECOdens[histkey], ProbePt, weight)   
				cappedPt = min(genmatched, 99999)#299.99)
				for histkey in  dProbeTrkResponseRECO_:
					if abs(ProbeEta) > histkey[0][0] and abs(ProbeEta) < histkey[0][1] and cappedPt > histkey[1][0] and cappedPt < histkey[1][1]:
						fillth1(dProbeTrkResponseRECO_[histkey],TMath.Log10(ProbePt/genmatched),weight) 


fnew = TFile('TagnProbeEleHists_'+identifier+'.root','recreate')
print 'making', 'TagnProbeEleHists_'+identifier+'.root'
fnew.cd()
hHt.Write()
hHtWeighted.Write()
hGenPtvsEta_DTnum.Write()
hGenPtvsEta_RECOden.Write()
hPtvsEta_DTnum.Write()    
hPtvsEta_RECOden.Write()
hEleTagPt.Write()
hEleTagEta.Write()

#Dictionaries:
for histkey in hEleProbePt_DTnums: 
	hEleProbePt_DTnums[histkey].Write()    
	hEleProbePt_RECOdens[histkey].Write()
	hGenEleProbePt_DTnums[histkey].Write()    
	hGenEleProbePt_RECOdens[histkey].Write()	
for histkey in  dProbeTrkResponseDT_: 
	dProbeTrkResponseDT_[histkey].Write()
	dProbeTrkResponseRECO_[histkey].Write()
for histkey in  dInvMassRECOHist:
	dInvMassRECOHist[histkey].Write()
	dInvMassDTHist[histkey].Write()

hGenPtvsResp.Write()

print "just created file:", fnew.GetName()
fnew.Close()

