import os as os_
import sys
import argparse
import json
from ROOT import *
from shared_utils import *
import numpy as np

TH1.SetDefaultSumw2(True)

def Load_SmearFunc():
    print 'Loading smearing stuffs'
    fphase0_data_barrel = TFile("./DedxSmear/phase0_data_dedxsmear_barrel.root")
    fphase0_data_endcap = TFile("./DedxSmear/phase0_data_dedxsmear_endcap.root")
    fphase0_mc_barrel = TFile("./DedxSmear/phase0_mc_dedxsmear_barrel.root")
    fphase0_mc_endcap = TFile("./DedxSmear/phase0_mc_dedxsmear_endcap.root")

    sigma_data_barrel = fphase0_data_barrel.Get("TFitResult-hTrkPixelDedxScale_fromZ_barrel-gaus").Parameters()[2]
    sigma_data_endcap = fphase0_data_endcap.Get("TFitResult-hTrkPixelDedxScale_fromZ_endcap-gaus").Parameters()[2]
    sigma_mc_barrel = fphase0_mc_barrel.Get("TFitResult-hTrkPixelDedxScale_fromZ_barrel-gaus").Parameters()[2]
    sigma_mc_endcap = fphase0_mc_endcap.Get("TFitResult-hTrkPixelDedxScale_fromZ_endcap-gaus").Parameters()[2]

    print 'sigma_data_barrel : ', sigma_data_barrel
    print 'sigma_data_endcap : ', sigma_data_endcap
    print 'sigma_mc_barrel : ', sigma_mc_barrel
    print 'sigma_mc_endcap : ', sigma_mc_endcap
    
    sigma_smear_phase0_barrel = TMath.Sqrt(sigma_data_barrel*sigma_data_barrel - sigma_mc_barrel*sigma_mc_barrel)
    sigma_smear_phase0_endcap = TMath.Sqrt(sigma_data_endcap*sigma_data_endcap - sigma_mc_endcap*sigma_mc_endcap)

    fsmear1_phase0_barrel = TF1('fsmear1_phase0_barrel','gaus',0,2)
    fsmear1_phase0_barrel.SetParameter(0,1)
    fsmear1_phase0_barrel.SetParameter(1,1)
    fsmear1_phase0_barrel.SetParameter(2,sigma_smear_phase0_barrel)
    
    fsmear1_phase0_endcap = TF1('fsmear1_phase0_endcap','gaus',0,2)
    fsmear1_phase0_endcap.SetParameter(0,1)
    fsmear1_phase0_endcap.SetParameter(1,1)
    fsmear1_phase0_endcap.SetParameter(2,sigma_smear_phase0_endcap)

    fsmear2_phase0_barrel = TF1('fsmear2_phase0_barrel','gaus',0,2)
    fsmear2_phase0_barrel.SetParameter(0,1)
    fsmear2_phase0_barrel.SetParameter(1,1)
    fsmear2_phase0_barrel.SetParameter(2,sigma_smear_phase0_barrel/sigma_mc_barrel)
    
    fsmear2_phase0_endcap = TF1('fsmear2_phase0_endcap','gaus',0,2)
    fsmear2_phase0_endcap.SetParameter(0,1)
    fsmear2_phase0_endcap.SetParameter(1,1)
    fsmear2_phase0_endcap.SetParameter(2,sigma_smear_phase0_endcap/sigma_mc_endcap)

    fsmear3_phase0_barrel = TF1('fsmear3_phase0_barrel','gaus',-1,1)
    fsmear3_phase0_barrel.SetParameter(0,1)
    fsmear3_phase0_barrel.SetParameter(1,0)
    fsmear3_phase0_barrel.SetParameter(2,sigma_smear_phase0_barrel)
    
    fsmear3_phase0_endcap = TF1('fsmear3_phase0_endcap','gaus',-1,1)
    fsmear3_phase0_endcap.SetParameter(0,1)
    fsmear3_phase0_endcap.SetParameter(1,0)
    fsmear3_phase0_endcap.SetParameter(2,sigma_smear_phase0_endcap)

    return fsmear1_phase0_barrel, fsmear1_phase0_endcap, fsmear2_phase0_barrel, fsmear2_phase0_endcap, fsmear3_phase0_barrel, fsmear3_phase0_endcap
    
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

