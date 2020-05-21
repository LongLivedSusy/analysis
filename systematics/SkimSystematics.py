#! /usr/bin/env python

from ROOT import *
from lib_systematics import *
import os, sys
from glob import glob
from shared_utils import *

gStyle.SetOptStat(111111)

def getBinNumber(fv):
    for binkey in binnumbers:
        foundbin = True
        for iwindow, window in enumerate(binkey):
            if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): 
            	foundbin = False
            	break
        if foundbin: return binnumbers[binkey]
    return -1

def main(inputfile, outputdir, sigmaBtag, sigmaJES, sigmaJER, sigmaISR) :
    
    tree = TChain("TreeMaker2/PreSelection")
    with open (inputfile,"r") as filenamelists : 
	filenamelist = filenamelists.readlines()
	for filename in filenamelist : 
	    tree.Add(filename.strip())
	    print 'adding', filename

    nentries = min(10000000,tree.GetEntries())
    print 'will analyze', nentries

    csv_b = 0.6324  #DeepCSVM

    if 'Fall17' in inputfile or 'Run2017' in inputfile : phase = 1
    else : phase = 0

    outputfilename = outputdir+'/'+(inputfile.split('/')[-1]).replace('*','').replace('Input','skim').replace("txt","root")
    print 'outputfilename : ',outputfilename
    fout = TFile(outputfilename,'recreate')

    ###########################################
    # Book histogram
    ##########################################
    hNev = TH1D('Nev','Total number of events',1,0,1)
    hNev_passAllSel = TH1D('Nev_passAllSel','Number of events passed all selection',1,0,1)
    hAnalysisBins = TH1F('hAnalysisBins','Each bin : Signal Region',32,1,33)

    prepareReaderBtagSF()
    
    # Event Loop
    for ientry in range(nentries) :
	verbosity = 1000
	if ientry %verbosity==0:
	    print 'analyzing event %d of %d' % (ientry, nentries)+ '....%f'%(100.*ientry/nentries)+'%'
	weight = 1.0
	weight_btag = 1.0
	weight_ISR = 1.0

	tree.GetEntry(ientry)
	hNev.Fill(0)
	
	sigmaBtagFastSim = 1.0
	isFastSim = False
	weight_btag = calc_btag_weight(tree,sigmaBtag,sigmaBtagFastSim,isFastSim)
	weight_ISR = get_isr_weight(tree, sigmaISR)
	weight *= weight_btag * weight_ISR 
	print 'weight:%.2f, weight_btag:%.2f, weight_ISR:%.2f'%(weight,weight_btag,weight_ISR)
	
	applysmearing = True
	if applysmearing : 
	    Jets = jets_rescale_smear(tree,applysmearing,sigmaJES,sigmaJER)
	else : Jets = tree.Jets
	'''
	# Start Selection
	if not (tree.MET>120) : continue
	if not (tree.NJets>0) : continue
	if not passesUniversalSelection(tree) : continue

	# calculate MinDeltaPhiMhtJets
	mhtvec = TLorentzVector()
	mhtvec.SetPtEtaPhiE(0, 0, 0, 0)
	MinDeltaPhiMhtJets = 9999
	nj = 0
	nb = 0
	ht = 0
	for ijet, jet in enumerate(Jets) :
	    if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
	    mhtvec-=jet
	    nj+=1
	    ht+=jet.Pt()
	    if tree.Jets_bDiscriminatorCSV[ijet]>csv_b : nb+=1
	    if abs(jet.DeltaPhi(mhtvec)) < MinDeltaPhiMhtJets:
		MinDeltaPhiMhtJets = abs(jet.DeltaPhi(mhtvec))
	
	var_NJets[0] = nj
	var_Mht[0] = mhtvec.Pt()
	var_Ht[0] = ht
	var_MinDeltaPhiMhtJets[0] = MinDeltaPhiMhtJets
	var_BTags[0] = nb
	var_NLeptons[0] = tree.NElectrons + tree.NMuons

	sumtagvec = TLorentzVector()
	sumtagvec.SetPtEtaPhiE(0,0,0,0)	
	mvas = []
    	trkpts = []
    	trketas = []
    	trkphis = []    
    	trkdxys = []
    	trkchisqs = [] 
    	dedxs = []
    	massfromdedxs = []
    	islong = []
    	ismatcheds = []
    	ntags = 0
    	nshort, nlong = 0, 0
    	disappearingTracks = []
	hMask = ""
	for itrack, track in enumerate(tree.tracks) :
	    if not isBaselineTrack(track, itrack, tree, hMask):continue
	    if not track.Pt()>20 and track.Pt()<9999 : continue
	    mva_ = isDisappearingTrack_(track, itrack, tree, readerShort, readerLong)
	    if mva_==0: continue

	    passeslep = True
	    drlep = 99
	    for ilep, lep in enumerate(tree.Electrons):
		drlep = min(drlep, lep.DeltaR(track))
		if drlep<0.01:
		    passeslep = False
		    break
	    for ilep, lep in enumerate(tree.Muons) :
		drlep = min(drlep, lep.DeltaR(track))
		if drlep<0.01:
		    passeslep = False
		    break
	    if not passeslep : continue

	    ntags+=1
	    mvas.append(mva_)
	    trkpts.append(tree.tracks[itrack].Pt())
	    trketas.append(tree.tracks[itrack].Eta())
	    trkphis.append(tree.tracks[itrack].Phi())
	    trkdxys.append(abs(tree.tracks_dxyVtx[itrack]))
	    trkchisqs.append(tree.tracks_chi2perNdof[itrack])
	    dedxs.append(tree.tracks_deDxHarmonic2[itrack])
            massfromdedxs.append(TMath.Sqrt((dedxs[-1]-2.557)*pow(tree.tracks[itrack].P(),2)/2.579))
	    sumtagvec+=track
            phits = tree.tracks_nValidPixelHits[itrack]
            thits = tree.tracks_nValidTrackerHits[itrack]        
            Short = phits>0 and thits==phits
            Long = not Short
            if Long: 
                islong.append(1)
                nlong+=1
            else: 
                islong.append(0) 
                nshort+=1
            disappearingTracks.append(tree.tracks[itrack])
            genParticles = []
            for igp, gp in enumerate(tree.GenParticles):
                if not gp.Pt()>3: continue        
                if not abs(tree.GenParticles_PdgId[igp]) in [11, 13, 211]: continue                    
                if not tree.GenParticles_Status[igp] == 1: continue
                genpart = [gp.Clone(),-int(abs(tree.GenParticles_PdgId[igp])/tree.GenParticles_PdgId[igp])]
                genParticles.append(genpart)        
            if isMatched_([track, 0], genParticles, 0.01): ismatcheds.append(True)
            else: ismatcheds.append(False)

	if len(mvas)==0: continue	

	adjustedMht = TLorentzVector()
    	adjustedMht.SetPxPyPzE(0,0,0,0)
    	adjustedJets = []
    	adjustedHt = 0
    	adjustedBTags = 0

    	for ijet, jet in enumerate(Jets):
    	    if not jet.Pt()>30: continue
    	    if not abs(jet.Eta())<5.0: continue
    	    drDt = 9999
    	    for dt in disappearingTracks: drDt = min(drDt, jet.DeltaR(dt))
    	    if not drDt>0.4: continue
    	    adjustedMht-=jet
    	    if not abs(jet.Eta())<2.4: continue
    	    adjustedJets.append(jet)            
    	    adjustedHt+=jet.Pt()
    	    if tree.Jets_bDiscriminatorCSV[ijet]>csv_b: adjustedBTags+=1
    	adjustedNJets = len(adjustedJets)
	adjustedMinDeltaPhiMhtJets = 4
	for jet in adjustedJets : adjustedMinDeltaPhiMhtJets = min(adjustedMinDeltaPhiMhtJets, abs(jet.DeltaPhi(adjustedMht))) 

	var_Mht_DTcleaned[0] = adjustedMht.Pt()
	var_Ht_DTcleaned[0] = adjustedHt
	var_BTags_DTcleaned[0] = adjustedBTags
	var_MinDeltaPhiMhtJets_DTcleaned[0] = adjustedMinDeltaPhiMhtJets
	var_NJets_DTcleaned[0] = adjustedNJets
	var_NTags[0] = ntags
	var_NShortTags[0] = nshort
	var_NLongTags[0] = nlong
	var_DPhiMhtSumTags[0] = abs(mhtvec.DeltaPhi(sumtagvec))
	var_SumTagPtOverMht[0] = sumtagvec.Pt() / mhtvec.Pt()

	var_CrossSection[0] = tree.CrossSection
	var_weight[0] = weight
	var_weight_btag[0] = weight_btag
	var_weight_ISR[0] = weight_ISR
	
	# Fill signal region
	fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags, ntags,nshort,nlong, adjustedMinDeltaPhiMhtJets]
    	binnumber = getBinNumber(fv)
    	fv.append(binnumber)
    	var_SearchBin[0] = binnumber

	tEvent.Fill()
	hAnalysisBins.Fill(binnumber,var_weight[0])
	hNev_passAllSel.Fill(0,var_weight[0])

	#print 'MHT:%f\t NJets:%f \t BTags:%f \t N_DT:%f \t NPix:%f \t NPixStrips:%f \t MinDPhiMhtJets:%f \t SR:%d'%(adjustedMht.Pt(), adjustedNJets,adjustedBTags, ntags,nshort,nlong, adjustedMinDeltaPhiMhtJets, binnumber)
    '''

    # Save to root file
    fout.cd()
    tEvent.Write()
    hNev.Write()
    hNev_passAllSel.Write()
    hAnalysisBins.Write()
    print 'just created',fout.GetName() 

if __name__ == "__main__" :
    inputfile = sys.argv[1]
    outputdir = sys.argv[2]
    sigmas = sys.argv[3].strip('[]').replace('\'','') .split(',')
    
    sigmaBtag= int(sigmas[0])
    sigmaJES = int(sigmas[1])
    sigmaJER = int(sigmas[2])
    sigmaISR = int(sigmas[3])
    print 'sigmabtag :%d, jes:%d,jer:%d,isr:%d'%(sigmaBtag,sigmaJES,sigmaJER,sigmaISR)
    
    main(inputfile, outputdir, sigmaBtag, sigmaJES, sigmaJER, sigmaISR)
