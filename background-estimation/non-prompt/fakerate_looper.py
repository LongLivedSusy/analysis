#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import os
import numpy as np

def isBaselineTrack(track, itrack, c, hMask):
	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not abs(c.tracks_dxyVtx[itrack]) < 0.1: return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False	
	if hMask!='':
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True

def loop(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", maskfile = "Masks.root"):

    do_dilepton_CR = True
    do_singlelepton_CR = False
    do_qcd_CR = True

    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
    
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

    xsec_written = False

    tout = TTree("Events", "tout")
 
    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            label = label.replace("tracks_", "")
            variables.append(label)

    # prepare variables for output tree
    tree_branch_values = {}
    for variable in [
                      "MET",
                      "MHT",
                      "MHT_cleaned",
                      "HT",
                      "HT_cleaned",
                      "MinDeltaPhiMhtJets",
                      "MinDeltaPhiMhtJets_cleaned",
                      "dilepton_invmass",
                      "PFCaloMETRatio",
                      "singlelepton_pt",
                    ]:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )

    for variable in [
                      "n_DT",
                      "n_DT_actualfake",
                      "n_jets",
                      "n_jets_cleaned",
                      "n_btags",
                      "n_btags_cleaned",
                      "n_leptons",
                      "n_allvertices",
                      "n_NVtx",
                      "EvtNumEven",
                      "lepton_type",
                      "dilepton_CR",
                      "singlelepton_CR",
                      "qcd_CR",
                      "DT1_is_pixel_track",
                      "DT2_is_pixel_track",
                      "DT3_is_pixel_track",
                      "DT1_trackerLayersWithMeasurement",
                      "DT2_trackerLayersWithMeasurement",
                      "DT3_trackerLayersWithMeasurement",
                      "DT1_actualfake",
                      "DT2_actualfake",
                      "DT3_actualfake",
                    ]:
        tree_branch_values[variable] = array( 'i', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )
        
    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}
    bdt_folders = ["../../disappearing-track-tag/short-tracks", "../../disappearing-track-tag/long-tracks"]

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_cut_pixelonly = 0.1
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_cut_pixelstrips = 0.25

    # load mask file:
    mask_file = False
    previous_file_name = ""

    # some loop variables:
    nevents_total = 0
    nevents_tagged = 0
    nevents_tagged_actualfake = 0

    # loop over events
    for iEv, event in enumerate(tree):

        if not xsec_written:
            if tree.GetBranch("CrossSection"):
                xsec = event.CrossSection
            else:
                xsec = -1
            h_xsec = TH1F("xsec", "xsec", 1, 0, 1)
            h_xsec.Fill(0, xsec)
            h_xsec.Write()
            xsec_written = True

        if nevents > 0 and iEv > nevents:
            break
        
        if (iEv+1) % 500 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if (madHT>0) and \
               ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
               ("TTJets_Tune" in current_file_name and madHT>600) or \
               ("100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("2500toInf_" in current_file_name and madHT<2500) or \
               ("2500ToInf_" in current_file_name and madHT<2500):
                continue
                  
        # reset all branch values:
        for label in tree_branch_values:
            tree_branch_values[label][0] = -1

        # set selection flags (veto event later if it does not fit into any selection):
        dilepton_CR = False
        singlelepton_CR = False
        qcd_CR = False

        # dilepton control region: do zmass matching
        if do_dilepton_CR:
            if "Run" not in current_file_name or "SingleElectron" in current_file_name or "SingleMuon" in current_file_name:
                min_lepton_pt = 30.0
                invariant_mass = 0
                if (len(event.Electrons) == 2 and len(event.Muons) == 0):
                    if (event.Electrons[0].Pt() > min_lepton_pt):
                        if bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1]):
                            if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                                invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    if bool(event.Electrons_passIso[0]) and bool(event.Electrons_passIso[1]):
                                        tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                        tree_branch_values["lepton_type"][0] = 11
                                        tree_branch_values["dilepton_CR"][0] = 1
                                        dilepton_CR = True       
                elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
                    if (event.Muons[0].Pt() > min_lepton_pt):
                        if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                            if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                                invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    if bool(event.Muons_passIso[0]) and bool(event.Muons_passIso[1]):
                                        tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                        tree_branch_values["lepton_type"][0] = 13
                                        tree_branch_values["dilepton_CR"][0] = 1
                                        dilepton_CR = True

        if do_singlelepton_CR:
            if "Run" not in current_file_name or "SingleElectron" in current_file_name or "SingleMuon" in current_file_name:
                min_lepton_pt = 30.0
                if (len(event.Electrons) == 1 and len(event.Muons) == 0):
                    if (event.Electrons[0].Pt() > min_lepton_pt) and bool(event.Electrons_mediumID[0]) and bool(event.Electrons_passIso[0]):
                        tree_branch_values["singlelepton_pt"][0] = event.Electrons[0].Pt()
                        tree_branch_values["lepton_type"][0] = 11
                        tree_branch_values["singlelepton_CR"][0] = 1
                        singlelepton_CR = True
                elif (len(event.Muons) == 1 and len(event.Electrons) == 0):
                    if (event.Muons[0].Pt() > min_lepton_pt) and bool(event.Muons_tightID[0]) and bool(event.Muons_passIso[0]):
                        tree_branch_values["singlelepton_pt"][0] = event.Muons[0].Pt()
                        tree_branch_values["lepton_type"][0] = 13
                        tree_branch_values["singlelepton_CR"][0] = 1
                        singlelepton_CR = True

        # check if low-MHT, QCD-only samples:
        if do_qcd_CR and ("QCD" in current_file_name or "JetHT" in current_file_name):
            if event.MHT < 200:
                tree_branch_values["qcd_CR"][0] = 1
                qcd_CR = True

        # CHECK: event selection
        if not dilepton_CR and not qcd_CR:
            continue
                
        # for the dilepton CR, clean event (recalculate HT, MHT, n_Jets without the two leptons):
        if dilepton_CR:
            csv_b = 0.8838
            metvec = TLorentzVector()
            metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET)
            mhtvec = TLorentzVector()
            mhtvec.SetPtEtaPhiE(0, 0, 0, 0)
            jets = []
            nb = 0
            HT_cleaned = 0
            
            for ijet, jet in enumerate(event.Jets):
                
                if not (abs(jet.Eta()) < 5 and jet.Pt() > 30): continue
                
                # check if lepton is in jet, and veto jet if that is the case
                lepton_is_in_jet = False
                for leptons in [event.Electrons, event.Muons]:
                    for lepton in leptons:
                        if jet.DeltaR(lepton) < 0.05:
                            lepton_is_in_jet = True
                if lepton_is_in_jet: continue
                
                mhtvec-=jet
                if not abs(jet.Eta()) < 2.4: continue

                jets.append(jet)
                HT_cleaned+=jet.Pt()        
                if event.Jets_bDiscriminatorCSV[ijet] > csv_b: nb+=1
                
            n_btags_cleaned = nb        
            n_jets_cleaned = len(jets)
            MHT_cleaned = mhtvec.Pt()

            MinDeltaPhiMhtJets_cleaned = 9999   
            for jet in jets: 
                if abs(jet.DeltaPhi(mhtvec)) < MinDeltaPhiMhtJets_cleaned:
                    MinDeltaPhiMhtJets_cleaned = abs(jet.DeltaPhi(mhtvec))

            tree_branch_values["n_btags_cleaned"][0] = n_btags_cleaned
            tree_branch_values["n_jets_cleaned"][0] = n_jets_cleaned
            tree_branch_values["MHT_cleaned"][0] = MHT_cleaned
            tree_branch_values["HT_cleaned"][0] = HT_cleaned
            tree_branch_values["MinDeltaPhiMhtJets_cleaned"][0] = MinDeltaPhiMhtJets_cleaned

        # calculate MinDeltaPhiMhtJets:
        csv_b = 0.8838
        mhtvec = TLorentzVector()
        mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
        MinDeltaPhiMhtJets = 9999
        nj = 0
        nb = 0
        for ijet, jet in enumerate(event.Jets):
            if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
            nj+=1
            if event.Jets_bDiscriminatorCSV[ijet]>csv_b: nb+=1
            if abs(jet.DeltaPhi(mhtvec))<MinDeltaPhiMhtJets:
                MinDeltaPhiMhtJets = abs(jet.DeltaPhi(mhtvec))
     
        # load mask file:
        mask = ''
        if maskfile:
            if "Run2016" in current_file_name:
                if current_file_name != previous_file_name:
                    mask_file = TFile(maskfile, "open")
                mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")
            # don't use mask for MC:
            #elif "Summer16" in current_file_name:
            #    if current_file_name != previous_file_name:
            #        mask_file = TFile(maskfile, "open")
            #    mask = mask_file.Get("hEtaVsPhiDT_maskedMC-2016MC-2016")
            previous_file_name = current_file_name

        # loop over tracks (tracks):
        nevents_total += 1
        n_DT = 0
        n_DT_actualfake = 0

        for iCand in xrange(len(event.tracks)):

            # set up booleans
            is_pixel_track = False
            is_tracker_track = False
            charged_genparticle_in_track_cone = False
            is_disappearing_track = False
            is_a_PF_lepton = False

            # re-check PF lepton veto:
            for k in range(len(event.Muons)):
                deltaR = event.tracks[iCand].DeltaR(event.Muons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True
            for k in range(len(event.Electrons)):
                deltaR = event.tracks[iCand].DeltaR(event.Electrons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True

            if is_a_PF_lepton: continue

            # fill custom variables:
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check for category:
            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True
                            
            # apply TMVA preselection:
            if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            # evaluate BDT:
            if is_pixel_track:

                tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
                tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
                tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
                tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
                tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
                tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
                tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelonly:
                    is_disappearing_track = True
                    if debug: print "pixel DT", iEv, event.HT, tree_branch_values["HT_cleaned"][0], event.nAllVertices

            elif is_tracker_track:

                tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
                tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
                tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
                tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
                tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
                tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
                tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
                tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelstrips:
                    is_disappearing_track = True
                    if debug: print "tracker DT", iEv, event.HT, tree_branch_values["HT_cleaned"][0], event.nAllVertices

            # apply baseline DT selection:
            if is_disappearing_track and not isBaselineTrack(event.tracks[iCand], iCand, event, mask):
                print "Failed baseline DT selection"
                is_disappearing_track = False

            if is_disappearing_track and debug:
                print event.tracks[iCand].Pt()
                print abs(event.tracks[iCand].Eta())
                print event.tracks_nMissingInnerHits[iCand]
                print event.tracks_nMissingMiddleHits[iCand]
                print bool(event.tracks_trackQualityHighPurity[iCand])
                print event.tracks_dxyVtx[iCand]
                print event.tracks_dzVtx[iCand]
                print event.tracks_matchedCaloEnergy[iCand]
                print event.tracks_trkRelIso[iCand]
                print event.tracks_nValidPixelHits[iCand]
                print event.tracks_nValidTrackerHits[iCand]
                print event.tracks_nMissingOuterHits[iCand]
                print ptErrOverPt2

            # check if actual fake track (no genparticle in cone around track):
            charged_genparticle_in_track_cone = False
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):

                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.02 and event.GenParticles_Status[k] != 1:
                           
                        gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])
                        if gen_track_cone_pdgid == 11 or gen_track_cone_pdgid == 13:
                            charged_genparticle_in_track_cone = True
                            break
                        elif gen_track_cone_pdgid == 15 and tree.GetBranch("GenTaus_LeadTrk"):
                            # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    charged_genparticle_in_track_cone = True
                                    break
                
            if is_disappearing_track:
               
                n_DT += 1
                if not charged_genparticle_in_track_cone:
                    n_DT_actualfake += 1

                # save track-level properties:
                tree_branch_values["DT%s_is_pixel_track" % n_DT][0] = is_pixel_track
                tree_branch_values["DT%s_trackerLayersWithMeasurement" % n_DT][0] = event.tracks_trackerLayersWithMeasurement[iCand]
                tree_branch_values["DT%s_actualfake" % n_DT][0] = not charged_genparticle_in_track_cone

 
        # event-level variables:
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_DT"][0] = n_DT
        tree_branch_values["n_DT_actualfake"][0] = n_DT_actualfake
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["n_NVtx"][0] = event.NVtx
               
        if event.EvtNum % 2 == 0:
            tree_branch_values["EvtNumEven"][0] = 1
        else:
            tree_branch_values["EvtNumEven"][0] = 0
     
        tout.Fill()
     
    fout.cd()
    fout.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    if len(args)>2 and args[2]>0:
        nev = int(args[2])
    else:
        nev = -1

    loop(iFile, out_tree, nevents=nev)

