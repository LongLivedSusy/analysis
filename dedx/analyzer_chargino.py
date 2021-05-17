import os as os_
import sys
import argparse
import json
from ROOT import *
from shared_utils import *
import numpy as np

TH1.SetDefaultSumw2(True)

def main(inputfiles,output_dir,output,nev,is_signal,is_fast):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    for i,inputfile in enumerate(inputfiles):
        print 'adding {}th file:{}'.format(i,inputfile)
    	c.Add(inputfile)
    
    nentries = c.GetEntries()
    if nev != -1: nentries = nev
    
    Identifiers = ['Summer16','Summer16PrivateFastSim']
    
    FileName = c.GetFile().GetName().split('/')[-1]
    for identifier in Identifiers:
	if not is_fast and identifier in FileName :
	    Identifier = 'Summer16'
	if is_fast and 'Summer16PrivateFastSim' in FileName :
	    Identifier = 'Summer16PrivateFastSim'

    
    # check if data:
    phase = 0
    for label in ["Summer16", "Fall17", "Autumn18"]:
        if label in FileName:
            if label == "Summer16":
                phase = 0
            elif label == "Fall17" or label == "Autumn18":
                phase = 1
    
    print "FileName : ",FileName
    #print "Indentifier : ",Identifier
    print "Phase:", phase
    print "Signal : ",is_signal
    print "FastSim : ",is_fastsim
    print "Total Entries : ",nentries 
    #c.Show(0)

    # dEdx smear histo
    doDedxSmear = False
    #doDedxSmear = True
    fsmear_barrel, fsmear_endcap = Load_DedxSmear(phase)
    
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

	weight = c.CrossSection * c.puWeight
	#weight = c.puWeight

	# Requiring vertex in the event
 	if not c.NVtx>0: continue
	
	# MET filters, etc
	if is_fastsim : 
	    #if not passesUniversalSelectionFastSim(c): continue
	    #if not bool(t.JetID): continue
 	    #if not  passQCDHighMETFilter(c): continue
 	    #if not passQCDHighMETFilter2(c): continue
	    pass
	else : 
	    #if not passesUniversalSelection(c): continue
	    #if not bool(c.JetID): continue
	    if not  passQCDHighMETFilter(c): continue
	    if not passQCDHighMETFilter2(c): continue
	    if not c.HBHENoiseFilter: continue    
	    if not c.HBHEIsoNoiseFilter: continue
	    if not c.eeBadScFilter: continue      
	    if not c.BadChargedCandidateFilter: continue
	    if not c.BadPFMuonFilter: continue
	    if not c.CSCTightHaloFilter: continue
	    if not c.EcalDeadCellTriggerPrimitiveFilter: continue      ##I think this one makes a sizeable difference    
	   
	fillth1(hMET,c.MET,weight)
	fillth1(hMHT,c.MHT,weight)
	fillth1(hHT,c.HT,weight)
	
	# Specific stop and LSP mass for signal sample
	if is_signal:
	    #chosenStopMass, chosenLSPMass = 1300, 1
	    #chosenStopMass, chosenLSPMass = 1300, 50
	    #chosenStopMass, chosenLSPMass = 1300, 200
	    #chosenStopMass, chosenLSPMass = 1300, 400
	    #chosenStopMass, chosenLSPMass = 1300, 600
	    #chosenStopMass, chosenLSPMass = 1300, 800
	    #chosenStopMass, chosenLSPMass = 1300, 1000
	    #chosenStopMass, chosenLSPMass = 1300, 1100
	    #chosenStopMass, chosenLSPMass = 2500, 1200
	    #chosenStopMass, chosenLSPMass = 2500, 1400
	    #chosenStopMass, chosenLSPMass = 2500, 1600
	    #chosenStopMass, chosenLSPMass = 2500, 1800
	    chosenStopMass, chosenLSPMass = 2500, 2000

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
	    	    
	    	    charginos.append(gp)
	    	    fillth1(hGenCharginoP,gp.P(),weight)
	    	    fillth1(hGenCharginoPt,gp.Pt(),weight)
	    	    fillth1(hGenCharginoEta,gp.Eta(),weight)
	    	    fillth1(hGenCharginoPhi,gp.Phi(),weight)
	    	    fillth1(hGenCharginoMass,gp.M(),weight)


	# Track
	goodtracks=[]
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>15 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not c.tracks_trkRelIso[itrack]<0.2 : continue
	    if not abs(c.tracks_dxyVtx[itrack])<0.02 : continue
	    if not abs(c.tracks_dzVtx[itrack])<0.1 : continue
	    if not c.tracks_ptError[itrack]/(track.Pt()*track.Pt())<10 : continue
	    if not bool(c.tracks_trackQualityHighPurity[itrack]) : continue
	    if not c.tracks_nMissingInnerHits[itrack]==0 : continue
	    if not c.tracks_nMissingMiddleHits[itrack]==0 : continue
	    if not c.tracks_nValidPixelHits[itrack]>=3 : continue
	    #if not c.tracks_nValidTrackerHits[itrack]>=2 : continue
	    
	    # Harmonic-2 dE/dx
	    dedx_pixel = c.tracks_deDxHarmonic2pixel[itrack]
	    dedx_strips = c.tracks_deDxHarmonic2strips[itrack]

	    if dedx_pixel==0 : continue

	    goodtracks.append([itrack,track])

	    # muon-track matcing
	    drmin=99
	    idx = -1
	    match = False
	    threshold = 0.01

	    for chargino in charginos:
		dr = chargino.DeltaR(track)
		if dr < drmin:
		    drmin=dr
		    idx = itrack
		    track_charginomatch = track
	    
	    if drmin < threshold : 
		match = True
		
	    if not match : continue
	   
	    fillth1(hTrkPixelDedx_charginomatch,dedx_pixel,weight)
	    fillth1(hTrkStripsDedx_charginomatch,dedx_strips,weight)

	    if abs(track.Eta())<=1.5 :
	        #scalefactor = DedxCorr_Pixel_barrel[Identifier]
	        scalefactor = 1.0
	        dedx_pixel_scale= dedx_pixel * scalefactor
	        if doDedxSmear:
		    smearfactor = fsmear_barrel.GetRandom()
		    dedx_pixel_scalesmear = dedx_pixel_scale + smearfactor
	        else : 
		    dedx_pixel_scalesmear = dedx_pixel_scale
	        
	        fillth1(hTrkPixelDedx_charginomatch_barrel,dedx_pixel,weight)
	        fillth1(hTrkPixelDedxScale_charginomatch_barrel,dedx_pixel_scale,weight)
	        fillth1(hTrkPixelDedxScaleSmear_charginomatch_barrel,dedx_pixel_scalesmear,weight)
	        fillth1(hTrkStripsDedx_charginomatch_barrel,dedx_strips,weight)
	    
	    elif abs(track.Eta())>1.5 :
	        #scalefactor = DedxCorr_Pixel_endcap[Identifier]
	        scalefactor = 1.0
	        dedx_pixel_scale = dedx_pixel * scalefactor
	        if doDedxSmear:
		    smearfactor = fsmear_endcap.GetRandom()
		    dedx_pixel_scalesmear = dedx_pixel_scale + smearfactor
	        else : 
		    dedx_pixel_scalesmear = dedx_pixel_scale
	        
	        fillth1(hTrkPixelDedx_charginomatch_endcap,dedx_pixel,weight)
	        fillth1(hTrkPixelDedxScale_charginomatch_endcap,dedx_pixel_scale,weight)
	        fillth1(hTrkPixelDedxScaleSmear_charginomatch_endcap,dedx_pixel_scalesmear,weight)
	        fillth1(hTrkStripsDedx_charginomatch_endcap,dedx_strips,weight)

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

