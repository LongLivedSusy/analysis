import os as os_
import sys
import argparse
import json
from ROOT import *
from shared_utils import *
import numpy as np

TH1.SetDefaultSumw2(True)

def main(inputfiles,output_dir,output,nev,mstop,mlsp,dedxcalibfactor,dedxsmearfactor):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    for i,inputfile in enumerate(inputfiles):
        print 'adding {}th file:{}'.format(i,inputfile)
    	c.Add(inputfile)
    
    nentries = c.GetEntries()
    if nev != -1: nentries = nev
    
    FileName = c.GetFile().GetName().split('/')[-1]
    
    # check if data:
    phase = 0
    for label in ["Summer16", "Fall17", "Autumn18"]:
        if label in FileName:
            if label == "Summer16":
                phase = 0
            elif label == "Fall17" or label == "Autumn18":
                phase = 1
    
    print "FileName : ",FileName
    print "Phase:", phase
    print "Total Entries : ",nentries 
    #c.Show(0)

    # dEdx smear histo
    doDedxSmear = False
    #doDedxSmear = True
    fsmear_barrel, fsmear_endcap = Load_DedxSmear(phase)
    
    # Output file
    fout = TFile(output_dir+'/'+output, "recreate")
    
    execfile("./histo_container_signal.py")

    # Event loop
    updateevery = 1000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	h_nev.Fill(0)
	hHT_unweighted.Fill(c.HT)

	#weight = c.CrossSection * c.puWeight
	weight = c.puWeight

	# Requiring vertex in the event
 	if not c.NVtx>0: continue
	
	# MET filters, etc
	#if is_fastsim : 
	#    #if not passesUniversalSelectionFastSim(c): continue
	#    #if not bool(t.JetID): continue
 	#    #if not  passQCDHighMETFilter(c): continue
 	#    #if not passQCDHighMETFilter2(c): continue
	#    pass
	#else : 
	#    #if not bool(c.JetID): continue
	#    if not  passQCDHighMETFilter(c): continue
	#    if not passQCDHighMETFilter2(c): continue
	#    if not c.HBHENoiseFilter: continue    
	#    if not c.HBHEIsoNoiseFilter: continue
	#    if not c.eeBadScFilter: continue      
	#    if not c.BadChargedCandidateFilter: continue
	#    if not c.BadPFMuonFilter: continue
	#    if not c.CSCTightHaloFilter: continue
	#    if not c.EcalDeadCellTriggerPrimitiveFilter: continue      ##I think this one makes a sizeable difference    
	   
	fillth1(hMET,c.MET,weight)
	fillth1(hMHT,c.MHT,weight)
	fillth1(hHT,c.HT,weight)
	
	# Specific stop and LSP mass for signal sample
	chosenStopMass, chosenLSPMass = mstop, mlsp
	
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

	charginos=[]
	for igp,gp in enumerate(c.GenParticles):
	    if abs(c.GenParticles_PdgId[igp])==1000024 :
		fillth1(hGenCharginoP,gp.P(),weight)
	    	fillth1(hGenCharginoPt,gp.Pt(),weight)
	    	fillth1(hGenCharginoEta,gp.Eta(),weight)
	    	fillth1(hGenCharginoPhi,gp.Phi(),weight)
	    	fillth1(hGenCharginoMass,gp.M(),weight)
	    	charginos.append(gp)
	
	# Track
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>25 : continue
	    if not abs(track.Eta()) < 2.0 : continue
	    if not c.tracks_trkRelIso[itrack]<0.2 : continue
	    if not abs(c.tracks_dxyVtx[itrack])<0.02 : continue
	    if not abs(c.tracks_dzVtx[itrack])<0.1 : continue
	    if not c.tracks_ptError[itrack]/(track.Pt()*track.Pt())<10 : continue
	    if not bool(c.tracks_trackQualityHighPurity[itrack]) : continue
	    if not c.tracks_nMissingInnerHits[itrack]==0 : continue
	    if not c.tracks_nMissingMiddleHits[itrack]==0 : continue
	    if not c.tracks_nValidPixelHits[itrack]>=3 : continue
	    #if not c.tracks_nValidTrackerHits[itrack]>=2 : continue
	    
	    # chargino-track matching
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for chargino in charginos:
		dr = chargino.DeltaR(track)
		if dr < threshold : 
		    match = True
		    fillth1(hGenCharginoP_trackmatch,chargino.P(),weight)
	    	    fillth1(hGenCharginoPt_trackmatch,chargino.Pt(),weight)
	    	    fillth1(hGenCharginoEta_trackmatch,chargino.Eta(),weight)
	    	    fillth1(hGenCharginoPhi_trackmatch,chargino.Phi(),weight)
		    break
		
	    if not match : continue
	    
	    # Harmonic-2 dE/dx
	    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
	    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]

	    if dedx_pixel==0 : continue

	    fillth1(hTrkP_charginomatch,track.P(),weight)
	    fillth1(hTrkPt_charginomatch,track.Pt(),weight)
	    fillth1(hTrkEta_charginomatch,track.Eta(),weight)
	    fillth1(hTrkPhi_charginomatch,track.Phi(),weight)
	    fillth1(hTrkPixelDedx_charginomatch,dedx_pixel,weight)
	    fillth1(hTrkStripsDedx_charginomatch,dedx_strips,weight)

	    if dedx_pixel<4.0 : fillth1(hTrkPixelDedx_charginomatch_SR,0,weight)
	    else : fillth1(hTrkPixelDedx_charginomatch_SR,1,weight)
	    
	    # Barrel calibration
	    if abs(track.Eta())<=1.5 :
	        dedx_pixel_scale= dedx_pixel * dedxcalibfactor
	        
	        fillth1(hTrkPixelDedx_charginomatch_barrel,dedx_pixel,weight)
	        fillth1(hTrkPixelDedxScale_charginomatch_barrel,dedx_pixel_scale,weight)
	        fillth1(hTrkPixelDedxScaleSmear_charginomatch_barrel,dedx_pixel_scalesmear,weight)
		if dedx_pixel_scale<4.0 : 
		    fillth1(hTrkPixelDedxScale_charginomatch_SR,0,weight)
		    fillth1(hTrkPixelDedxScale_charginomatch_barrel_SR,0,weight)
		else : 
		    fillth1(hTrkPixelDedxScale_charginomatch_SR,1,weight)
		    fillth1(hTrkPixelDedxScale_charginomatch_barrel_SR,1,weight)
	        
		fillth1(hTrkStripsDedx_charginomatch_barrel,dedx_strips,weight)
	    
	    # Endcap calibration
	    elif abs(track.Eta())>1.5 :
	        scalefactor =1.125
	        dedx_pixel_scale = dedx_pixel * dedxcalibfactor
	        if doDedxSmear:
		    smearfactor = fsmear_endcap.GetRandom()
		    dedx_pixel_scalesmear = dedx_pixel_scale + smearfactor
	        else : 
		    dedx_pixel_scalesmear = dedx_pixel_scale
	        
	        fillth1(hTrkPixelDedx_charginomatch_endcap,dedx_pixel,weight)
	        fillth1(hTrkPixelDedxScale_charginomatch_endcap,dedx_pixel_scale,weight)
	        fillth1(hTrkPixelDedxScaleSmear_charginomatch_endcap,dedx_pixel_scalesmear,weight)
		if dedx_pixel_scale<4.0 : 
		    fillth1(hTrkPixelDedxScale_charginomatch_SR,0,weight)
		    fillth1(hTrkPixelDedxScale_charginomatch_endcap_SR,0,weight)
		else : 
		    fillth1(hTrkPixelDedxScale_charginomatch_SR,1,weight)
		    fillth1(hTrkPixelDedxScale_charginomatch_endcap_SR,1,weight)
	        
	        fillth1(hTrkStripsDedx_charginomatch_endcap,dedx_strips,weight)
	    else : print 'what is this?'

    fout.Write()
    fout.Close()
    print(output_dir+'/'+output+" just created")

if __name__ == "__main__":
    
    print 'Running signal analyzer'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="*", dest="inputfiles", required=True)
    parser.add_argument("--output_dir",default="outputs_smallchunks",dest="output_dir")
    parser.add_argument("--output",default="output.root",dest="output")
    parser.add_argument("--nev",default=-1,dest="nev")
    #parser.add_argument("--mgluino",default=-1,dest="mgluino")
    parser.add_argument("--mstop",default=-1,dest="mstop")
    parser.add_argument("--mlsp",default=-1,dest="mlsp")
    parser.add_argument("--dedxcalibfactor",default=1,dest="dedxcalibfactor")
    parser.add_argument("--dedxsmearfactor",default=1,dest="dedxsmearfactor")

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_dir = args.output_dir
    output = args.output
    nev = int(args.nev)
    #mgluino = int(args.mgluino)
    mstop = int(args.mstop)
    mlsp = int(args.mlsp)
    dedxcalibfactor = int(args.dedxcalibfactor)
    dedxsmearfactor = int(args.dedxsmearfactor)

    main(inputfiles,output_dir,output,nev,mstop,mlsp,dedxcalibfactor,dedxsmearfactor)
