#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import os

def pass_background_stitching(file_name, madHT):

    # backgrounds are HT-binned, do stitching

    passed = True
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in file_name and madHT>100) or \
       ("TTJets_Tune" in file_name and madHT>600) or \
       ("100to200_" in file_name and (madHT<100 or madHT>200)) or \
       ("100To200_" in file_name and (madHT<100 or madHT>200)) or \
       ("200to400_" in file_name and (madHT<200 or madHT>400)) or \
       ("200To400_" in file_name and (madHT<200 or madHT>400)) or \
       ("400to600_" in file_name and (madHT<400 or madHT>600)) or \
       ("400To600_" in file_name and (madHT<400 or madHT>600)) or \
       ("600to800_" in file_name and (madHT<600 or madHT>800)) or \
       ("600To800_" in file_name and (madHT<600 or madHT>800)) or \
       ("800to1200_" in file_name and (madHT<800 or madHT>1200)) or \
       ("800To1200_" in file_name and (madHT<800 or madHT>1200)) or \
       ("1200to2500_" in file_name and (madHT<1200 or madHT>2500)) or \
       ("1200To2500_" in file_name and (madHT<1200 or madHT>2500)) or \
       ("2500toInf_" in file_name and madHT<2500) or \
       ("2500ToInf_" in file_name and madHT<2500):
            passed = False

    return passed


def calculate_MinDeltaPhiMhtJets(event):

    csv_b = 0.8484
    mhtvec = TLorentzVector()
    mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
    mindphi = 9999
    nj = 0
    nb = 0
    for ijet, jet in enumerate(event.Jets):
            if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
            nj+=1
            if event.Jets_bDiscriminatorCSV[ijet]>csv_b: nb+=1
            if abs(jet.DeltaPhi(mhtvec))<mindphi:
                    mindphi = abs(jet.DeltaPhi(mhtvec))

    return mindphi


def get_signal_region(event, cleaned_event_variables = False):

    # signal regions as defined in https://indico.desy.de/indico/event/20437/contribution/2/material/slides/0.pdf
    
    if cleaned_event_variables:
        NJets = cleaned_event_variables["NJets"]
        MHT = cleaned_event_variables["MHT"]
        MinDeltaPhiMhtJets = cleaned_event_variables["MinDeltaPhiMhtJets"]
    else:
        NJets = len(event.Jets)
        MHT = event.MHT
        MinDeltaPhiMhtJets = calculate_MinDeltaPhiMhtJets(event)

    region = 0

    if MHT>=250 and MHT<400 and MinDeltaPhiMhtJets>0.5:
        if NJets==1:
            region = 1
        elif NJets>=2 and NJets<=5:
            region = 2
        elif NJets>=6:
            region = 3
    elif MHT>=400 and MHT<650 and MinDeltaPhiMhtJets>0.3:
        if NJets==1:
            region = 4
        elif NJets>=2 and NJets<=5:
            region = 5
        elif NJets>=6:
            region = 6
    elif MHT>=650 and MinDeltaPhiMhtJets>0.3:
        if NJets==1:
            region = 7
        elif NJets>=2 and NJets<=5:
            region = 8
        elif NJets>=6:
            region = 9

    return region


def clean_event(event):

    cleaned_event_variables = {}

    csv_b = 0.8484

    # recalculate MHT: 
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET)
    mhtvec = TLorentzVector()
    mhtvec.SetPtEtaPhiE(0, 0, 0, 0)
    jets = []
    nb = 0
    ht = 0
    
    for ijet, jet in enumerate(event.Jets):
        
        if not (abs(jet.Eta()) < 2.4 and jet.Pt() > 30): continue
        
        # check if lepton is in jet, and veto jet if that is the case
        lepton_is_in_jet = False
        for leptons in [event.Electrons, event.Muons]:
            for lepton in leptons:
                if jet.DeltaR(lepton) < 0.05:
                    lepton_is_in_jet = True
        if lepton_is_in_jet: continue
        
        mhtvec-=jet
        jets.append(jet)
        ht+=jet.Pt()        
        if event.Jets_bDiscriminatorCSV[ijet] > csv_b: nb+=1
        
    cleaned_event_variables["NJets"] = len(jets)
    cleaned_event_variables["MHT"] = mhtvec.Pt()
    mindphi = 9999   
    for jet in jets: 
    	if abs(jet.DeltaPhi(mhtvec)) < mindphi:
        	mindphi = abs(jet.DeltaPhi(mhtvec))
            
    cleaned_event_variables["HT"] = ht
    cleaned_event_variables["MinDeltaPhiMhtJets"] = mindphi
   
    return cleaned_event_variables


