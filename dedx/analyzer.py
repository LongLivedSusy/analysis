import os as os_
import sys
import argparse
import json
from ROOT import *
from shared_utils import *
import numpy as np

TH1.SetDefaultSumw2(True)

_dxyVtx_ = array('f',[0])
_dzVtx_ = array('f',[0])
_matchedCaloEnergy_ = array('f',[0])
_trkRelIso_ = array('f',[0])
_nValidPixelHits_ = array('f',[0])
_nValidTrackerHits_ = array('f',[0])
_nMissingOuterHits_ = array('f',[0])
_ptErrOverPt2_ = array('f',[0])
_trkRelIsoSTARpt_ = array('f',[0])
_neutralPtSum_ = array('f',[0])
_chargedPtSum_ = array('f',[0])
_pixelLayersWithMeasurement_ = array('f',[0])
_trackerLayersWithMeasurement_ = array('f',[0])
_nMissingMiddleHits_ = array('f',[0])
_chi2perNdof_ = array('f',[0])

def prepareReaderPixelStrips_loose(reader, xmlfilename):
                reader.AddVariable("tracks_dzVtx",_dzVtx_)
                reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
                reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
                reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
                reader.AddVariable("tracks_nValidTrackerHits",_nValidTrackerHits_)
                reader.AddVariable("tracks_nMissingOuterHits",_nMissingOuterHits_)
                reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
                reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)
                reader.BookMVA("BDT", xmlfilename)

def prepareReaderPixel_loose(reader, xmlfilename):
                reader.AddVariable("tracks_dzVtx",_dzVtx_)
                reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
                reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
                reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
                reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
                reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)
                reader.BookMVA("BDT", xmlfilename)

def passesUniversalSelection(t):
	#if not bool(t.JetID): return False
	if not t.NVtx>0: return False
	#print 'made a'
	if not  passQCDHighMETFilter(t): return False
	if not passQCDHighMETFilter2(t): return False
	#print 'made b'    
	#if not t.PFCaloMETRatio<5: return False # turned off now that we use muons
	###if not t.globalSuperTightHalo2016Filter: return False
	#print 'made c'    
	if not t.HBHENoiseFilter: return False    
	if not t.HBHEIsoNoiseFilter: return False
	if not t.eeBadScFilter: return False      
	#print 'made d'    
	if not t.BadChargedCandidateFilter: return False
	if not t.BadPFMuonFilter: return False
	#print 'made e'    
	if not t.CSCTightHaloFilter: return False
	#print 'made f'        
	if not t.EcalDeadCellTriggerPrimitiveFilter: return False      ##I think this one makes a sizeable difference    
	##if not t.ecalBadCalibReducedExtraFilter: return False
	##if not t.ecalBadCalibReducedFilter: return False      
	   
	return True

def passesUniversalSelectionFastSim(t):
 	#if not bool(t.JetID): return False
 	if not t.NVtx>0: return False
 	#print 'made a'
 	if not  passQCDHighMETFilter(t): return False
 	if not passQCDHighMETFilter2(t): return False
 	return True	

def pass_background_stitching(current_file_name, madHT, phase):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>100) or \
       (phase == 1 and "TTJets_Tune" in current_file_name and madHT>600) or \
       ("HT-100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-2500toInf_" in current_file_name and madHT<2500) or \
       ("HT-500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-2500ToInf_" in current_file_name and madHT<2500):
        return False
    else:
        return True

