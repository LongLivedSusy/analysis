#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import os
import numpy as np

def get_signal_region(event, MinDeltaPhiMhtJets, n_DT, n_jets_cleaned = False, MHT_cleaned = False, MinDeltaPhiMhtJets_cleaned = False, n_btags_cleaned = False):

    # signal regions as defined in https://indico.desy.de/indico/event/20437/contribution/2/material/slides/0.pdf
    
    if n_jets_cleaned and MHT_cleaned and MinDeltaPhiMhtJets_cleaned:
        NJets = n_jets_cleaned
        MHT = MHT_cleaned
        MinDeltaPhiMhtJets = MinDeltaPhiMhtJets_cleaned
        n_btags = n_btags_cleaned
    else:
        NJets = len(event.Jets)
        MHT = event.MHT
        MinDeltaPhiMhtJets = MinDeltaPhiMhtJets
        n_btags = event.BTags

    region = 0

    if n_DT==1:
        if MHT>=250 and MHT<400 and MinDeltaPhiMhtJets>0.5:
            if NJets==1 and n_btags>=0:
                region = 1
            elif NJets>=2 and NJets<=5 and n_btags==0:
                region = 2
            elif NJets>=2 and NJets<=5 and n_btags>0:
                region = 3
            elif NJets>=6 and n_btags==0:
                region = 4
            elif NJets>=6 and n_btags>0:
                region = 5
        elif MHT>=400 and MHT<650 and MinDeltaPhiMhtJets>0.3:
            if NJets==1 and n_btags>=0:
                region = 6
            elif NJets>=2 and NJets<=5 and n_btags==0:
                region = 7
            elif NJets>=2 and NJets<=5 and n_btags>0:
                region = 8
            elif NJets>=6 and n_btags==0:
                region = 9
            elif NJets>=6 and n_btags>0:
                region = 10
        elif MHT>=650 and MinDeltaPhiMhtJets>0.3:
            if NJets==1 and n_btags>=0:
                region = 11
            elif NJets>=2 and NJets<=5 and n_btags==0:
                region = 12
            elif NJets>=2 and NJets<=5 and n_btags>0:
                region = 13
            elif NJets>=6 and n_btags==0:
                region = 14
            elif NJets>=6 and n_btags>0:
                region = 15
    
    elif n_DT>1 and NJets>=1:
        if MHT>=250 and MHT<400:
            region = 16
        elif MHT>=400:
            region = 17
            
    return region