def loop(event_tree_filenames, track_tree_output, bdt_folders, nevents = -1, treename = "TreeMaker2/PreSelection", select_zmass_dilepton_events_only = True):

    print "Input:\t\t", event_tree_filenames
    print "Tree:\t\t", treename
    print "Output:\t\t", track_tree_output

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
    tout_output_values = {}
    for variable in [
                      "MET",
                      "MHT",
                      "MHT_cleaned",
                      "HT",
                      "HT_cleaned",
                      "MinDeltaPhiMhtJets",
                      "MinDeltaPhiMhtJets_cleaned",
                      "tagged_track_highest_bdt",
                      "tagged_track_pt",
                      "tagged_track_eta",
                      "tagged_track_chi2perNdof",
                      "tagged_track_trkRelIso",
                      "tagged_track_dxyVtx",
                      "tagged_track_dzVtx",
                      "zmass",
                      "PFCaloMETRatio",
                    ]:
        tout_output_values[variable] = array( 'f', [ -1000 ] )

    for variable in [
                      "pass_sr",
                      "pass_sr_cleaned",
                      "n_DT",
                      "n_DT_no_genparticle_in_track_cone",
                      "n_jets",
                      "n_jets_cleaned",
                      "n_btags",
                      "n_leptons",
                      "n_allvertices",
                      "n_NVtx",
                      "tagged_track_trackerlayers",
                      "tagged_track_pixellayers",
                      "EvtNumEven",
                      "lepton_type",
                      "gen_track_cone_pdgid",
                      "gen_track_cone_parent",
                      "gen_track_cone_genstatus",
                      "gen_track_cone_taucorrected",
                    ]:
        tout_output_values[variable] = array( 'i', [ -1000 ] )

    tout.Branch( "MET", tout_output_values["MET"], 'MET/F' )
    tout.Branch( "MHT", tout_output_values["MHT"], 'MHT/F' )
    tout.Branch( "MHT_cleaned", tout_output_values["MHT_cleaned"], 'MHT_cleaned/F' )
    tout.Branch( "HT", tout_output_values["HT"], 'HT/F' )
    tout.Branch( "HT_cleaned", tout_output_values["HT_cleaned"], 'HT_cleaned/F' )
    tout.Branch( "MinDeltaPhiMhtJets", tout_output_values["MinDeltaPhiMhtJets"], 'MinDeltaPhiMhtJets/F' )
    tout.Branch( "MinDeltaPhiMhtJets_cleaned", tout_output_values["MinDeltaPhiMhtJets_cleaned"], 'MinDeltaPhiMhtJets_cleaned/F' )
    tout.Branch( "pass_sr", tout_output_values["pass_sr"], 'pass_sr/I' )
    tout.Branch( "pass_sr_cleaned", tout_output_values["pass_sr_cleaned"], 'pass_sr_cleaned/I' )
    tout.Branch( "n_DT", tout_output_values["n_DT"], 'n_DT/I' )
    tout.Branch( "n_DT_no_genparticle_in_track_cone", tout_output_values["n_DT_no_genparticle_in_track_cone"], 'n_DT_no_genparticle_in_track_cone/I' )
    tout.Branch( "n_jets", tout_output_values["n_jets"], 'n_jets/I' )
    tout.Branch( "n_jets_cleaned", tout_output_values["n_jets_cleaned"], 'n_jets_cleaned/I' )
    tout.Branch( "n_btags", tout_output_values["n_btags"], 'n_btags/I' )
    tout.Branch( "n_leptons", tout_output_values["n_leptons"], 'n_leptons/I' )
    tout.Branch( "n_allvertices", tout_output_values["n_allvertices"], 'n_allvertices/I' )
    tout.Branch( "tagged_track_highest_bdt", tout_output_values["tagged_track_highest_bdt"], 'tagged_track_highest_bdt/F' )
    tout.Branch( "tagged_track_pt", tout_output_values["tagged_track_pt"], 'tagged_track_pt/F' )
    tout.Branch( "tagged_track_eta", tout_output_values["tagged_track_eta"], 'tagged_track_eta/F' )
    tout.Branch( "tagged_track_trackerlayers", tout_output_values["tagged_track_trackerlayers"], 'tagged_track_trackerlayers/I' )
    tout.Branch( "tagged_track_pixellayers", tout_output_values["tagged_track_pixellayers"], 'tagged_track_pixellayers/I' )
    tout.Branch( "tagged_track_chi2perNdof", tout_output_values["tagged_track_chi2perNdof"], 'tagged_track_chi2perNdof/F' )
    tout.Branch( "tagged_track_trkRelIso", tout_output_values["tagged_track_trkRelIso"], 'tagged_track_trkRelIso/F' )
    tout.Branch( "tagged_track_dxyVtx", tout_output_values["tagged_track_dxyVtx"], 'tagged_track_dxyVtx/F' )
    tout.Branch( "tagged_track_dzVtx", tout_output_values["tagged_track_dzVtx"], 'tagged_track_dzVtx/F' )
    tout.Branch( "PFCaloMETRatio", tout_output_values["PFCaloMETRatio"], 'PFCaloMETRatio/F' )
    tout.Branch( "zmass", tout_output_values["zmass"], 'zmass/F' )
    tout.Branch( "n_NVtx", tout_output_values["n_NVtx"], 'n_NVtx/I' )
    tout.Branch( "EvtNumEven", tout_output_values["EvtNumEven"], 'EvtNumEven/I' )
    tout.Branch( "lepton_type", tout_output_values["lepton_type"], 'lepton_type/I' )
    tout.Branch( "gen_track_cone_pdgid", tout_output_values["gen_track_cone_pdgid"], 'gen_track_cone_pdgid/I' )
    tout.Branch( "gen_track_cone_parent", tout_output_values["gen_track_cone_parent"], 'gen_track_cone_parent/I' )
    tout.Branch( "gen_track_cone_genstatus", tout_output_values["gen_track_cone_genstatus"], 'gen_track_cone_genstatus/I' )
    tout.Branch( "gen_track_cone_taucorrected", tout_output_values["gen_track_cone_taucorrected"], 'gen_track_cone_taucorrected/I' )
    
    # BDT configuration:
    readerPixelOnly = 0
    bdt_bestcut_pixelonly = 0
    readerPixelStrips = 0
    bdt_bestcut_pixelstrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        bdt_bestcut = tmva_tools.get_get_bdt_cut_value(bdt_folders[i_category] + '/output.root')["best_cut_value"]
        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        print category, "classifier >", bdt_bestcut, bdt_infos["variables"], bdt_infos["spectators"]

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_bestcut_pixelonly = bdt_bestcut
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_bestcut_pixelstrips = bdt_bestcut

    # some loop variables:
    nevents_total = 0
    nevents_tagged = 0
    nevents_tagged_no_genparticle_in_track_cone = 0

    # loop over events
    # ****************

    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents:
            break
        
        if (iEv+1) % 500 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        if "Run201" not in current_file_name:
            if not pass_background_stitching(current_file_name, event.madHT):
                continue

        # only two oppositely charged leptons matched to Z mass:
        min_lepton_pt = 30.0        
        invariant_mass = 0
        
        if (len(event.Electrons) == 2 and len(event.Muons) == 0):
            if (event.Electrons[0].Pt() > min_lepton_pt):
                if (bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1])):
                    if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                        invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                        if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                            tout_output_values["zmass"][0] = invariant_mass
                            tout_output_values["lepton_type"][0] = 11
        
        elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
            if (event.Muons[0].Pt() > min_lepton_pt):
                if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                    if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                        if (bool(event.Muons_passIso[0]) * bool(event.Muons_passIso[1]) == 1):
                            invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                            if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                tout_output_values["zmass"][0] = invariant_mass
                                tout_output_values["lepton_type"][0] = 13
                                
        if select_zmass_dilepton_events_only and invariant_mass == 0:
            continue
        
        # clean event (remove leptons):
        cleaned_event_variables = clean_event(event)
             
        # get signal region for event:
        MinDeltaPhiMhtJets = calculate_MinDeltaPhiMhtJets(event)
        tout_output_values["pass_sr"][0] = get_signal_region(event)
        tout_output_values["pass_sr_cleaned"][0] = get_signal_region(event, cleaned_event_variables = cleaned_event_variables)
     
        nevents_total += 1
        n_DT = 0
        n_DT_no_genparticle_in_track_cone = 0
        highest_bdt_value = -1
        highest_bdt_index = -1
    
        gen_track_cone_pdgid = -1000
        gen_track_cone_parent = -1000
        gen_track_cone_genstatus = -1000
        gen_track_cone_taucorrected = -1000

        # loop over tracks (tracks)
        # ***************************
        number_of_tracks = len(event.tracks)

        for i_iCand, iCand in enumerate(xrange(number_of_tracks)):

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

            # apply TMVA preselection with modified pt (30 instead of 15 GeV):
            if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                bool(event.tracks_passPFCandVeto[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 30 and \
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
            
            mva = -1

            # final categorization:
            if is_pixel_track:
                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_bestcut_pixelonly:
                    is_disappearing_track = True
            elif is_tracker_track:
                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_bestcut_pixelstrips:
                    is_disappearing_track = True

            if is_disappearing_track:
                os.system("echo '%s, event=%s, track_pt=%s, mva=%s' >> samples-with-dt" % (current_file_name, iEv, event.tracks[iCand].Pt(), mva))

            # check if "real" fake (no genparticle around track):            
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):
                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.01:
                                                
                        gen_track_cone_pdgid = event.GenParticles_PdgId[k]
                        gen_track_cone_parent = event.GenParticles_ParentId[k]
                        gen_track_cone_genstatus = event.GenParticles_Status[k]
                
                        if event.GenParticles_Status[k] == 1:
                            genparticle_in_track_cone = True
                
                        os.system("echo '%s, event=%s, track_pt=%s, mva=%s, genparticle=%s, genstatus=%s' >> samples-with-dt" % (current_file_name, iEv, event.tracks[iCand].Pt(), mva, gen_track_cone_pdgid, gen_track_cone_genstatus))
                
                        # check if track matches with a GenTaus_LeadTrk track:
                        if abs(gen_track_cone_pdgid) != 15:
                            gen_track_cone_taucorrected = gen_track_cone_pdgid
                        
                        if tree.GetBranch("GenTaus_LeadTrk"):
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    if event.tracks[iCand].charge() > 0:
                                        gen_track_cone_taucorrected = 15
                                    elif event.tracks[iCand].charge() < 0:
                                        gen_track_cone_taucorrected = -15
                
            if mva > highest_bdt_value:
                highest_bdt_value = mva
                highest_bdt_index = iCand

            if is_disappearing_track:
                n_DT += 1
                if not genparticle_in_track_cone:
                    n_DT_no_genparticle_in_track_cone += 1
 
        # fill track info for highest BDT score track
        tout_output_values["tagged_track_pt"][0] = event.tracks[highest_bdt_index].Pt()
        tout_output_values["tagged_track_eta"][0] = event.tracks[highest_bdt_index].Eta()
        tout_output_values["tagged_track_trackerlayers"][0] = event.tracks_trackerLayersWithMeasurement[highest_bdt_index]
        tout_output_values["tagged_track_pixellayers"][0] = event.tracks_pixelLayersWithMeasurement[highest_bdt_index]
        tout_output_values["tagged_track_chi2perNdof"][0] = event.tracks_chi2perNdof[highest_bdt_index]
        tout_output_values["tagged_track_trkRelIso"][0] = event.tracks_trkRelIso[highest_bdt_index]
        tout_output_values["tagged_track_dxyVtx"][0] = event.tracks_dxyVtx[highest_bdt_index]
        tout_output_values["tagged_track_dzVtx"][0] = event.tracks_dzVtx[highest_bdt_index]

        # other event info
        tout_output_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tout_output_values["n_btags"][0] = event.BTags
        tout_output_values["n_DT"][0] = n_DT
        tout_output_values["n_DT_no_genparticle_in_track_cone"][0] = n_DT_no_genparticle_in_track_cone
        tout_output_values["n_jets"][0] = len(event.Jets)
        tout_output_values["n_jets_cleaned"][0] = cleaned_event_variables["NJets"]
        tout_output_values["n_allvertices"][0] = event.nAllVertices
        tout_output_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tout_output_values["MET"][0] = event.MET
        tout_output_values["MHT"][0] = event.MHT
        tout_output_values["MHT_cleaned"][0] = cleaned_event_variables["MHT"]
        tout_output_values["HT"][0] = event.HT
        tout_output_values["HT_cleaned"][0] = cleaned_event_variables["HT"]
        tout_output_values["tagged_track_highest_bdt"][0] = highest_bdt_value
        tout_output_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tout_output_values["MinDeltaPhiMhtJets_cleaned"][0] = cleaned_event_variables["MinDeltaPhiMhtJets"]
                
        tout_output_values["n_NVtx"][0] = event.NVtx
        
        if event.EvtNum % 2 == 0:
            tout_output_values["EvtNumEven"][0] = 1
        else:
            tout_output_values["EvtNumEven"][0] = 0

        tout_output_values["gen_track_cone_pdgid"][0] = gen_track_cone_pdgid
        tout_output_values["gen_track_cone_parent"][0] = gen_track_cone_parent
        tout_output_values["gen_track_cone_genstatus"][0] = gen_track_cone_genstatus
        tout_output_values["gen_track_cone_taucorrected"][0] = gen_track_cone_taucorrected
    
        tout.Fill()
        
    fout.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    if len(args)>2:
        nev = int(args[2])
    else:
        nev = -1

    loop(iFile, out_tree, ["../cutoptimization/tmva/newpresel3-200-4-short", "../cutoptimization/tmva/newpresel2-200-4-medium"], nevents=nev )