def main(inputfiles,output_dir,output,nev,is_signal,is_fast):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    for i,inputfile in enumerate(inputfiles):
        print 'adding {}th file:{}'.format(i,inputfile)
    	c.Add(inputfile)
    
    nentries = c.GetEntries()
    if nev != -1: nentries = nev
    
    Identifiers = ['Run2016B','Run2016C','Run2016D','Run2016E','Run2016F','Run2016G','Run2016H',
		    'Run2017B','Run2017C','Run2017D','Run2017E','Run2017F',
		    'Run2018A','Run2018B','Run2018C','Run2018D',
		    'Summer16','Fall17','Summer16FastSim']
    
    FileName = c.GetFile().GetName().split('/')[-1]
    for identifier in Identifiers:
	if identifier in FileName :
	    Identifier = identifier
	if 'Summer16PrivateFastSim' in FileName :
	    Identifier = 'Summer16FastSim'

    
    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in FileName:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1
    
    print "FileName : ",FileName
    print "Indentifier : ",Identifier
    print "Phase:", phase
    print "Signal : ",is_signal
    print "FastSim : ",is_fastsim
    print "Total Entries : ",nentries 
    #c.Show(0)

    #FIXME: no special handling for Autumn18 yet
    if data_period == "Autumn18":
        data_period == "Fall17" 

    if data_period != "":
        print "data_period: %s, phase: %s" % (data_period, phase)
    else:
        print "Can't determine data/MC era!"
        quit(1)

    # Load BDT
    #print 'Loading BDTs'
    #if phase==0:
    #    pixelXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/current-phase0-shorttracks/dataset/weights/TMVAClassification_BDT.weights.xml'
    #    pixelstripsXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/current-phase0-longtracks/dataset/weights/TMVAClassification_BDT.weights.xml'
    #    #pixelXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml'
    #    #pixelstripsXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml'
    #else :
    #    pixelXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-nov20-noEdep/weights/TMVAClassification_BDT.weights.xml'
    #    pixelstripsXml = os_.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-nov20-noEdep/weights/TMVAClassification_BDT.weights.xml'
    #
    #readerPixelOnly = TMVA.Reader()
    #readerPixelStrips = TMVA.Reader()
    #print 'going to process', pixelXml
    #prepareReaderPixel_loose(readerPixelOnly, pixelXml)
    #print 'going to process', pixelstripsXml
    #prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)

    # load and configure data mask:
    #fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to15.root')
    #fMask = TFile('../disappearing-track-tag/Masks_mcal10to15.root')
    #hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')
    #print "Loaded mask:", hMask
    
    # Output file
    fout = TFile(output_dir+'/'+output, "recreate")

    # write number of events to histogram:
    nev = c.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

    ## Load Histograms
    execfile('./histo_container.py')
    
    # Event loop
    updateevery = 1000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	fillth1(hHT_unweighted,c.HT)

	# store runs for JSON output:
    	runs = {}

	# Weight
	if is_data:
            runnum = c.RunNum
            lumisec = c.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)
	    weight = 1.0
	else : 
	    #weight = c.CrossSection * c.puWeight
	    weight = c.puWeight

	# data trigger and mc madHT check
	if is_data and "MET" in FileName :
	    if not PassTrig(c,'MhtMet6pack') : continue
	elif is_data and "SingleMuon" in FileName :
	    if not PassTrig(c,'SingleMuon') : continue
	elif is_data and ("SingleElectron" in FileName or "EGamma" in FileName) :
	    if not PassTrig(c,'SingleElectron') : continue
	else :
	    # madHT check
	    if c.GetBranch("madHT"):
		madHT = c.madHT
	    	if not pass_background_stitching(FileName, madHT, phase): continue
	
	# Requiring vertex in the event
 	if not c.NVtx>0: continue
	
	# MET filters, etc
	if is_fastsim : 
	    #if not passesUniversalSelectionFastSim(c): continue
	    #if not bool(t.JetID): continue
 	    if not  passQCDHighMETFilter(c): continue
 	    if not passQCDHighMETFilter2(c): continue
	else : 
	    #if not passesUniversalSelection(c): continue
	    #if not bool(c.JetID): continue
	    if not c.NVtx>0: continue
	    if not  passQCDHighMETFilter(c): continue
	    if not passQCDHighMETFilter2(c): continue
	    #if not c.PFCaloMETRatio<5: continue # turned off now that we use muons
	    ###if not c.globalSuperTightHalo2016Filter: continue
	    if not c.HBHENoiseFilter: continue    
	    if not c.HBHEIsoNoiseFilter: continue
	    if not c.eeBadScFilter: continue      
	    if not c.BadChargedCandidateFilter: continue
	    if not c.BadPFMuonFilter: continue
	    if not c.CSCTightHaloFilter: continue
	    if not c.EcalDeadCellTriggerPrimitiveFilter: continue      ##I think this one makes a sizeable difference    
	    ##if not c.ecalBadCalibReducedExtraFilter: continue
	    ##if not c.ecalBadCalibReducedFilter: continue      
	   
	
	# some preselection on event
	#if not c.MET>50 : continue

	fillth1(hMET,c.MET,weight)
	fillth1(hMHT,c.MHT,weight)
	fillth1(hHT,c.HT,weight)
  
	# Specific stop and LSP mass
	if is_signal:
	    #chosenStopMass, chosenLSPMass = 1300, 1
	    #chosenStopMass, chosenLSPMass = 1300, 50
	    #chosenStopMass, chosenLSPMass = 1300, 200
	    chosenStopMass, chosenLSPMass = 1300, 1100

	    #hasRightGluinoMass = True
	    #for igp,gp in enumerate(c.GenParticles):
	    #    if not abs(c.GenParticles_PdgId[igp])==1000021 : continue
	    #    print 'mGluino:',c.GenParticles[igp].M()
	    #    if not abs(c.GenParticles[igp].M()-chosenGluinoMass)<0.1:
	    #       hasRightGluinoMass = False
	    #	   break
	    #    fillth1(hGenGluinoMass,gp.M(),weight)
	    #if not hasRightGluinoMass: continue

	    hasRightStopMass = True
	    for igp,gp in enumerate(c.GenParticles):
	        if not abs(c.GenParticles_PdgId[igp])==1000006 : continue
	        if not abs(c.GenParticles[igp].M()-chosenStopMass)<0.1:
		   hasRightStopMass = False
		   break
	        fillth1(hGenStopMass,gp.M(),weight)
	    if not hasRightStopMass: continue

	    hasRightLSPMass = True
	    for igp,gp in enumerate(c.GenParticles):
	        if not abs(c.GenParticles_PdgId[igp])==1000022 : continue
	        if not abs(c.GenParticles[igp].M()-chosenLSPMass)<0.1:
		   hasRightLSPMass = False
		   break
	        fillth1(hGenLSPMass,gp.M(),weight)
	    if not hasRightLSPMass: continue
	    
	    # Gen-chargino
	    charginos=[]
	    for igp,gp in enumerate(c.GenParticles):
	        if not abs(c.GenParticles_PdgId[igp])==1000024 : continue
	        if not gp.Pt() > 15 : continue
	        
	        charginos.append(gp)
	        fillth1(hGenCharginoP,gp.P(),weight)
	        fillth1(hGenCharginoPt,gp.Pt(),weight)
	        fillth1(hGenCharginoEta,gp.Eta(),weight)
	        fillth1(hGenCharginoPhi,gp.Phi(),weight)
	
	# Muons
	n_tightmuon = 0
	tightmuons=[]
	tightmuons_genmatch=[]
	for imu, mu in enumerate(c.Muons):
	    if not (mu.Pt()>30): continue
	    if not abs(mu.Eta())<2.4: continue
	    if not (abs(mu.Eta()) > 1.566 or abs(mu.Eta()) < 1.4442): continue
	    if not c.Muons_passIso[imu]: continue
	    if not c.Muons_tightID[imu]: continue
	    
	    n_tightmuon+=1
	    tightmuons.append(mu)
	    
	    beta_mu = mu.Beta()
	    gamma_mu = mu.E()/0.105
	    betagamma_mu = beta_mu*gamma_mu
	    
	    fillth1(hMuP,mu.P(),weight)
	    fillth1(hMuPt,mu.Pt(),weight)
	    fillth1(hMuEta,mu.Eta(),weight)
	    fillth1(hMuPhi,mu.Phi(),weight)
	    fillth1(hMuGamma,gamma_mu,weight)
	    fillth1(hMuBetaGamma,betagamma_mu,weight)
	    
	    # Gen-muon matching
	    if not is_data:
		drmin=99
		idx = -1
		match = False
		threshold = 0.01

		for igp,gp in enumerate(c.GenParticles):
		    if not abs(c.GenParticles_PdgId[igp])==13 : continue
		    if not gp.Pt() > 20 : continue

		    dr_mu_gen = mu.DeltaR(gp)
		    if dr_mu_gen < drmin:
			drmin = dr_mu_gen
			idx = imu
			mu_genmatch = mu
	
		if drmin < threshold :
		    match = True
		    tightmuons_genmatch.append(mu_genmatch)
		    gamma_mu_genmatch = mu_genmatch.E()/0.105
		    betagamma_mu_genmatch = mu_genmatch.Beta()*gamma_mu_genmatch

		    fillth1(hMuP_genmatch,mu_genmatch.P(),weight)
		    fillth1(hMuPt_genmatch,mu_genmatch.Pt(),weight)
		    fillth1(hMuEta_genmatch,mu_genmatch.Eta(),weight)
	    	    fillth1(hMuPhi_genmatch,mu_genmatch.Phi(),weight)
		    fillth1(hMuGamma_genmatch,gamma_mu_genmatch,weight)
	    	    fillth1(hMuBetaGamma_genmatch,betagamma_mu_genmatch,weight)


	# Electrons
	n_tightelectron =0
	tightelectrons=[]
	tightelectrons_genmatch=[]
	n_electron = len(c.Electrons)
	for iele, ele in enumerate(c.Electrons):
	    if not (ele.Pt()>30): continue
	    if not abs(ele.Eta())<2.4: continue
	    if not (abs(ele.Eta()) > 1.566 or abs(ele.Eta()) < 1.4442): continue
	    if not c.Electrons_passIso[iele]: continue
	    if not c.Electrons_tightID[iele]: continue
	    
	    n_tightelectron+=1
	    tightelectrons.append(ele)
	    
	    beta_ele = ele.Beta()
	    #gamma_ele = ele.Gamma()
	    #gamma_ele = TMath.Sqrt(1+((ele.P()/0.000511)**2))
	    gamma_ele = ele.E()/0.000511
	    betagamma_ele = beta_ele*gamma_ele
	    
	    fillth1(hEleP,ele.P(),weight)
	    fillth1(hElePt,ele.Pt(),weight)
	    fillth1(hEleEta,ele.Eta(),weight)
	    fillth1(hElePhi,ele.Phi(),weight)
	    fillth1(hEleGamma,gamma_ele,weight)
	    fillth1(hEleBetaGamma,betagamma_ele,weight)
	    
	    # Gen-electron matching
	    if not is_data:
		drmin=99
		idx = -1
		match = False
		threshold = 0.001

		for igp,gp in enumerate(c.GenParticles):
		    if not abs(c.GenParticles_PdgId[igp])==11 : continue
		    if not gp.Pt() > 20 : continue

		    dr_ele_gen = ele.DeltaR(gp)
		    if dr_ele_gen < drmin:
			drmin = dr_ele_gen
			idx = iele
			ele_genmatch = ele
	
		if drmin < threshold :
		    match = True
		    tightelectrons_genmatch.append(ele_genmatch)
		    gamma_ele_genmatch = ele_genmatch.E()/0.000511
		    betagamma_ele_genmatch = ele_genmatch.Beta() * gamma_ele_genmatch

		    fillth1(hEleP_genmatch,ele_genmatch.P(),weight)
		    fillth1(hElePt_genmatch,ele_genmatch.Pt(),weight)
		    fillth1(hEleEta_genmatch,ele_genmatch.Eta(),weight)
	    	    fillth1(hElePhi_genmatch,ele_genmatch.Phi(),weight)
		    fillth1(hEleGamma_genmatch,gamma_ele_genmatch,weight)
	    	    fillth1(hEleBetaGamma_genmatch,betagamma_ele_genmatch,weight)

	# Number of tight leptons
	n_lepton = n_tightmuon + n_tightelectron
	#fillth1(hNlepton,n_lepton,weight)

	# Track
	isShort=True
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>15 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not c.tracks_trkRelIso[itrack]<0.1 : continue
	    if not abs(c.tracks_dzVtx[itrack])<0.1 : continue
	    if not c.tracks_ptError[itrack]/(track.Pt()*track.Pt())<10 : continue
	    if not c.tracks_nMissingInnerHits[itrack]==0 : continue
	    if not bool(c.tracks_passPFCandVeto[itrack]) : continue
	    if not bool(c.tracks_trackQualityHighPurity[itrack]) : continue
	    if not c.tracks_nValidPixelHits[itrack]>=3 : continue
	    #if not c.tracks_nValidTrackerHits[itrack]>=2 : continue
	    
	    if c.tracks_nValidPixelHits[itrack] == c.tracks_nValidTrackerHits[itrack] :
		isShort = True
	    elif track.Pt()>30 and c.tracks_nValidPixelHits[itrack] < c.tracks_nValidTrackerHits[itrack] :
		isShort = False
	    
	    fillth1(hTrkP,track.P(),weight)
	    fillth1(hTrkPt,track.Pt(),weight)
	    fillth1(hTrkEta,track.Eta(),weight)
	    fillth1(hTrkPhi,track.Phi(),weight)
	    #print 'track pT : ', track.Pt()

	    # Gen-chargino - track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for ichi, chi in enumerate(charginos):
                dr_track = chi.DeltaR(track)
		if dr_track < drmin:
		    drmin = dr_track
		    idx = itrack
		    track_charginomatch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_charginomatch,track_charginomatch.P(),weight)
		fillth1(hTrkPt_charginomatch,track_charginomatch.Pt(),weight)
		fillth1(hTrkEta_charginomatch,track_charginomatch.Eta(),weight)
		fillth1(hTrkPhi_charginomatch,track_charginomatch.Phi(),weight)
		fillth1(hTrkPixelDedx_charginomatch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_charginomatch,dedx_strips,weight)

		fillth2(h2_Trk_P_vs_PixelDedx_charginomatch,track_charginomatch.P(),dedx_pixel,weight)
		fillth2(h2_Trk_P_vs_StripsDedx_charginomatch,track_charginomatch.P(),dedx_strips,weight)
		    
		if abs(track_charginomatch.Eta())<=1.5 : 
		    #print Identifier, ' barrel region(chargino matching) SF : ', DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkPixelDedx_charginomatch_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_charginomatch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_charginomatch_barrel,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_charginomatch_barrel,dedx_strips*SF_dedx_strips,weight)
		elif abs(track_charginomatch.Eta())>1.5 : 
		    #print Identifier, ' endcap region(chargino matching) SF : ', DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkPixelDedx_charginomatch_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_charginomatch_endcap,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_charginomatch_endcap,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_charginomatch_endcap,dedx_strips*SF_dedx_strips,weight)
		else : print 'should not see this'
    
	    # Muon-track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for imu, mu in enumerate(tightmuons):
                dr_mu_track = mu.DeltaR(track)
		if dr_mu_track < drmin:
		    drmin = dr_mu_track
		    idx = itrack
		    track_mumatch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_tightmumatch,track_mumatch.P(),weight)
		fillth1(hTrkPt_tightmumatch,track_mumatch.Pt(),weight)
		fillth1(hTrkPixelDedx_tightmumatch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_tightmumatch,dedx_strips,weight)
		
		if abs(track_mumatch.Eta())<=1.5 : 
		    #print 'barrel region(mu matching)'
		    SF_dedx_pixel = DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightmumatch_barrel,track_mumatch.P(),weight)
		    fillth1(hTrkPt_tightmumatch_barrel,track_mumatch.Pt(),weight)
		    fillth1(hTrkEta_tightmumatch_barrel,track_mumatch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightmumatch_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightmumatch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightmumatch_barrel,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightmumatch_barrel,dedx_strips*SF_dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightmumatch,dedx_strips*SF_dedx_strips,weight)
		elif abs(track_mumatch.Eta())>1.5 : 
		    #print 'endcap region(mu matching)'
		    SF_dedx_pixel = DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightmumatch_endcap,track_mumatch.P(),weight)
		    fillth1(hTrkPt_tightmumatch_endcap,track_mumatch.Pt(),weight)
		    fillth1(hTrkEta_tightmumatch_endcap,track_mumatch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightmumatch_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightmumatch_endcap,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightmumatch_endcap,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightmumatch_endcap,dedx_strips*SF_dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightmumatch,dedx_strips*SF_dedx_strips,weight)
		else : print 'should not see this'

	    # Genmatched Muon - track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for imu, mu in enumerate(tightmuons_genmatch):
                dr_mu_track = mu.DeltaR(track)
		if dr_mu_track < drmin:
		    drmin = dr_mu_track
		    idx = itrack
		    track_genmumatch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_tightgenmumatch,track_genmumatch.P(),weight)
		fillth1(hTrkPt_tightgenmumatch,track_genmumatch.Pt(),weight)
		fillth1(hTrkPixelDedx_tightgenmumatch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_tightgenmumatch,dedx_strips,weight)
		
		if abs(track_genmumatch.Eta())<=1.5 : 
		    #print Identifier, ' barrel region(genmu matching) SF : ', DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_barrel[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightgenmumatch_barrel,track_genmumatch.P(),weight)
		    fillth1(hTrkPt_tightgenmumatch_barrel,track_genmumatch.Pt(),weight)
		    fillth1(hTrkEta_tightgenmumatch_barrel,track_genmumatch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightgenmumatch_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightgenmumatch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightgenmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightgenmumatch_barrel,dedx_strips,weight)
		    #fillth1(hTrkStripsDedxCalib_tightgenmumatch_barrel,dedx_strips*SF_dedx_strips,weight)
		    #fillth1(hTrkStripsDedxCalib_tightgenmumatch,dedx_strips*SF_dedx_strips,weight)
		elif abs(track_genmumatch.Eta())>1.5 : 
		    #print Identifier, ' endcap region(genmu matching) SF : ', DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_pixel = DedxCorr_Pixel_endcap[Identifier]
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightgenmumatch_endcap,track_genmumatch.P(),weight)
		    fillth1(hTrkPt_tightgenmumatch_endcap,track_genmumatch.Pt(),weight)
		    fillth1(hTrkEta_tightgenmumatch_endcap,track_genmumatch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightgenmumatch_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightgenmumatch_endcap,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightgenmumatch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightgenmumatch_endcap,dedx_strips,weight)
		    #fillth1(hTrkStripsDedxCalib_tightgenmumatch_endcap,dedx_strips*SF_dedx_strips,weight)
		    #fillth1(hTrkStripsDedxCalib_tightgenmumatch,dedx_strips*SF_dedx_strips,weight)
		else : print 'should not see this'

	    # Electron-track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01
	    
	    for iele, ele in enumerate(tightelectrons):
                dr_ele_track = ele.DeltaR(track)
		if dr_ele_track < drmin:
		    drmin = dr_ele_track
		    idx = itrack
		    track_elematch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_tightelematch,track_elematch.P(),weight)
		fillth1(hTrkPt_tightelematch,track_elematch.Pt(),weight)
		fillth1(hTrkPixelDedx_tightelematch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_tightelematch,dedx_strips,weight)
		
		if abs(track_elematch.Eta())<=1.5 : 
		    #print 'barrel region(ele matching)'
		    SF_dedx_pixel = 1.0
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightelematch_barrel,track_elematch.P(),weight)
		    fillth1(hTrkPt_tightelematch_barrel,track_elematch.Pt(),weight)
		    fillth1(hTrkEta_tightelematch_barrel,track_elematch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightelematch_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightelematch_barrel,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightelematch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightelematch_barrel,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightelematch_barrel,dedx_strips*SF_dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightelematch,dedx_strips*SF_dedx_strips,weight)
		elif abs(track_elematch.Eta())>1.5 : 
		    #print 'endcap region(ele matching)'
		    SF_dedx_pixel = 1.0
		    SF_dedx_strips = 1.0
		    fillth1(hTrkP_tightelematch_endcap,track_elematch.P(),weight)
		    fillth1(hTrkPt_tightelematch_endcap,track_elematch.Pt(),weight)
		    fillth1(hTrkEta_tightelematch_endcap,track_elematch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightelematch_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightelematch_endcap,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkPixelDedxCalib_tightelematch,dedx_pixel*SF_dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightelematch_endcap,dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightelematch_endcap,dedx_strips*SF_dedx_strips,weight)
		    fillth1(hTrkStripsDedxCalib_tightelematch,dedx_strips*SF_dedx_strips,weight)
	    
	    # Gen-matched Electron matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for iele, ele in enumerate(tightelectrons_genmatch):
                dr_ele_track = ele.DeltaR(track)
		if dr_ele_track < drmin:
		    drmin = dr_ele_track
		    idx = itrack
		    track_genelematch = track

	    if drmin < threshold : 
		match = True
		dedx_pixel = c.tracks_deDxHarmonic2pixel[idx]
		dedx_strips = c.tracks_deDxHarmonic2strips[idx]
		fillth1(hTrkP_tightgenelematch,track_genelematch.P(),weight)
		fillth1(hTrkPt_tightgenelematch,track_genelematch.Pt(),weight)
		fillth1(hTrkPixelDedx_tightgenelematch,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_tightgenelematch,dedx_strips,weight)
		
		if abs(track_genelematch.Eta())<=1.5 : 
		    #print 'barrel region(ele matching)'
		    fillth1(hTrkP_tightgenelematch_barrel,track_genelematch.P(),weight)
		    fillth1(hTrkPt_tightgenelematch_barrel,track_genelematch.Pt(),weight)
		    fillth1(hTrkEta_tightgenelematch_barrel,track_genelematch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightgenelematch_barrel,dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightgenelematch_barrel,dedx_strips,weight)
		elif abs(track_genelematch.Eta())>1.5 : 
		    #print 'endcap region(ele matching)'
		    fillth1(hTrkP_tightgenelematch_endcap,track_genelematch.P(),weight)
		    fillth1(hTrkPt_tightgenelematch_endcap,track_genelematch.Pt(),weight)
		    fillth1(hTrkEta_tightgenelematch_endcap,track_genelematch.Eta(),weight)
		    fillth1(hTrkPixelDedx_tightgenelematch_endcap,dedx_pixel,weight)
		    fillth1(hTrkStripsDedx_tightgenelematch_endcap,dedx_strips,weight)
		else : print 'should not see this'
		    
    fout.Write()
    fout.Close()
    print(output_dir+'/'+output+" just created")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="*", dest="inputfiles", required=True)
    parser.add_argument("--output_dir",default="outputs_smallchunks",dest="output_dir")
    parser.add_argument("--output",default="output.root",dest="output")
    parser.add_argument("--nev",default=-1,dest="nev")
    parser.add_argument("--signal",default=False,action='store_true')
    parser.add_argument("--fast",default=False,action='store_true')

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_dir = args.output_dir
    output = args.output
    nev = int(args.nev)
    is_signal = args.signal
    is_fastsim = args.fast
    
    main(inputfiles,output_dir,output,nev,is_signal,is_fastsim)