def event_in_HEM_region(obj):
    for particle in obj:
        eta = particle.Eta()
        phi = particle.Phi()
        if -3.0<eta and eta<-1.3 and -1.57<phi and phi<-0.87:
            return True
        else : 
	   return False

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

    # dEdx smear histo
    doSmear = False
    if not is_data :
	doSmear = True
	if doSmear : 
	    fsmear1_phase0_barrel, fsmear1_phase0_endcap, fsmear2_phase0_barrel, fsmear2_phase0_endcap, fsmear3_phase0_barrel, fsmear3_phase0_endcap = Load_SmearFunc()
    
    # load and configure data mask:
    #fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal10to15.root')
    #fMask = TFile('../disappearing-track-tag/Masks_mcal10to15.root')
    #hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')
    #print "Loaded mask:", hMask

    # Output file
    fout = TFile(output_dir+'/'+output, "recreate")
    
    execfile("./histo_container.py")

    # Event loop
    updateevery = 1000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	h_nev.Fill(0)
	hHT_unweighted.Fill(c.HT)

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
	    weight = c.CrossSection * c.puWeight
	    #weight = c.puWeight

	# data trigger and mc madHT check
	if is_data and "SingleMuon" in FileName :
	    if not PassTrig(c,'SingleMuon') : continue
	else :
	    # madHT check
	    if c.GetBranch("madHT"):
		madHT = c.madHT
	    	#if not pass_background_stitching(FileName, madHT, phase): continue
	
	# Requiring vertex in the event
 	if not c.NVtx>0: continue
	
	# Requiring at least 2 muons in the event
 	if not len(c.Muons)>1: continue

	# veto HEM failure region for 2018 data
	if is_data and data_period == 'Run2018' and c.RunNum > 319077 : 
	    if event_in_HEM_region(c.Muons) : continue
	
	## MET filters, etc
	#if is_fastsim : 
	#    #if not passesUniversalSelectionFastSim(c): continue
	#    #if not bool(t.JetID): continue
 	#    if not  passQCDHighMETFilter(c): continue
 	#    if not passQCDHighMETFilter2(c): continue
	#else : 
	#    #if not passesUniversalSelection(c): continue
	#    #if not bool(c.JetID): continue
	#    if not  passQCDHighMETFilter(c): continue
	#    if not passQCDHighMETFilter2(c): continue
	#    #if not c.PFCaloMETRatio<5: continue # turned off now that we use muons
	#    ###if not c.globalSuperTightHalo2016Filter: continue
	#    if not c.HBHENoiseFilter: continue    
	#    if not c.HBHEIsoNoiseFilter: continue
	#    if not c.eeBadScFilter: continue      
	#    if not c.BadChargedCandidateFilter: continue
	#    if not c.BadPFMuonFilter: continue
	#    if not c.CSCTightHaloFilter: continue
	#    if not c.EcalDeadCellTriggerPrimitiveFilter: continue      ##I think this one makes a sizeable difference    
	#    ##if not c.ecalBadCalibReducedExtraFilter: continue
	#    ##if not c.ecalBadCalibReducedFilter: continue      
	   
	
	# some preselection on event
	#if not c.MET>50 : continue

	fillth1(hMET,c.MET,weight)
	fillth1(hMHT,c.MHT,weight)
	fillth1(hHT,c.HT,weight)
	
	# Specific stop and LSP mass for signal sample
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
	    if hasRightStopMass and hasRightLSPMass : 
	    	for igp,gp in enumerate(c.GenParticles):
	    	    if not abs(c.GenParticles_PdgId[igp])==1000024 : continue
	    	    if not gp.Pt() > 15 : continue
	    	    
	    	    charginos.append(gp)
	    	    fillth1(hGenCharginoP,gp.P(),weight)
	    	    fillth1(hGenCharginoPt,gp.Pt(),weight)
	    	    fillth1(hGenCharginoEta,gp.Eta(),weight)
	    	    fillth1(hGenCharginoPhi,gp.Phi(),weight)
	
  
	# Muons
	tightmuons=[]
	tightmuons_genmatch=[]
	for imu, mu in enumerate(c.Muons):
	    if not (mu.Pt()>30): continue
	    if not abs(mu.Eta())<2.4: continue
	    if not (abs(mu.Eta()) > 1.566 or abs(mu.Eta()) < 1.4442): continue
	    if not c.Muons_passIso[imu]: continue
	    if not c.Muons_tightID[imu]: continue
	    
	    tightmuons.append([imu,mu])
	    
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
		    tightmuons_genmatch.append([idx,mu_genmatch])
		    gamma_mu_genmatch = mu_genmatch.E()/0.105
		    betagamma_mu_genmatch = mu_genmatch.Beta()*gamma_mu_genmatch

		    fillth1(hMuP_genmatch,mu_genmatch.P(),weight)
		    fillth1(hMuPt_genmatch,mu_genmatch.Pt(),weight)
		    fillth1(hMuEta_genmatch,mu_genmatch.Eta(),weight)
	    	    fillth1(hMuPhi_genmatch,mu_genmatch.Phi(),weight)
		    fillth1(hMuGamma_genmatch,gamma_mu_genmatch,weight)
	    	    fillth1(hMuBetaGamma_genmatch,betagamma_mu_genmatch,weight)
	#print 'n tightmuons:{}, genmatched:{}'.format(len(tightmuons),len(tightmuons_genmatch))
	# Track
	goodtracks=[]
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>15 : continue
	    if not abs(track.Eta()) < 2.2 : continue
	    if not c.tracks_trkRelIso[itrack]<0.2 : continue
	    if not abs(c.tracks_dxyVtx[itrack])<0.02 : continue
	    if not abs(c.tracks_dzVtx[itrack])<0.1 : continue
	    if not c.tracks_ptError[itrack]/(track.Pt()*track.Pt())<10 : continue
	    if not c.tracks_nMissingInnerHits[itrack]==0 : continue
	    if not bool(c.tracks_trackQualityHighPurity[itrack]) : continue
	    if not c.tracks_nValidPixelHits[itrack]>=3 : continue
	    #if not c.tracks_nValidTrackerHits[itrack]>=2 : continue

	    fillth1(hTrkP,track.P(),weight)
	    fillth1(hTrkPt,track.Pt(),weight)
	    fillth1(hTrkEta,track.Eta(),weight)
	    fillth1(hTrkPhi,track.Phi(),weight)

	    goodtracks.append([itrack,track])
	
	    # Harmonic-2 dE/dx
	    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
	    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]

	    if dedx_pixel==0 or dedx_strips==0 : continue

	    # muon-track matcing
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for imu, mu in tightmuons:
		dr = mu.DeltaR(track)
		if dr < drmin:
		    drmin=dr
		    idx = itrack
		    track_mumatch = track
	    
	    if drmin < threshold : 
		match = True
		
	    if not match : continue
	    
	    # Z mass reconstruction (muon + traack invariant mass)
	    for imu, mu in tightmuons:
		if not c.Muons_charge[imu] * c.tracks_charge[itrack] == -1 : continue  # require opposite charge
		invmass = (track+mu).M()
		fillth1(hTrkMuInvMass,invmass,weight)
		if invmass < 76 or invmass > 106 : continue
		fillth1(hTrkMuInvMass_ZmassWindow,invmass,weight)

		beta_mu = mu.Beta()
	    	gamma_mu = mu.E()/0.105
	    	betagamma_mu = beta_mu*gamma_mu
	
		fillth1(hMuP_fromZ,mu.P(),weight)
	    	fillth1(hMuPt_fromZ,mu.Pt(),weight)
	    	fillth1(hMuEta_fromZ,mu.Eta(),weight)
	    	fillth1(hMuPhi_fromZ,mu.Phi(),weight)
	    	fillth1(hMuGamma_fromZ,gamma_mu,weight)
	    	fillth1(hMuBetaGamma_fromZ,betagamma_mu,weight)
	    
		fillth1(hTrkP_fromZ,track.P(),weight)
		fillth1(hTrkPt_fromZ,track.Pt(),weight)
		fillth1(hTrkEta_fromZ,track.Eta(),weight)
		fillth1(hTrkPhi_fromZ,track.Phi(),weight)

		fillth1(hTrkPixelDedx_fromZ,dedx_pixel,weight)
		fillth1(hTrkStripsDedx_fromZ,dedx_strips,weight)

		if abs(track.Eta())<=1.5 :
		    scalefactor = DedxCorr_Pixel_barrel[Identifier]
		    dedx_pixel_scale= dedx_pixel * scalefactor
		    if Identifier == 'Summer16' :
			smearfactor1 = fsmear1_phase0_barrel.GetRandom()
			smearfactor2 = fsmear2_phase0_barrel.GetRandom()
			smearfactor3 = fsmear3_phase0_barrel.GetRandom()
			print 'in barrel smear1 : {}, smear2:{}, smear3:{}'.format(smearfactor1,smearfactor2,smearfactor3)
			dedx_pixel_scalesmear1 = dedx_pixel_scale * smearfactor1
			dedx_pixel_scalesmear2 = dedx_pixel_scale * smearfactor2
			dedx_pixel_scalesmear3 = dedx_pixel_scale + smearfactor3
		    else : 
			dedx_pixel_scalesmear1 = dedx_pixel_scale
			dedx_pixel_scalesmear2 = dedx_pixel_scale
			dedx_pixel_scalesmear3 = dedx_pixel_scale
		    
		    fillth1(hTrkPixelDedx_fromZ_barrel,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxScale_fromZ_barrel,dedx_pixel*scalefactor,weight)
		    fillth1(hTrkPixelDedxScaleSmear1_fromZ_barrel,dedx_pixel_scalesmear1,weight)
		    fillth1(hTrkPixelDedxScaleSmear2_fromZ_barrel,dedx_pixel_scalesmear2,weight)
		    fillth1(hTrkPixelDedxScaleSmear3_fromZ_barrel,dedx_pixel_scalesmear3,weight)
		    fillth1(hTrkStripsDedx_fromZ_barrel,dedx_strips,weight)
		
		elif abs(track.Eta())>1.5 :
		    scalefactor = DedxCorr_Pixel_endcap[Identifier]
		    dedx_pixel_scale = dedx_pixel * scalefactor
		    if Identifier == 'Summer16' :
			smearfactor1 = fsmear1_phase0_endcap.GetRandom()
			smearfactor2 = fsmear2_phase0_endcap.GetRandom()
			smearfactor2 = fsmear3_phase0_endcap.GetRandom()
			print 'in endcap smear1:{}, smear2:{}, smear3:{}'.format(smearfactor1,smearfactor2,smearfactor3)
			dedx_pixel_scalesmear1 = dedx_pixel_scale * smearfactor1
			dedx_pixel_scalesmear2 = dedx_pixel_scale * smearfactor2
			dedx_pixel_scalesmear3 = dedx_pixel_scale + smearfactor3
		    else : 
			dedx_pixel_scalesmear1 = dedx_pixel_scale
			dedx_pixel_scalesmear2 = dedx_pixel_scale
			dedx_pixel_scalesmear3 = dedx_pixel_scale
		    
		    fillth1(hTrkPixelDedx_fromZ_endcap,dedx_pixel,weight)
		    fillth1(hTrkPixelDedxScale_fromZ_endcap,dedx_pixel*scalefactor,weight)
		    fillth1(hTrkPixelDedxScaleSmear1_fromZ_endcap,dedx_pixel_scalesmear1,weight)
		    fillth1(hTrkPixelDedxScaleSmear2_fromZ_endcap,dedx_pixel_scalesmear2,weight)
		    fillth1(hTrkPixelDedxScaleSmear3_fromZ_endcap,dedx_pixel_scalesmear3,weight)
		    fillth1(hTrkStripsDedx_fromZ_endcap,dedx_strips,weight)
    
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