def loop(event_tree_filenames, track_tree_output, bdt_folders, nevents = -1, treename = "TreeMaker2/PreSelection", zmass_matching = True, maskfile = "Masks.root"):

    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
    
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

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
                      "zmass",
                      "PFCaloMETRatio",
                      "CrossSection",
                    ]:
        tree_branch_values[variable] = array( 'f', [ -1000 ] )

    for variable in [
                      "signalregion",
                      "signalregion_cleaned",
                      "n_DT",
                      "n_DT_realfake",
                      "n_DT_mask",
                      "n_DT_realfake_mask",
                      "n_jets",
                      "n_jets_cleaned",
                      "n_btags",
                      "n_btags_cleaned",
                      "n_leptons",
                      "n_allvertices",
                      "n_NVtx",
                      "n_gen_particles_in_cone",
                      "n_gen_taus_in_cone",
                      "n_leading_tracks_in_cone",
                      "EvtNumEven",
                      "lepton_type",
                    ]:
        tree_branch_values[variable] = array( 'i', [ -1000 ] )

    vector_length = 20

    # float vectors:
    for variable in [
                      "tagged_track_bdt",
                      "tagged_track_pt",
                      "tagged_track_eta",
                      "tagged_track_chi2perNdof",
                      "tagged_track_trkRelIso",
                      "tagged_track_dxyVtx",
                      "tagged_track_dzVtx",
                    ]:
        tree_branch_values[variable] = array( 'f', vector_length*[ -1000 ] )

    # integer vectors:
    for variable in [
                      "tagged_track_trackerlayers",
                      "tagged_track_pixellayers",
                    ]:
        tree_branch_values[variable] = array( 'i', vector_length*[ -1000 ] )

    for variable in [
                      "gen_track_cone_pdgid",
                      "gen_track_cone_taucorrected",
                    ]:
        tree_branch_values[variable] = array( 'i', vector_length*vector_length*[ -1000 ] )

    tout.Branch( "MET", tree_branch_values["MET"], 'MET/F' )
    tout.Branch( "MHT", tree_branch_values["MHT"], 'MHT/F' )
    tout.Branch( "MHT_cleaned", tree_branch_values["MHT_cleaned"], 'MHT_cleaned/F' )
    tout.Branch( "HT", tree_branch_values["HT"], 'HT/F' )
    tout.Branch( "HT_cleaned", tree_branch_values["HT_cleaned"], 'HT_cleaned/F' )
    tout.Branch( "MinDeltaPhiMhtJets", tree_branch_values["MinDeltaPhiMhtJets"], 'MinDeltaPhiMhtJets/F' )
    tout.Branch( "MinDeltaPhiMhtJets_cleaned", tree_branch_values["MinDeltaPhiMhtJets_cleaned"], 'MinDeltaPhiMhtJets_cleaned/F' )
    tout.Branch( "signalregion", tree_branch_values["signalregion"], 'signalregion/I' )
    tout.Branch( "signalregion_cleaned", tree_branch_values["signalregion_cleaned"], 'signalregion_cleaned/I' )
    tout.Branch( "n_DT", tree_branch_values["n_DT"], 'n_DT/I' )
    tout.Branch( "n_DT_realfake", tree_branch_values["n_DT_realfake"], 'n_DT_realfake/I' )
    tout.Branch( "n_DT_mask", tree_branch_values["n_DT_mask"], 'n_DT_mask/I' )
    tout.Branch( "n_DT_realfake_mask", tree_branch_values["n_DT_realfake_mask"], 'n_DT_realfake_mask/I' )
    tout.Branch( "n_jets", tree_branch_values["n_jets"], 'n_jets/I' )
    tout.Branch( "n_jets_cleaned", tree_branch_values["n_jets_cleaned"], 'n_jets_cleaned/I' )
    tout.Branch( "n_btags", tree_branch_values["n_btags"], 'n_btags/I' )
    tout.Branch( "n_btags_cleaned", tree_branch_values["n_btags_cleaned"], 'n_btags_cleaned/I' )
    tout.Branch( "n_leptons", tree_branch_values["n_leptons"], 'n_leptons/I' )
    tout.Branch( "n_allvertices", tree_branch_values["n_allvertices"], 'n_allvertices/I' )
    tout.Branch( "PFCaloMETRatio", tree_branch_values["PFCaloMETRatio"], 'PFCaloMETRatio/F' )
    tout.Branch( "zmass", tree_branch_values["zmass"], 'zmass/F' )
    tout.Branch( "n_NVtx", tree_branch_values["n_NVtx"], 'n_NVtx/I' )
    tout.Branch( "EvtNumEven", tree_branch_values["EvtNumEven"], 'EvtNumEven/I' )
    tout.Branch( "lepton_type", tree_branch_values["lepton_type"], 'lepton_type/I' )
    tout.Branch( "n_gen_particles_in_cone", tree_branch_values["n_gen_particles_in_cone"], 'n_gen_particles_in_cone/I' )   
    tout.Branch( "n_gen_taus_in_cone", tree_branch_values["n_gen_taus_in_cone"], 'n_gen_taus_in_cone/I' )
    tout.Branch( "n_leading_tracks_in_cone", tree_branch_values["n_leading_tracks_in_cone"], 'n_leading_tracks_in_cone/I' )

    # vectors:
    tout.Branch( "tagged_track_bdt", tree_branch_values["tagged_track_bdt"], 'tagged_track_bdt[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_pt", tree_branch_values["tagged_track_pt"], 'tagged_track_pt[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_eta", tree_branch_values["tagged_track_eta"], 'tagged_track_eta[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_chi2perNdof", tree_branch_values["tagged_track_chi2perNdof"], 'tagged_track_chi2perNdof[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_trkRelIso", tree_branch_values["tagged_track_trkRelIso"], 'tagged_track_trkRelIso[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_dxyVtx", tree_branch_values["tagged_track_dxyVtx"], 'tagged_track_dxyVtx[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_dzVtx", tree_branch_values["tagged_track_dzVtx"], 'tagged_track_dzVtx[%s]/F' % (vector_length))
    tout.Branch( "tagged_track_trackerlayers", tree_branch_values["tagged_track_trackerlayers"], 'tagged_track_trackerlayers[%s]/I' % (vector_length))
    tout.Branch( "tagged_track_pixellayers", tree_branch_values["tagged_track_pixellayers"], 'tagged_track_pixellayers[%s]/I' % (vector_length))
    tout.Branch( "gen_track_cone_pdgid", tree_branch_values["gen_track_cone_pdgid"], 'gen_track_cone_pdgid[%s]/I' % (vector_length*vector_length))
    tout.Branch( "gen_track_cone_taucorrected", tree_branch_values["gen_track_cone_taucorrected"], 'gen_track_cone_taucorrected[%s]/I' % (vector_length*vector_length))

    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        #bdt_bestcut = tmva_tools.get_get_bdt_cut_value(bdt_folders[i_category] + '/output.root')["best_cut_value"]
        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_cut_pixelonly = 0.1
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_cut_pixelstrips = 0.25

    # some loop variables:
    nevents_total = 0
    nevents_tagged = 0
    nevents_tagged_realfake = 0

    # loop over events
    # ****************

    for iEv, event in enumerate(tree):

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
               ("200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("2500toInf_" in current_file_name and madHT<2500) or \
               ("2500ToInf_" in current_file_name and madHT<2500):
                continue
                    
        # reset all branch values
        for label in tree_branch_values:
            tree_branch_values[label][0] = -1000

        if zmass_matching:
            # only two oppositely charged leptons matched to Z mass:
            min_lepton_pt = 30.0        
            invariant_mass = 0
            
            if (len(event.Electrons) == 2 and len(event.Muons) == 0):
                if (event.Electrons[0].Pt() > min_lepton_pt):
                    if (bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1])):
                        if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                            if (bool(event.Electrons_passIso[0]) * bool(event.Electrons_passIso[1]) == 1):
                                invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    tree_branch_values["zmass"][0] = invariant_mass
                                    tree_branch_values["lepton_type"][0] = 11
            
            elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
                if (event.Muons[0].Pt() > min_lepton_pt):
                    if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                        if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                            if (bool(event.Muons_passIso[0]) * bool(event.Muons_passIso[1]) == 1):
                                invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    tree_branch_values["zmass"][0] = invariant_mass
                                    tree_branch_values["lepton_type"][0] = 13

            # veto events with incompatible Z mass
            if tree_branch_values["zmass"][0] < 0:
                continue
                
        # clean event (recalculate HT, MHT, n_Jets without the two leptons):
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

        # get signal region for event:
        #tree_branch_values["signalregion"][0] = get_signal_region(event, MinDeltaPhiMhtJets, n_DT)
        #tree_branch_values["signalregion_cleaned"][0] = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, n_jets_cleaned=n_jets_cleaned, MHT_cleaned=MHT_cleaned, MinDeltaPhiMhtJets_cleaned=MinDeltaPhiMhtJets_cleaned, n_btags_cleaned=n_btags_cleaned)
     
        nevents_total += 1
        n_DT = 0
        n_DT_realfake = 0
        n_DT_mask = 0
        n_DT_realfake_mask = 0

        gen_track_cone_pdgid = -1000
        gen_track_cone_taucorrected = -1000
        n_gen_particles_in_cone = 0

        n_gen_taus_in_cone = 0
        n_leading_tracks_in_cone = 0

        # loop over tracks (tracks)
        for i_iCand, iCand in enumerate(xrange(len(event.tracks))):

            # set up booleans
            is_pixel_track = False
            is_tracker_track = False
            genparticle_in_track_cone = False
            tau_leadtrk_in_track_cone = False
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
            if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True

            # apply TMVA preselection:
            if is_pixel_track and not (event.tracks[iCand].Pt() > 15 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                bool(event.tracks_passPFCandVeto[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 15 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                bool(event.tracks_passPFCandVeto[iCand]) == 1):
                    continue

            # evalulate BDT:
            tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
            tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
            tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
            tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
            tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
            tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
            tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
            tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2
            
            # final categorization:
            if is_pixel_track:
                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelonly:
                    is_disappearing_track = True
            elif is_tracker_track:
                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelstrips:
                    is_disappearing_track = True

            # check if "real" fake (no genparticle around track):            
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):
                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.01:

                        # we only need genparticles with status 1:
                        if event.GenParticles_Status[k] != 1:
                            continue

                        gen_track_cone_pdgid = event.GenParticles_PdgId[k]
                        gen_track_cone_taucorrected = -1000

                        # ignore certain non-charged genparticles (neutrinos, gluons and photons):
                        if abs(gen_track_cone_pdgid) == 12 or abs(gen_track_cone_pdgid) == 14 or abs(gen_track_cone_pdgid) == 16 or abs(gen_track_cone_pdgid) == 21 or abs(gen_track_cone_pdgid) == 22:
                            continue

                        # check if track matches with a GenTaus_LeadTrk track:
                        if abs(gen_track_cone_pdgid) != 15:
                            gen_track_cone_taucorrected = gen_track_cone_pdgid
                        else:
                            n_gen_taus_in_cone += 1
                        
                        if tree.GetBranch("GenTaus_LeadTrk"):
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    n_leading_tracks_in_cone += 1

                                    if event.tracks_charge[iCand] > 0:
                                        gen_track_cone_taucorrected = 15
                                    elif event.tracks_charge[iCand] < 0:
                                        gen_track_cone_taucorrected = -15
                                        
                        if gen_track_cone_taucorrected != -1000:
                            genparticle_in_track_cone = True

                        tree_branch_values["gen_track_cone_pdgid"][n_DT * vector_length + n_gen_particles_in_cone] = gen_track_cone_pdgid
                        tree_branch_values["gen_track_cone_taucorrected"][n_DT * vector_length + n_gen_particles_in_cone] = gen_track_cone_taucorrected
                        n_gen_particles_in_cone += 1
                
            if is_disappearing_track:

                tree_branch_values["tagged_track_pt"][n_DT] = event.tracks[iCand].Pt()
                tree_branch_values["tagged_track_eta"][n_DT] = event.tracks[iCand].Eta()
                tree_branch_values["tagged_track_trackerlayers"][n_DT] = event.tracks_trackerLayersWithMeasurement[iCand]
                tree_branch_values["tagged_track_pixellayers"][n_DT] = event.tracks_pixelLayersWithMeasurement[iCand]
                tree_branch_values["tagged_track_chi2perNdof"][n_DT] = event.tracks_chi2perNdof[iCand]
                tree_branch_values["tagged_track_trkRelIso"][n_DT] = event.tracks_trkRelIso[iCand]
                tree_branch_values["tagged_track_dxyVtx"][n_DT] = event.tracks_dxyVtx[iCand]
                tree_branch_values["tagged_track_dzVtx"][n_DT] = event.tracks_dzVtx[iCand]
                tree_branch_values["tagged_track_bdt"][n_DT] = mva
                n_DT += 1

                # check eta/phi mask:
                masked = -1.0
                if maskfile:
                    mask_file = TFile(maskfile, "open")
                    if "Run2016" in current_file_name:
                        mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")
                    elif "Summer16" in current_file_name:
                        mask = mask_file.Get("hEtaVsPhiDT_maskedMC-2016MC-2016")
                masked = mask.GetBinContent(mask.GetXaxis().FindBin(event.tracks[iCand].Phi()), mask.GetYaxis().FindBin(event.tracks[iCand].Eta()))

                if masked > 0:
                    n_DT_mask += 1

                if not genparticle_in_track_cone:
                    n_DT_realfake += 1
                    if masked > 0:
                        n_DT_realfake_mask += 1
 
        # event-level variables:
        if tree.GetBranch("CrossSection"):
            tree_branch_values["CrossSection"][0] = event.CrossSection
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_btags_cleaned"][0] = n_btags_cleaned
        tree_branch_values["n_DT"][0] = n_DT
        tree_branch_values["n_DT_realfake"][0] = n_DT_realfake
        tree_branch_values["n_DT_mask"][0] = n_DT_mask
        tree_branch_values["n_DT_realfake_mask"][0] = n_DT_mask
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_jets_cleaned"][0] = n_jets_cleaned
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["MHT_cleaned"][0] = MHT_cleaned
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["HT_cleaned"][0] = HT_cleaned
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["MinDeltaPhiMhtJets_cleaned"][0] = MinDeltaPhiMhtJets_cleaned
        tree_branch_values["n_NVtx"][0] = event.NVtx
        
        if event.EvtNum % 2 == 0:
            tree_branch_values["EvtNumEven"][0] = 1
        else:
            tree_branch_values["EvtNumEven"][0] = 0

        tree_branch_values["n_gen_particles_in_cone"][0] = n_gen_particles_in_cone
        tree_branch_values["n_gen_taus_in_cone"][0] = n_gen_taus_in_cone
        tree_branch_values["n_leading_tracks_in_cone"][0] = n_leading_tracks_in_cone
   
        tout.Fill()
        
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

    if len(args)>3:
        zmass_matching = int(args[3])
    else:
        zmass_matching = True

    loop(iFile, out_tree, ["../cutoptimization/tmva/newpresel3-200-4-short", "../cutoptimization/tmva/newpresel2-200-4-medium"], nevents=nev, zmass_matching = zmass_matching )

